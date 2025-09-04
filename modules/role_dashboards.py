import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import Dict, List

class RoleDashboards:
    """Dashboards personalizados por rol del usuario"""
    
    def __init__(self):
        self.role_configs = {
            'admin': {
                'layout': 'comprehensive',
                'priority_metrics': ['system_overview', 'user_activity', 'performance', 'security'],
                'chart_types': ['executive_summary', 'strategic_kpis', 'trend_analysis'],
                'colors': ['#1a365d', '#2d3748', '#e53e3e']
            },
            'gestor': {
                'layout': 'management',
                'priority_metrics': ['operational_efficiency', 'capacity_usage', 'access_times'],
                'chart_types': ['operational_metrics', 'capacity_charts', 'service_coverage'],
                'colors': ['#2b6cb0', '#3182ce', '#4299e1']
            },
            'analista': {
                'layout': 'data_focused',
                'priority_metrics': ['data_quality', 'statistical_insights', 'correlations'],
                'chart_types': ['statistical_analysis', 'demographic_trends', 'correlation_matrices'],
                'colors': ['#059669', '#10b981', '#34d399']
            },
            'invitado': {
                'layout': 'basic',
                'priority_metrics': ['basic_info', 'public_data'],
                'chart_types': ['basic_overview', 'simple_charts'],
                'colors': ['#6b7280', '#9ca3af', '#d1d5db']
            }
        }
    
    def render_personalized_dashboard(self, role: str, data: Dict, role_info: Dict):
        """Renderizar dashboard personalizado según el rol"""
        
        config = self.role_configs.get(role, self.role_configs['invitado'])
        theme = role_info.get('theme', {})
        
        # Header personalizado del dashboard
        st.markdown(f"""
        <div style="background: {theme.get('primary_gradient', 'linear-gradient(135deg, #6b7280, #9ca3af)')}; 
                    padding: 1.5rem; border-radius: 12px; margin-bottom: 2rem; color: white;">
            <h2 style="color: white; margin: 0;">
                {role_info['icon']} Dashboard {role_info['name']}
            </h2>
            <p style="color: rgba(255,255,255,0.8); margin: 0.5rem 0 0 0;">
                {theme.get('welcome_message', 'Dashboard personalizado')}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Renderizar según el layout del rol
        if config['layout'] == 'comprehensive':
            self.render_executive_dashboard(data, config, theme)
        elif config['layout'] == 'management':
            self.render_management_dashboard(data, config, theme)
        elif config['layout'] == 'data_focused':
            self.render_analytical_dashboard(data, config, theme)
        else:
            self.render_basic_dashboard(data, config, theme)
    
    def render_executive_dashboard(self, data: Dict, config: Dict, theme: Dict):
        """Dashboard ejecutivo completo"""
        
        # KPIs principales en la parte superior
        st.markdown("### 📊 KPIs Ejecutivos")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_hospitals = len(data['hospitales'])
            st.metric(
                "🏥 Centros Sanitarios",
                total_hospitals,
                delta=f"+{int(total_hospitals * 0.02)} este año"
            )
        
        with col2:
            total_population = data['demografia']['poblacion_2025'].sum()
            st.metric(
                "👥 Población Total",
                f"{total_population/1000:.0f}K",
                delta=f"+{data['demografia']['crecimiento_2024_2025'].sum():,}"
            )
        
        with col3:
            total_beds = data['hospitales']['camas_funcionamiento_2025'].sum()
            bed_ratio = (total_beds / total_population) * 1000
            st.metric(
                "🛏️ Ratio Camas/1000hab",
                f"{bed_ratio:.1f}",
                delta="Dentro del estándar" if bed_ratio >= 3.0 else "Por debajo del estándar"
            )
        
        with col4:
            if 'accesibilidad' in data:
                avg_access = data['accesibilidad']['tiempo_coche_minutos'].mean()
                st.metric(
                    "⏱️ Tiempo Acceso Promedio",
                    f"{avg_access:.0f} min",
                    delta="Bueno" if avg_access <= 45 else "Mejorable"
                )
        
        # Gráficos estratégicos
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🏥 Distribución de Centros por Tipo")
            hospital_types = data['hospitales']['tipo_centro'].value_counts()
            fig_pie = px.pie(
                values=hospital_types.values,
                names=hospital_types.index,
                color_discrete_sequence=config['colors']
            )
            fig_pie.update_layout(height=300)
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            st.markdown("#### 📈 Crecimiento Poblacional por Municipio")
            top_growth = data['demografia'].nlargest(10, 'crecimiento_2024_2025')
            fig_bar = px.bar(
                top_growth,
                x='municipio',
                y='crecimiento_2024_2025',
                color='crecimiento_2024_2025',
                color_continuous_scale=['#1a365d', '#2d3748', '#e53e3e']
            )
            fig_bar.update_xaxes(tickangle=45)
            fig_bar.update_layout(height=300)
            st.plotly_chart(fig_bar, use_container_width=True)
        
        # Tabla resumen ejecutivo
        st.markdown("#### 📋 Resumen Ejecutivo por Distrito")
        if 'indicadores' in data:
            executive_summary = data['indicadores'][['distrito_sanitario', 'poblacion_total_2025', 
                                                   'ratio_medico_1000_hab', 'esperanza_vida_2023']].copy()
            executive_summary.columns = ['Distrito', 'Población 2025', 'Ratio Médicos/1000', 'Esperanza de Vida']
            st.dataframe(executive_summary, use_container_width=True)
    
    def render_management_dashboard(self, data: Dict, config: Dict, theme: Dict):
        """Dashboard de gestión operativa"""
        
        st.markdown("### ⚙️ Panel de Gestión Operativa")
        
        # Métricas operativas
        col1, col2, col3 = st.columns(3)
        
        with col1:
            total_capacity = data['hospitales']['camas_funcionamiento_2025'].sum()
            st.metric("🛏️ Capacidad Total", f"{total_capacity:,} camas")
        
        with col2:
            if 'servicios' in data:
                urgent_centers = data['servicios']['urgencias_generales'].sum()
                st.metric("🚨 Centros con Urgencias", urgent_centers)
        
        with col3:
            if 'accesibilidad' in data:
                routes_over_60 = len(data['accesibilidad'][data['accesibilidad']['tiempo_coche_minutos'] > 60])
                st.metric("⚠️ Rutas >60min", routes_over_60)
        
        # Gráficos operativos
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🏥 Capacidad por Hospital")
            capacity_data = data['hospitales'].nlargest(10, 'camas_funcionamiento_2025')
            fig_capacity = px.bar(
                capacity_data,
                x='nombre',
                y='camas_funcionamiento_2025',
                color='tipo_centro',
                color_discrete_sequence=config['colors']
            )
            fig_capacity.update_xaxes(tickangle=45)
            fig_capacity.update_layout(height=400)
            st.plotly_chart(fig_capacity, use_container_width=True)
        
        with col2:
            if 'accesibilidad' in data:
                st.markdown("#### ⏱️ Distribución de Tiempos de Acceso")
                fig_hist = px.histogram(
                    data['accesibilidad'],
                    x='tiempo_coche_minutos',
                    nbins=20,
                    color_discrete_sequence=[config['colors'][0]]
                )
                fig_hist.update_layout(height=400)
                st.plotly_chart(fig_hist, use_container_width=True)
    
    def render_analytical_dashboard(self, data: Dict, config: Dict, theme: Dict):
        """Dashboard analítico con foco en datos"""
        
        st.markdown("### 📊 Laboratorio de Análisis de Datos")
        
        # Métricas analíticas
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            datasets_count = len([k for k in data.keys() if isinstance(data[k], pd.DataFrame)])
            st.metric("📁 Datasets", datasets_count)
        
        with col2:
            total_records = sum(len(df) for df in data.values() if isinstance(df, pd.DataFrame))
            st.metric("📊 Total Registros", f"{total_records:,}")
        
        with col3:
            if 'indicadores' in data:
                avg_life_exp = data['indicadores']['esperanza_vida_2023'].mean()
                st.metric("📈 Esperanza Vida Media", f"{avg_life_exp:.1f} años")
        
        with col4:
            if 'demografia' in data:
                growth_variance = data['demografia']['crecimiento_2024_2025'].std()
                st.metric("📏 Varianza Crecimiento", f"{growth_variance:.0f}")
        
        # Análisis correlacional
        st.markdown("#### 🔗 Matriz de Correlaciones")
        if 'indicadores' in data:
            numeric_cols = data['indicadores'].select_dtypes(include=['float64', 'int64']).columns
            if len(numeric_cols) > 1:
                corr_matrix = data['indicadores'][numeric_cols].corr()
                fig_heatmap = px.imshow(
                    corr_matrix,
                    color_continuous_scale='RdBu',
                    aspect='auto'
                )
                fig_heatmap.update_layout(height=500)
                st.plotly_chart(fig_heatmap, use_container_width=True)
        
        # Análisis demográfico detallado
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 👥 Análisis Demográfico")
            demo_analysis = data['demografia'].copy()
            fig_scatter = px.scatter(
                demo_analysis,
                x='poblacion_2025',
                y='crecimiento_2024_2025',
                size='densidad_hab_km2_2025',
                hover_name='municipio',
                color='indice_envejecimiento_2025',
                color_continuous_scale=config['colors']
            )
            fig_scatter.update_layout(height=400)
            st.plotly_chart(fig_scatter, use_container_width=True)
        
        with col2:
            st.markdown("#### 📊 Distribución de Indicadores")
            if 'indicadores' in data:
                fig_box = px.box(
                    data['indicadores'],
                    y='ratio_medico_1000_hab',
                    color_discrete_sequence=[config['colors'][0]]
                )
                fig_box.update_layout(height=400)
                st.plotly_chart(fig_box, use_container_width=True)
    
    def render_basic_dashboard(self, data: Dict, config: Dict, theme: Dict):
        """Dashboard básico para usuarios invitados"""
        
        st.markdown("### 👁️ Información Pública del Sistema Sanitario")
        
        # Información básica
        col1, col2, col3 = st.columns(3)
        
        with col1:
            public_hospitals = len(data['hospitales'][data['hospitales']['tipo_centro'].isin(['Hospital Regional', 'Hospital Universitario'])])
            st.metric("🏥 Hospitales Principales", public_hospitals)
        
        with col2:
            total_population = data['demografia']['poblacion_2025'].sum() if 'demografia' in data else 0
            st.metric("👥 Población Málaga", f"{total_population/1000:.0f}K")
        
        with col3:
            municipalities = len(data['demografia']) if 'demografia' in data else 0
            st.metric("🏘️ Municipios", municipalities)
        
        # Gráfico simple
        st.markdown("#### 🏥 Centros Sanitarios por Tipo")
        hospital_types = data['hospitales']['tipo_centro'].value_counts()
        fig_simple = px.bar(
            x=hospital_types.index,
            y=hospital_types.values,
            color_discrete_sequence=[config['colors'][0]]
        )
        fig_simple.update_layout(
            xaxis_title="Tipo de Centro",
            yaxis_title="Cantidad",
            height=300
        )
        st.plotly_chart(fig_simple, use_container_width=True)
        
        # Información adicional
        st.info("ℹ️ Para acceder a análisis más detallados, solicita permisos de analista o superior.")
