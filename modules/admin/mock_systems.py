"""
Sistemas Mock para Dashboard Administrativo
Implementaciones simuladas cuando los sistemas reales no están disponibles
"""

import random
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any
import json


class MockPerformanceOptimizer:
    """Simulador del sistema de optimización de rendimiento"""

    def __init__(self):
        self.cache_data = {
            'admin': random.randint(50, 150),
            'gestor': random.randint(30, 100),
            'analista': random.randint(20, 80),
            'invitado': random.randint(10, 50)
        }

    def get_cache_stats(self) -> Dict:
        """Obtener estadísticas de cache simuladas"""
        total_entries = sum(self.cache_data.values())
        memory_usage = f"{total_entries * 0.25:.1f} MB"

        return {
            'total_entries': total_entries,
            'memory_usage': memory_usage,
            'entries_by_role': self.cache_data.copy(),
            'hit_rate': random.uniform(75, 95),
            'last_cleanup': datetime.now().isoformat()
        }

    def clear_user_cache(self, role: str = None):
        """Limpiar cache (simulado)"""
        if role:
            self.cache_data[role] = 0
        else:
            for key in self.cache_data:
                self.cache_data[key] = 0
        return True


class MockSecurityAuditor:
    """Simulador del sistema de auditoría de seguridad"""

    def get_security_dashboard_data(self, hours: int = 24) -> Dict:
        """Obtener datos de seguridad simulados"""
        total_actions = random.randint(200, 800)
        failed_actions = random.randint(5, 25)
        success_rate = ((total_actions - failed_actions) / total_actions) * 100

        # Generar tipos de acciones
        action_types = {
            'login': random.randint(50, 150),
            'data_access': random.randint(100, 300),
            'report_generation': random.randint(20, 80),
            'map_visualization': random.randint(30, 120),
            'admin_operations': random.randint(5, 20)
        }

        # Top usuarios (simulados)
        top_users = [
            ['admin', random.randint(20, 50)],
            ['gestor.malaga', random.randint(15, 40)],
            ['analista.datos', random.randint(10, 35)],
            ['user_001', random.randint(8, 25)],
            ['user_002', random.randint(5, 20)]
        ]

        return {
            'total_actions': total_actions,
            'failed_actions': failed_actions,
            'success_rate': success_rate,
            'unique_users': random.randint(15, 50),
            'action_types': action_types,
            'top_users': top_users,
            'timestamp': datetime.now().isoformat()
        }


class MockRateLimiter:
    """Simulador del sistema de rate limiting"""

    def __init__(self):
        self.blocked_users = ['user_suspicious_1', 'test_user_blocked']
        self.suspicious_ips = ['192.168.1.100', '10.0.0.50']

    def get_system_stats(self) -> Dict:
        """Obtener estadísticas del sistema de rate limiting"""
        active_requests = {
            'data_access': random.randint(10, 50),
            'map_generation': random.randint(5, 25),
            'ai_analysis': random.randint(2, 15),
            'report_creation': random.randint(1, 10)
        }

        return {
            'active_blocks': len(self.blocked_users),
            'suspicious_ips': len(self.suspicious_ips),
            'total_limits': 12,  # Número de límites configurados
            'active_requests': active_requests,
            'requests_per_minute': sum(active_requests.values()),
            'last_update': datetime.now().isoformat()
        }

    def unblock_user(self, username: str):
        """Desbloquear usuario"""
        if username in self.blocked_users:
            self.blocked_users.remove(username)
        return True

    def clear_suspicious_ip(self, ip: str):
        """Limpiar IP sospechosa"""
        if ip in self.suspicious_ips:
            self.suspicious_ips.remove(ip)
        return True


class MockDataEncryption:
    """Simulador del sistema de encriptación"""

    def get_encryption_status(self) -> Dict:
        """Obtener estado del sistema de encriptación"""
        return {
            'algorithm': 'AES-256-GCM',
            'key_exists': True,
            'salt_exists': True,
            'last_modified': datetime.now().isoformat(),
            'encryption_enabled': True,
            'key_rotation_date': (datetime.now() - timedelta(days=random.randint(10, 90))).isoformat()
        }

    def validate_encryption_integrity(self) -> Dict:
        """Validar integridad del sistema de encriptación"""
        # Simular un test exitoso la mayoría de las veces
        is_working = random.random() > 0.1  # 90% de probabilidad de éxito

        return {
            'encryption_working': is_working,
            'test_timestamp': datetime.now().isoformat(),
            'test_duration_ms': random.randint(50, 200),
            'key_valid': True,
            'salt_valid': True,
            'error': None if is_working else 'Simulated test failure'
        }

    def rotate_encryption_key(self) -> bool:
        """Rotar clave de encriptación (simulado)"""
        # Simular proceso de rotación
        time.sleep(0.5)  # Simular tiempo de procesamiento
        return random.random() > 0.05  # 95% de probabilidad de éxito


class MockAIProcessor:
    """Simulador del procesador de IA"""

    def get_async_processing_metrics(self) -> Dict:
        """Obtener métricas de procesamiento asíncrono"""
        total_requests = random.randint(100, 500)
        successful = random.randint(int(total_requests * 0.85), total_requests)

        return {
            'total_requests': total_requests,
            'successful_requests': successful,
            'failed_requests': total_requests - successful,
            'average_response_time': random.uniform(1.2, 3.8),
            'cache_hits': random.randint(int(total_requests * 0.6), int(total_requests * 0.9)),
            'active_threads': random.randint(2, 8),
            'queue_size': random.randint(0, 15),
            'last_update': datetime.now().isoformat()
        }

    def clear_async_cache(self):
        """Limpiar cache asíncrono"""
        return True


def create_mock_systems() -> Dict[str, Any]:
    """Crear todos los sistemas mock"""
    return {
        'performance_optimizer': MockPerformanceOptimizer(),
        'security_auditor': MockSecurityAuditor(),
        'rate_limiter': MockRateLimiter(),
        'data_encryption': MockDataEncryption(),
        'ai_processor': MockAIProcessor()
    }


def initialize_admin_systems_safely():
    """Inicializar sistemas administrativos de forma segura"""
    systems = {}

    # Intentar importar sistemas reales, usar mock si fallan
    try:
        from modules.performance.performance_optimizer import PerformanceOptimizer
        systems['performance_optimizer'] = PerformanceOptimizer()
    except (ImportError, Exception):
        systems['performance_optimizer'] = MockPerformanceOptimizer()

    try:
        from modules.security.security_auditor import SecurityAuditor
        systems['security_auditor'] = SecurityAuditor()
    except (ImportError, Exception):
        systems['security_auditor'] = MockSecurityAuditor()

    try:
        from modules.security.rate_limiter import RateLimiter
        systems['rate_limiter'] = RateLimiter()
    except (ImportError, Exception):
        systems['rate_limiter'] = MockRateLimiter()

    try:
        from modules.security.data_encryption import DataEncryption
        systems['data_encryption'] = DataEncryption()
    except (ImportError, Exception):
        systems['data_encryption'] = MockDataEncryption()

    return systems