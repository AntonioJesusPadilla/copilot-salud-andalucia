import os
import json
import pandas as pd
from groq import Groq
from typing import Dict, List, Optional
import re
import streamlit as st
from datetime import datetime

class HealthAnalyticsAI:
    def __init__(self):
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        self.model = "llama-3.3-70b-versatile"  # Modelo más potente actualizado
        
    def get_dataset_context(self, data: Dict) -> str:
        """Generar contexto detallado de los datasets"""

        context = f"""
        DATASETS SISTEMA SANITARIO MÁLAGA 2025:

        1. HOSPITALES ({len(data['hospitales'])} centros):
           Columnas: {', '.join(data['hospitales'].columns.tolist())}
           Tipos: {', '.join(data['hospitales']['tipo_centro'].unique())}
           Total camas: {data['hospitales']['camas_funcionamiento_2025'].sum()}
           Personal sanitario: {data['hospitales']['personal_sanitario_2025'].sum()}

        2. DEMOGRAFÍA ({len(data['demografia'])} municipios):
           Población total 2025: {data['demografia']['poblacion_2025'].sum():,}
           Crecimiento medio: {data['demografia']['crecimiento_2024_2025'].mean():.0f} habitantes
           Municipio más poblado: {data['demografia'].loc[data['demografia']['poblacion_2025'].idxmax(), 'municipio']}

        3. SERVICIOS SANITARIOS:
           Centros con cardiología: {data['servicios']['cardiologia'].sum()}
           Centros con neurología: {data['servicios']['neurologia'].sum()}
           Centros con UCI: {data['servicios']['uci_adultos'].sum()}
           Total consultas 2024: {data['servicios']['consultas_externas_anuales_2024'].sum():,}

        4. ACCESIBILIDAD:
           Rutas analizadas: {len(data['accesibilidad'])}
           Tiempo medio acceso: {data['accesibilidad']['tiempo_coche_minutos'].mean():.1f} min
           Score accesibilidad medio: {data['accesibilidad']['accesibilidad_score'].mean():.1f}/10

        5. INDICADORES SALUD:
           Distritos sanitarios: {len(data['indicadores'])}
           Ratio médicos promedio: {data['indicadores']['ratio_medico_1000_hab'].mean():.2f}/1000 hab
           Esperanza vida media: {data['indicadores']['esperanza_vida_2023'].mean():.1f} años
        """
        return context

    def analyze_query_intent(self, query: str) -> Dict[str, str]:
        """Analizar la intención de la consulta para generar contexto específico"""
        query_lower = query.lower()

        # Palabras clave para diferentes tipos de análisis
        analysis_patterns = {
            'geographic': ['municipio', 'distrito', 'zona', 'mapa', 'ubicación', 'dónde', 'regional'],
            'financial': ['costo', 'gasto', 'presupuesto', 'roi', 'financiero', 'inversión', 'euro'],
            'capacity': ['camas', 'ocupación', 'capacidad', 'saturación', 'disponibilidad'],
            'personnel': ['personal', 'médico', 'enfermero', 'profesional', 'plantilla', 'recurso humano'],
            'services': ['especialidad', 'servicio', 'cardiología', 'neurología', 'oncología', 'pediatría'],
            'accessibility': ['acceso', 'tiempo', 'distancia', 'transporte', 'llegar', 'ruta'],
            'demographics': ['población', 'habitantes', 'demográfico', 'edad', 'envejecimiento'],
            'quality': ['calidad', 'mortalidad', 'esperanza vida', 'indicador', 'resultado'],
            'comparison': ['comparar', 'mejor', 'peor', 'ranking', 'diferencia', 'versus'],
            'optimization': ['optimizar', 'mejorar', 'eficiencia', 'redistribuir', 'reorganizar'],
            'planning': ['planificar', 'futuro', 'necesidad', 'proyección', 'estrategia'],
            'urgent': ['urgencia', 'emergencia', 'crítico', 'inmediato', 'prioridad']
        }

        # Entidades específicas que se mencionan
        entities = {
            'hospitals': ['hospital', 'centro', 'clínico', 'regional', 'costa del sol', 'axarquía'],
            'municipalities': ['málaga', 'marbella', 'vélez', 'antequera', 'ronda', 'estepona'],
            'specialties': ['cardiología', 'neurología', 'oncología', 'pediatría', 'ginecología'],
            'districts': ['málaga', 'costa del sol', 'axarquía', 'norte', 'serranía', 'guadalhorce']
        }

        # Detectar tipo de análisis principal
        main_analysis = 'general'
        for analysis_type, keywords in analysis_patterns.items():
            if any(keyword in query_lower for keyword in keywords):
                main_analysis = analysis_type
                break

        # Detectar entidades mencionadas
        mentioned_entities = []
        for entity_type, entity_list in entities.items():
            for entity in entity_list:
                if entity in query_lower:
                    mentioned_entities.append(f"{entity_type}:{entity}")

        return {
            'main_analysis': main_analysis,
            'entities': ', '.join(mentioned_entities) if mentioned_entities else 'general',
            'complexity': 'high' if len(mentioned_entities) > 2 else 'medium' if mentioned_entities else 'low'
        }

    def get_specific_data_context(self, data: Dict, query: str, intent: Dict) -> str:
        """Generar contexto específico basado en la consulta e intención"""

        analysis_type = intent['main_analysis']
        specific_context = ""

        try:
            if analysis_type == 'geographic':
                # Datos específicos de ubicaciones
                municipios_data = data['hospitales'].groupby('municipio').agg({
                    'camas_funcionamiento_2025': 'sum',
                    'personal_sanitario_2025': 'sum'
                }).to_string()
                specific_context = f"DATOS GEOGRÁFICOS:\n{municipios_data}\n"

            elif analysis_type == 'financial':
                # Datos específicos financieros
                gasto_per_capita = data['indicadores'][['distrito_sanitario', 'gasto_sanitario_per_capita']].to_string(index=False)
                specific_context = f"DATOS FINANCIEROS:\n{gasto_per_capita}\n"

            elif analysis_type == 'capacity':
                # Datos específicos de capacidad
                capacity_data = data['hospitales'][['nombre', 'camas_funcionamiento_2025', 'uci_camas']].to_string(index=False)
                specific_context = f"DATOS CAPACIDAD:\n{capacity_data}\n"

            elif analysis_type == 'personnel':
                # Datos específicos de personal
                personal_data = data['hospitales'][['nombre', 'personal_sanitario_2025']].merge(
                    data['servicios'][['centro_sanitario', 'profesionales_medicos_2025', 'profesionales_enfermeria_2025']],
                    left_on='nombre', right_on='centro_sanitario', how='left'
                ).to_string(index=False)
                specific_context = f"DATOS PERSONAL:\n{personal_data}\n"

            elif analysis_type == 'services':
                # Datos específicos de servicios
                services_data = data['servicios'][['centro_sanitario', 'cardiologia', 'neurologia', 'oncologia_medica', 'pediatria']].to_string(index=False)
                specific_context = f"DATOS SERVICIOS:\n{services_data}\n"

            elif analysis_type == 'accessibility':
                # Datos específicos de accesibilidad
                access_data = data['accesibilidad'][['municipio_origen', 'hospital_destino', 'tiempo_coche_minutos', 'accesibilidad_score']].to_string(index=False)
                specific_context = f"DATOS ACCESIBILIDAD:\n{access_data}\n"

            elif analysis_type == 'demographics':
                # Datos específicos demográficos
                demo_data = data['demografia'][['municipio', 'poblacion_2025', 'crecimiento_2024_2025', 'indice_envejecimiento_2025']].to_string(index=False)
                specific_context = f"DATOS DEMOGRÁFICOS:\n{demo_data}\n"

            elif analysis_type == 'quality':
                # Datos específicos de calidad
                quality_data = data['indicadores'][['distrito_sanitario', 'esperanza_vida_2023', 'mortalidad_infantil_x1000', 'cobertura_vacunal_infantil_pct']].to_string(index=False)
                specific_context = f"DATOS CALIDAD:\n{quality_data}\n"

        except Exception as e:
            specific_context = f"Error extrayendo datos específicos: {str(e)}\n"

        return specific_context
    
    def create_system_prompt(self, data: Dict, user_role: str = "analista", query: str = "") -> str:
        """Crear prompt especializado según rol de usuario y consulta específica"""

        # Análisis de contexto general
        context = self.get_dataset_context(data)

        # Análisis específico de la consulta
        specific_context = ""
        if query:
            intent = self.analyze_query_intent(query)
            specific_context = self.get_specific_data_context(data, query, intent)
            context += f"\nANÁLISIS ESPECÍFICO PARA: '{query}'\nTipo: {intent['main_analysis']}\nEntidades: {intent['entities']}\n{specific_context}"

        # Prompts específicos por rol
        role_prompts = {
            "admin": """Eres un CONSULTOR ESTRATÉGICO para la Consejería de Salud de Andalucía.

            ENFOQUE ADMINISTRATIVO:
            - Análisis de ROI y sostenibilidad financiera
            - Planificación estratégica a largo plazo
            - Comparativa de rendimiento entre distritos
            - Optimización de inversiones sanitarias
            - Informes ejecutivos para toma de decisiones

            CAPACIDADES ESPECIALES:
            - Acceso completo a todos los datos
            - Análisis de eficiencia de gasto sanitario
            - Recomendaciones de política pública
            - Evaluación de necesidades de inversión""",

            "gestor": """Eres un ANALISTA OPERACIONAL especializado en gestión hospitalaria.

            ENFOQUE GESTIÓN:
            - Optimización de recursos y ocupación de camas
            - Gestión de flujos de pacientes y listas de espera
            - Redistribución de personal sanitario
            - Planificación de turnos y servicios
            - Coordinación entre centros sanitarios

            CAPACIDADES ESPECIALES:
            - Análisis de eficiencia operativa
            - Detección de cuellos de botella
            - Optimización de rutas y traslados
            - Planificación de capacidad asistencial""",

            "analista": """Eres un CIENTÍFICO DE DATOS especializado en epidemiología y salud pública.

            ENFOQUE ANALÍTICO:
            - Estudios estadísticos y correlaciones
            - Modelos predictivos y machine learning
            - Análisis de inequidades territoriales
            - Visualizaciones avanzadas y mapas
            - Análisis de supervivencia y tendencias

            CAPACIDADES ESPECIALES:
            - Análisis multivariante y regresiones
            - Clustering y segmentación poblacional
            - Tests de significancia estadística
            - Modelos de predicción demográfica""",

            "invitado": """Eres un ASISTENTE DE INFORMACIÓN SANITARIA para ciudadanos.

            ENFOQUE CIUDADANO:
            - Información clara y accesible
            - Orientación sobre servicios disponibles
            - Datos básicos de centros sanitarios
            - Indicaciones de acceso y ubicación
            - Consejos generales de salud

            CAPACIDADES LIMITADAS:
            - Solo información pública general
            - Sin datos estratégicos o sensibles
            - Respuestas simples y orientativas"""
        }

        role_prompt = role_prompts.get(user_role, role_prompts["analista"])

        return f"""{role_prompt}

        {context}

        INSTRUCCIONES ESPECÍFICAS:
        1. ANALIZA LA CONSULTA ESPECÍFICA - No uses respuestas genéricas
        2. USA LOS DATOS ESPECÍFICOS proporcionados arriba para esa consulta
        3. Adapta el análisis al nivel de acceso del usuario ({user_role})
        4. Proporciona recomendaciones ESPECÍFICAS para la consulta realizada
        5. Cada respuesta debe ser ÚNICA y ESPECÍFICA para la pregunta
        6. Usa los datos reales proporcionados, no generes datos falsos
        7. Si mencionan un municipio/hospital específico, enfócate en ESE específicamente
        8. Responde SIEMPRE en formato JSON con esta estructura:

        {{
            "analysis_type": "strategic|operational|statistical|informational|geographic|demographic|equity|services|planning|capacity|financial|personnel|quality|urgent|comparison|optimization",
            "main_insight": "Insight ESPECÍFICO basado en los datos proporcionados para esta consulta exacta",
            "data_query": "Código Python/pandas ESPECÍFICO para extraer EXACTAMENTE los datos relevantes a la consulta",
            "chart_config": {{
                "type": "bar|line|scatter|pie|heatmap|map|gauge|funnel|box|violin|radar|treemap|sankey",
                "title": "Título ESPECÍFICO relacionado con la consulta",
                "x_axis": "columna_x específica",
                "y_axis": "columna_y específica",
                "color_by": "columna_color específica",
                "filter_criteria": "criterio específico si aplica"
            }},
            "metrics": [
                {{"name": "Métrica ESPECÍFICA 1", "value": "valor REAL", "unit": "unidad"}},
                {{"name": "Métrica ESPECÍFICA 2", "value": "valor REAL", "unit": "unidad"}},
                {{"name": "Métrica ESPECÍFICA 3", "value": "valor REAL", "unit": "unidad"}}
            ],
            "recommendations": [
                "Recomendación ESPECÍFICA basada en los datos analizados",
                "Acción práctica ESPECÍFICA para esta situación",
                "Siguiente paso CONCRETO y measurable"
            ],
            "detailed_findings": [
                "Hallazgo específico 1 con datos",
                "Hallazgo específico 2 con datos",
                "Hallazgo específico 3 con datos"
            ],
            "explanation": "Explicación DETALLADA Y ESPECÍFICA usando los datos reales proporcionados, mencionando valores exactos y conclusiones basadas en evidencia"
        }}

        EJEMPLOS DE RESPUESTAS ESPECÍFICAS:

        PREGUNTA: "¿Cuántas camas tiene el Hospital Regional?"
        → Buscar ESPECÍFICAMENTE datos del Hospital Regional, dar número exacto de camas

        PREGUNTA: "¿Qué municipio tiene peor acceso a cardiología?"
        → Analizar datos de accesibilidad + servicios cardiología, identificar municipio específico

        PREGUNTA: "Compara Málaga y Marbella en demografía"
        → Comparar ESPECÍFICAMENTE estos 2 municipios con datos demográficos reales

        PREGUNTA: "¿Dónde faltan más médicos?"
        → Calcular ratio médico/habitante por distrito, identificar déficits específicos

        IMPORTANTE: NUNCA repitas la misma respuesta. Cada consulta debe generar análisis únicos basados en los datos específicos proporcionados.
        """
    
    def process_health_query(self, query: str, data: Dict, user_role: str = "analista") -> Dict:
        """Procesar consulta sanitaria con Groq adaptada al rol"""

        try:
            system_prompt = self.create_system_prompt(data, user_role, query)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"CONSULTA: {query}"}
                ],
                temperature=0.2,
                max_tokens=2000
            )
            
            content = response.choices[0].message.content
            
            # Extraer JSON de la respuesta
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                try:
                    result = json.loads(json_match.group())
                    return result
                except json.JSONDecodeError:
                    pass
            
            # Fallback con análisis de la consulta
            intent = self.analyze_query_intent(query)

            return {
                "analysis_type": intent['main_analysis'],
                "main_insight": f"Análisis de {intent['main_analysis']} realizado para: {query}",
                "data_query": f"# Consulta específica: {query}\ndata['{intent['main_analysis']}'].head()",
                "chart_config": {
                    "type": "bar",
                    "title": f"Análisis: {query}",
                    "x_axis": "nombre",
                    "y_axis": "valor"
                },
                "metrics": [
                    {"name": "Tipo de consulta", "value": intent['main_analysis'], "unit": ""},
                    {"name": "Entidades detectadas", "value": intent['entities'], "unit": ""}
                ],
                "recommendations": [
                    f"Análisis específico para: {query}",
                    "Recomendación basada en el tipo de consulta detectado"
                ],
                "detailed_findings": [
                    f"Consulta categorizada como: {intent['main_analysis']}",
                    f"Entidades detectadas: {intent['entities']}",
                    "Análisis procesado con contexto específico"
                ],
                "explanation": f"Análisis específico para la consulta '{query}' categorizada como {intent['main_analysis']}. " + (content[:400] + "..." if len(content) > 400 else content)
            }
            
        except Exception as e:
            return {
                "analysis_type": "error",
                "main_insight": f"Error en el análisis: {str(e)}",
                "data_query": "data['hospitales'].head()",
                "chart_config": {"type": "bar", "title": "Error", "x_axis": "nombre", "y_axis": "camas_funcionamiento_2025"},
                "metrics": [{"name": "Estado", "value": "Error", "unit": ""}],
                "recommendations": ["Revisar configuración de API"],
                "explanation": f"Se produjo un error: {str(e)}"
            }
    
    def execute_data_query(self, query: str, data: Dict) -> pd.DataFrame:
        """Ejecutar consulta de datos de forma segura"""
        
        try:
            # Contexto seguro para eval
            safe_context = {
                'data': data,
                'pd': pd,
                'len': len,
                'sum': sum,
                'mean': lambda x: x.mean() if hasattr(x, 'mean') else 0,
                'max': max,
                'min': min
            }
            
            # Ejecutar consulta
            result = eval(query, {"__builtins__": {}}, safe_context)
            
            # Convertir a DataFrame si no lo es
            if isinstance(result, pd.Series):
                return result.reset_index()
            elif isinstance(result, pd.DataFrame):
                return result
            else:
                # Crear DataFrame simple
                return pd.DataFrame({'resultado': [result]})
                
        except Exception as e:
            # DataFrame de error
            return pd.DataFrame({
                'error': [f'Error ejecutando consulta: {str(e)}'],
                'query': [query]
            })
    
    def process_health_query_async(self, query: str, data: Dict, user_role: str = "invitado") -> Dict:
        """Procesar consulta de salud de forma asíncrona (simulado)"""
        try:
            # Por ahora, usar procesamiento síncrono normal
            # TODO: Implementar procesamiento asíncrono real cuando sea necesario
            result = self.process_health_query(query, data)
            
            # Añadir información de procesamiento asíncrono simulado
            result['processed_async'] = True
            result['processing_time'] = datetime.now().isoformat()
            result['async_simulation'] = True
            
            return result
            
        except Exception as e:
            # Fallback a procesamiento síncrono si hay error
            st.warning(f"⚠️ Error en procesamiento asíncrono, usando modo síncrono: {str(e)}")
            return self.process_health_query(query, data)
    
    def get_async_processing_metrics(self) -> Dict:
        """Obtener métricas del procesamiento asíncrono"""
        try:
            # Métricas simuladas para procesamiento asíncrono
            return {
                'total_requests': 0,
                'successful_requests': 0,
                'failed_requests': 0,
                'cache_hits': 0,
                'average_response_time': 0.0,
                'active_tasks': 0,
                'last_update': datetime.now().isoformat(),
                'async_simulation': True
            }
        except Exception as e:
            return {'error': f'Error obteniendo métricas: {str(e)}'}
    
    def clear_async_cache(self) -> None:
        """Limpiar cache del procesamiento asíncrono"""
        try:
            # Limpiar cache simulado
            st.success("✅ Cache de IA limpiado (simulado)")
        except Exception as e:
            st.error(f"❌ Error limpiando cache: {str(e)}")
    
    def render_async_status(self) -> None:
        """Renderizar estado del procesamiento asíncrono"""
        try:
            # Estado simulado del procesamiento asíncrono
            st.info("🔄 Procesamiento asíncrono simulado activo")
        except Exception as e:
            st.error(f"❌ Error mostrando estado: {str(e)}")


