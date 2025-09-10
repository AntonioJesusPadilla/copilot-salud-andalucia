"""
Configuración de Optimización y Seguridad - Copilot Salud Andalucía
Configuraciones centralizadas para todos los sistemas de optimización
"""

import os
from typing import Dict, Any

class OptimizationConfig:
    """Configuración centralizada para optimización y seguridad"""
    
    # Configuración de Cache
    CACHE_CONFIG = {
        'default_ttl': {
            'admin': 3600,      # 1 hora
            'gestor': 1800,     # 30 minutos
            'analista': 900,    # 15 minutos
            'invitado': 300     # 5 minutos
        },
        'max_cache_size': 100,  # Máximo 100 entradas en cache
        'cleanup_interval': 3600,  # Limpiar cache cada hora
        'enable_compression': True
    }
    
    # Configuración de Rate Limiting
    RATE_LIMITING_CONFIG = {
        'limits': {
            'login': (5, 300),           # 5 intentos por 5 minutos
            'ai_query': (10, 60),        # 10 consultas IA por minuto
            'data_access': (100, 60),    # 100 accesos a datos por minuto
            'admin_action': (20, 60),    # 20 acciones admin por minuto
            'user_management': (5, 300), # 5 gestiones de usuario por 5 minutos
            'system_config': (3, 600),   # 3 configuraciones por 10 minutos
            'general': (200, 60)         # 200 acciones generales por minuto
        },
        'block_config': {
            'max_failed_attempts': 5,
            'block_duration': 1800,      # 30 minutos
            'escalation_factor': 2,
            'max_block_duration': 86400  # 24 horas máximo
        }
    }
    
    # Configuración de Auditoría
    AUDIT_CONFIG = {
        'log_retention_days': 90,
        'suspicious_thresholds': {
            'max_actions_per_hour': 100,
            'max_failed_logins_per_hour': 5,
            'max_ai_queries_per_hour': 50,
            'max_data_access_per_hour': 200,
            'suspicious_ip_changes': 3,
            'unusual_hours_access': True
        },
        'log_levels': ['info', 'warning', 'error', 'critical'],
        'enable_real_time_monitoring': True
    }
    
    # Configuración de Encriptación
    ENCRYPTION_CONFIG = {
        'algorithm': 'Fernet',
        'key_derivation': 'PBKDF2HMAC',
        'iterations': 100000,
        'salt_length': 32,
        'key_rotation_days': 90,
        'enable_integrity_checks': True
    }
    
    # Configuración de Rendimiento
    PERFORMANCE_CONFIG = {
        'enable_async_processing': True,
        'max_concurrent_requests': 10,
        'request_timeout': 30,
        'enable_data_compression': True,
        'optimize_dataframes': True,
        'enable_lazy_loading': True
    }
    
    # Configuración de Seguridad
    SECURITY_CONFIG = {
        'enable_ip_whitelist': False,
        'enable_geolocation_blocking': False,
        'enable_session_timeout': True,
        'session_timeout_minutes': 120,
        'enable_2fa': False,
        'password_policy': {
            'min_length': 8,
            'require_special_chars': True,
            'require_numbers': True,
            'require_uppercase': True
        }
    }
    
    # Configuración de Monitoreo
    MONITORING_CONFIG = {
        'enable_metrics_collection': True,
        'metrics_retention_days': 30,
        'enable_alerts': True,
        'alert_thresholds': {
            'high_cpu_usage': 80,
            'high_memory_usage': 85,
            'high_error_rate': 5,
            'low_response_time': 1000  # ms
        },
        'enable_health_checks': True
    }
    
    @classmethod
    def get_config(cls, section: str) -> Dict[str, Any]:
        """Obtener configuración de una sección específica"""
        config_map = {
            'cache': cls.CACHE_CONFIG,
            'rate_limiting': cls.RATE_LIMITING_CONFIG,
            'audit': cls.AUDIT_CONFIG,
            'encryption': cls.ENCRYPTION_CONFIG,
            'performance': cls.PERFORMANCE_CONFIG,
            'security': cls.SECURITY_CONFIG,
            'monitoring': cls.MONITORING_CONFIG
        }
        return config_map.get(section, {})
    
    @classmethod
    def get_all_configs(cls) -> Dict[str, Dict[str, Any]]:
        """Obtener todas las configuraciones"""
        return {
            'cache': cls.CACHE_CONFIG,
            'rate_limiting': cls.RATE_LIMITING_CONFIG,
            'audit': cls.AUDIT_CONFIG,
            'encryption': cls.ENCRYPTION_CONFIG,
            'performance': cls.PERFORMANCE_CONFIG,
            'security': cls.SECURITY_CONFIG,
            'monitoring': cls.MONITORING_CONFIG
        }
    
    @classmethod
    def update_config(cls, section: str, key: str, value: Any) -> bool:
        """Actualizar una configuración específica"""
        try:
            config = cls.get_config(section)
            if config and key in config:
                config[key] = value
                return True
            return False
        except Exception:
            return False
    
    @classmethod
    def get_environment_overrides(cls) -> Dict[str, Any]:
        """Obtener configuraciones desde variables de entorno"""
        overrides = {}
        
        # Cache TTL desde variables de entorno
        cache_ttl_admin = os.getenv('CACHE_TTL_ADMIN')
        if cache_ttl_admin:
            overrides['cache_ttl_admin'] = int(cache_ttl_admin)
        
        # Rate limiting desde variables de entorno
        max_ai_queries = os.getenv('MAX_AI_QUERIES_PER_HOUR')
        if max_ai_queries:
            overrides['max_ai_queries_per_hour'] = int(max_ai_queries)
        
        # Configuración de seguridad
        enable_2fa = os.getenv('ENABLE_2FA')
        if enable_2fa:
            overrides['enable_2fa'] = enable_2fa.lower() == 'true'
        
        return overrides
    
    @classmethod
    def apply_environment_overrides(cls):
        """Aplicar configuraciones desde variables de entorno"""
        overrides = cls.get_environment_overrides()
        
        # Aplicar overrides específicos
        if 'cache_ttl_admin' in overrides:
            cls.CACHE_CONFIG['default_ttl']['admin'] = overrides['cache_ttl_admin']
        
        if 'max_ai_queries_per_hour' in overrides:
            cls.RATE_LIMITING_CONFIG['limits']['ai_query'] = (
                overrides['max_ai_queries_per_hour'], 60
            )
        
        if 'enable_2fa' in overrides:
            cls.SECURITY_CONFIG['enable_2fa'] = overrides['enable_2fa']

# Aplicar configuraciones de entorno al importar
OptimizationConfig.apply_environment_overrides()
