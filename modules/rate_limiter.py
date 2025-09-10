"""
Sistema de Rate Limiting - Copilot Salud Andalucía
Protección contra ataques de fuerza bruta y limitación de uso por usuario
"""

import time
import streamlit as st
from collections import defaultdict, deque
from typing import Dict, Tuple, Optional
from datetime import datetime, timedelta
import json
import os

class RateLimiter:
    def __init__(self):
        """Inicializar sistema de rate limiting"""
        self.requests = defaultdict(deque)
        self.blocked_users = {}
        self.suspicious_ips = {}
        
        # Límites por tipo de acción (max_requests, window_seconds)
        self.limits = {
            'login': (5, 300),           # 5 intentos por 5 minutos
            'ai_query': (10, 60),        # 10 consultas IA por minuto
            'data_access': (100, 60),    # 100 accesos a datos por minuto
            'admin_action': (20, 60),    # 20 acciones admin por minuto
            'user_management': (5, 300), # 5 gestiones de usuario por 5 minutos
            'system_config': (3, 600),   # 3 configuraciones por 10 minutos
            'general': (200, 60)         # 200 acciones generales por minuto
        }
        
        # Configuración de bloqueos
        self.block_config = {
            'max_failed_attempts': 5,    # Máximo intentos fallidos
            'block_duration': 1800,      # 30 minutos de bloqueo
            'escalation_factor': 2,      # Factor de escalación de bloqueo
            'max_block_duration': 86400  # Máximo 24 horas de bloqueo
        }
        
        # Cargar estado persistente
        self._load_persistent_state()
    
    def is_allowed(self, user: str, action_type: str, ip_address: str = None) -> Tuple[bool, str, Dict]:
        """Verificar si la acción está permitida según rate limiting"""
        now = time.time()
        user_key = f"{user}_{action_type}"
        
        # Verificar si el usuario está bloqueado
        if self._is_user_blocked(user):
            block_info = self.blocked_users[user]
            remaining_time = block_info['expires_at'] - now
            return False, f"Usuario bloqueado por {int(remaining_time/60)} minutos", {
                'blocked': True,
                'reason': block_info['reason'],
                'expires_at': block_info['expires_at']
            }
        
        # Verificar IP sospechosa
        if ip_address and self._is_ip_suspicious(ip_address):
            return False, "IP marcada como sospechosa", {
                'blocked': True,
                'reason': 'suspicious_ip'
            }
        
        # Obtener límites para el tipo de acción
        max_requests, window = self.limits.get(action_type, self.limits['general'])
        
        # Limpiar requests antiguos
        self._clean_old_requests(user_key, now, window)
        
        # Verificar límite
        if len(self.requests[user_key]) >= max_requests:
            # Registrar intento de exceso
            self._log_rate_limit_exceeded(user, action_type, ip_address)
            return False, f"Rate limit excedido: {max_requests} {action_type} por {window}s", {
                'rate_limited': True,
                'max_requests': max_requests,
                'window': window,
                'retry_after': window
            }
        
        # Registrar request exitoso
        self.requests[user_key].append(now)
        
        # Verificar si se acerca al límite (advertencia)
        remaining = max_requests - len(self.requests[user_key])
        warning = None
        if remaining <= 3:
            warning = f"Advertencia: {remaining} {action_type} restantes en {window}s"
        
        return True, "OK", {
            'allowed': True,
            'remaining_requests': remaining,
            'warning': warning
        }
    
    def record_failed_attempt(self, user: str, action_type: str, ip_address: str = None) -> None:
        """Registrar intento fallido y aplicar bloqueo si es necesario"""
        now = time.time()
        
        # Incrementar contador de fallos
        if user not in self.blocked_users:
            self.blocked_users[user] = {
                'failed_attempts': 0,
                'first_failure': now,
                'last_failure': now,
                'block_level': 0
            }
        
        user_block = self.blocked_users[user]
        user_block['failed_attempts'] += 1
        user_block['last_failure'] = now
        
        # Aplicar bloqueo si excede el límite
        if user_block['failed_attempts'] >= self.block_config['max_failed_attempts']:
            self._apply_user_block(user, action_type, ip_address)
        
        # Marcar IP como sospechosa si hay muchos fallos
        if ip_address and user_block['failed_attempts'] >= 3:
            self._mark_ip_suspicious(ip_address)
        
        # Guardar estado
        self._save_persistent_state()
    
    def record_successful_attempt(self, user: str, action_type: str) -> None:
        """Registrar intento exitoso y limpiar bloqueos si es necesario"""
        # Limpiar bloqueo si existe
        if user in self.blocked_users:
            del self.blocked_users[user]
        
        # Limpiar IP sospechosa si es del mismo usuario
        # (esto se puede mejorar con más lógica)
        
        # Guardar estado
        self._save_persistent_state()
    
    def get_remaining_requests(self, user: str, action_type: str) -> int:
        """Obtener número de requests restantes para el usuario"""
        user_key = f"{user}_{action_type}"
        max_requests, window = self.limits.get(action_type, self.limits['general'])
        now = time.time()
        
        # Limpiar requests antiguos
        self._clean_old_requests(user_key, now, window)
        
        return max(0, max_requests - len(self.requests[user_key]))
    
    def get_user_status(self, user: str) -> Dict:
        """Obtener estado completo del usuario"""
        status = {
            'user': user,
            'blocked': self._is_user_blocked(user),
            'remaining_requests': {},
            'failed_attempts': 0,
            'last_activity': None
        }
        
        if user in self.blocked_users:
            block_info = self.blocked_users[user]
            status.update({
                'blocked': True,
                'failed_attempts': block_info['failed_attempts'],
                'block_reason': block_info.get('reason', 'unknown'),
                'block_expires_at': block_info['expires_at'],
                'remaining_block_time': max(0, block_info['expires_at'] - time.time())
            })
        
        # Obtener requests restantes por tipo de acción
        for action_type in self.limits.keys():
            status['remaining_requests'][action_type] = self.get_remaining_requests(user, action_type)
        
        return status
    
    def get_system_stats(self) -> Dict:
        """Obtener estadísticas del sistema de rate limiting"""
        now = time.time()
        
        # Contar usuarios bloqueados
        active_blocks = len([u for u, info in self.blocked_users.items() 
                           if info['expires_at'] > now])
        
        # Contar IPs sospechosas
        active_suspicious_ips = len([ip for ip, info in self.suspicious_ips.items() 
                                   if info['expires_at'] > now])
        
        # Contar requests activos por tipo
        active_requests = {}
        for action_type in self.limits.keys():
            count = 0
            for user_key, requests in self.requests.items():
                if user_key.endswith(f"_{action_type}"):
                    # Limpiar requests antiguos
                    max_requests, window = self.limits[action_type]
                    self._clean_old_requests(user_key, now, window)
                    count += len(requests)
            active_requests[action_type] = count
        
        return {
            'active_blocks': active_blocks,
            'suspicious_ips': active_suspicious_ips,
            'active_requests': active_requests,
            'total_limits': len(self.limits),
            'timestamp': now
        }
    
    def _is_user_blocked(self, user: str) -> bool:
        """Verificar si el usuario está bloqueado"""
        if user not in self.blocked_users:
            return False
        
        block_info = self.blocked_users[user]
        return block_info['expires_at'] > time.time()
    
    def _is_ip_suspicious(self, ip_address: str) -> bool:
        """Verificar si la IP está marcada como sospechosa"""
        if ip_address not in self.suspicious_ips:
            return False
        
        ip_info = self.suspicious_ips[ip_address]
        return ip_info['expires_at'] > time.time()
    
    def _apply_user_block(self, user: str, action_type: str, ip_address: str = None) -> None:
        """Aplicar bloqueo al usuario"""
        now = time.time()
        block_info = self.blocked_users[user]
        
        # Calcular duración del bloqueo (escalación)
        block_level = block_info['block_level']
        base_duration = self.block_config['block_duration']
        escalation_factor = self.block_config['escalation_factor']
        
        block_duration = min(
            base_duration * (escalation_factor ** block_level),
            self.block_config['max_block_duration']
        )
        
        block_info.update({
            'expires_at': now + block_duration,
            'reason': f'Rate limit exceeded for {action_type}',
            'block_level': block_level + 1,
            'blocked_at': now,
            'ip_address': ip_address
        })
        
        # Log del bloqueo
        self._log_user_blocked(user, action_type, block_duration, ip_address)
    
    def _mark_ip_suspicious(self, ip_address: str) -> None:
        """Marcar IP como sospechosa"""
        now = time.time()
        self.suspicious_ips[ip_address] = {
            'marked_at': now,
            'expires_at': now + 3600,  # 1 hora
            'reason': 'multiple_failed_attempts'
        }
    
    def _clean_old_requests(self, user_key: str, now: float, window: int) -> None:
        """Limpiar requests antiguos del usuario"""
        while (self.requests[user_key] and 
               self.requests[user_key][0] <= now - window):
            self.requests[user_key].popleft()
    
    def _log_rate_limit_exceeded(self, user: str, action_type: str, ip_address: str = None) -> None:
        """Registrar exceso de rate limit"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'event': 'rate_limit_exceeded',
            'user': user,
            'action_type': action_type,
            'ip_address': ip_address
        }
        
        # Log en archivo
        self._write_log_entry(log_entry)
    
    def _log_user_blocked(self, user: str, action_type: str, duration: int, ip_address: str = None) -> None:
        """Registrar bloqueo de usuario"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'event': 'user_blocked',
            'user': user,
            'action_type': action_type,
            'duration_seconds': duration,
            'ip_address': ip_address
        }
        
        # Log en archivo
        self._write_log_entry(log_entry)
    
    def _write_log_entry(self, log_entry: Dict) -> None:
        """Escribir entrada en log"""
        try:
            os.makedirs("logs", exist_ok=True)
            with open("logs/rate_limiting.jsonl", "a", encoding="utf-8") as f:
                f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
        except Exception:
            pass  # No fallar si no se puede escribir el log
    
    def _load_persistent_state(self) -> None:
        """Cargar estado persistente del rate limiter"""
        try:
            state_file = "data/rate_limiter_state.json"
            if os.path.exists(state_file):
                with open(state_file, "r", encoding="utf-8") as f:
                    state = json.load(f)
                
                # Cargar usuarios bloqueados
                if 'blocked_users' in state:
                    for user, info in state['blocked_users'].items():
                        # Solo cargar si el bloqueo no ha expirado
                        if info['expires_at'] > time.time():
                            self.blocked_users[user] = info
                
                # Cargar IPs sospechosas
                if 'suspicious_ips' in state:
                    for ip, info in state['suspicious_ips'].items():
                        # Solo cargar si la marca no ha expirado
                        if info['expires_at'] > time.time():
                            self.suspicious_ips[ip] = info
                            
        except Exception:
            pass  # Continuar sin estado persistente si hay error
    
    def _save_persistent_state(self) -> None:
        """Guardar estado persistente del rate limiter"""
        try:
            os.makedirs("data", exist_ok=True)
            state = {
                'blocked_users': self.blocked_users,
                'suspicious_ips': self.suspicious_ips,
                'last_saved': time.time()
            }
            
            with open("data/rate_limiter_state.json", "w", encoding="utf-8") as f:
                json.dump(state, f, ensure_ascii=False, indent=2)
                
        except Exception:
            pass  # No fallar si no se puede guardar el estado
    
    def unblock_user(self, user: str, admin_user: str = None) -> bool:
        """Desbloquear usuario (solo administradores)"""
        if user in self.blocked_users:
            del self.blocked_users[user]
            self._save_persistent_state()
            
            # Log del desbloqueo
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'event': 'user_unblocked',
                'user': user,
                'unblocked_by': admin_user or 'system'
            }
            self._write_log_entry(log_entry)
            
            return True
        return False
    
    def clear_ip_suspicion(self, ip_address: str, admin_user: str = None) -> bool:
        """Limpiar marca de IP sospechosa"""
        if ip_address in self.suspicious_ips:
            del self.suspicious_ips[ip_address]
            self._save_persistent_state()
            
            # Log de la limpieza
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'event': 'ip_cleared',
                'ip_address': ip_address,
                'cleared_by': admin_user or 'system'
            }
            self._write_log_entry(log_entry)
            
            return True
        return False

# Función de utilidad para usar el rate limiter
def get_rate_limiter() -> RateLimiter:
    """Obtener instancia del rate limiter"""
    if 'rate_limiter' not in st.session_state:
        st.session_state['rate_limiter'] = RateLimiter()
    return st.session_state['rate_limiter']
