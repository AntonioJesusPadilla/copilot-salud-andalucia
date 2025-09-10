import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from typing import Dict, Optional

class SmartChartGenerator:
    def __init__(self):
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
    
    def generate_chart(self, chart_config: Dict, data: pd.DataFrame) -> go.Figure:
        """Generar gráfico basado en configuración de IA"""
        
        chart_type = chart_config.get('type', 'bar')
        title = chart_config.get('title', 'Análisis Sanitario')
        
        try:
            if chart_type == 'bar':
                return self._create_bar_chart(chart_config, data)
            elif chart_type == 'line':
                return self._create_line_chart(chart_config, data)
            elif chart_type == 'scatter':
                return self._create_scatter_chart(chart_config, data)
            elif chart_type == 'pie':
                return self._create_pie_chart(chart_config, data)
            elif chart_type == 'heatmap':
                return self._create_heatmap(chart_config, data)
            elif chart_type == 'map':
                return self._create_geographic_chart(chart_config, data)
            else:
                return self._create_fallback_chart(title, data)
                
        except Exception as e:
            return self._create_error_chart(f"Error generando gráfico: {str(e)}")
    
    def _create_bar_chart(self, config: Dict, data: pd.DataFrame) -> go.Figure:
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
            fig.update_xaxis(tickangle=45)
        
        return self._apply_health_theme(fig)
    
    def _create_scatter_chart(self, config: Dict, data: pd.DataFrame) -> go.Figure:
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
        
        return self._apply_health_theme(fig)
    
    def _create_pie_chart(self, config: Dict, data: pd.DataFrame) -> go.Figure:
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
            hovertemplate='<b>%{label}</b><br>Valor: %{value}<br>Porcentaje: %{percent}<extra></extra>'
        )
        
        return self._apply_health_theme(fig)
    
    def _create_heatmap(self, config: Dict, data: pd.DataFrame) -> go.Figure:
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
        
        return self._apply_health_theme(fig)
    
    def _create_geographic_chart(self, config: Dict, data: pd.DataFrame) -> go.Figure:
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
        
        return self._apply_health_theme(fig)
    
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
    
    def _create_line_chart(self, config: Dict, data: pd.DataFrame) -> go.Figure:
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
        
        return self._apply_health_theme(fig)
    
    def _create_fallback_chart(self, title: str, data: pd.DataFrame) -> go.Figure:
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
        
        return self._apply_health_theme(fig)
    
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
    
    def _apply_health_theme(self, fig: go.Figure) -> go.Figure:
        """Aplicar tema sanitario consistente"""
        
        fig.update_layout(
            # Colores del tema
            plot_bgcolor='rgba(248, 249, 250, 0.8)',
            paper_bgcolor='white',
            
            # Tipografía
            font=dict(family="Arial, sans-serif", size=12, color="#2c3e50"),
            title_font=dict(size=16, color="#00a86b", family="Arial Black"),
            
            # Márgenes y espaciado
            margin=dict(l=60, r=60, t=80, b=60),
            
            # Grid y ejes
            xaxis=dict(
                showgrid=True, 
                gridcolor='rgba(0,0,0,0.1)',
                linecolor='rgba(0,0,0,0.2)'
            ),
            yaxis=dict(
                showgrid=True, 
                gridcolor='rgba(0,0,0,0.1)',
                linecolor='rgba(0,0,0,0.2)'
            ),
            
            # Hover
            hoverlabel=dict(
                bgcolor="white",
                font_size=12,
                font_family="Arial"
            )
        )
        
        # Actualizar colores de barras si es un gráfico de barras
        if hasattr(fig.data[0], 'marker') and hasattr(fig.data[0].marker, 'color'):
            if isinstance(fig.data[0].marker.color, str):
                fig.update_traces(marker_color=self.health_colors['primary'])
        
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
        
        # Reglas basadas en el tipo de análisis
        if analysis_type == "geographic":
            if 'lat' in data.columns or 'latitud' in data.columns:
                return "map"
            else:
                return "bar"
                
        elif analysis_type == "equity":
            if numeric_cols >= 3:
                return "heatmap"
            else:
                return "bar"
                
        elif analysis_type == "demographic":
            if total_rows > 20:
                return "scatter"
            else:
                return "bar"
                
        elif analysis_type == "services":
            if categorical_cols > 0 and numeric_cols > 0:
                return "pie" if total_rows < 8 else "bar"
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
        
        # Detectar columnas por nombre/contexto
        name_patterns = {
            'geographic': ['municipio', 'distrito', 'provincia', 'zona'],
            'hospital': ['hospital', 'centro', 'nombre'],
            'population': ['poblacion', 'habitantes', 'hab'],
            'health_metrics': ['ratio', 'camas', 'personal', 'consultas'],
            'time': ['fecha', 'año', 'mes', 'tiempo']
        }
        
        # Asignar X (categórica preferiblemente)
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