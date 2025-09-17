"""
Wrapper Síncrono para Procesamiento Asíncrono - Copilot Salud Andalucía
Integración de procesamiento asíncrono con Streamlit
"""

import streamlit as st
import asyncio
import threading
from typing import Dict, Any, Optional
from datetime import datetime
from modules.ai.async_ai_processor import get_async_ai_processor

class StreamlitAsyncWrapper:
    def __init__(self):
        """Inicializar wrapper para procesamiento asíncrono"""
        self.async_processor = get_async_ai_processor()
        self._loop = None
        self._thread = None
    
    def _get_or_create_loop(self):
        """Obtener o crear loop de asyncio en thread separado"""
        if self._loop is None or self._loop.is_closed():
            def run_loop():
                self._loop = asyncio.new_event_loop()
                asyncio.set_event_loop(self._loop)
                self._loop.run_forever()
            
            self._thread = threading.Thread(target=run_loop, daemon=True)
            self._thread.start()
            
            # Esperar a que el loop esté listo
            while self._loop is None:
                pass
        
        return self._loop
    
    def process_query_sync(self, query: str, data: dict, user_role: str, 
                          user_context: dict = None) -> Dict[str, Any]:
        """Procesar consulta de forma síncrona usando asyncio"""
        try:
            # Obtener loop de asyncio
            loop = self._get_or_create_loop()
            
            # Crear tarea asíncrona
            future = asyncio.run_coroutine_threadsafe(
                self.async_processor.process_query_async(query, data, user_role, user_context),
                loop
            )
            
            # Esperar resultado con timeout
            result = future.result(timeout=30)
            return result
            
        except Exception as e:
            return {
                "error": f"Error en procesamiento asíncrono: {str(e)}",
                "analysis_type": "error",
                "main_insight": "Error procesando consulta con IA",
                "timestamp": datetime.now().isoformat()
            }
    
    def process_multiple_queries(self, queries: list, data: dict, user_role: str, 
                                user_context: dict = None) -> list:
        """Procesar múltiples consultas de forma asíncrona"""
        try:
            loop = self._get_or_create_loop()
            
            # Crear tareas para todas las consultas
            tasks = []
            for query in queries:
                task = asyncio.run_coroutine_threadsafe(
                    self.async_processor.process_query_async(query, data, user_role, user_context),
                    loop
                )
                tasks.append(task)
            
            # Esperar todas las tareas
            results = []
            for task in tasks:
                try:
                    result = task.result(timeout=30)
                    results.append(result)
                except Exception as e:
                    results.append({
                        "error": str(e),
                        "analysis_type": "error"
                    })
            
            return results
            
        except Exception as e:
            return [{
                "error": f"Error procesando consultas múltiples: {str(e)}",
                "analysis_type": "error"
            } for _ in queries]
    
    def get_processing_metrics(self) -> Dict[str, Any]:
        """Obtener métricas de procesamiento"""
        return self.async_processor.get_metrics()
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Obtener estadísticas del cache"""
        return self.async_processor.get_cache_stats()
    
    def clear_ai_cache(self) -> None:
        """Limpiar cache de IA"""
        self.async_processor.clear_cache()
    
    def render_processing_status(self) -> None:
        """Renderizar estado del procesamiento asíncrono"""
        metrics = self.get_processing_metrics()
        cache_stats = self.get_cache_stats()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("🔄 Total Requests", metrics.get('total_requests', 0))
        
        with col2:
            success_rate = (
                metrics.get('successful_requests', 0) / 
                max(1, metrics.get('total_requests', 1))
            ) * 100
            st.metric("✅ Tasa de Éxito", f"{success_rate:.1f}%")
        
        with col3:
            avg_time = metrics.get('average_response_time', 0)
            st.metric("⏱️ Tiempo Promedio", f"{avg_time:.2f}s")
        
        with col4:
            cache_hit_rate = cache_stats.get('cache_hit_rate', 0)
            st.metric("💾 Cache Hit Rate", f"{cache_hit_rate:.1f}%")

# Función de utilidad para usar el wrapper
def get_streamlit_async_wrapper() -> StreamlitAsyncWrapper:
    """Obtener instancia del wrapper asíncrono"""
    if 'streamlit_async_wrapper' not in st.session_state:
        st.session_state['streamlit_async_wrapper'] = StreamlitAsyncWrapper()
    return st.session_state['streamlit_async_wrapper']
