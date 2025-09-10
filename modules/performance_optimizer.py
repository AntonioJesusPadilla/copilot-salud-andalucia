"""
Módulo de Optimización de Rendimiento - Copilot Salud Andalucía
Sistema de cache inteligente por usuario y rol para mejorar rendimiento
"""

import streamlit as st
import pandas as pd
import hashlib
import time
import os
from typing import Dict, Any, Optional, Callable
from functools import wraps
import json

class PerformanceOptimizer:
    def __init__(self):
        """Inicializar optimizador de rendimiento"""
        self.cache_ttl = {
            'admin': 3600,      # 1 hora para admin
            'gestor': 1800,     # 30 min para gestor
            'analista': 900,    # 15 min para analista
            'invitado': 300     # 5 min para invitado
        }
        
        # Configuración de tipos de datos optimizados
        self.dtype_configs = {
            'demografia': {
                'municipio': 'string',
                'poblacion_2025': 'int32',
                'poblacion_2024': 'int32',
                'crecimiento_2024_2025': 'int16',
                'densidad_hab_km2_2025': 'float32',
                'renta_per_capita_2024': 'float32',
                'indice_envejecimiento_2025': 'float32'
            },
            'hospitales': {
                'nombre': 'string',
                'tipo_centro': 'string',
                'distrito_sanitario': 'string',
                'camas_funcionamiento_2025': 'int16',
                'personal_sanitario_2025': 'int16',
                'poblacion_referencia_2025': 'int32'
            },
            'servicios': {
                'centro_sanitario': 'string',
                'cardiologia': 'bool',
                'neurologia': 'bool',
                'uci_adultos': 'bool',
                'consultas_externas_anuales_2024': 'int32'
            },
            'accesibilidad': {
                'municipio_origen': 'string',
                'tiempo_coche_minutos': 'float32',
                'coste_transporte_euros': 'float32',
                'accesibilidad_score': 'float32'
            },
            'indicadores': {
                'distrito': 'string',
                'ratio_medico_1000_hab': 'float32',
                'esperanza_vida_2023': 'float32'
            }
        }
        
        # Datasets requeridos por rol
        self.role_datasets = {
            'admin': ['hospitales', 'demografia', 'servicios', 'accesibilidad', 'indicadores'],
            'gestor': ['hospitales', 'demografia', 'servicios', 'accesibilidad', 'indicadores'],
            'analista': ['demografia', 'indicadores', 'servicios'],
            'invitado': ['hospitales', 'demografia']
        }
    
    def get_user_cache_key(self, user_role: str, operation: str, params: dict = None) -> str:
        """Generar clave única de cache por usuario y operación"""
        key_data = f"{user_role}_{operation}_{str(sorted(params.items())) if params else ''}"
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def cached_data_loader(self, user_role: str, operation: str):
        """Decorador para cache inteligente por rol"""
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs):
                cache_key = self.get_user_cache_key(user_role, operation, kwargs)
                ttl = self.cache_ttl.get(user_role, 300)
                
                # Inicializar cache si no existe
                if 'performance_cache' not in st.session_state:
                    st.session_state['performance_cache'] = {}
                
                # Verificar cache
                if cache_key in st.session_state['performance_cache']:
                    cached_data, timestamp = st.session_state['performance_cache'][cache_key]
                    if time.time() - timestamp < ttl:
                        st.info(f"📊 Datos cargados desde cache (válido por {int((ttl - (time.time() - timestamp))/60)} min)")
                        return cached_data
                
                # Ejecutar función y cachear resultado
                with st.spinner(f"🔄 Cargando datos para {user_role}..."):
                    result = func(*args, **kwargs)
                
                if result is not None:
                    st.session_state['performance_cache'][cache_key] = (result, time.time())
                    st.success(f"✅ Datos cacheados para {user_role} (TTL: {ttl//60} min)")
                
                return result
            return wrapper
        return decorator
    
    def load_health_datasets_optimized(self, user_role: str = "invitado") -> Optional[Dict[str, pd.DataFrame]]:
        """Cargar datasets optimizados según el rol del usuario"""
        try:
            datasets = {}
            file_mapping = {
                'hospitales': 'data/raw/hospitales_malaga_2025.csv',
                'demografia': 'data/raw/demografia_malaga_2025.csv', 
                'servicios': 'data/raw/servicios_sanitarios_2025.csv',
                'accesibilidad': 'data/raw/accesibilidad_sanitaria_2025.csv',
                'indicadores': 'data/raw/indicadores_salud_2025.csv'
            }
            
            # Obtener datasets requeridos para el rol
            datasets_to_load = self.role_datasets.get(user_role, ['hospitales'])
            
            loaded_count = 0
            total_count = len(datasets_to_load)
            
            for key in datasets_to_load:
                if key in file_mapping and os.path.exists(file_mapping[key]):
                    try:
                        # Obtener configuración de tipos optimizada
                        dtype_config = self.dtype_configs.get(key, {})
                        
                        # Cargar con tipos optimizados
                        datasets[key] = pd.read_csv(file_mapping[key], dtype=dtype_config)
                        loaded_count += 1
                        
                        # Mostrar progreso
                        progress = loaded_count / total_count
                        st.progress(progress, text=f"Cargando {key}... ({loaded_count}/{total_count})")
                        
                    except Exception as file_error:
                        st.warning(f"⚠️ Error cargando {file_mapping[key]}: {str(file_error)}")
                else:
                    st.warning(f"⚠️ Archivo no encontrado: {file_mapping.get(key, 'N/A')}")
            
            if datasets:
                st.success(f"✅ Cargados {loaded_count}/{total_count} datasets optimizados para {user_role}")
                
                # Mostrar estadísticas de memoria
                total_memory = sum(df.memory_usage(deep=True).sum() for df in datasets.values())
                st.info(f"💾 Memoria utilizada: {total_memory / 1024 / 1024:.2f} MB")
                
                return datasets
            else:
                st.error("❌ No se pudieron cargar los datasets")
                return None
                
        except Exception as e:
            st.error(f"❌ Error crítico cargando datasets: {str(e)}")
            return None
    
    def get_optimized_dtypes(self, dataset_key: str) -> dict:
        """Obtener configuración optimizada de tipos de datos por dataset"""
        return self.dtype_configs.get(dataset_key, {})
    
    def clear_user_cache(self, user_role: str = None):
        """Limpiar cache del usuario o todo el cache"""
        if 'performance_cache' not in st.session_state:
            return
        
        if user_role:
            # Limpiar solo cache del usuario específico
            keys_to_remove = [k for k in st.session_state['performance_cache'].keys() 
                            if k.startswith(f"{user_role}_")]
            for key in keys_to_remove:
                del st.session_state['performance_cache'][key]
            st.success(f"🗑️ Cache limpiado para {user_role}")
        else:
            # Limpiar todo el cache
            st.session_state['performance_cache'] = {}
            st.success("🗑️ Todo el cache limpiado")
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Obtener estadísticas del cache"""
        if 'performance_cache' not in st.session_state:
            return {"total_entries": 0, "memory_usage": "0 MB"}
        
        cache = st.session_state['performance_cache']
        total_entries = len(cache)
        
        # Calcular memoria aproximada
        memory_usage = 0
        for key, (data, timestamp) in cache.items():
            if isinstance(data, dict):
                for df in data.values():
                    if isinstance(df, pd.DataFrame):
                        memory_usage += df.memory_usage(deep=True).sum()
            elif isinstance(data, pd.DataFrame):
                memory_usage += data.memory_usage(deep=True).sum()
        
        return {
            "total_entries": total_entries,
            "memory_usage": f"{memory_usage / 1024 / 1024:.2f} MB",
            "entries_by_role": self._count_entries_by_role(cache)
        }
    
    def _count_entries_by_role(self, cache: Dict) -> Dict[str, int]:
        """Contar entradas de cache por rol"""
        role_counts = {}
        for key in cache.keys():
            role = key.split('_')[0]
            role_counts[role] = role_counts.get(role, 0) + 1
        return role_counts
    
    def optimize_dataframe(self, df: pd.DataFrame, dataset_type: str = None) -> pd.DataFrame:
        """Optimizar DataFrame reduciendo uso de memoria"""
        if df.empty:
            return df
        
        # Convertir tipos de datos
        for col in df.columns:
            if df[col].dtype == 'object':
                # Intentar convertir a string si es texto
                if df[col].str.len().max() < 50:  # Strings cortos
                    df[col] = df[col].astype('string')
            elif df[col].dtype == 'int64':
                # Reducir enteros
                if df[col].min() >= 0 and df[col].max() <= 255:
                    df[col] = df[col].astype('uint8')
                elif df[col].min() >= -128 and df[col].max() <= 127:
                    df[col] = df[col].astype('int8')
                elif df[col].min() >= 0 and df[col].max() <= 65535:
                    df[col] = df[col].astype('uint16')
                elif df[col].min() >= -32768 and df[col].max() <= 32767:
                    df[col] = df[col].astype('int16')
                elif df[col].min() >= 0 and df[col].max() <= 4294967295:
                    df[col] = df[col].astype('uint32')
                else:
                    df[col] = df[col].astype('int32')
            elif df[col].dtype == 'float64':
                # Reducir flotantes
                if df[col].min() >= -3.4e38 and df[col].max() <= 3.4e38:
                    df[col] = df[col].astype('float32')
        
        return df

# Función de utilidad para usar el optimizador
def get_performance_optimizer() -> PerformanceOptimizer:
    """Obtener instancia del optimizador de rendimiento"""
    if 'performance_optimizer' not in st.session_state:
        st.session_state['performance_optimizer'] = PerformanceOptimizer()
    return st.session_state['performance_optimizer']
