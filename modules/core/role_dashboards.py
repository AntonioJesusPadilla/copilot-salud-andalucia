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
        <div class="dashboard-header-dark" style="background: {theme.get('primary_gradient', 'linear-gradient(135deg, #6b7280, #9ca3af)')};
                    padding: 1.5rem; border-radius: 12px; margin-bottom: 2rem; color: white;">
            <h2 class="dashboard-title-white" style="color: white !important; margin: 0; text-shadow: 0 2px 4px rgba(0,0,0,0.3);">
                {role_info['icon']} Dashboard {role_info['name']}
            </h2>
            <p class="dashboard-subtitle-white" style="color: rgba(255,255,255,0.95) !important; margin: 0.5rem 0 0 0; text-shadow: 0 1px 3px rgba(0,0,0,0.2);">
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

        # Dashboard especial para administradores con widgets avanzados
        try:
            from modules.admin.admin_dashboard import get_admin_dashboard
            admin_dashboard = get_admin_dashboard()

            # Mostrar botón para acceder al dashboard administrativo completo
            if st.button("🛠️ Acceder a Dashboard Administrativo Completo",
                        type="primary"):
                st.session_state.show_admin_dashboard = True

            # Si se solicita mostrar el dashboard administrativo
            if st.session_state.get('show_admin_dashboard', False):
                st.markdown("---")
                admin_dashboard.render_admin_dashboard()

                if st.button("⬅️ Volver al Dashboard Ejecutivo"):
                    st.session_state.show_admin_dashboard = False
                    st.rerun()
                return

        except ImportError:
            pass

        # KPIs principales en la parte superior
        st.markdown("### 📊 KPIs Ejecutivos Mejorados")
        
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

        # Sección adicional: KPIs de Rendimiento Administrativo
        st.markdown("---")
        st.markdown("### 🎛️ KPIs de Gestión Administrativa")

        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            import numpy as np
            admin_efficiency = 94.2 + np.random.normal(0, 2)
            st.metric(
                "⚡ Eficiencia Admin",
                f"{admin_efficiency:.1f}%",
                delta=f"{np.random.normal(0, 1.5):.1f}%",
                help="Eficiencia en procesos administrativos"
            )

        with col2:
            digital_adoption = 87.6 + np.random.normal(0, 3)
            st.metric(
                "📱 Adopción Digital",
                f"{digital_adoption:.1f}%",
                delta=f"{np.random.normal(0, 2):.1f}%",
                help="Porcentaje de procesos digitalizados"
            )

        with col3:
            cost_control = 2.34 + np.random.normal(0, 0.1)
            st.metric(
                "💰 Control Costes",
                f"€{cost_control:.2f}M",
                delta=f"€{np.random.normal(0, 0.05):.2f}M",
                help="Desviación presupuestaria"
            )

        with col4:
            response_time = 2.8 + np.random.normal(0, 0.3)
            st.metric(
                "⏱️ Tiempo Respuesta",
                f"{response_time:.1f}h",
                delta=f"{np.random.normal(0, 0.2):.1f}h",
                help="Tiempo promedio de respuesta administrativa"
            )

        with col5:
            compliance_score = 96.8 + np.random.normal(0, 1)
            st.metric(
                "✅ Cumplimiento",
                f"{compliance_score:.1f}%",
                delta=f"{np.random.normal(0, 0.5):.1f}%",
                help="Cumplimiento normativo y regulatorio"
            )

        # Gráfico de tendencias administrativas
        st.markdown("#### 📈 Tendencias de Gestión (Último Trimestre)")

        import plotly.graph_objects as go
        from datetime import datetime, timedelta

        # Generar datos de tendencias para los últimos 3 meses
        months = [(datetime.now() - timedelta(days=30*i)).strftime('%b %Y') for i in range(3, 0, -1)]

        efficiency_trend = [92.1, 93.5, 94.2]
        digital_trend = [83.2, 85.8, 87.6]
        compliance_trend = [95.1, 96.0, 96.8]

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=months, y=efficiency_trend,
            mode='lines+markers',
            name='Eficiencia Administrativa',
            line=dict(color='#1a365d', width=3),
            marker=dict(size=8)
        ))

        fig.add_trace(go.Scatter(
            x=months, y=digital_trend,
            mode='lines+markers',
            name='Adopción Digital',
            line=dict(color='#2b6cb0', width=3),
            marker=dict(size=8)
        ))

        fig.add_trace(go.Scatter(
            x=months, y=compliance_trend,
            mode='lines+markers',
            name='Cumplimiento Normativo',
            line=dict(color='#059669', width=3),
            marker=dict(size=8)
        ))

        fig.update_layout(
            title="Evolución de Indicadores Administrativos",
            xaxis_title="Mes",
            yaxis_title="Porcentaje (%)",
            height=350,
            showlegend=True,
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01
            )
        )

        st.plotly_chart(fig, use_container_width=True)

        # Panel de alertas administrativas
        st.markdown("#### 🚨 Alertas y Notificaciones Administrativas")

        alerts = [
            {"type": "warning", "icon": "⚠️", "message": "Presupuesto Q1 al 87% - Revisar asignaciones", "priority": "Media"},
            {"type": "success", "icon": "✅", "message": "Auditoría externa completada - Sin observaciones", "priority": "Info"},
            {"type": "critical", "icon": "🔴", "message": "Actualización de seguridad pendiente en 3 sistemas", "priority": "Alta"},
            {"type": "info", "icon": "💡", "message": "Nueva regulación UE aplicable a partir del próximo mes", "priority": "Media"}
        ]

        for alert in alerts:
            alert_color = {
                "critical": "#e53e3e",
                "warning": "#ff8c00",
                "success": "#00a86b",
                "info": "#0066cc"
            }.get(alert["type"], "#6b7280")

            st.markdown(f"""
            <div class="alert-card alert-{alert['type']}" style="border-left-color: {alert_color};">
                <div class="alert-content">
                    <span class="alert-icon">{alert['icon']}</span>
                    <div class="alert-message-container">
                        <div class="alert-message">{alert['message']}</div>
                    </div>
                    <span class="alert-priority" style="background: {alert_color};">{alert['priority']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
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