class HealthMetricsCalculator:
    """Calculadora de métricas sanitarias especializadas"""
    
    @staticmethod
    def calculate_equity_index(data: Dict) -> pd.DataFrame:
        """Calcular índice de equidad sanitaria"""
        
        try:
            # Combinar datos de hospitales e indicadores
            hospitales = data['hospitales']
            indicadores = data['indicadores']
            
            # Calcular métricas por distrito
            equity_data = []
            
            for distrito in hospitales['distrito_sanitario'].unique():
                distrito_hospitals = hospitales[hospitales['distrito_sanitario'] == distrito]
                distrito_indicators = indicadores[indicadores['distrito_sanitario'] == distrito]
                
                if len(distrito_indicators) > 0:
                    equity_data.append({
                        'distrito': distrito,
                        'poblacion': distrito_indicators['poblacion_total_2025'].iloc[0],
                        'camas_totales': distrito_hospitals['camas_funcionamiento_2025'].sum(),
                        'personal_total': distrito_hospitals['personal_sanitario_2025'].sum(),
                        'ratio_camas_1000hab': (distrito_hospitals['camas_funcionamiento_2025'].sum() / distrito_indicators['poblacion_total_2025'].iloc[0]) * 1000,
                        'ratio_personal_1000hab': (distrito_hospitals['personal_sanitario_2025'].sum() / distrito_indicators['poblacion_total_2025'].iloc[0]) * 1000,
                        'centros_con_uci': distrito_hospitals['uci_camas'].sum(),
                        'score_equidad': 0  # Calcularemos después
                    })
            
            df = pd.DataFrame(equity_data)
            
            # Calcular score de equidad (normalizado 0-100)
            if len(df) > 0:
                # Normalizar ratios (mayor es mejor hasta cierto punto)
                df['score_camas'] = (df['ratio_camas_1000hab'] / df['ratio_camas_1000hab'].max()) * 40
                df['score_personal'] = (df['ratio_personal_1000hab'] / df['ratio_personal_1000hab'].max()) * 40
                df['score_uci'] = (df['centros_con_uci'] > 0).astype(int) * 20
                
                df['score_equidad'] = df['score_camas'] + df['score_personal'] + df['score_uci']
            
            return df
            
        except Exception as e:
            return pd.DataFrame({'error': [f'Error calculando equidad: {str(e)}']})
    
    @staticmethod
    def analyze_accessibility_gaps(data: Dict) -> pd.DataFrame:
        """Analizar brechas de accesibilidad"""
        
        try:
            accesibilidad = data['accesibilidad']
            
            # Agrupar por municipio origen
            gaps_analysis = accesibilidad.groupby('municipio_origen', observed=True).agg({
                'tiempo_coche_minutos': ['mean', 'min'],
                'accesibilidad_score': 'mean',
                'coste_transporte_euros': 'mean'
            }).round(2)
            
            # Aplanar columnas multi-nivel
            gaps_analysis.columns = ['tiempo_medio', 'tiempo_minimo', 'score_accesibilidad', 'coste_medio']
            gaps_analysis = gaps_analysis.reset_index()
            
            # Clasificar nivel de accesibilidad
            def classify_accessibility(score):
                if score >= 8: return 'Excelente'
                elif score >= 6: return 'Buena'
                elif score >= 4: return 'Regular'
                else: return 'Deficiente'
            
            gaps_analysis['nivel_accesibilidad'] = gaps_analysis['score_accesibilidad'].apply(classify_accessibility)
            
            # Identificar municipios con problemas
            gaps_analysis['requiere_atencion'] = (
                (gaps_analysis['tiempo_medio'] > 60) | 
                (gaps_analysis['score_accesibilidad'] < 5)
            )
            
            return gaps_analysis.sort_values('score_accesibilidad', ascending=True)
            
        except Exception as e:
            return pd.DataFrame({'error': [f'Error analizando accesibilidad: {str(e)}']})
    
    @staticmethod
    def identify_service_gaps(data: Dict) -> Dict:
        """Identificar brechas en servicios sanitarios"""
        
        try:
            servicios = data['servicios']
            hospitales = data['hospitales']
            
            # Servicios críticos a analizar
            critical_services = [
                'cardiologia', 'neurologia', 'oncologia_medica', 
                'uci_adultos', 'hemodialisis', 'urgencias_generales'
            ]
            
            gaps = {}
            
            for service in critical_services:
                if service in servicios.columns:
                    # Centros que SÍ tienen el servicio
                    with_service = servicios[servicios[service] == True]['centro_sanitario'].tolist()
                    
                    # Centros que NO tienen el servicio  
                    without_service = servicios[servicios[service] == False]['centro_sanitario'].tolist()
                    
                    # Población afectada (aproximada)
                    centers_without = hospitales[hospitales['nombre'].isin([s.replace('Hospital ', '').replace('CAR ', '') for s in without_service])]
                    affected_population = centers_without['poblacion_referencia_2025'].sum()
                    
                    gaps[service] = {
                        'centros_con_servicio': len(with_service),
                        'centros_sin_servicio': len(without_service),
                        'cobertura_porcentaje': (len(with_service) / len(servicios)) * 100,
                        'poblacion_sin_acceso': affected_population,
                        'prioridad': 'Alta' if len(without_service) > len(servicios) * 0.6 else 'Media' if len(without_service) > 0 else 'Baja'
                    }
            
            return gaps
            
        except Exception as e:
            return {'error': f'Error identificando brechas: {str(e)}'}