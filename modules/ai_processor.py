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
    
    def create_system_prompt(self, data: Dict) -> str:
        """Crear prompt especializado en análisis sociosanitario"""
        
        context = self.get_dataset_context(data)
        
        return f"""Eres un analista experto en sistemas sanitarios de Andalucía, especializado en:
        - Equidad territorial y accesibilidad sanitaria
        - Planificación de recursos sanitarios
        - Análisis demográfico y epidemiológico
        - Optimización de la red asistencial

        {context}

        INSTRUCCIONES:
        1. Analiza consultas sobre el sistema sanitario de Málaga
        2. Proporciona análisis cuantitativos basados en los datos
        3. Sugiere visualizaciones apropiadas
        4. Identifica problemas de equidad y propón soluciones
        5. Responde SIEMPRE en formato JSON con esta estructura:

        {{
            "analysis_type": "geographic|demographic|equity|services|planning",
            "main_insight": "Insight principal del análisis",
            "data_query": "Código Python/pandas para extraer datos relevantes",
            "chart_config": {{
                "type": "bar|line|scatter|pie|heatmap|map",
                "title": "Título del gráfico",
                "x_axis": "columna_x",
                "y_axis": "columna_y", 
                "color_by": "columna_color"
            }},
            "metrics": [
                {{"name": "Métrica 1", "value": "valor", "unit": "unidad"}},
                {{"name": "Métrica 2", "value": "valor", "unit": "unidad"}}
            ],
            "recommendations": [
                "Recomendación 1 para gestores sanitarios",
                "Recomendación 2 para planificación"
            ],
            "explanation": "Explicación detallada del análisis en español"
        }}

        EJEMPLOS DE ANÁLISIS:
        - "¿Qué municipios tienen peor acceso?" → analysis_type: "geographic", chart_type: "bar"
        - "Analiza la equidad por distrito" → analysis_type: "equity", chart_type: "heatmap"  
        - "¿Dónde faltan especialistas?" → analysis_type: "services", chart_type: "scatter"
        
        Responde siempre con datos precisos y recomendaciones prácticas.
        """
    
    def process_health_query(self, query: str, data: Dict) -> Dict:
        """Procesar consulta sanitaria con Groq"""
        
        try:
            system_prompt = self.create_system_prompt(data)
            
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
            
            # Fallback si no encuentra JSON válido
            return {
                "analysis_type": "general",
                "main_insight": "Análisis realizado con IA",
                "data_query": "data['hospitales'].head()",
                "chart_config": {
                    "type": "bar",
                    "title": "Análisis General",
                    "x_axis": "nombre",
                    "y_axis": "camas_funcionamiento_2025"
                },
                "metrics": [
                    {"name": "Respuesta", "value": "Procesada", "unit": ""}
                ],
                "recommendations": [
                    "Consulta procesada correctamente"
                ],
                "explanation": content[:500] + "..." if len(content) > 500 else content
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
    
    def process_health_query_async(self, query: str, data: Dict, user_role: str = "invitado") -> Dict:
        """Procesar consulta de salud de forma asíncrona"""
        try:
            # Importar wrapper asíncrono
            from modules.streamlit_async_wrapper import get_streamlit_async_wrapper
            
            # Obtener wrapper asíncrono
            async_wrapper = get_streamlit_async_wrapper()
            
            # Preparar contexto del usuario
            user_context = {
                'role': user_role,
                'timestamp': datetime.now().isoformat()
            }
            
            # Procesar consulta de forma asíncrona
            result = async_wrapper.process_query_sync(query, data, user_role, user_context)
            
            # Añadir información adicional
            result['processed_async'] = True
            result['processing_time'] = datetime.now().isoformat()
            
            return result
            
        except Exception as e:
            # Fallback a procesamiento síncrono si hay error
            st.warning(f"⚠️ Error en procesamiento asíncrono, usando modo síncrono: {str(e)}")
            return self.process_health_query(query, data)
    
    def get_async_processing_metrics(self) -> Dict:
        """Obtener métricas del procesamiento asíncrono"""
        try:
            from modules.streamlit_async_wrapper import get_streamlit_async_wrapper
            async_wrapper = get_streamlit_async_wrapper()
            return async_wrapper.get_processing_metrics()
        except Exception as e:
            return {'error': f'Error obteniendo métricas: {str(e)}'}
    
    def clear_async_cache(self) -> None:
        """Limpiar cache del procesamiento asíncrono"""
        try:
            from modules.streamlit_async_wrapper import get_streamlit_async_wrapper
            async_wrapper = get_streamlit_async_wrapper()
            async_wrapper.clear_ai_cache()
            st.success("✅ Cache de IA limpiado")
        except Exception as e:
            st.error(f"❌ Error limpiando cache: {str(e)}")
    
    def render_async_status(self) -> None:
        """Renderizar estado del procesamiento asíncrono"""
        try:
            from modules.streamlit_async_wrapper import get_streamlit_async_wrapper
            async_wrapper = get_streamlit_async_wrapper()
            async_wrapper.render_processing_status()
        except Exception as e:
            st.error(f"❌ Error mostrando estado: {str(e)}")