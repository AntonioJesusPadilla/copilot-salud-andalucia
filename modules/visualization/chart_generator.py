import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from typing import Dict, Optional
import traceback
import json

class SmartChartGenerator:
    def __init__(self):
        self.debug_mode = False  # Debug desactivado ahora que encontramos el problema
        self.debug_log = []

        # Paleta de colores sanitarios
        self.health_colors = {
            'primary': '#00a86b',      # Verde sanitario
            'secondary': '#4CAF50',     # Verde claro
            'accent': '#ff6b6b',        # Rojo para alertas
            'warning': '#ffa726',       # Naranja para advertencias
            'info': '#42a5f5',          # Azul para información
            'success': '#66bb6a'        # Verde para éxito
        }
        
        self.color_scales = {
            'equity': 'RdYlGn',
            'accessibility': 'RdYlBu_r',
            'population': 'Viridis',
            'services': 'Set3',
            'health_metrics': 'Spectral'
        }

    def debug_log_add(self, message: str, data=None):
        """Agregar entrada al log de debug"""
        if self.debug_mode:
            entry = {
                'message': message,
                'data': str(data)[:200] if data else None
            }
            self.debug_log.append(entry)
            print(f"🔍 DEBUG: {message}")

    def debug_figure_inspection(self, fig: go.Figure, stage: str):
        """Inspeccionar figura en profundidad"""
        if not self.debug_mode:
            return

        try:
            self.debug_log_add(f"=== INSPECCIÓN FIGURA EN {stage.upper()} ===")

            # Verificar layout
            if hasattr(fig, 'layout'):
                layout_dict = dict(fig.layout)
                self.debug_log_add(f"Layout keys: {list(layout_dict.keys())}")

                # Inspeccionar xaxis específicamente
                for key in layout_dict.keys():
                    if 'xaxis' in key:
                        xaxis_data = layout_dict[key]
                        self.debug_log_add(f"{key} contenido: {type(xaxis_data)}")

                        if isinstance(xaxis_data, dict):
                            if 'rangeslider' in xaxis_data:
                                rangeslider_data = xaxis_data['rangeslider']
                                self.debug_log_add(f"🚨 ENCONTRADO RANGESLIDER en {key}: {type(rangeslider_data)}")
                                self.debug_log_add(f"Rangeslider content: {rangeslider_data}")

                                # Verificar si tiene yaxis problemático
                                if isinstance(rangeslider_data, dict) and 'yaxis' in rangeslider_data:
                                    yaxis_data = rangeslider_data['yaxis']
                                    self.debug_log_add(f"🔴 YAXIS EN RANGESLIDER: {type(yaxis_data)} = {yaxis_data}")

            # Verificar data traces
            if hasattr(fig, 'data'):
                self.debug_log_add(f"Número de traces: {len(fig.data)}")
                for i, trace in enumerate(fig.data):
                    self.debug_log_add(f"Trace {i}: {type(trace).__name__}")

        except Exception as e:
            self.debug_log_add(f"❌ Error en inspección: {str(e)}")

    def print_debug_report(self):
        """Imprimir reporte completo de debug"""
        if self.debug_mode and self.debug_log:
            print("\n" + "="*60)
            print("📋 REPORTE DEBUG COMPLETO")
            print("="*60)
            for i, entry in enumerate(self.debug_log):
                print(f"{i+1:2d}. {entry['message']}")
                if entry['data']:
                    print(f"    Data: {entry['data']}")
            print("="*60 + "\n")
    
    def generate_chart(self, chart_config: Dict, data: pd.DataFrame, theme_mode: str = 'light') -> go.Figure:
        """Generar gráfico basado en configuración de IA"""

        # RESET del log de debug
        self.debug_log = []
        self.debug_log_add("🚀 INICIANDO GENERACIÓN DE GRÁFICO")

        # Validaciones básicas
        if data is None or data.empty:
            self.debug_log_add("❌ Datos vacíos o None")
            return self._create_error_chart("Datos vacíos o None")

        if not isinstance(chart_config, dict):
            self.debug_log_add("❌ Configuración de gráfico inválida")
            return self._create_error_chart("Configuración de gráfico inválida")

        chart_type = chart_config.get('type', 'bar')
        title = chart_config.get('title', 'Análisis Sanitario')

        self.debug_log_add(f"📊 Tipo de gráfico: {chart_type}")
        self.debug_log_add(f"📝 Título: {title}")
        self.debug_log_add(f"📋 Datos shape: {data.shape}")

        try:
            self.debug_log_add(f"🎯 Creando gráfico tipo: {chart_type}")

            if chart_type == 'bar':
                result = self._create_bar_chart(chart_config, data, theme_mode)
            elif chart_type == 'line':
                result = self._create_line_chart(chart_config, data, theme_mode)
            elif chart_type == 'scatter':
                result = self._create_scatter_chart(chart_config, data, theme_mode)
            elif chart_type == 'pie':
                result = self._create_pie_chart(chart_config, data, theme_mode)
            elif chart_type == 'heatmap':
                result = self._create_heatmap(chart_config, data, theme_mode)
            elif chart_type == 'map':
                result = self._create_geographic_chart(chart_config, data, theme_mode)
            elif chart_type == 'histogram':
                result = self._create_histogram_chart(chart_config, data, theme_mode)
            else:
                result = self._create_fallback_chart(title, data, theme_mode)

            self.debug_log_add(f"✅ Gráfico creado exitosamente")

            # INSPECCIÓN POST-CREACIÓN
            self.debug_figure_inspection(result, "POST-CREACIÓN")

            # Verificar que el resultado no sea None
            if result is None:
                self.debug_log_add(f"❌ Método {chart_type} devolvió None")
                return self._create_error_chart(f"Método {chart_type} devolvió None")

            # PROTECCIÓN FINAL EXTREMA: Asegurar que no hay rangeslider problemático para Streamlit
            self.debug_log_add("🛡️ Aplicando protección final extrema anti-rangeslider para Streamlit")
            try:
                # Múltiples métodos de protección
                result.update_layout(
                    xaxis=dict(
                        rangeslider=dict(visible=False)
                    )
                )

                # Protección adicional para subplots
                for i in range(10):
                    if i == 0:
                        continue
                    try:
                        result.update_layout(**{f'xaxis{i+1}': dict(rangeslider=dict(visible=False))})
                    except:
                        pass

                self.debug_log_add("✅ Protección extrema aplicada correctamente")
            except Exception as e:
                self.debug_log_add(f"⚠️ Warning: No se pudo aplicar protección extrema: {e}")

            # INSPECCIÓN FINAL
            self.debug_figure_inspection(result, "FINAL")

            # IMPRIMIR REPORTE COMPLETO
            self.print_debug_report()

            return result

        except Exception as e:
            import traceback
            error_details = traceback.format_exc()

            # LOG DE ERROR COMPLETO
            self.debug_log_add(f"💥 ERROR CRÍTICO: {str(e)}")
            self.debug_log_add(f"📋 Traceback: {error_details}")

            # Verificar si es específicamente el error de rangeslider
            if 'rangeslider' in str(e).lower() or 'Rangeslider' in str(e):
                self.debug_log_add("🎯 ERROR CONFIRMADO: Es el problema de Rangeslider")

            self.print_debug_report()

            return self._create_error_chart(f"Error generando gráfico tipo {chart_type}: {str(e)}\n{error_details[:200]}...")
    
    def _create_bar_chart(self, config: Dict, data: pd.DataFrame, theme_mode: str = 'light') -> go.Figure:
        """Crear gráfico de barras inteligente"""
        
        x_col = config.get('x_axis', data.columns[0])
        y_col = config.get('y_axis', data.columns[1] if len(data.columns) > 1 else data.columns[0])
        color_col = config.get('color_by', None)
        
        
        # Determinar orientación automática
        if len(data) > 10 or max(len(str(x)) for x in data[x_col]) > 15:
            # Horizontal si muchos elementos o nombres largos
            fig = px.bar(
                data, 
                x=y_col, 
                y=x_col, 
                orientation='h',
                color=color_col,
                color_continuous_scale=self.color_scales.get('equity', 'Viridis'),
                title=config.get('title', 'Análisis de Barras')
            )
        else:
            fig = px.bar(
                data,
                x=x_col,
                y=y_col,
                color=color_col,
                color_continuous_scale=self.color_scales.get('equity', 'Viridis'),
                title=config.get('title', 'Análisis de Barras')
            )
            fig.update_xaxes(tickangle=45)
        
        # PROTECCIÓN EXTREMA: Eliminar rangeslider antes de aplicar tema
        self.debug_log_add("🛡️ Aplicando protección extrema anti-rangeslider en método individual")
        try:
            fig.update_layout(
                xaxis=dict(rangeslider=dict(visible=False))
            )
            self.debug_log_add("✅ Protección extrema aplicada en método individual")
        except Exception as e:
            self.debug_log_add(f"⚠️ Error en protección individual: {e}")

        # INSPECCIÓN ANTES DEL TEMA
        self.debug_figure_inspection(fig, "ANTES-DEL-TEMA")

        result = self._apply_health_theme(fig, theme_mode)

        # INSPECCIÓN DESPUÉS DEL TEMA
        self.debug_figure_inspection(result, "DESPUÉS-DEL-TEMA")

        return result
    
    def _create_scatter_chart(self, config: Dict, data: pd.DataFrame, theme_mode: str = 'light') -> go.Figure:
        """Crear gráfico de dispersión con insights"""
        
        x_col = config.get('x_axis', data.columns[0])
        y_col = config.get('y_axis', data.columns[1] if len(data.columns) > 1 else data.columns[0])
        size_col = config.get('size_by', None)
        color_col = config.get('color_by', None)
        
        # Detectar si es análisis de correlación
        if size_col and size_col in data.columns:
            fig = px.scatter(
                data,
                x=x_col,
                y=y_col,
                size=size_col,
                color=color_col,
                hover_data=data.columns.tolist()[:5],  # Primeras 5 columnas
                title=config.get('title', 'Análisis de Correlación'),
                color_continuous_scale='Viridis'
            )
        else:
            fig = px.scatter(
                data,
                x=x_col,
                y=y_col,
                color=color_col,
                hover_data=data.columns.tolist()[:3],
                title=config.get('title', 'Análisis de Dispersión'),
                color_continuous_scale='Plasma'
            )
        
        # PROTECCIÓN EXTREMA: Eliminar rangeslider antes de aplicar tema
        self.debug_log_add("🛡️ Aplicando protección extrema anti-rangeslider en método individual")
        try:
            fig.update_layout(
                xaxis=dict(rangeslider=dict(visible=False))
            )
            self.debug_log_add("✅ Protección extrema aplicada en método individual")
        except Exception as e:
            self.debug_log_add(f"⚠️ Error en protección individual: {e}")

        # INSPECCIÓN ANTES DEL TEMA
        self.debug_figure_inspection(fig, "ANTES-DEL-TEMA")

        result = self._apply_health_theme(fig, theme_mode)

        # INSPECCIÓN DESPUÉS DEL TEMA
        self.debug_figure_inspection(result, "DESPUÉS-DEL-TEMA")

        return result
    
    def _create_pie_chart(self, config: Dict, data: pd.DataFrame, theme_mode: str = 'light') -> go.Figure:
        """Crear gráfico circular con etiquetas inteligentes"""
        
        # Detectar columna de categorías y valores
        category_col = None
        value_col = None
        
        for col in data.columns:
            if data[col].dtype == 'object' or data[col].dtype == 'category':
                category_col = col
            elif pd.api.types.is_numeric_dtype(data[col]):
                value_col = col
        
        if category_col and value_col:
            fig = px.pie(
                data,
                names=category_col,
                values=value_col,
                title=config.get('title', 'Distribución'),
                color_discrete_sequence=px.colors.qualitative.Set3
            )
        else:
            # Si es una serie, usar índice y valores
            if isinstance(data, pd.Series):
                fig = px.pie(
                    names=data.index,
                    values=data.values,
                    title=config.get('title', 'Distribución')
                )
            else:
                # Fallback: primera columna como categorías, segunda como valores
                fig = px.pie(
                    data,
                    names=data.columns[0],
                    values=data.columns[1] if len(data.columns) > 1 else data.columns[0],
                    title=config.get('title', 'Distribución')
                )
        
        fig.update_traces(
            textposition='inside',
            textinfo='percent+label',
            hoverinfo='none'  # Deshabilitar hover completamente
        )
        
        # PROTECCIÓN EXTREMA: Eliminar rangeslider antes de aplicar tema
        self.debug_log_add("🛡️ Aplicando protección extrema anti-rangeslider en método individual")
        try:
            fig.update_layout(
                xaxis=dict(rangeslider=dict(visible=False))
            )
            self.debug_log_add("✅ Protección extrema aplicada en método individual")
        except Exception as e:
            self.debug_log_add(f"⚠️ Error en protección individual: {e}")

        # INSPECCIÓN ANTES DEL TEMA
        self.debug_figure_inspection(fig, "ANTES-DEL-TEMA")

        result = self._apply_health_theme(fig, theme_mode)

        # INSPECCIÓN DESPUÉS DEL TEMA
        self.debug_figure_inspection(result, "DESPUÉS-DEL-TEMA")

        return result
    
    def _create_heatmap(self, config: Dict, data: pd.DataFrame, theme_mode: str = 'light') -> go.Figure:
        """Crear mapa de calor para análisis de correlación o matriz"""
        
        # Si los datos son numéricos, crear matriz de correlación
        numeric_data = data.select_dtypes(include=['number'])
        
        if len(numeric_data.columns) > 2:
            correlation_matrix = numeric_data.corr()
            
            fig = px.imshow(
                correlation_matrix,
                text_auto=True,
                aspect="auto",
                color_continuous_scale='RdBu_r',
                title=config.get('title', 'Matriz de Correlación')
            )
        else:
            # Crear heatmap directo de los datos
            fig = px.imshow(
                data.values,
                x=data.columns,
                y=data.index,
                color_continuous_scale='Viridis',
                title=config.get('title', 'Mapa de Calor'),
                text_auto=True
            )
        
        # PROTECCIÓN EXTREMA: Eliminar rangeslider antes de aplicar tema
        self.debug_log_add("🛡️ Aplicando protección extrema anti-rangeslider en método individual")
        try:
            fig.update_layout(
                xaxis=dict(rangeslider=dict(visible=False))
            )
            self.debug_log_add("✅ Protección extrema aplicada en método individual")
        except Exception as e:
            self.debug_log_add(f"⚠️ Error en protección individual: {e}")

        # INSPECCIÓN ANTES DEL TEMA
        self.debug_figure_inspection(fig, "ANTES-DEL-TEMA")

        result = self._apply_health_theme(fig, theme_mode)

        # INSPECCIÓN DESPUÉS DEL TEMA
        self.debug_figure_inspection(result, "DESPUÉS-DEL-TEMA")

        return result
    
    def _create_geographic_chart(self, config: Dict, data: pd.DataFrame, theme_mode: str = 'light') -> go.Figure:
        """Crear visualización geográfica (scatter_mapbox básico)"""
        
        # Buscar columnas de coordenadas
        lat_col = None
        lon_col = None
        
        for col in data.columns:
            col_lower = col.lower()
            if 'lat' in col_lower or 'latitud' in col_lower:
                lat_col = col
            elif 'lon' in col_lower or 'lng' in col_lower or 'longitud' in col_lower:
                lon_col = col
        
        if lat_col and lon_col:
            # Detectar columna de tamaño/color
            size_col = None
            color_col = None
            
            for col in data.columns:
                if col not in [lat_col, lon_col] and pd.api.types.is_numeric_dtype(data[col]):
                    if size_col is None:
                        size_col = col
                    elif color_col is None:
                        color_col = col
                        break
            
            fig = px.scatter_geo(
                data,
                lat=lat_col,
                lon=lon_col,
                size=size_col,
                color=color_col,
                hover_data=data.columns.tolist()[:4],
                title=config.get('title', 'Distribución Geográfica'),
                projection='natural earth'
            )
            
            # Centrar en Andalucía
            fig.update_geos(
                center_lat=36.7,
                center_lon=-4.4,
                projection_scale=8,
                showland=True,
                landcolor='lightgray'
            )
        else:
            # Fallback: crear gráfico de barras
            return self._create_bar_chart(config, data)
        
        # PROTECCIÓN EXTREMA: Eliminar rangeslider antes de aplicar tema
        self.debug_log_add("🛡️ Aplicando protección extrema anti-rangeslider en método individual")
        try:
            fig.update_layout(
                xaxis=dict(rangeslider=dict(visible=False))
            )
            self.debug_log_add("✅ Protección extrema aplicada en método individual")
        except Exception as e:
            self.debug_log_add(f"⚠️ Error en protección individual: {e}")

        # INSPECCIÓN ANTES DEL TEMA
        self.debug_figure_inspection(fig, "ANTES-DEL-TEMA")

        result = self._apply_health_theme(fig, theme_mode)

        # INSPECCIÓN DESPUÉS DEL TEMA
        self.debug_figure_inspection(result, "DESPUÉS-DEL-TEMA")

        return result
    
    def _create_equity_dashboard(self, equity_data: pd.DataFrame) -> go.Figure:
        """Dashboard especializado en equidad sanitaria"""
        
        # Crear subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Ratio Camas/1000 hab', 'Score de Equidad', 'Población por Distrito', 'Personal Sanitario'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # Gráfico 1: Ratio camas
        fig.add_trace(
            go.Bar(x=equity_data['distrito'], y=equity_data['ratio_camas_1000hab'], 
                   name='Camas/1000 hab', marker_color=self.health_colors['primary']),
            row=1, col=1
        )
        
        # Gráfico 2: Score equidad
        colors = ['red' if score < 50 else 'orange' if score < 75 else 'green' 
                  for score in equity_data['score_equidad']]
        fig.add_trace(
            go.Bar(x=equity_data['distrito'], y=equity_data['score_equidad'],
                   name='Score Equidad', marker_color=colors),
            row=1, col=2
        )
        
        # Gráfico 3: Población
        fig.add_trace(
            go.Scatter(x=equity_data['distrito'], y=equity_data['poblacion'],
                      mode='markers+lines', name='Población', 
                      marker_color=self.health_colors['info']),
            row=2, col=1
        )
        
        # Gráfico 4: Personal
        fig.add_trace(
            go.Bar(x=equity_data['distrito'], y=equity_data['personal_total'],
                   name='Personal Total', marker_color=self.health_colors['success']),
            row=2, col=2
        )
        
        fig.update_layout(
            title_text="Dashboard de Equidad Sanitaria",
            showlegend=False,
            height=600
        )
        
        return fig
    
    def _create_histogram_chart(self, config: Dict, data: pd.DataFrame, theme_mode: str = 'light') -> go.Figure:
        """Crear histograma para análisis de distribución"""
        
        # Detectar columna numérica para el histograma
        numeric_cols = data.select_dtypes(include=['number']).columns
        if len(numeric_cols) == 0:
            return self._create_fallback_chart(config.get('title', 'Histograma'), data)
        
        # Usar la primera columna numérica o la especificada
        col = config.get('x_axis', numeric_cols[0])
        
        fig = px.histogram(
            data,
            x=col,
            nbins=20,
            title=config.get('title', 'Distribución de Datos'),
            color_discrete_sequence=[self.health_colors['primary']]
        )
        
        # Añadir línea de media
        mean_val = data[col].mean()
        fig.add_vline(
            x=mean_val, 
            line_dash="dash", 
            line_color="red",
            annotation_text=f"Media: {mean_val:.2f}"
        )
        
        # PROTECCIÓN EXTREMA: Eliminar rangeslider antes de aplicar tema
        self.debug_log_add("🛡️ Aplicando protección extrema anti-rangeslider en método individual")
        try:
            fig.update_layout(
                xaxis=dict(rangeslider=dict(visible=False))
            )
            self.debug_log_add("✅ Protección extrema aplicada en método individual")
        except Exception as e:
            self.debug_log_add(f"⚠️ Error en protección individual: {e}")

        # INSPECCIÓN ANTES DEL TEMA
        self.debug_figure_inspection(fig, "ANTES-DEL-TEMA")

        result = self._apply_health_theme(fig, theme_mode)

        # INSPECCIÓN DESPUÉS DEL TEMA
        self.debug_figure_inspection(result, "DESPUÉS-DEL-TEMA")

        return result
    
    def _create_line_chart(self, config: Dict, data: pd.DataFrame, theme_mode: str = 'light') -> go.Figure:
        """Crear gráfico de líneas para tendencias temporales"""

        x_col = config.get('x_axis', data.columns[0])
        y_col = config.get('y_axis', data.columns[1] if len(data.columns) > 1 else data.columns[0])

        fig = px.line(
            data,
            x=x_col,
            y=y_col,
            title=config.get('title', 'Evolución Temporal'),
            markers=True
        )

        # PROTECCIÓN EXTREMA: Eliminar rangeslider antes de aplicar tema
        self.debug_log_add("🛡️ Aplicando protección extrema anti-rangeslider en método individual")
        try:
            fig.update_layout(
                xaxis=dict(rangeslider=dict(visible=False))
            )
            self.debug_log_add("✅ Protección extrema aplicada en método individual")
        except Exception as e:
            self.debug_log_add(f"⚠️ Error en protección individual: {e}")

        # INSPECCIÓN ANTES DEL TEMA
        self.debug_figure_inspection(fig, "ANTES-DEL-TEMA")

        result = self._apply_health_theme(fig, theme_mode)

        # INSPECCIÓN DESPUÉS DEL TEMA
        self.debug_figure_inspection(result, "DESPUÉS-DEL-TEMA")

        return result
    
    def _create_fallback_chart(self, title: str, data: pd.DataFrame, theme_mode: str = 'light') -> go.Figure:
        """Gráfico por defecto cuando no se puede determinar el tipo"""
        
        # Intentar crear el gráfico más apropiado
        numeric_cols = data.select_dtypes(include=['number']).columns
        
        if len(numeric_cols) >= 2:
            fig = px.scatter(data, x=numeric_cols[0], y=numeric_cols[1], title=title)
        elif len(numeric_cols) == 1:
            fig = px.histogram(data, x=numeric_cols[0], title=title)
        else:
            # Gráfico de conteo por primera columna categórica
            cat_col = data.select_dtypes(include=['object', 'category']).columns[0]
            value_counts = data[cat_col].value_counts()
            fig = px.bar(x=value_counts.index, y=value_counts.values, title=title)
        
        # PROTECCIÓN EXTREMA: Eliminar rangeslider antes de aplicar tema
        self.debug_log_add("🛡️ Aplicando protección extrema anti-rangeslider en método individual")
        try:
            fig.update_layout(
                xaxis=dict(rangeslider=dict(visible=False))
            )
            self.debug_log_add("✅ Protección extrema aplicada en método individual")
        except Exception as e:
            self.debug_log_add(f"⚠️ Error en protección individual: {e}")

        # INSPECCIÓN ANTES DEL TEMA
        self.debug_figure_inspection(fig, "ANTES-DEL-TEMA")

        result = self._apply_health_theme(fig, theme_mode)

        # INSPECCIÓN DESPUÉS DEL TEMA
        self.debug_figure_inspection(result, "DESPUÉS-DEL-TEMA")

        return result
    
    def _create_error_chart(self, error_message: str) -> go.Figure:
        """Crear gráfico de error"""
        
        fig = go.Figure()
        fig.add_annotation(
            text=f"⚠️ {error_message}",
            x=0.5, y=0.5,
            xref="paper", yref="paper",
            showarrow=False,
            font=dict(size=16, color="red")
        )
        fig.update_layout(
            title="Error en la Visualización",
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
        )
        
        return fig
    
    def _validate_plotly_config(self, fig: go.Figure) -> go.Figure:
        """Validar y corregir configuraciones problemáticas de Plotly para Streamlit"""
        try:
            # SOLUCIÓN EXTREMA: Eliminar rangeslider de forma más agresiva para Streamlit
            self.debug_log_add("🛡️ Iniciando validación extrema anti-rangeslider para Streamlit")

            # Método 1: Eliminar rangeslider directamente del layout
            if hasattr(fig, 'layout'):
                layout_dict = fig.to_plotly_json()

                # Eliminar rangeslider de todos los ejes x
                for key in list(layout_dict.get('layout', {}).keys()):
                    if 'xaxis' in key:
                        if 'rangeslider' in layout_dict['layout'][key]:
                            self.debug_log_add(f"🔴 ELIMINANDO rangeslider de {key}")
                            del layout_dict['layout'][key]['rangeslider']

                # Recrear la figura sin rangeslider
                fig = go.Figure(data=layout_dict['data'], layout=layout_dict['layout'])
                self.debug_log_add("✅ Figura recreada sin rangeslider")

            # Método 2: Forzar deshabilitación de rangeslider en todas las configuraciones posibles
            update_dict = {}
            for i in range(10):  # Hasta 10 subplots
                if i == 0:
                    update_dict['xaxis'] = dict(rangeslider=dict(visible=False))
                else:
                    update_dict[f'xaxis{i+1}'] = dict(rangeslider=dict(visible=False))

            fig.update_layout(**update_dict)
            self.debug_log_add("✅ Rangeslider deshabilitado en todos los ejes")

            return fig

        except Exception as e:
            self.debug_log_add(f"❌ Error en validación anti-rangeslider: {e}")
            # Fallback final: crear figura básica sin nada de rangeslider
            try:
                fig.update_layout(
                    xaxis=dict(rangeslider=dict(visible=False))
                )
            except:
                pass
            return fig

    def _apply_health_theme(self, fig: go.Figure, theme_mode: str = 'light') -> go.Figure:
        """Aplicar tema sanitario compatible con modo claro y oscuro"""

        self.debug_log_add("🎨 INICIANDO aplicación de tema sanitario adaptativo")

        # Primero validar configuración
        self.debug_log_add("🔍 Validando configuración Plotly")
        fig = self._validate_plotly_config(fig)
        self.debug_log_add("✅ Configuración validada")

        # Tema adaptativo que funciona tanto en claro como en oscuro
        if theme_mode == 'dark':
            # Colores para modo oscuro
            plot_bg = 'rgba(17, 24, 39, 0.95)'
            paper_bg = 'rgba(31, 41, 55, 0.98)'
            text_color = '#f9fafb'
            title_color = '#4ade80'
            grid_color = 'rgba(156, 163, 175, 0.3)'
            line_color = 'rgba(156, 163, 175, 0.5)'
            hover_bg = 'rgba(31, 41, 55, 0.95)'
            hover_border = 'rgba(74, 222, 128, 0.5)'
            legend_bg = 'rgba(17, 24, 39, 0.9)'
            legend_border = 'rgba(75, 85, 99, 0.5)'
        else:
            # Colores para modo claro
            plot_bg = 'rgba(255, 255, 255, 0.95)'
            paper_bg = 'rgba(248, 250, 252, 0.98)'
            text_color = '#1f2937'
            title_color = '#059669'
            grid_color = 'rgba(156, 163, 175, 0.3)'
            line_color = 'rgba(75, 85, 99, 0.5)'
            hover_bg = 'rgba(255, 255, 255, 0.95)'
            hover_border = 'rgba(0, 168, 107, 0.5)'
            legend_bg = 'rgba(255, 255, 255, 0.9)'
            legend_border = 'rgba(156, 163, 175, 0.3)'

        fig.update_layout(
            # Fondo adaptativo según tema
            plot_bgcolor=plot_bg,
            paper_bgcolor=paper_bg,

            # Tipografía con colores adaptativos
            font=dict(family="Inter, Arial, sans-serif", size=12, color=text_color),
            title_font=dict(size=16, color=title_color, family="Inter"),

            # Márgenes y espaciado
            margin=dict(l=60, r=60, t=80, b=60),

            # Grid y ejes con colores adaptativos
            xaxis=dict(
                showgrid=True,
                gridcolor=grid_color,
                linecolor=line_color,
                tickfont=dict(color=text_color),
                title=dict(font=dict(color=text_color)),
                rangeslider=dict(visible=False)  # IMPORTANTE: sin rangeslider
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor=grid_color,
                linecolor=line_color,
                tickfont=dict(color=text_color),
                title=dict(font=dict(color=text_color))
            ),

            # Hover deshabilitado completamente para evitar cualquier error
            hovermode=False,  # Deshabilitar completamente hover para evitar errores

            # Leyenda con tema adaptativo
            legend=dict(
                bgcolor=legend_bg,
                bordercolor=legend_border,
                font=dict(color=text_color)
            ),

            # PROTECCIONES ADICIONALES PARA STREAMLIT
            # rangeslider solo se configura en xaxis específicos

            # IMPORTANTE: NO incluir hoversubplots, hoverdistance, spikedistance
            # Estos parámetros causan errores en Plotly
        )

        # Actualizar colores de elementos para mejor legibilidad
        if len(fig.data) > 0:
            # Colores optimizados para modo claro con buena legibilidad
            light_colors = [
                '#059669',  # Verde sanitario principal
                '#0ea5e9',  # Azul médico
                '#dc2626',  # Rojo médico
                '#d97706',  # Naranja advertencia
                '#7c3aed',  # Púrpura
                '#0d9488',  # Teal médico
                '#be185d',  # Rosa médico
                '#4338ca'   # Índigo
            ]

            # Aplicar colores según el tipo de gráfico
            for i, trace in enumerate(fig.data):
                if hasattr(trace, 'marker'):
                    # Para gráficos de barras, scatter, etc.
                    if isinstance(getattr(trace.marker, 'color', None), str):
                        fig.data[i].marker.color = light_colors[i % len(light_colors)]
                    elif hasattr(trace.marker, 'colorscale'):
                        # Para gráficos con escala de colores apropiada para modo claro
                        fig.data[i].marker.colorscale = 'RdYlBu_r'

                if hasattr(trace, 'line') and hasattr(trace.line, 'color'):
                    # Para gráficos de líneas
                    fig.data[i].line.color = light_colors[i % len(light_colors)]

        self.debug_log_add("🎨 TEMA ADAPTATIVO APLICADO exitosamente")
        return fig

    def enable_rangeslider(self, fig: go.Figure, enable_buttons: bool = True) -> go.Figure:
        """Habilitar rangeslider en gráficos temporales de forma segura"""
        try:
            # Configurar rangeslider con tema sanitario
            fig.update_layout(
                xaxis=dict(
                    rangeslider=dict(
                        visible=True,
                        bgcolor='rgba(30, 30, 30, 0.8)',
                        bordercolor='rgba(76, 175, 80, 0.6)',
                        borderwidth=2,
                        thickness=0.15,
                        # Configuración específica para evitar errores
                        yaxis=dict(
                            rangemode='auto'  # CORREGIDO: 'tozero' no es válido para rangeslider
                        )
                    ),
                    type='date' if enable_buttons else 'linear'
                )
            )

            # Agregar botones de rango temporal si es necesario
            if enable_buttons:
                fig.update_layout(
                    xaxis=dict(
                        rangeselector=dict(
                            buttons=list([
                                dict(count=7, label="7d", step="day", stepmode="backward"),
                                dict(count=30, label="30d", step="day", stepmode="backward"),
                                dict(count=90, label="3m", step="day", stepmode="backward"),
                                dict(step="all", label="Todo")
                            ]),
                            bgcolor='rgba(30, 30, 30, 0.9)',
                            bordercolor='rgba(76, 175, 80, 0.6)',
                            font=dict(color='#ffffff')
                        )
                    )
                )

            return fig

        except Exception as e:
            # Si hay error con rangeslider, devolver sin él
            print(f"Warning: No se pudo configurar rangeslider: {e}")
            fig.update_layout(xaxis=dict(rangeslider=dict(visible=False)))
            return fig

