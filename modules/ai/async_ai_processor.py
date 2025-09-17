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
import re

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
        if not self.groq_api_key:
            raise Exception("GROQ_API_KEY no configurada")

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
            Eres un DIRECTOR EJECUTIVO del Sistema Sanitario de Málaga especializado en análisis estratégico de alto nivel.

            TU ENFOQUE ESPECÍFICO:
            - Análisis de rendimiento global del sistema sanitario
            - Evaluación de KPIs críticos y métricas de gestión ejecutiva
            - Identificación de oportunidades de mejora sistémica
            - Recomendaciones para decisiones estratégicas de recursos
            - Análisis de impacto económico y eficiencia operativa
            - Evaluación de cumplimiento de objetivos institucionales

            FORMATO DE RESPUESTA REQUERIDO:
            - Resumen ejecutivo con conclusiones clave
            - Métricas críticas y tendencias principales
            - Recomendaciones estratégicas priorizadas
            - Análisis de riesgos y oportunidades
            - Próximos pasos operativos concretos
            """,
            'gestor': """
            Eres un GESTOR OPERACIONAL del Sistema Sanitario de Málaga especializado en optimización de servicios.

            TU ENFOQUE ESPECÍFICO:
            - Optimización de flujos de trabajo y procesos operativos
            - Gestión eficiente de recursos humanos y materiales
            - Planificación táctica de servicios sanitarios
            - Coordinación entre centros y departamentos
            - Análisis de capacidad y demanda operativa
            - Mejora de la experiencia del usuario/paciente

            FORMATO DE RESPUESTA REQUERIDO:
            - Diagnóstico operativo actual
            - Identificación de cuellos de botella
            - Propuestas de optimización específicas
            - Plan de implementación por fases
            - Métricas de seguimiento operativo
            """,
            'analista': """
            Eres un ANALISTA DE DATOS SANITARIOS especializado en estadística avanzada y análisis técnico profundo.

            TU ENFOQUE ESPECÍFICO:
            - Análisis estadístico riguroso de datos sanitarios
            - Identificación de patrones y correlaciones significativas
            - Metodologías avanzadas de análisis de datos
            - Visualizaciones técnicas y modelado predictivo
            - Evaluación de calidad y validez de datos
            - Análisis de tendencias y proyecciones técnicas

            FORMATO DE RESPUESTA REQUERIDO:
            - Metodología de análisis utilizada
            - Hallazgos estadísticos con significancia
            - Análisis de correlaciones y patrones
            - Limitaciones técnicas del análisis
            - Recomendaciones para análisis adicionales
            """,
            'invitado': """
            Eres un CONSULTOR PÚBLICO del Sistema Sanitario de Málaga especializado en información ciudadana.

            TU ENFOQUE ESPECÍFICO:
            - Información general accesible sobre servicios sanitarios
            - Datos públicos relevantes para la ciudadanía
            - Orientación sobre acceso a servicios de salud
            - Estadísticas básicas de salud pública
            - Información educativa sobre prevención
            - Recursos disponibles para la comunidad

            FORMATO DE RESPUESTA REQUERIDO:
            - Información clara y comprensible
            - Datos verificados y públicos únicamente
            - Orientación práctica para ciudadanos
            - Recursos y contactos útiles
            - Limitaciones claras sobre información restringida
            """
        }
        
        base_prompt = role_prompts.get(user_role, role_prompts['invitado'])
        
        return f"""
        {base_prompt}
        
        CONTEXTO DE DATOS DISPONIBLES:
        {context}
        
        INSTRUCCIONES:
        1. Responde ÚNICAMENTE en español
        2. Basa tu respuesta en los datos proporcionados en el contexto
        3. Si tienes datos relevantes en el contexto, úsalos para responder
        4. NO inventes datos específicos que no estén en el contexto
        5. Si no tienes datos suficientes para una consulta específica, sé honesto sobre las limitaciones
        6. Proporciona análisis útiles basados en los datos disponibles
        7. Adapta el nivel técnico al rol del usuario
        8. Si la consulta requiere datos que no están disponibles, sugiere qué información adicional se necesitaría
        """
    
    def _prepare_context_by_role(self, data: dict, user_role: str, user_context: dict = None) -> str:
        """Preparar contexto optimizado según permisos del usuario"""
        context_parts = []
        
        # Datos básicos para todos los roles
        if 'hospitales' in data:
            if hasattr(data['hospitales'], '__len__'):
                context_parts.append(f"Hospitales: {len(data['hospitales'])} centros")
            else:
                context_parts.append("Hospitales: datos disponibles")
        
        if 'demografia' in data:
            try:
                # Manejar tanto DataFrames como diccionarios
                if hasattr(data['demografia'], 'sum'):  # DataFrame de pandas
                    total_pop = data['demografia']['poblacion_2025'].sum()
                elif isinstance(data['demografia'], dict) and 'poblacion_2025' in data['demografia']:
                    # Diccionario con lista
                    total_pop = sum(data['demografia']['poblacion_2025'])
                else:
                    total_pop = 0
                context_parts.append(f"Población total: {total_pop:,} habitantes")
            except Exception as e:
                context_parts.append("Población: datos no disponibles")
        
        # Datos específicos por rol
        if user_role in ['admin', 'gestor']:
            if 'accesibilidad' in data:
                try:
                    if hasattr(data['accesibilidad'], 'mean'):  # DataFrame de pandas
                        avg_time = data['accesibilidad']['tiempo_coche_minutos'].mean()
                    elif isinstance(data['accesibilidad'], dict) and 'tiempo_coche_minutos' in data['accesibilidad']:
                        # Diccionario con lista
                        times = data['accesibilidad']['tiempo_coche_minutos']
                        avg_time = sum(times) / len(times) if times else 0
                    else:
                        avg_time = 0
                    context_parts.append(f"Tiempo medio de acceso: {avg_time:.1f} minutos")
                except Exception as e:
                    context_parts.append("Tiempo de acceso: datos no disponibles")
        
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
            
            # Filtrar contenido para eliminar datos inventados
            filtered_content = self._filter_invented_data(content, data)
            
            # Generar métricas reales basadas en datos disponibles
            metrics = self._generate_real_metrics(data, user_role)
            
            # Generar recomendaciones
            recommendations = self._generate_recommendations(filtered_content, user_role)
            
            # Detectar si necesita visualización
            needs_visualization = self._needs_visualization(filtered_content)
            
            return {
                "main_insight": filtered_content[:200] + "..." if len(filtered_content) > 200 else filtered_content,
                "full_response": filtered_content,
                "analysis_type": analysis_type,
                "metrics": metrics,
                "recommendations": recommendations,
                "needs_visualization": needs_visualization,
                "data_query": self._generate_data_query(filtered_content, data),
                "chart_config": self._generate_chart_config(filtered_content, analysis_type),
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
        
        # Detectar tipos específicos de análisis sanitario - orden de prioridad
        if any(word in content_lower for word in ['usuarios', 'administración', 'configuración', 'supervisión', 'gestión de usuarios', 'roles', 'permisos']):
            return 'user_management'
        elif any(word in content_lower for word in ['planificación estratégica', 'planificación avanzada', 'estrategia', 'objetivos estratégicos', 'metas', 'plan de acción']):
            return 'strategic_planning'
        elif any(word in content_lower for word in ['informe ejecutivo', 'resumen ejecutivo', 'dashboard ejecutivo']):
            return 'executive_summary'
        elif any(word in content_lower for word in ['equidad', 'territorial', 'distrito', 'municipio', 'análisis de equidad', 'desigualdades']):
            return 'equity'
        elif any(word in content_lower for word in ['demografía', 'población', 'habitantes', 'crecimiento', 'análisis demográfico']):
            return 'demographic'
        elif any(word in content_lower for word in ['hospitales', 'centros', 'infraestructura', 'camas', 'análisis de infraestructura']):
            return 'infrastructure'
        elif any(word in content_lower for word in ['servicios', 'cobertura', 'disponibilidad', 'acceso', 'análisis de servicios']):
            return 'services'
        elif any(word in content_lower for word in ['accesibilidad', 'tiempo', 'distancia', 'transporte', 'análisis de accesibilidad']):
            return 'accessibility'
        elif any(word in content_lower for word in ['indicadores', 'métricas', 'ratios', 'kpi', 'análisis de métricas']):
            return 'metrics'
        elif any(word in content_lower for word in ['gráfico', 'chart', 'visualización', 'plot']):
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
        """Extraer métricas del contenido de la respuesta - SOLO datos reales"""
        # NO extraer métricas automáticamente del texto de la IA
        # Esto evita que se generen datos inventados
        return []
    
    def _generate_real_metrics(self, data: dict, user_role: str) -> List[Dict[str, Any]]:
        """Generar métricas reales basadas en los datos disponibles"""
        metrics = []
        
        try:
            # Métricas de hospitales
            if 'hospitales' in data and hasattr(data['hospitales'], '__len__'):
                metrics.append({
                    "name": "Centros Sanitarios",
                    "value": len(data['hospitales']),
                    "unit": "centros"
                })
                
                # Total de camas si está disponible
                if hasattr(data['hospitales'], 'sum'):
                    total_beds = data['hospitales']['camas_funcionamiento_2025'].sum()
                    metrics.append({
                        "name": "Camas Totales",
                        "value": int(total_beds),
                        "unit": "camas"
                    })
            
            # Métricas de población
            if 'demografia' in data:
                if hasattr(data['demografia'], 'sum'):
                    total_pop = data['demografia']['poblacion_2025'].sum()
                    metrics.append({
                        "name": "Población Total",
                        "value": int(total_pop),
                        "unit": "habitantes"
                    })
            
            # Métricas de accesibilidad
            if 'accesibilidad' in data and user_role in ['admin', 'gestor']:
                if hasattr(data['accesibilidad'], 'mean'):
                    avg_time = data['accesibilidad']['tiempo_coche_minutos'].mean()
                    metrics.append({
                        "name": "Tiempo Medio de Acceso",
                        "value": round(avg_time, 1),
                        "unit": "minutos"
                    })
            
        except Exception as e:
            # Si hay error, no agregar métricas
            pass
        
        return metrics[:4]  # Máximo 4 métricas
    
    def _filter_invented_data(self, content: str, data: dict) -> str:
        """Filtrar datos inventados del contenido de la IA - versión suavizada"""
        # Por ahora, no filtrar agresivamente para permitir respuestas útiles
        # Solo filtrar patrones muy específicos de datos claramente inventados
        import re
        
        # Solo filtrar patrones muy específicos de datos inventados comunes
        specific_invented_patterns = [
            r'\d+\.\d+\s*minutos?\s*de\s*acceso',  # Tiempos específicos inventados
            r'\d{1,3}(?:,\d{3})*\s*habitantes?\s*en\s*total',  # Población total inventada
        ]
        
        filtered_content = content
        for pattern in specific_invented_patterns:
            filtered_content = re.sub(pattern, '[Datos no disponibles]', filtered_content, flags=re.IGNORECASE)
        
        return filtered_content
    
    def _get_real_data_summary(self, data: dict) -> str:
        """Obtener resumen de datos reales disponibles"""
        summary_parts = []
        
        try:
            if 'hospitales' in data and hasattr(data['hospitales'], '__len__'):
                summary_parts.append(f"- {len(data['hospitales'])} centros hospitalarios")
            
            if 'demografia' in data and hasattr(data['demografia'], 'sum'):
                total_pop = data['demografia']['poblacion_2025'].sum()
                summary_parts.append(f"- Población total: {total_pop:,} habitantes")
            
            if 'servicios' in data and hasattr(data['servicios'], '__len__'):
                summary_parts.append(f"- {len(data['servicios'])} centros de servicios")
            
            if 'indicadores' in data and hasattr(data['indicadores'], '__len__'):
                summary_parts.append(f"- {len(data['indicadores'])} distritos con indicadores")
                
        except Exception:
            summary_parts.append("- Datos básicos del sistema sanitario")
        
        return "\n".join(summary_parts) if summary_parts else "Datos limitados disponibles"
    
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
        content_lower = content.lower()
        
        # Detectar qué datos específicos necesita la consulta
        if any(word in content_lower for word in ['hospitales', 'centros', 'camas', 'personal']):
            return "data['hospitales']"
        elif any(word in content_lower for word in ['demografía', 'población', 'habitantes', 'municipio']):
            return "data['demografia']"
        elif any(word in content_lower for word in ['servicios', 'cobertura', 'disponibilidad']):
            return "data['servicios']"
        elif any(word in content_lower for word in ['accesibilidad', 'tiempo', 'distancia', 'acceso']):
            return "data['accesibilidad']"
        elif any(word in content_lower for word in ['indicadores', 'métricas', 'ratios', 'equidad']):
            return "data['indicadores']"
        elif any(word in content_lower for word in ['equidad', 'territorial', 'distrito']):
            # Para análisis de equidad, combinar datos relevantes
            return "data"
        else:
            return "data"
    
    def _generate_chart_config(self, content: str, analysis_type: str) -> Dict[str, Any]:
        """Generar configuración de gráfico basada en el contenido"""
        content_lower = content.lower()
        
        # Debug: mostrar contenido y tipo de análisis
        
        # Configuraciones específicas por tipo de análisis
        chart_configs = {
            'user_management': {'type': 'bar', 'title': 'Gestión de Usuarios y Permisos'},
            'strategic_planning': {'type': 'bar', 'title': 'Planificación Estratégica - Objetivos y Metas'},
            'executive_summary': {'type': 'bar', 'title': 'Resumen Ejecutivo del Sistema Sanitario'},
            'equity': {'type': 'bar', 'title': 'Análisis de Equidad Territorial'},
            'demographic': {'type': 'bar', 'title': 'Análisis Demográfico'},
            'infrastructure': {'type': 'bar', 'title': 'Análisis de Infraestructura Sanitaria'},
            'services': {'type': 'bar', 'title': 'Análisis de Servicios'},  # Cambiado de heatmap a bar
            'accessibility': {'type': 'histogram', 'title': 'Análisis de Accesibilidad'},
            'metrics': {'type': 'scatter', 'title': 'Análisis de Métricas'},
            'visualization': {'type': 'bar', 'title': 'Análisis Visual'},
            'statistical': {'type': 'scatter', 'title': 'Análisis Estadístico'},
            'predictive': {'type': 'line', 'title': 'Análisis Predictivo'},
            'recommendation': {'type': 'pie', 'title': 'Recomendaciones'},
            'general': {'type': 'bar', 'title': 'Análisis General'}
        }
        
        # Usar configuración específica del tipo de análisis
        config = chart_configs.get(analysis_type, chart_configs['general'])
        # Solo sobrescribir si hay palabras clave muy específicas y el tipo de análisis no es específico
        if analysis_type in ['general', 'visualization']:
            if any(word in content_lower for word in ['distribución', 'porcentaje', 'proporción', 'parte']):
                config['type'] = 'pie'
                config['title'] = 'Distribución de Datos'
            elif any(word in content_lower for word in ['tendencia', 'evolución', 'tiempo', 'año', 'mes']):
                config['type'] = 'line'
                config['title'] = 'Evolución Temporal'
            elif any(word in content_lower for word in ['correlación', 'relación', 'comparación', 'scatter']):
                config['type'] = 'scatter'
                config['title'] = 'Análisis de Correlación'
        
        # Añadir campos de detección automática
        config['x_axis'] = None
        config['y_axis'] = None
        config['color_by'] = None
        
        return config
    
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
