"""
Sistema de Auditoría de Seguridad - Copilot Salud Andalucía
Registro completo de acciones de usuario y detección de actividad sospechosa
"""

import json
import os
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import streamlit as st

class SecurityAuditor:
    def __init__(self):
        """Inicializar sistema de auditoría de seguridad"""
        self.audit_log_file = "logs/security_audit.jsonl"
        self.suspicious_log_file = "logs/suspicious_activity.jsonl"
        self.ensure_log_directories()
        
        # Configuración de umbrales de seguridad
        self.security_thresholds = {
            'max_actions_per_hour': 100,
            'max_failed_logins_per_hour': 5,
            'max_ai_queries_per_hour': 50,
            'max_data_access_per_hour': 200,
            'suspicious_ip_changes': 3,  # Cambios de IP en 1 hora
            'unusual_hours_access': True  # Acceso fuera de horario laboral
        }
        
        # Patrones de actividad sospechosa
        self.suspicious_patterns = {
            'rapid_succession': 10,  # Acciones en menos de 10 segundos
            'repeated_failures': 3,  # Fallos consecutivos
            'bulk_data_access': 50,  # Acceso masivo a datos
            'unusual_endpoints': True  # Acceso a endpoints no habituales
        }
    
    def ensure_log_directories(self):
        """Crear directorios de logs si no existen"""
        os.makedirs("logs", exist_ok=True)
        
        # Crear archivos de log si no existen
        for log_file in [self.audit_log_file, self.suspicious_log_file]:
            if not os.path.exists(log_file):
                with open(log_file, "w", encoding="utf-8") as f:
                    f.write("")  # Archivo vacío inicial
    
    def log_user_action(self, user: str, action: str, resource: str, 
                       success: bool, details: Dict = None, severity: str = "info") -> None:
        """Registrar acción del usuario con auditoría completa"""
        try:
            audit_entry = {
                "timestamp": datetime.now().isoformat(),
                "user": user,
                "action": action,
                "resource": resource,
                "success": success,
                "severity": severity,
                "ip_address": self._get_client_ip(),
                "user_agent": self._get_user_agent(),
                "session_id": self._get_session_id(),
                "request_id": self._generate_request_id(),
                "details": details or {},
                "risk_score": self._calculate_risk_score(user, action, success)
            }
            
            # Escribir en log de auditoría
            with open(self.audit_log_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(audit_entry, ensure_ascii=False) + "\n")
            
            # Verificar si es actividad sospechosa
            if audit_entry["risk_score"] > 50:
                self._log_suspicious_activity(audit_entry)
            
        except Exception as e:
            # Log de error interno (no debe fallar la aplicación)
            self._log_internal_error(f"Error en auditoría: {str(e)}")
    
    def detect_suspicious_activity(self, user: str, time_window_hours: int = 1) -> List[Dict]:
        """Detectar actividad sospechosa del usuario"""
        suspicious_activities = []
        
        try:
            # Obtener acciones recientes del usuario
            recent_actions = self._get_recent_user_actions(user, time_window_hours)
            
            if not recent_actions:
                return suspicious_activities
            
            # Detectar patrones sospechosos
            suspicious_activities.extend(self._detect_high_frequency_activity(user, recent_actions))
            suspicious_activities.extend(self._detect_failed_login_patterns(user, recent_actions))
            suspicious_activities.extend(self._detect_unusual_access_patterns(user, recent_actions))
            suspicious_activities.extend(self._detect_rapid_succession_actions(user, recent_actions))
            suspicious_activities.extend(self._detect_bulk_data_access(user, recent_actions))
            
            # Log de actividades sospechosas detectadas
            if suspicious_activities:
                self._log_suspicious_activity({
                    "timestamp": datetime.now().isoformat(),
                    "user": user,
                    "type": "suspicious_activity_detected",
                    "activities": suspicious_activities,
                    "risk_level": max(activity.get("risk_level", 0) for activity in suspicious_activities)
                })
            
        except Exception as e:
            self._log_internal_error(f"Error detectando actividad sospechosa: {str(e)}")
        
        return suspicious_activities
    
    def _detect_high_frequency_activity(self, user: str, actions: List[Dict]) -> List[Dict]:
        """Detectar actividad de alta frecuencia"""
        suspicious = []
        
        # Contar acciones por tipo
        action_counts = {}
        for action in actions:
            action_type = action.get("action", "unknown")
            action_counts[action_type] = action_counts.get(action_type, 0) + 1
        
        # Verificar umbrales
        for action_type, count in action_counts.items():
            threshold = self.security_thresholds.get(f"max_{action_type}_per_hour", 50)
            if count > threshold:
                suspicious.append({
                    "type": "high_frequency",
                    "action_type": action_type,
                    "count": count,
                    "threshold": threshold,
                    "risk_level": min(100, (count / threshold) * 50),
                    "description": f"Usuario {user} realizó {count} acciones de tipo '{action_type}' en 1 hora (límite: {threshold})"
                })
        
        return suspicious
    
    def _detect_failed_login_patterns(self, user: str, actions: List[Dict]) -> List[Dict]:
        """Detectar patrones de login fallido"""
        suspicious = []
        
        failed_logins = [a for a in actions if a.get("action") == "login" and not a.get("success")]
        
        if len(failed_logins) >= self.security_thresholds["max_failed_logins_per_hour"]:
            suspicious.append({
                "type": "brute_force_attempt",
                "count": len(failed_logins),
                "risk_level": min(100, len(failed_logins) * 20),
                "description": f"Usuario {user} falló {len(failed_logins)} intentos de login en 1 hora"
            })
        
        # Detectar fallos consecutivos
        consecutive_failures = 0
        for action in reversed(actions):
            if action.get("action") == "login":
                if not action.get("success"):
                    consecutive_failures += 1
                else:
                    break
        
        if consecutive_failures >= self.suspicious_patterns["repeated_failures"]:
            suspicious.append({
                "type": "consecutive_failures",
                "count": consecutive_failures,
                "risk_level": min(100, consecutive_failures * 25),
                "description": f"Usuario {user} falló {consecutive_failures} logins consecutivos"
            })
        
        return suspicious
    
    def _detect_unusual_access_patterns(self, user: str, actions: List[Dict]) -> List[Dict]:
        """Detectar patrones de acceso inusuales"""
        suspicious = []
        
        # Verificar acceso fuera de horario laboral
        if self.security_thresholds["unusual_hours_access"]:
            unusual_hours = []
            for action in actions:
                timestamp = datetime.fromisoformat(action["timestamp"])
                hour = timestamp.hour
                if hour < 7 or hour > 22:  # Fuera de 7:00-22:00
                    unusual_hours.append(timestamp)
            
            if unusual_hours:
                suspicious.append({
                    "type": "unusual_hours_access",
                    "count": len(unusual_hours),
                    "hours": [h.strftime("%H:%M") for h in unusual_hours],
                    "risk_level": min(100, len(unusual_hours) * 10),
                    "description": f"Usuario {user} accedió {len(unusual_hours)} veces fuera de horario laboral"
                })
        
        return suspicious
    
    def _detect_rapid_succession_actions(self, user: str, actions: List[Dict]) -> List[Dict]:
        """Detectar acciones en rápida sucesión"""
        suspicious = []
        
        if len(actions) < 2:
            return suspicious
        
        # Ordenar por timestamp
        sorted_actions = sorted(actions, key=lambda x: x["timestamp"])
        
        rapid_actions = 0
        for i in range(1, len(sorted_actions)):
            prev_time = datetime.fromisoformat(sorted_actions[i-1]["timestamp"])
            curr_time = datetime.fromisoformat(sorted_actions[i]["timestamp"])
            
            if (curr_time - prev_time).total_seconds() < self.suspicious_patterns["rapid_succession"]:
                rapid_actions += 1
        
        if rapid_actions > 0:
            suspicious.append({
                "type": "rapid_succession",
                "count": rapid_actions,
                "risk_level": min(100, rapid_actions * 15),
                "description": f"Usuario {user} realizó {rapid_actions} acciones en rápida sucesión (<{self.suspicious_patterns['rapid_succession']}s)"
            })
        
        return suspicious
    
    def _detect_bulk_data_access(self, user: str, actions: List[Dict]) -> List[Dict]:
        """Detectar acceso masivo a datos"""
        suspicious = []
        
        data_access_actions = [a for a in actions if "data" in a.get("action", "").lower()]
        
        if len(data_access_actions) >= self.suspicious_patterns["bulk_data_access"]:
            suspicious.append({
                "type": "bulk_data_access",
                "count": len(data_access_actions),
                "risk_level": min(100, len(data_access_actions) * 2),
                "description": f"Usuario {user} accedió a datos {len(data_access_actions)} veces en 1 hora"
            })
        
        return suspicious
    
    def _get_recent_user_actions(self, user: str, hours: int = 1) -> List[Dict]:
        """Obtener acciones recientes del usuario"""
        try:
            if not os.path.exists(self.audit_log_file):
                return []
            
            cutoff_time = datetime.now() - timedelta(hours=hours)
            recent_actions = []
            
            with open(self.audit_log_file, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        try:
                            entry = json.loads(line.strip())
                            if entry.get("user") == user:
                                entry_time = datetime.fromisoformat(entry["timestamp"])
                                if entry_time >= cutoff_time:
                                    recent_actions.append(entry)
                        except json.JSONDecodeError:
                            continue
            
            return recent_actions
            
        except Exception as e:
            self._log_internal_error(f"Error leyendo acciones recientes: {str(e)}")
            return []
    
    def _calculate_risk_score(self, user: str, action: str, success: bool) -> int:
        """Calcular puntuación de riesgo para la acción"""
        risk_score = 0
        
        # Puntuación base por tipo de acción
        action_risk = {
            "login": 10 if not success else 0,
            "data_access": 5,
            "ai_query": 3,
            "admin_action": 15,
            "user_management": 20,
            "system_config": 25
        }
        
        risk_score += action_risk.get(action, 1)
        
        # Penalización por fallo
        if not success:
            risk_score += 20
        
        # Verificar actividad reciente del usuario
        recent_actions = self._get_recent_user_actions(user, 1)
        if len(recent_actions) > 50:
            risk_score += 30  # Alta frecuencia
        
        return min(100, risk_score)
    
    def _log_suspicious_activity(self, activity: Dict) -> None:
        """Registrar actividad sospechosa"""
        try:
            with open(self.suspicious_log_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(activity, ensure_ascii=False) + "\n")
        except Exception as e:
            self._log_internal_error(f"Error registrando actividad sospechosa: {str(e)}")
    
    def _log_internal_error(self, error_message: str) -> None:
        """Registrar errores internos del sistema de auditoría"""
        try:
            error_log = {
                "timestamp": datetime.now().isoformat(),
                "type": "audit_system_error",
                "message": error_message
            }
            with open("logs/audit_errors.jsonl", "a", encoding="utf-8") as f:
                f.write(json.dumps(error_log) + "\n")
        except:
            pass  # No fallar si no se puede escribir el error
    
    def _get_client_ip(self) -> str:
        """Obtener IP del cliente"""
        try:
            # En Streamlit Cloud, usar headers de la request
            if hasattr(st, 'request') and hasattr(st.request, 'headers'):
                return st.request.headers.get('x-forwarded-for', 'unknown')
            return 'localhost'
        except:
            return 'unknown'
    
    def _get_user_agent(self) -> str:
        """Obtener User Agent del cliente"""
        try:
            if hasattr(st, 'request') and hasattr(st.request, 'headers'):
                return st.request.headers.get('user-agent', 'unknown')
            return 'streamlit'
        except:
            return 'unknown'
    
    def _get_session_id(self) -> str:
        """Obtener ID de sesión"""
        try:
            return st.session_state.get('session_id', 'unknown')
        except:
            return 'unknown'
    
    def _generate_request_id(self) -> str:
        """Generar ID único para la request"""
        return hashlib.md5(f"{datetime.now().isoformat()}{self._get_client_ip()}".encode()).hexdigest()[:12]
    
    def get_security_dashboard_data(self, hours: int = 24) -> Dict[str, Any]:
        """Obtener datos para dashboard de seguridad"""
        try:
            cutoff_time = datetime.now() - timedelta(hours=hours)
            
            # Leer logs de auditoría
            audit_entries = []
            if os.path.exists(self.audit_log_file):
                with open(self.audit_log_file, "r", encoding="utf-8") as f:
                    for line in f:
                        if line.strip():
                            try:
                                entry = json.loads(line.strip())
                                entry_time = datetime.fromisoformat(entry["timestamp"])
                                if entry_time >= cutoff_time:
                                    audit_entries.append(entry)
                            except json.JSONDecodeError:
                                continue
            
            # Estadísticas básicas
            total_actions = len(audit_entries)
            failed_actions = len([e for e in audit_entries if not e.get("success", True)])
            unique_users = len(set(e.get("user", "unknown") for e in audit_entries))
            
            # Actividades por tipo
            action_types = {}
            for entry in audit_entries:
                action = entry.get("action", "unknown")
                action_types[action] = action_types.get(action, 0) + 1
            
            # Usuarios más activos
            user_activity = {}
            for entry in audit_entries:
                user = entry.get("user", "unknown")
                user_activity[user] = user_activity.get(user, 0) + 1
            
            top_users = sorted(user_activity.items(), key=lambda x: x[1], reverse=True)[:10]
            
            return {
                "total_actions": total_actions,
                "failed_actions": failed_actions,
                "success_rate": ((total_actions - failed_actions) / total_actions * 100) if total_actions > 0 else 0,
                "unique_users": unique_users,
                "action_types": action_types,
                "top_users": top_users,
                "time_range_hours": hours
            }
            
        except Exception as e:
            self._log_internal_error(f"Error generando dashboard de seguridad: {str(e)}")
            return {"error": str(e)}

# Función de utilidad para usar el auditor
def get_security_auditor() -> SecurityAuditor:
    """Obtener instancia del auditor de seguridad"""
    if 'security_auditor' not in st.session_state:
        st.session_state['security_auditor'] = SecurityAuditor()
    return st.session_state['security_auditor']