# Clase auxiliar para análisis automático de datos
class DataAnalyzer:
    """Analizador automático para sugerir el mejor tipo de visualización"""
    
    @staticmethod
    def suggest_chart_type(data: pd.DataFrame, analysis_type: str = "general") -> str:
        """Sugerir el tipo de gráfico más apropiado basado en los datos"""
        
        if len(data) == 0:
            return "bar"
        
        numeric_cols = len(data.select_dtypes(include=['number']).columns)
        categorical_cols = len(data.select_dtypes(include=['object', 'category']).columns)
        total_rows = len(data)
        
        # Reglas específicas por tipo de análisis sanitario
        if analysis_type == "equity":
            if numeric_cols >= 3:
                return "heatmap"
            elif 'distrito' in data.columns or 'municipio' in data.columns:
                return "bar"
            else:
                return "scatter"
                
        elif analysis_type == "demographic":
            if 'municipio' in data.columns and 'poblacion' in data.columns:
                return "bar"
            elif total_rows > 20:
                return "scatter"
            else:
                return "bar"
                
        elif analysis_type == "infrastructure":
            if 'tipo_centro' in data.columns:
                return "pie" if total_rows <= 8 else "bar"
            elif 'camas' in data.columns or 'personal' in data.columns:
                return "bar"
            else:
                return "bar"
                
        elif analysis_type == "services":
            if categorical_cols > 0 and numeric_cols > 0:
                return "pie" if total_rows <= 8 else "bar"
            else:
                return "heatmap"
                
        elif analysis_type == "accessibility":
            if 'tiempo' in str(data.columns).lower():
                return "histogram"
            else:
                return "bar"
                
        elif analysis_type == "metrics":
            if numeric_cols >= 2:
                return "scatter"
            else:
                return "bar"
        
        # Reglas generales basadas en estructura de datos
        if numeric_cols >= 2:
            if total_rows > 50:
                return "scatter"
            elif 'tiempo' in str(data.columns).lower() or 'fecha' in str(data.columns).lower():
                return "line"
            else:
                return "scatter"
                
        elif numeric_cols == 1 and categorical_cols >= 1:
            if total_rows <= 8:
                return "pie"
            else:
                return "bar"
                
        elif categorical_cols >= 1:
            return "pie" if total_rows <= 6 else "bar"
        
        return "bar"  # Fallback por defecto
    
    @staticmethod
    def detect_key_columns(data: pd.DataFrame, analysis_type: str = "general") -> Dict:
        """Detectar columnas clave para el análisis"""
        
        result = {
            'x_axis': None,
            'y_axis': None,
            'color_by': None,
            'size_by': None
        }
        
        numeric_cols = data.select_dtypes(include=['number']).columns.tolist()
        categorical_cols = data.select_dtypes(include=['object', 'category']).columns.tolist()
        
        # Forzar detección de columnas específicas que sabemos que son categóricas
        known_categorical = ['distrito_sanitario', 'tipo_centro', 'municipio', 'nombre', 'codigo_sas']
        for col in known_categorical:
            if col in data.columns and col not in categorical_cols:
                categorical_cols.append(col)
        
        # Debug: mostrar tipos de columnas detectadas
        
        # Detectar columnas por nombre/contexto
        name_patterns = {
            'geographic': ['municipio', 'distrito', 'provincia', 'zona'],
            'hospital': ['hospital', 'centro', 'nombre'],
            'population': ['poblacion', 'habitantes', 'hab'],
            'health_metrics': ['ratio', 'camas', 'personal', 'consultas'],
            'time': ['fecha', 'año', 'mes', 'tiempo']
        }
        
        # Asignar X e Y basado en el tipo de análisis
        if analysis_type == "executive_summary":
            # Para resumen ejecutivo, usar tipo de centro como X y métricas clave como Y
            if 'tipo_centro' in categorical_cols:
                result['x_axis'] = 'tipo_centro'
            elif 'distrito_sanitario' in categorical_cols:
                result['x_axis'] = 'distrito_sanitario'
            elif 'municipio' in categorical_cols:
                result['x_axis'] = 'municipio'
            elif categorical_cols:
                result['x_axis'] = categorical_cols[0]
            else:
                result['x_axis'] = data.columns[0]
            
            # Para Y, usar métricas clave del sistema sanitario
            if 'camas_funcionamiento_2025' in numeric_cols:
                result['y_axis'] = 'camas_funcionamiento_2025'
            elif 'personal_sanitario_2025' in numeric_cols:
                result['y_axis'] = 'personal_sanitario_2025'
            elif 'poblacion_referencia_2025' in numeric_cols:
                result['y_axis'] = 'poblacion_referencia_2025'
            elif numeric_cols:
                result['y_axis'] = numeric_cols[0]
            else:
                result['y_axis'] = data.columns[1] if len(data.columns) > 1 else data.columns[0]
                
        elif analysis_type == "strategic_planning":
            # Para planificación estratégica, usar distritos como X y métricas de rendimiento como Y
            if 'distrito_sanitario' in categorical_cols:
                result['x_axis'] = 'distrito_sanitario'
            elif 'tipo_centro' in categorical_cols:
                result['x_axis'] = 'tipo_centro'
            elif 'municipio' in categorical_cols:
                result['x_axis'] = 'municipio'
            elif categorical_cols:
                result['x_axis'] = categorical_cols[0]
            else:
                result['x_axis'] = data.columns[0]
            
            # Para Y, usar métricas de rendimiento o eficiencia
            if 'personal_sanitario_2025' in numeric_cols:
                result['y_axis'] = 'personal_sanitario_2025'
            elif 'camas_funcionamiento_2025' in numeric_cols:
                result['y_axis'] = 'camas_funcionamiento_2025'
            elif 'poblacion_referencia_2025' in numeric_cols:
                result['y_axis'] = 'poblacion_referencia_2025'
            elif numeric_cols:
                result['y_axis'] = numeric_cols[0]
            else:
                result['y_axis'] = data.columns[1] if len(data.columns) > 1 else data.columns[0]
                
        elif analysis_type == "user_management":
            # Para gestión de usuarios, crear un gráfico de distribución por tipo de centro
            if 'tipo_centro' in categorical_cols:
                result['x_axis'] = 'tipo_centro'
            elif 'distrito_sanitario' in categorical_cols:
                result['x_axis'] = 'distrito_sanitario'
            elif 'municipio' in categorical_cols:
                result['x_axis'] = 'municipio'
            elif categorical_cols:
                result['x_axis'] = categorical_cols[0]
            else:
                result['x_axis'] = data.columns[0]
            
            # Para Y, usar personal sanitario como proxy de usuarios
            if 'personal_sanitario_2025' in numeric_cols:
                result['y_axis'] = 'personal_sanitario_2025'
            elif 'camas_funcionamiento_2025' in numeric_cols:
                result['y_axis'] = 'camas_funcionamiento_2025'
            elif 'poblacion_referencia_2025' in numeric_cols:
                result['y_axis'] = 'poblacion_referencia_2025'
            elif numeric_cols:
                result['y_axis'] = numeric_cols[0]
            else:
                result['y_axis'] = data.columns[1] if len(data.columns) > 1 else data.columns[0]
            
            # Para gestión de usuarios, usar color por distrito para mostrar distribución
            if 'distrito_sanitario' in categorical_cols:
                result['color_by'] = 'distrito_sanitario'
                
        elif analysis_type == "equity":
            # Para equidad, priorizar distrito_sanitario sobre municipio
            if 'distrito_sanitario' in categorical_cols:
                result['x_axis'] = 'distrito_sanitario'
            elif 'municipio' in categorical_cols:
                result['x_axis'] = 'municipio'
            elif categorical_cols:
                result['x_axis'] = categorical_cols[0]
            else:
                result['x_axis'] = data.columns[0]
            
            # Para Y, priorizar métricas de equidad (evitar latitud/longitud)
            equity_metrics = ['camas_funcionamiento_2025', 'personal_sanitario_2025', 'poblacion_referencia_2025', 'urgencias_24h', 'uci_camas', 'quirofanos_activos']
            for metric in equity_metrics:
                if metric in numeric_cols:
                    result['y_axis'] = metric
                    break
            else:
                # Si no encuentra métricas de equidad, usar la primera numérica que no sea latitud/longitud
                for col in numeric_cols:
                    if col not in ['latitud', 'longitud']:
                        result['y_axis'] = col
                        break
                else:
                    result['y_axis'] = numeric_cols[0] if numeric_cols else data.columns[1] if len(data.columns) > 1 else data.columns[0]
                
        elif analysis_type == "demographic":
            # Para demografía, usar municipio como X y población como Y
            if 'municipio' in categorical_cols:
                result['x_axis'] = 'municipio'
            elif categorical_cols:
                result['x_axis'] = categorical_cols[0]
            else:
                result['x_axis'] = data.columns[0]
            
            if 'poblacion_2025' in numeric_cols:
                result['y_axis'] = 'poblacion_2025'
            elif 'crecimiento_2024_2025' in numeric_cols:
                result['y_axis'] = 'crecimiento_2024_2025'
            elif numeric_cols:
                result['y_axis'] = numeric_cols[0]
            else:
                result['y_axis'] = data.columns[1] if len(data.columns) > 1 else data.columns[0]
                
        elif analysis_type == "infrastructure":
            # Para infraestructura, usar nombre/tipo como X y camas/personal como Y
            if 'nombre' in categorical_cols:
                result['x_axis'] = 'nombre'
            elif 'tipo_centro' in categorical_cols:
                result['x_axis'] = 'tipo_centro'
            elif categorical_cols:
                result['x_axis'] = categorical_cols[0]
            else:
                result['x_axis'] = data.columns[0]
            
            if 'camas_funcionamiento_2025' in numeric_cols:
                result['y_axis'] = 'camas_funcionamiento_2025'
            elif 'personal_sanitario_2025' in numeric_cols:
                result['y_axis'] = 'personal_sanitario_2025'
            elif numeric_cols:
                result['y_axis'] = numeric_cols[0]
            else:
                result['y_axis'] = data.columns[1] if len(data.columns) > 1 else data.columns[0]
        else:
            # Lógica general
            if categorical_cols:
                # Priorizar columnas importantes por contexto
                for pattern_type, patterns in name_patterns.items():
                    for col in categorical_cols:
                        if any(pattern in col.lower() for pattern in patterns):
                            result['x_axis'] = col
                            break
                    if result['x_axis']:
                        break
                
                if not result['x_axis']:
                    result['x_axis'] = categorical_cols[0]
            else:
                result['x_axis'] = data.columns[0]
        
        # Asignar Y (numérica preferiblemente)
        if numeric_cols:
            # Priorizar métricas importantes
            priority_metrics = ['score', 'ratio', 'total', 'suma', 'promedio', 'media']
            for col in numeric_cols:
                if any(metric in col.lower() for metric in priority_metrics):
                    result['y_axis'] = col
                    break
            
            if not result['y_axis']:
                result['y_axis'] = numeric_cols[0]
        else:
            result['y_axis'] = data.columns[1] if len(data.columns) > 1 else data.columns[0]
        
        # Asignar color (preferir categóricas o métricas importantes)
        available_cols = [col for col in data.columns if col not in [result['x_axis'], result['y_axis']]]
        
        if available_cols:
            # Priorizar columnas de distrito, tipo, etc.
            priority_color = ['distrito', 'tipo', 'categoria', 'nivel', 'estado']
            for col in available_cols:
                if any(priority in col.lower() for priority in priority_color):
                    result['color_by'] = col
                    break
            
            if not result['color_by'] and len(available_cols) > 0:
                result['color_by'] = available_cols[0]
        
        # Asignar tamaño (solo para scatter plots)
        remaining_numeric = [col for col in numeric_cols if col not in [result['y_axis'], result['color_by']]]
        if remaining_numeric and analysis_type in ['demographic', 'geographic']:
            result['size_by'] = remaining_numeric[0]
        
        return result