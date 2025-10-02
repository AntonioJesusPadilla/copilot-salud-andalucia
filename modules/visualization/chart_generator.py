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

        # ========== PALETA DE COLORES PROFESIONAL SAS ANDALUCÍA ==========
        # Colores adaptativos según tema con contraste WCAG AA

        # Colores para MODO CLARO (saturados, contraste >4.5:1)
        self.health_colors_light = {
            'primary': '#0369a1',      # Azul sanitario SAS profundo
            'secondary': '#0284c7',    # Azul institucional
            'accent': '#047857',       # Verde salud oscuro
            'warning': '#c2410c',      # Naranja terracota
            'info': '#0ea5e9',         # Azul cielo SAS
            'success': '#059669',      # Verde esmeralda
            'error': '#b91c1c',        # Rojo médico intenso
            'purple': '#6d28d9',       # Púrpura datos
            'cyan': '#0e7490',         # Cyan profesional
            'pink': '#be123c'          # Rosa sanitario
        }

        # Colores para MODO OSCURO (brillantes, luminosos >7:1)
        self.health_colors_dark = {
            'primary': '#7dd3fc',      # Azul cielo brillante
            'secondary': '#38bdf8',    # Azul eléctrico
            'accent': '#6ee7b7',       # Verde menta luminoso
            'warning': '#fdba74',      # Naranja melocotón
            'info': '#38bdf8',         # Azul brillante
            'success': '#34d399',      # Verde neón suave
            'error': '#fca5a5',        # Rojo coral suave
            'purple': '#c4b5fd',       # Púrpura lavanda
            'cyan': '#67e8f9',         # Cyan aguamarina
            'pink': '#f9a8d4'          # Rosa pastel
        }

        # Paleta de gráficos de 8 colores profesionales
        self.chart_palette_light = [
            '#0369a1',  # Azul sanitario principal
            '#047857',  # Verde salud
            '#b91c1c',  # Rojo médico
            '#6d28d9',  # Púrpura datos
            '#c2410c',  # Naranja terracota
            '#0e7490',  # Cyan profesional
            '#be123c',  # Rosa sanitario
            '#475569'   # Gris corporativo
        ]

        self.chart_palette_dark = [
            '#7dd3fc',  # Azul cielo brillante
            '#6ee7b7',  # Verde menta
            '#fca5a5',  # Rojo coral
            '#c4b5fd',  # Púrpura lavanda
            '#fdba74',  # Naranja melocotón
            '#67e8f9',  # Cyan aguamarina
            '#f9a8d4',  # Rosa pastel
            '#cbd5e1'   # Gris plata
        ]

        # Colores actuales (se actualizan con set_theme)
        self.health_colors = self.health_colors_light.copy()
        self.chart_palette = self.chart_palette_light.copy()

        # Tema actual
        self.current_theme = 'light'

        # Escalas de colores profesionales por contexto (se adaptan al tema)
        self.color_scales = {
            'equity': 'RdBu_r',        # Divergente para equidad
            'accessibility': 'Blues',  # Secuencial azul
            'population': 'Viridis',   # Perceptualmente uniforme
            'services': 'Set2',        # Cualitativa suave
            'health_metrics': 'RdBu_r' # Divergente sanitario
        }

    def set_theme(self, theme_mode: str):
        """Actualizar paleta de colores según el tema activo"""
        self.current_theme = theme_mode

        if theme_mode == 'dark':
            self.health_colors = self.health_colors_dark.copy()
            self.chart_palette = self.chart_palette_dark.copy()
        else:
            self.health_colors = self.health_colors_light.copy()
            self.chart_palette = self.chart_palette_light.copy()

        self.debug_log_add(f"✨ Tema actualizado a: {theme_mode}")
        self.debug_log_add(f"Paleta principal: {self.health_colors['primary']}")

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
                try:
                    # Intentar múltiples métodos para obtener el dict del layout
                    if hasattr(fig.layout, 'to_dict'):
                        layout_dict = fig.layout.to_dict()
                    elif hasattr(fig.layout, '_props'):
                        layout_dict = dict(fig.layout._props)
                    else:
                        layout_dict = dict(fig.layout)
                    self.debug_log_add(f"Layout keys: {list(layout_dict.keys())}")
                except Exception as layout_error:
                    self.debug_log_add(f"Error accediendo al layout: {layout_error}")
                    layout_dict = {}

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
        """Generar gráfico basado en configuración de IA con colores adaptativos"""

        # RESET del log de debug
        self.debug_log = []
        self.debug_log_add("🚀 INICIANDO GENERACIÓN DE GRÁFICO")

        # ✨ ACTUALIZAR TEMA Y COLORES
        self.set_theme(theme_mode)

        # Validaciones básicas
        if data is None or data.empty:
            self.debug_log_add("❌ Datos vacíos o None")
            return self._create_error_chart("Datos vacíos o None")

        if not isinstance(chart_config, dict):
            self.debug_log_add("❌ Configuración de gráfico inválida")
            return self._create_error_chart("Configuración de gráfico inválida")

        chart_type = chart_config.get('type', 'bar')
        title = chart_config.get('title', 'Análisis Sanitario')

        self.debug_log_add(f"🎨 Tema activo: {theme_mode}")
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

            # LIMPIEZA NUCLEAR ANTI-RANGESLIDER
            self.debug_log_add("🧨 Aplicando LIMPIEZA NUCLEAR anti-rangeslider")
            try:
                result = self._nuclear_rangeslider_cleaner(result)
                self.debug_log_add("✅ Limpieza nuclear completada exitosamente")
            except Exception as e:
                self.debug_log_add(f"❌ Error en limpieza nuclear: {e}")
                # Fallback extremo
                try:
                    result = go.Figure(data=result.data, layout=dict(
                        xaxis=dict(rangeslider=dict(visible=False)),
                        yaxis=dict(),
                        showlegend=True
                    ))
                except:
                    result = self._create_error_chart("Error en limpieza nuclear")

            # INSPECCIÓN FINAL
            self.debug_figure_inspection(result, "FINAL")

            # VERIFICACIÓN FINAL ABSOLUTA ANTI-RANGESLIDER
            try:
                layout_check = result.to_plotly_json().get('layout', {})
                problematic_found = False

                for key, value in layout_check.items():
                    if key.startswith('yaxis') and isinstance(value, dict) and 'rangeslider' in value:
                        print(f"🚨 INTERCEPTADO rangeslider ilegal en {key} en verificación final!")
                        problematic_found = True

                if problematic_found:
                    print("🧨 APLICANDO CORRECCIÓN FINAL DE EMERGENCIA")
                    # Recrear completamente la figura sin rangeslider problemáticos
                    safe_layout = {}
                    for key, value in layout_check.items():
                        if key.startswith('yaxis') and isinstance(value, dict):
                            # Crear yaxis sin rangeslider
                            safe_layout[key] = {k: v for k, v in value.items() if k != 'rangeslider'}
                        else:
                            safe_layout[key] = value

                    result = go.Figure(data=result.data, layout=safe_layout)
                    print("✅ Corrección final aplicada exitosamente")

            except Exception as e:
                print(f"❌ Error en verificación final: {e}")

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
                color_discrete_sequence=self.chart_palette  # ✨ Paleta adaptativa
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
            color_discrete_sequence=[self.health_colors['primary']]  # ✨ Color adaptativo
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
    
    def _nuclear_rangeslider_cleaner(self, fig: go.Figure) -> go.Figure:
        """LIMPIEZA NUCLEAR: Eliminar TODO rastro de rangeslider problemático"""
        try:
            self.debug_log_add("🧨 INICIANDO LIMPIEZA NUCLEAR ANTI-RANGESLIDER")

            # Paso 1: Convertir a diccionario y limpiar COMPLETAMENTE
            fig_dict = fig.to_plotly_json()

            # Función recursiva para limpiar cualquier rangeslider en cualquier lugar
            def clean_recursive(obj, path=""):
                if isinstance(obj, dict):
                    keys_to_remove = []
                    for key, value in obj.items():
                        current_path = f"{path}.{key}" if path else key

                        # Si encontramos rangeslider en yaxis, ELIMINARLO
                        if key == "rangeslider" and "yaxis" in path:
                            self.debug_log_add(f"🧨 ELIMINANDO rangeslider PROHIBIDO en {path}")
                            keys_to_remove.append(key)

                        # Si es un yaxis que contiene rangeslider, LIMPIAR
                        elif key.startswith("yaxis") and isinstance(value, dict) and "rangeslider" in value:
                            self.debug_log_add(f"🧨 LIMPIANDO yaxis con rangeslider: {key}")
                            del value["rangeslider"]

                        # Si es rangeslider que contiene yaxis, ELIMINAR yaxis
                        elif key == "rangeslider" and isinstance(value, dict) and "yaxis" in value:
                            self.debug_log_add(f"🧨 ELIMINANDO yaxis de rangeslider en {path}")
                            del value["yaxis"]

                        # Seguir limpiando recursivamente
                        else:
                            clean_recursive(value, current_path)

                    # Eliminar las keys marcadas
                    for key in keys_to_remove:
                        del obj[key]

                elif isinstance(obj, list):
                    for i, item in enumerate(obj):
                        clean_recursive(item, f"{path}[{i}]")

            # Aplicar limpieza recursiva
            clean_recursive(fig_dict)

            # Recrear figura limpia
            fig = go.Figure(data=fig_dict.get('data', []), layout=fig_dict.get('layout', {}))

            # Paso 2: Aplicar configuración segura forzada
            safe_config = {}

            # Para TODOS los posibles ejes
            for i in range(20):  # Máximo 20 subplots por seguridad
                if i == 0:
                    safe_config['xaxis'] = dict(rangeslider=dict(visible=False))
                    safe_config['yaxis'] = dict()  # SIEMPRE vacío
                else:
                    safe_config[f'xaxis{i+1}'] = dict(rangeslider=dict(visible=False))
                    safe_config[f'yaxis{i+1}'] = dict()  # SIEMPRE vacío

            fig.update_layout(**safe_config)

            # Paso 3: Verificación final AGRESIVA
            final_check = fig.to_plotly_json()
            for key, value in final_check.get('layout', {}).items():
                if key.startswith('yaxis') and isinstance(value, dict):
                    if 'rangeslider' in value:
                        self.debug_log_add(f"🚨 CRÍTICO: Aún hay rangeslider en {key} - ELIMINANDO")
                        fig.update_layout(**{key: dict()})

            self.debug_log_add("✅ LIMPIEZA NUCLEAR COMPLETADA")
            return fig

        except Exception as e:
            self.debug_log_add(f"❌ Error en limpieza nuclear: {e}")
            # FALLBACK DE EMERGENCIA: Figura básica sin nada
            try:
                return go.Figure(data=fig.data, layout=dict(
                    xaxis=dict(rangeslider=dict(visible=False)),
                    yaxis=dict(),
                    showlegend=True
                ))
            except:
                return go.Figure()

    def _validate_plotly_config(self, fig: go.Figure) -> go.Figure:
        """Validar y corregir configuraciones problemáticas de Plotly para Streamlit"""
        try:
            # LIMPIEZA NUCLEAR PRIMERO
            fig = self._nuclear_rangeslider_cleaner(fig)

            # VERIFICACIÓN ADICIONAL ANTI-RANGESLIDER EN YAXIS
            layout_dict = fig.to_plotly_json().get('layout', {})

            # Verificar y limpiar cualquier yaxis que tenga rangeslider
            updates = {}
            for key, value in layout_dict.items():
                if key.startswith('yaxis') and isinstance(value, dict):
                    if 'rangeslider' in value:
                        print(f"🚨 ENCONTRADO rangeslider ilegal en {key} - ELIMINANDO")
                        # Crear una copia del yaxis sin rangeslider
                        clean_yaxis = {k: v for k, v in value.items() if k != 'rangeslider'}
                        updates[key] = clean_yaxis

            # Aplicar las correcciones
            if updates:
                fig.update_layout(**updates)
                print(f"✅ Corregidos {len(updates)} ejes problemáticos")

            return fig

        except Exception as e:
            print(f"❌ Error en validación de Plotly: {e}")
            # Fallback de emergencia
            try:
                return go.Figure(data=fig.data, layout=dict(
                    xaxis=dict(rangeslider=dict(visible=False)),
                    yaxis=dict(),
                    showlegend=True
                ))
            except:
                return go.Figure()

    def _apply_health_theme(self, fig: go.Figure, theme_mode: str = 'light') -> go.Figure:
        """Aplicar tema sanitario profesional SAS Andalucía con colores adaptativos"""

        self.debug_log_add("🎨 INICIANDO aplicación de tema sanitario SAS Andalucía")

        # Primero validar configuración
        self.debug_log_add("🔍 Validando configuración Plotly")
        fig = self._validate_plotly_config(fig)
        self.debug_log_add("✅ Configuración validada")

        # ========== TEMA PROFESIONAL SAS ANDALUCÍA ==========
        if theme_mode == 'dark':
            # ✨ MODO OSCURO - Colores elegantes y luminosos
            plot_bg = 'rgba(15, 23, 42, 0.95)'      # --bg-primary oscuro
            paper_bg = 'rgba(30, 41, 59, 0.98)'     # --bg-surface oscuro
            text_color = '#f8fafc'                   # --text-primary claro
            title_color = '#7dd3fc'                  # Azul brillante (chart-1 dark)
            grid_color = 'rgba(100, 116, 139, 0.25)' # Grilla sutil
            line_color = 'rgba(148, 163, 184, 0.4)'  # Líneas sutiles
            hover_bg = 'rgba(51, 65, 85, 0.95)'     # --bg-elevated oscuro
            hover_border = 'rgba(125, 211, 252, 0.5)' # Azul brillante
            legend_bg = 'rgba(15, 23, 42, 0.9)'
            legend_border = 'rgba(71, 85, 105, 0.5)'
        else:
            # ✨ MODO CLARO - Colores profesionales institucionales
            plot_bg = 'rgba(255, 255, 255, 1.0)'    # --bg-primary claro
            paper_bg = 'rgba(248, 250, 252, 1.0)'   # --bg-surface claro
            text_color = '#0f172a'                   # --text-primary oscuro
            title_color = '#0369a1'                  # Azul SAS institucional
            grid_color = 'rgba(226, 232, 240, 0.6)' # Grilla profesional
            line_color = 'rgba(100, 116, 139, 0.4)' # Líneas sutiles
            hover_bg = 'rgba(249, 250, 251, 1.0)'
            hover_border = 'rgba(5, 150, 105, 0.8)'
            legend_bg = 'rgba(255, 255, 255, 1.0)'
            legend_border = 'rgba(209, 213, 219, 0.6)'

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
                # CRÍTICO: NUNCA añadir rangeslider aquí - solo válido en xaxis
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

        # Aplicar paleta de colores profesional unificada
        if len(fig.data) > 0:
            # Colores profesionales basados en el tema
            if theme_mode == 'dark':
                # Paleta para modo oscuro - Colores claros y vibrantes
                chart_colors = [
                    '#3b82f6',  # Azul médico claro
                    '#10b981',  # Verde sanitario claro
                    '#ef4444',  # Rojo claro
                    '#a855f7',  # Púrpura claro
                    '#f59e0b',  # Amarillo profesional
                    '#06b6d4',  # Cyan médico
                    '#ec4899',  # Rosa claro
                    '#94a3b8'   # Gris neutro claro
                ]
                default_colorscale = 'Viridis'
            else:
                # Paleta para modo claro - Colores oscuros y contrastantes
                chart_colors = [
                    '#1e40af',  # Azul médico oscuro
                    '#059669',  # Verde sanitario oscuro
                    '#dc2626',  # Rojo oscuro
                    '#7c3aed',  # Púrpura oscuro
                    '#d97706',  # Naranja oscuro
                    '#0891b2',  # Cyan oscuro
                    '#be185d',  # Rosa oscuro
                    '#374151'   # Gris neutro oscuro
                ]
                default_colorscale = 'Blues'

            # Aplicar colores de forma inteligente según el tipo de gráfico
            for i, trace in enumerate(fig.data):
                color_index = i % len(chart_colors)

                if hasattr(trace, 'marker'):
                    # Para gráficos de barras, scatter, etc.
                    if isinstance(getattr(trace.marker, 'color', None), str) or getattr(trace.marker, 'color', None) is None:
                        fig.data[i].marker.color = chart_colors[color_index]

                    # Configurar escalas de colores para mapas de calor, etc.
                    elif hasattr(trace.marker, 'colorscale'):
                        fig.data[i].marker.colorscale = default_colorscale

                    # Mejorar visibilidad con contornos
                    if hasattr(trace.marker, 'line'):
                        fig.data[i].marker.line = dict(
                            width=1,
                            color='rgba(255,255,255,0.3)' if theme_mode == 'dark' else 'rgba(0,0,0,0.1)'
                        )

                if hasattr(trace, 'line') and hasattr(trace.line, 'color'):
                    # Para gráficos de líneas - colores más contrastantes
                    fig.data[i].line.color = chart_colors[color_index]
                    fig.data[i].line.width = 3  # Líneas más gruesas para visibilidad

                # Para gráficos de área/fill
                if hasattr(trace, 'fillcolor'):
                    # Color de relleno con transparencia
                    base_color = chart_colors[color_index]
                    fig.data[i].fillcolor = f"{base_color}40"  # 25% transparencia

        self.debug_log_add("🎨 TEMA ADAPTATIVO APLICADO exitosamente")
        return fig

    def enable_rangeslider(self, fig: go.Figure, enable_buttons: bool = True) -> go.Figure:
        """Habilitar rangeslider en gráficos temporales de forma segura"""
        try:
            # CONFIGURACIÓN CORREGIDA: rangeslider NUNCA debe tener yaxis
            fig.update_layout(
                xaxis=dict(
                    rangeslider=dict(
                        visible=True,
                        bgcolor='rgba(30, 30, 30, 0.8)',
                        bordercolor='rgba(76, 175, 80, 0.6)',
                        borderwidth=2,
                        thickness=0.15
                        # ELIMINADO: yaxis NO es válido dentro de rangeslider
                    ),
                    type='date' if enable_buttons else 'linear'
                ),
                # Configurar yaxis por separado (NUNCA dentro de rangeslider)
                yaxis=dict(
                    fixedrange=False
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
            # Si hay error con rangeslider, devolver configuración segura
            print(f"Warning: Error en rangeslider (corregido): {e}")
            fig.update_layout(
                xaxis=dict(rangeslider=dict(visible=False)),
                yaxis=dict(fixedrange=False)  # yaxis separado, NUNCA dentro de rangeslider
            )
            return fig


# FUNCIÓN GLOBAL DE EMERGENCIA ANTI-RANGESLIDER
def emergency_rangeslider_cleaner(fig):
    """Función de emergencia para limpiar rangeslider de cualquier figura"""
    try:
        if fig is None:
            return go.Figure()

        # Conversión completa y limpieza
        fig_dict = fig.to_plotly_json()

        # Eliminar TODO rangeslider de yaxis
        if 'layout' in fig_dict:
            for key, value in list(fig_dict['layout'].items()):
                if key.startswith('yaxis') and isinstance(value, dict):
                    if 'rangeslider' in value:
                        print(f"🧨 EMERGENCY: Eliminando rangeslider de {key}")
                        del value['rangeslider']

                elif key.startswith('xaxis') and isinstance(value, dict):
                    if 'rangeslider' in value and isinstance(value['rangeslider'], dict):
                        if 'yaxis' in value['rangeslider']:
                            print(f"🧨 EMERGENCY: Eliminando yaxis de rangeslider en {key}")
                            del value['rangeslider']['yaxis']

        # Recrear figura
        clean_fig = go.Figure(data=fig_dict.get('data', []), layout=fig_dict.get('layout', {}))

        # Aplicar configuración segura
        safe_update = {}
        for i in range(10):
            if i == 0:
                safe_update['xaxis'] = dict(rangeslider=dict(visible=False))
                safe_update['yaxis'] = dict()
            else:
                safe_update[f'xaxis{i+1}'] = dict(rangeslider=dict(visible=False))
                safe_update[f'yaxis{i+1}'] = dict()

        clean_fig.update_layout(**safe_update)
        return clean_fig

    except Exception as e:
        print(f"❌ Emergency cleaner failed: {e}")
        return go.Figure()


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