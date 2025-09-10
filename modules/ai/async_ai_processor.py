"""
Procesador Asíncrono de IA - Copilot Salud Andalucía
Sistema de procesamiento asíncrono para consultas IA con optimización de rendimiento
"""

import asyncio
import aiohttp
import streamlit as st
import json
import time
from typing import Dict, Any, Optional, List
from datetime import datetime
import os
from concurrent.futures import ThreadPoolExecutor
import threading

class AsyncAIProcessor:
    def __init__(self):
        """Inicializar procesador asíncrono de IA"""
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"
        self.model = "llama-3.3-70b-versatile"
        
        # Configuración de procesamiento asíncrono
        self.max_concurrent_requests = 5
        self.request_timeout = 30
        self.retry_attempts = 3
        self.retry_delay = 1
        
        # Pool de threads para operaciones síncronas
        self.thread_pool = ThreadPoolExecutor(max_workers=3)
        
        # Cache de respuestas para evitar consultas duplicadas
        self.response_cache = {}
        self.cache_ttl = 300  # 5 minutos
        
        # Métricas de rendimiento
        self.metrics = {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'average_response_time': 0,
            'cache_hits': 0
        }
    
    async def process_query_async(self, query: str, data: dict, user_role: str, 
                                user_context: dict = None) -> Dict[str, Any]:
        """Procesar consulta IA de forma asíncrona con optimización"""
        start_time = time.time()
        
        try:
            # Verificar cache primero
            cache_key = self._generate_cache_key(query, user_role)
            cached_response = self._get_cached_response(cache_key)
            if cached_response:
                self.metrics['cache_hits'] += 1
                return cached_response
            
            # Preparar contexto optimizado según rol
            context = self._prepare_context_by_role(data, user_role, user_context)
            
            # Procesar consulta en background
            response = await self._make_groq_request_async(query, context, user_role)
            
            # Procesar respuesta
            processed_response = await self._process_response_async(response, data, user_role)
            
            # Cachear respuesta
            self._cache_response(cache_key, processed_response)
            
            # Actualizar métricas
            self._update_metrics(start_time, True)
            
            return processed_response
            
        except Exception as e:
            self._update_metrics(start_time, False)
            return {
                "error": str(e),
                "analysis_type": "error",
                "main_insight": f"Error procesando consulta: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
    
    async def _make_groq_request_async(self, query: str, context: str, user_role: str) -> Dict[str, Any]:
        """Realizar petición asíncrona a Groq API"""
        headers = {
            "Authorization": f"Bearer {self.groq_api_key}",
            "Content-Type": "application/json"
        }
        
        # Preparar prompt optimizado
        system_prompt = self._create_optimized_system_prompt(context, user_role)
        
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query}
            ],
            "temperature": 0.7,
            "max_tokens": 2000,
            "stream": False
        }
        
        timeout = aiohttp.ClientTimeout(total=self.request_timeout)
        
        async with aiohttp.ClientSession(timeout=timeout) as session:
            for attempt in range(self.retry_attempts):
                try:
                    async with session.post(self.base_url, headers=headers, json=payload) as response:
                        if response.status == 200:
                            return await response.json()
                        elif response.status == 429:  # Rate limit
                            wait_time = self.retry_delay * (2 ** attempt)
                            await asyncio.sleep(wait_time)
                            continue
                        else:
                            error_text = await response.text()
                            raise Exception(f"API Error {response.status}: {error_text}")
                            
                except asyncio.TimeoutError:
                    if attempt < self.retry_attempts - 1:
                        await asyncio.sleep(self.retry_delay * (2 ** attempt))
                        continue
                    raise Exception("Timeout en petición a Groq API")
                
                except Exception as e:
                    if attempt < self.retry_attempts - 1:
                        await asyncio.sleep(self.retry_delay * (2 ** attempt))
                        continue
                    raise e
            
            raise Exception("Máximo número de reintentos alcanzado")
    
    def _create_optimized_system_prompt(self, context: str, user_role: str) -> str:
        """Crear prompt del sistema optimizado según el rol"""
        role_prompts = {
            'admin': """
            Eres un asistente especializado en análisis sociosanitario con acceso administrativo completo.
            Puedes acceder a todos los datos del sistema sanitario de Málaga.
            Proporciona análisis ejecutivos, métricas de rendimiento y recomendaciones estratégicas.
            """,
            'gestor': """
            Eres un asistente especializado en gestión sanitaria operacional.
            Te enfocas en optimización de recursos, planificación y gestión de servicios.
            Proporciona análisis operacionales y recomendaciones de gestión.
            """,
            'analista': """
            Eres un asistente especializado en análisis estadístico y de datos sanitarios.
            Te enfocas en análisis técnicos, visualizaciones y estadísticas avanzadas.
            Proporciona análisis detallados y metodologías estadísticas.
            """,
            'invitado': """
            Eres un asistente de consulta para información básica del sistema sanitario.
            Proporcionas información general y consultas básicas sobre salud pública.
            """
        }
        
        base_prompt = role_prompts.get(user_role, role_prompts['invitado'])
        
        return f"""
        {base_prompt}
        
        CONTEXTO DE DATOS:
        {context}
        
        INSTRUCCIONES:
        1. Responde en español
        2. Sé preciso y basado en datos
        3. Proporciona visualizaciones cuando sea apropiado
        4. Incluye métricas específicas cuando sea relevante
        5. Adapta el nivel técnico al rol del usuario
        """
    
    def _prepare_context_by_role(self, data: dict, user_role: str, user_context: dict = None) -> str:
        """Preparar contexto optimizado según permisos del usuario"""
        context_parts = []
        
        # Datos básicos para todos los roles
        if 'hospitales' in data:
            context_parts.append(f"Hospitales: {len(data['hospitales'])} centros")
        
        if 'demografia' in data:
            total_pop = data['demografia']['poblacion_2025'].sum()
            context_parts.append(f"Población total: {total_pop:,} habitantes")
        
        # Datos específicos por rol
        if user_role in ['admin', 'gestor']:
            if 'accesibilidad' in data:
                avg_time = data['accesibilidad']['tiempo_coche_minutos'].mean()
                context_parts.append(f"Tiempo medio de acceso: {avg_time:.1f} minutos")
        
        if user_role in ['admin', 'analista']:
            if 'indicadores' in data:
                context_parts.append(f"Indicadores de salud: {len(data['indicadores'])} distritos")
            
            if 'servicios' in data:
                context_parts.append(f"Servicios sanitarios: {len(data['servicios'])} centros")
        
        # Contexto del usuario si está disponible
        if user_context:
            context_parts.append(f"Usuario: {user_context.get('name', 'N/A')}")
            context_parts.append(f"Organización: {user_context.get('organization', 'N/A')}")
        
        return " | ".join(context_parts)
    
    async def _process_response_async(self, response: dict, data: dict, user_role: str) -> Dict[str, Any]:
        """Procesar respuesta de la IA de forma asíncrona"""
        try:
            # Extraer contenido de la respuesta
            if 'choices' in response and len(response['choices']) > 0:
                content = response['choices'][0]['message']['content']
            else:
                return {
                    "error": "Respuesta inválida de la IA",
                    "analysis_type": "error"
                }
            
            # Procesar contenido en thread pool para operaciones síncronas
            loop = asyncio.get_event_loop()
            processed_content = await loop.run_in_executor(
                self.thread_pool,
                self._parse_ai_response,
                content,
                data,
                user_role
            )
            
            return processed_content
            
        except Exception as e:
            return {
                "error": f"Error procesando respuesta: {str(e)}",
                "analysis_type": "error"
            }
    
    def _parse_ai_response(self, content: str, data: dict, user_role: str) -> Dict[str, Any]:
        """Parsear respuesta de la IA (ejecutado en thread pool)"""
        try:
            # Análisis básico del contenido
            analysis_type = self._detect_analysis_type(content)
            
            # Extraer métricas si están presentes
            metrics = self._extract_metrics(content)
            
            # Generar recomendaciones
            recommendations = self._generate_recommendations(content, user_role)
            
            # Detectar si necesita visualización
            needs_visualization = self._needs_visualization(content)
            
            return {
                "main_insight": content[:200] + "..." if len(content) > 200 else content,
                "full_response": content,
                "analysis_type": analysis_type,
                "metrics": metrics,
                "recommendations": recommendations,
                "needs_visualization": needs_visualization,
                "data_query": self._generate_data_query(content, data),
                "chart_config": self._generate_chart_config(content, analysis_type),
                "timestamp": datetime.now().isoformat(),
                "user_role": user_role
            }
            
        except Exception as e:
            return {
                "error": f"Error parseando respuesta: {str(e)}",
                "analysis_type": "error"
            }
    
    def _detect_analysis_type(self, content: str) -> str:
        """Detectar tipo de análisis basado en el contenido"""
        content_lower = content.lower()
        
        if any(word in content_lower for word in ['gráfico', 'chart', 'visualización', 'plot']):
            return 'visualization'
        elif any(word in content_lower for word in ['estadística', 'correlación', 'regresión', 'análisis']):
            return 'statistical'
        elif any(word in content_lower for word in ['tendencia', 'predicción', 'forecast', 'proyección']):
            return 'predictive'
        elif any(word in content_lower for word in ['recomendación', 'sugerencia', 'mejora', 'optimización']):
            return 'recommendation'
        else:
            return 'general'
    
    def _extract_metrics(self, content: str) -> List[Dict[str, Any]]:
        """Extraer métricas del contenido de la respuesta"""
        metrics = []
        
        # Buscar patrones de métricas en el texto
        import re
        
        # Patrón para números con unidades
        metric_pattern = r'(\d+(?:\.\d+)?)\s*([a-zA-Z%]+)'
        matches = re.findall(metric_pattern, content)
        
        for value, unit in matches:
            try:
                metrics.append({
                    "name": f"Métrica {len(metrics) + 1}",
                    "value": float(value),
                    "unit": unit
                })
            except ValueError:
                continue
        
        return metrics[:5]  # Máximo 5 métricas
    
    def _generate_recommendations(self, content: str, user_role: str) -> List[str]:
        """Generar recomendaciones basadas en el contenido y rol"""
        recommendations = []
        
        # Recomendaciones específicas por rol
        role_recommendations = {
            'admin': [
                "Revisar métricas de rendimiento del sistema",
                "Evaluar distribución de recursos por distrito",
                "Implementar mejoras en accesibilidad"
            ],
            'gestor': [
                "Optimizar asignación de personal sanitario",
                "Mejorar tiempos de respuesta en servicios",
                "Planificar expansión de infraestructura"
            ],
            'analista': [
                "Profundizar en análisis estadísticos",
                "Crear visualizaciones adicionales",
                "Validar correlaciones encontradas"
            ],
            'invitado': [
                "Consultar información adicional disponible",
                "Contactar con administrador para más detalles"
            ]
        }
        
        # Añadir recomendaciones del rol
        recommendations.extend(role_recommendations.get(user_role, []))
        
        # Añadir recomendaciones basadas en contenido
        if 'bajo' in content.lower() or 'deficiente' in content.lower():
            recommendations.append("Implementar medidas de mejora inmediata")
        
        if 'alto' in content.lower() or 'excelente' in content.lower():
            recommendations.append("Mantener y replicar buenas prácticas")
        
        return recommendations[:3]  # Máximo 3 recomendaciones
    
    def _needs_visualization(self, content: str) -> bool:
        """Determinar si la respuesta necesita visualización"""
        visualization_keywords = [
            'gráfico', 'chart', 'visualización', 'plot', 'diagrama',
            'distribución', 'tendencia', 'comparación', 'análisis visual'
        ]
        
        return any(keyword in content.lower() for keyword in visualization_keywords)
    
    def _generate_data_query(self, content: str, data: dict) -> str:
        """Generar consulta de datos basada en el contenido"""
        # Esta es una implementación simplificada
        # En una implementación real, se usaría NLP para generar consultas SQL/Pandas
        
        if 'hospitales' in content.lower():
            return "data['hospitales']"
        elif 'demografía' in content.lower() or 'población' in content.lower():
            return "data['demografia']"
        elif 'servicios' in content.lower():
            return "data['servicios']"
        else:
            return "data"
    
    def _generate_chart_config(self, content: str, analysis_type: str) -> Dict[str, Any]:
        """Generar configuración de gráfico basada en el contenido"""
        chart_configs = {
            'visualization': {
                'type': 'bar',
                'title': 'Análisis Visual'
            },
            'statistical': {
                'type': 'scatter',
                'title': 'Análisis Estadístico'
            },
            'predictive': {
                'type': 'line',
                'title': 'Análisis Predictivo'
            },
            'recommendation': {
                'type': 'pie',
                'title': 'Recomendaciones'
            },
            'general': {
                'type': 'bar',
                'title': 'Análisis General'
            }
        }
        
        return chart_configs.get(analysis_type, chart_configs['general'])
    
    def _generate_cache_key(self, query: str, user_role: str) -> str:
        """Generar clave de cache para la consulta"""
        import hashlib
        key_data = f"{user_role}_{query}_{datetime.now().strftime('%Y%m%d%H')}"
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def _get_cached_response(self, cache_key: str) -> Optional[Dict[str, Any]]:
        """Obtener respuesta del cache"""
        if cache_key in self.response_cache:
            cached_data, timestamp = self.response_cache[cache_key]
            if time.time() - timestamp < self.cache_ttl:
                return cached_data
            else:
                # Limpiar entrada expirada
                del self.response_cache[cache_key]
        return None
    
    def _cache_response(self, cache_key: str, response: Dict[str, Any]) -> None:
        """Cachear respuesta"""
        self.response_cache[cache_key] = (response, time.time())
        
        # Limpiar cache si está lleno
        if len(self.response_cache) > 100:
            # Eliminar entradas más antiguas
            oldest_key = min(self.response_cache.keys(), 
                           key=lambda k: self.response_cache[k][1])
            del self.response_cache[oldest_key]
    
    def _update_metrics(self, start_time: float, success: bool) -> None:
        """Actualizar métricas de rendimiento"""
        self.metrics['total_requests'] += 1
        
        if success:
            self.metrics['successful_requests'] += 1
        else:
            self.metrics['failed_requests'] += 1
        
        # Actualizar tiempo promedio de respuesta
        response_time = time.time() - start_time
        total_requests = self.metrics['total_requests']
        current_avg = self.metrics['average_response_time']
        
        self.metrics['average_response_time'] = (
            (current_avg * (total_requests - 1) + response_time) / total_requests
        )
    
    def get_metrics(self) -> Dict[str, Any]:
        """Obtener métricas de rendimiento"""
        return self.metrics.copy()
    
    def clear_cache(self) -> None:
        """Limpiar cache de respuestas"""
        self.response_cache.clear()
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Obtener estadísticas del cache"""
        return {
            'cache_size': len(self.response_cache),
            'cache_hit_rate': (
                self.metrics['cache_hits'] / max(1, self.metrics['total_requests'])
            ) * 100,
            'total_requests': self.metrics['total_requests'],
            'success_rate': (
                self.metrics['successful_requests'] / max(1, self.metrics['total_requests'])
            ) * 100
        }

# Función de utilidad para usar el procesador asíncrono
def get_async_ai_processor() -> AsyncAIProcessor:
    """Obtener instancia del procesador asíncrono de IA"""
    if 'async_ai_processor' not in st.session_state:
        st.session_state['async_ai_processor'] = AsyncAIProcessor()
    return st.session_state['async_ai_processor']
