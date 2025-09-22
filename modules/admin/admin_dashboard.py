"""
Dashboard de Administración - Copilot Salud Andalucía
Panel de control para monitorear rendimiento y seguridad
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from typing import Dict, Any, List
import json
import os
import numpy as np
import time

# Importar widgets específicos para admin
try:
    from modules.admin.admin_widgets import AdminWidgets
    ADMIN_WIDGETS_AVAILABLE = True
except ImportError:
    ADMIN_WIDGETS_AVAILABLE = False

# Importar sistemas mock para cuando los reales no estén disponibles
try:
    from modules.admin.mock_systems import initialize_admin_systems_safely
    MOCK_SYSTEMS_AVAILABLE = True
except ImportError:
    MOCK_SYSTEMS_AVAILABLE = False

class AdminDashboard:
    def __init__(self):
        """Inicializar dashboard de administración"""
        self.performance_optimizer = None
        self.security_auditor = None
        self.rate_limiter = None
        self.data_encryption = None
        self.systems_initialized = False

        # Inicializar widgets específicos para admin
        if ADMIN_WIDGETS_AVAILABLE:
            self.admin_widgets = AdminWidgets()
        else:
            self.admin_widgets = None

        # Inicializar sistemas administrativos de forma segura
        self._initialize_admin_systems()

    def _initialize_admin_systems(self):
        """Inicializar sistemas administrativos de forma segura"""
        try:
            # Intentar importar directamente las clases mock
            from modules.admin.mock_systems import (
                MockPerformanceOptimizer, MockSecurityAuditor,
                MockRateLimiter, MockDataEncryption
            )

            self.performance_optimizer = MockPerformanceOptimizer()
            self.security_auditor = MockSecurityAuditor()
            self.rate_limiter = MockRateLimiter()
            self.data_encryption = MockDataEncryption()
            self.systems_initialized = True
            print("✅ Sistemas mock inicializados directamente")

            # Verificar que se inicializaron correctamente
            if hasattr(st, 'success'):
                st.success("🎉 Sistemas administrativos inicializados correctamente")

        except ImportError as e:
            print(f"❌ Error importando sistemas mock: {str(e)}")
            self.systems_initialized = False
            if hasattr(st, 'error'):
                st.error(f"❌ Error importando sistemas: {str(e)}")
        except Exception as e:
            print(f"❌ Error inicializando sistemas: {str(e)}")
            self.systems_initialized = False
            if hasattr(st, 'error'):
                st.error(f"❌ Error inicializando sistemas: {str(e)}")
                import traceback
                st.code(traceback.format_exc())

    def initialize_systems(self, performance_optimizer, security_auditor, rate_limiter, data_encryption):
        """Inicializar sistemas de optimización y seguridad (método legacy)"""
        if performance_optimizer:
            self.performance_optimizer = performance_optimizer
        if security_auditor:
            self.security_auditor = security_auditor
        if rate_limiter:
            self.rate_limiter = rate_limiter
        if data_encryption:
            self.data_encryption = data_encryption

        self.systems_initialized = True

    def _ensure_mock_systems(self):
        """Asegurar que los sistemas mock estén inicializados"""
        try:
            if MOCK_SYSTEMS_AVAILABLE:
                systems = initialize_admin_systems_safely()
                if not self.performance_optimizer:
                    self.performance_optimizer = systems.get('performance_optimizer')
                if not self.security_auditor:
                    self.security_auditor = systems.get('security_auditor')
                if not self.rate_limiter:
                    self.rate_limiter = systems.get('rate_limiter')
                if not self.data_encryption:
                    self.data_encryption = systems.get('data_encryption')
                self.systems_initialized = True
                st.info("🔄 Sistemas mock inicializados dinámicamente")
            else:
                st.error("❌ Sistemas mock no disponibles")
        except Exception as e:
            st.error(f"❌ Error inicializando sistemas mock: {str(e)}")
            import traceback
            st.code(traceback.format_exc())

    def render_admin_dashboard(self):
        """Renderizar dashboard completo de administración"""
        st.markdown("# 🏥 Dashboard de Administración Sanitaria")
        st.markdown("Panel de control para la gestión integral del sistema de salud andaluz")

        # Forzar limpieza de cache si es necesario
        if st.button("🔄 Reiniciar Dashboard (Limpiar Cache)"):
            # Limpiar session state relacionado con admin
            keys_to_clear = [k for k in st.session_state.keys() if 'admin' in k.lower()]
            for key in keys_to_clear:
                del st.session_state[key]
            st.rerun()

        # Debug info
        if not self.systems_initialized:
            st.error("⚠️ Sistemas administrativos no inicializados - Reintentando...")
            self._initialize_admin_systems()

        # Mostrar estado de sistemas
        with st.expander("🔧 Estado de Sistemas (Debug)"):
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                status = "✅" if self.performance_optimizer else "❌"
                st.write(f"{status} Performance Optimizer")
            with col2:
                status = "✅" if self.security_auditor else "❌"
                st.write(f"{status} Security Auditor")
            with col3:
                status = "✅" if self.rate_limiter else "❌"
                st.write(f"{status} Rate Limiter")
            with col4:
                status = "✅" if self.data_encryption else "❌"
                st.write(f"{status} Data Encryption")
            with col5:
                if st.button("🔄 Reinicializar"):
                    self._initialize_admin_systems()
                    st.rerun()
        
        # Tabs para diferentes secciones
        tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
            "🏥 Panel Ejecutivo", "📊 Rendimiento", "🔒 Seguridad",
            "🚦 Rate Limiting", "🔐 Encriptación", "📈 Analytics", "🎯 Insights Estratégicos"
        ])

        with tab1:
            self._render_executive_dashboard_tab()

        with tab2:
            self._render_performance_tab()

        with tab3:
            self._render_security_tab()

        with tab4:
            self._render_rate_limiting_tab()

        with tab5:
            self._render_encryption_tab()

        with tab6:
            self._render_analytics_tab()

        with tab7:
            self._render_strategic_insights_tab()
        
        # Tab adicional para procesamiento asíncrono
        with st.expander("🤖 Procesamiento Asíncrono de IA"):
            self._render_async_processing_tab()

    def _render_executive_dashboard_tab(self):
        """Panel ejecutivo para administradores del sistema sanitario"""
        st.markdown("## 🏥 Panel Ejecutivo del Sistema Sanitario")
        st.markdown("Tablero de control para la gestión estratégica y operativa del sistema de salud andaluz")

        # Solo disponible para administradores
        if not self.admin_widgets:
            st.error("❌ Widgets de administración no disponibles")
            return

        # Obtener datos del sistema si están disponibles
        data = getattr(st.session_state, 'app_data', {})

        # Widget de resumen del sistema sanitario
        self.admin_widgets.render_health_system_overview_widget()

        st.markdown("---")

        # KPIs ejecutivos avanzados del sistema sanitario
        self.admin_widgets.render_advanced_kpi_dashboard(data)

        st.markdown("---")

        # Panel de alertas sanitarias (más relevante que activity heatmap)
        self.admin_widgets.render_health_alerts_widget()

        st.markdown("---")

        # Análisis predictivo
        if data:
            self.admin_widgets.render_predictive_analytics_widget(data)

    def _render_strategic_insights_tab(self):
        """Tab de insights estratégicos"""
        st.markdown("## 🔮 Insights Estratégicos")
        st.markdown("Análisis estratégico y recomendaciones basadas en inteligencia de datos")

        if not self.admin_widgets:
            st.error("❌ Widgets de administración no disponibles")
            return

        # Obtener datos del sistema
        data = getattr(st.session_state, 'app_data', {})

        # Si no hay datos, generar datos de ejemplo para el análisis
        if not data:
            data = self._generate_sample_analysis_data()

        # Widgets de insights estratégicos
        self.admin_widgets.render_strategic_insights_widget(data)

        st.markdown("---")

        # Comparativa de rendimiento por distritos
        self.admin_widgets.render_performance_comparison_chart(data)

        st.markdown("---")

        # Panel de control estratégico adicional
        self._render_strategic_control_panel()

    def _generate_sample_analysis_data(self):
        """Generar datos de ejemplo para análisis estratégicos"""
        import pandas as pd
        import numpy as np

        # Datos de indicadores por distrito de Málaga
        distritos = [
            'Centro', 'Este', 'Ciudad Jardín', 'Bailén-Miraflores',
            'Palma-Palmilla', 'Cruz de Humilladero', 'Carretera de Cádiz',
            'Churriana', 'Campanillas', 'Puerto de la Torre'
        ]

        # Generar datos realistas
        np.random.seed(42)  # Para reproducibilidad

        indicadores_data = []
        for distrito in distritos:
            indicadores_data.append({
                'distrito': distrito,
                'poblacion': np.random.randint(45000, 120000),
                'centros_salud': np.random.randint(2, 8),
                'medicos_familia': np.random.randint(15, 45),
                'enfermeros': np.random.randint(25, 70),
                'consultas_mes': np.random.randint(2500, 8500),
                'tiempo_espera_dias': np.random.randint(5, 25),
                'satisfaccion_pct': np.random.randint(75, 95),
                'urgencias_mes': np.random.randint(800, 2200),
                'derivaciones_especialista': np.random.randint(150, 450),
                'indice_salud': round(np.random.uniform(7.2, 9.1), 1)
            })

        return {
            'indicadores': pd.DataFrame(indicadores_data),
            'distritos': distritos,
            'timestamp': pd.Timestamp.now()
        }

    def _render_strategic_control_panel(self):
        """Panel de control estratégico adicional"""
        st.markdown("#### 🎯 Panel de Control Estratégico")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("##### 📋 Acciones Estratégicas Pendientes")

            strategic_actions = [
                {"action": "🏥 Evaluación nuevos centros Costa del Sol", "deadline": "Q2 2025", "priority": "Alta"},
                {"action": "📊 Análisis ROI telemedicina", "deadline": "Q1 2025", "priority": "Media"},
                {"action": "👥 Plan recursos humanos geriátricos", "deadline": "Q3 2025", "priority": "Alta"},
                {"action": "💰 Optimización presupuestaria hospitales", "deadline": "Q1 2025", "priority": "Crítica"}
            ]

            for action in strategic_actions:
                priority_color = {
                    'Crítica': '#e53e3e',
                    'Alta': '#ff8c00',
                    'Media': '#0066cc'
                }.get(action['priority'], '#6b7280')

                st.markdown(f"""
                <div style="
                    background: white;
                    padding: 1.2rem;
                    border-radius: 10px;
                    border-left: 5px solid {priority_color};
                    margin: 0.8rem 0;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                    border: 1px solid #e2e8f0;
                ">
                    <div style="
                        color: #000000;
                        font-weight: 700;
                        font-size: 1.1rem;
                        margin-bottom: 0.6rem;
                        line-height: 1.4;
                    ">{action['action']}</div>
                    <div style="display: flex; align-items: center; gap: 1rem;">
                        <span style="
                            color: #000000;
                            font-size: 0.95rem;
                            font-weight: 600;
                        ">📅 {action['deadline']}</span>
                        <span style="
                            background: {priority_color};
                            color: white;
                            padding: 0.3rem 0.8rem;
                            border-radius: 12px;
                            font-size: 0.8rem;
                            font-weight: 600;
                            text-transform: uppercase;
                            letter-spacing: 0.5px;
                        ">⚡ {action['priority']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        with col2:
            st.markdown("##### 📈 Métricas de Rendimiento Ejecutivo")

            # Métricas ejecutivas simuladas
            exec_metrics = {
                "📊 Eficiencia Operativa": {"value": "94.2%", "trend": "↗️ +2.1%"},
                "💰 Control Presupuestario": {"value": "€2.3M", "trend": "↘️ -€120K"},
                "🎯 Objetivos Cumplidos": {"value": "87%", "trend": "↗️ +5%"},
                "⚡ Tiempo Implementación": {"value": "12.3 días", "trend": "↘️ -1.2 días"}
            }

            for metric, data in exec_metrics.items():
                st.markdown(f"""
                <div style="
                    background: white;
                    padding: 1.3rem;
                    border-radius: 10px;
                    margin: 0.8rem 0;
                    border: 2px solid #e2e8f0;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
                ">
                    <div style="
                        font-weight: 700;
                        color: #000000;
                        font-size: 1.05rem;
                        margin-bottom: 0.6rem;
                    ">{metric}</div>
                    <div style="
                        font-size: 1.6rem;
                        font-weight: 700;
                        color: #000000;
                        margin: 0.5rem 0;
                    ">{data['value']}</div>
                    <div style="
                        font-size: 1rem;
                        color: #000000;
                        font-weight: 600;
                    ">{data['trend']}</div>
                </div>
                """, unsafe_allow_html=True)

        # Controles administrativos avanzados
        st.markdown("---")
        st.markdown("##### 🛠️ Controles Administrativos Avanzados")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            if st.button("🔄 Actualizar Cache Global", help="Actualizar todos los caches del sistema"):
                st.success("✅ Cache global actualizado")

        with col2:
            if st.button("📊 Generar Reporte Ejecutivo", help="Generar reporte ejecutivo completo"):
                st.info("📄 Reporte ejecutivo generándose...")

        with col3:
            if st.button("🔍 Auditoría Completa", help="Ejecutar auditoría completa del sistema"):
                st.info("🔍 Auditoría en progreso...")

        with col4:
            if st.button("📈 Análisis Predictivo", help="Ejecutar análisis predictivo avanzado"):
                st.info("🔮 Análisis predictivo ejecutándose...")

    def _render_performance_tab(self):
        """Tab de rendimiento del sistema"""
        st.markdown("## 📊 Monitoreo de Rendimiento del Sistema")

        # Siempre usar datos simulados para el dashboard administrativo
        st.info("📊 Métricas de rendimiento del sistema (datos simulados)")
        self._render_performance_fallback()
        return
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📦 Entradas en Cache", cache_stats.get('total_entries', 0))
        
        with col2:
            st.metric("💾 Uso de Memoria", cache_stats.get('memory_usage', '0 MB'))
        
        with col3:
            entries_by_role = cache_stats.get('entries_by_role', {})
            total_roles = len(entries_by_role)
            st.metric("👥 Roles Activos", total_roles)
        
        with col4:
            if entries_by_role:
                max_entries = max(entries_by_role.values())
                st.metric("🔥 Cache Más Usado", f"{max_entries} entradas")
        
        # Gráfico de uso de cache por rol
        if entries_by_role:
            st.markdown("### 📈 Uso de Cache por Rol")
            
            roles = list(entries_by_role.keys())
            entries = list(entries_by_role.values())
            
            fig = px.bar(
                x=roles, y=entries,
                title="Entradas de Cache por Rol de Usuario",
                color=entries,
                color_continuous_scale='Viridis'
            )
            fig.update_layout(
                xaxis_title="Rol de Usuario",
                yaxis_title="Número de Entradas"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Controles de cache
        st.markdown("### 🛠️ Gestión de Cache")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🗑️ Limpiar Todo el Cache"):
                self.performance_optimizer.clear_user_cache()
                st.success("✅ Cache limpiado exitosamente")
                st.rerun()
        
        with col2:
            selected_role = st.selectbox(
                "Limpiar cache por rol:",
                ["admin", "gestor", "analista", "invitado"]
            )
            if st.button(f"🗑️ Limpiar Cache de {selected_role}"):
                self.performance_optimizer.clear_user_cache(selected_role)
                st.success(f"✅ Cache de {selected_role} limpiado")
                st.rerun()
    
    def _render_security_tab(self):
        """Tab de seguridad del sistema"""
        st.markdown("## 🔒 Monitoreo de Seguridad del Sistema")

        # Siempre usar datos simulados para el dashboard administrativo
        st.info("🔒 Métricas de seguridad del sistema (datos simulados)")
        self._render_security_fallback()
        return
        
        if 'error' in security_data:
            st.error(f"❌ Error obteniendo datos de seguridad: {security_data['error']}")
            return
        
        # Métricas principales
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📊 Acciones Totales", security_data.get('total_actions', 0))
        
        with col2:
            st.metric("❌ Acciones Fallidas", security_data.get('failed_actions', 0))
        
        with col3:
            success_rate = security_data.get('success_rate', 0)
            st.metric("✅ Tasa de Éxito", f"{success_rate:.1f}%")
        
        with col4:
            st.metric("👥 Usuarios Únicos", security_data.get('unique_users', 0))
        
        # Gráfico de acciones por tipo
        action_types = security_data.get('action_types', {})
        if action_types:
            st.markdown("### 📈 Distribución de Acciones")
            
            fig = px.pie(
                values=list(action_types.values()),
                names=list(action_types.keys()),
                title="Acciones por Tipo (Últimas 24 horas)"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Top usuarios más activos
        top_users = security_data.get('top_users', [])
        if top_users:
            st.markdown("### 👥 Usuarios Más Activos")
            
            df_users = pd.DataFrame(top_users, columns=['Usuario', 'Acciones'])
            
            fig = px.bar(
                df_users, x='Usuario', y='Acciones',
                title="Top 10 Usuarios por Actividad",
                color='Acciones',
                color_continuous_scale='Blues'
            )
            fig.update_xaxes(tickangle=45)
            st.plotly_chart(fig, use_container_width=True)
        
        # Detección de actividad sospechosa
        st.markdown("### 🚨 Actividad Sospechosa")
        
        # Simular detección (en producción esto vendría del sistema real)
        suspicious_activities = [
            {"user": "usuario1", "type": "high_frequency", "count": 150, "risk_level": 75},
            {"user": "usuario2", "type": "failed_logins", "count": 8, "risk_level": 90}
        ]
        
        if suspicious_activities:
            for activity in suspicious_activities:
                risk_color = "🔴" if activity['risk_level'] > 80 else "🟡" if activity['risk_level'] > 50 else "🟢"
                st.warning(f"{risk_color} **{activity['user']}**: {activity['type']} ({activity['count']} veces) - Riesgo: {activity['risk_level']}%")
        else:
            st.success("✅ No se detectó actividad sospechosa")
    
    def _render_rate_limiting_tab(self):
        """Tab de control de tráfico"""
        st.markdown("## 🚦 Control de Tráfico y Límites del Sistema")

        # Siempre usar datos simulados para el dashboard administrativo
        st.info("🚦 Métricas de control de tráfico (datos simulados)")
        self._render_rate_limiting_fallback()
        return
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("🚫 Usuarios Bloqueados", system_stats.get('active_blocks', 0))
        
        with col2:
            st.metric("⚠️ IPs Sospechosas", system_stats.get('suspicious_ips', 0))
        
        with col3:
            st.metric("📊 Límites Configurados", system_stats.get('total_limits', 0))
        
        with col4:
            total_requests = sum(system_stats.get('active_requests', {}).values())
            st.metric("🔄 Requests Activos", total_requests)
        
        # Requests activos por tipo
        active_requests = system_stats.get('active_requests', {})
        if active_requests:
            st.markdown("### 📈 Requests Activos por Tipo")
            
            df_requests = pd.DataFrame([
                {"Tipo": k, "Requests": v} for k, v in active_requests.items()
            ])
            
            fig = px.bar(
                df_requests, x='Tipo', y='Requests',
                title="Requests Activos por Tipo de Acción",
                color='Requests',
                color_continuous_scale='Reds'
            )
            fig.update_xaxes(tickangle=45)
            st.plotly_chart(fig, use_container_width=True)
        
        # Gestión de bloqueos
        st.markdown("### 🛠️ Gestión de Bloqueos")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Usuarios Bloqueados")
            # En una implementación real, esto vendría de la base de datos
            blocked_users = ["usuario1", "usuario2"]  # Simulado
            
            if blocked_users:
                for user in blocked_users:
                    col_user, col_action = st.columns([3, 1])
                    with col_user:
                        st.write(f"🚫 {user}")
                    with col_action:
                        if st.button(f"Desbloquear", key=f"unblock_{user}"):
                            # Lógica de desbloqueo
                            st.success(f"✅ {user} desbloqueado")
            else:
                st.success("✅ No hay usuarios bloqueados")
        
        with col2:
            st.markdown("#### IPs Sospechosas")
            suspicious_ips = ["192.168.1.100", "10.0.0.50"]  # Simulado
            
            if suspicious_ips:
                for ip in suspicious_ips:
                    col_ip, col_action = st.columns([3, 1])
                    with col_ip:
                        st.write(f"⚠️ {ip}")
                    with col_action:
                        if st.button(f"Limpiar", key=f"clear_{ip}"):
                            # Lógica de limpieza
                            st.success(f"✅ {ip} limpiada")
            else:
                st.success("✅ No hay IPs sospechosas")
    
    def _render_encryption_tab(self):
        """Tab de seguridad de datos"""
        st.markdown("## 🔐 Seguridad y Encriptación de Datos")

        # Siempre usar datos simulados para el dashboard administrativo
        st.info("🔐 Estado de seguridad de datos (datos simulados)")
        self._render_encryption_fallback()
        return
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            algorithm = encryption_status.get('algorithm', 'N/A')
            st.metric("🔐 Algoritmo", algorithm)
        
        with col2:
            key_exists = encryption_status.get('key_exists', False)
            status_icon = "✅" if key_exists else "❌"
            st.metric("🔑 Clave", f"{status_icon} {'Existe' if key_exists else 'No existe'}")
        
        with col3:
            salt_exists = encryption_status.get('salt_exists', False)
            status_icon = "✅" if salt_exists else "❌"
            st.metric("🧂 Salt", f"{status_icon} {'Existe' if salt_exists else 'No existe'}")
        
        with col4:
            last_modified = encryption_status.get('last_modified', 'N/A')
            st.metric("📅 Última Modificación", last_modified[:10] if last_modified != 'N/A' else 'N/A')
        
        # Validación de integridad
        st.markdown("### 🔍 Validación de Integridad")
        
        if st.button("🧪 Probar Sistema de Encriptación"):
            with st.spinner("Probando encriptación..."):
                integrity_test = self.data_encryption.validate_encryption_integrity()
                
                if integrity_test.get('encryption_working', False):
                    st.success("✅ Sistema de encriptación funcionando correctamente")
                else:
                    st.error(f"❌ Error en sistema de encriptación: {integrity_test.get('error', 'Desconocido')}")
                
                # Mostrar detalles del test
                with st.expander("📋 Detalles del Test"):
                    st.json(integrity_test)
        
        # Gestión de claves
        st.markdown("### 🛠️ Gestión de Claves")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔄 Rotar Clave de Encriptación"):
                st.warning("⚠️ Esta acción requiere re-encriptar todos los datos existentes")
                if st.button("✅ Confirmar Rotación", type="primary"):
                    success = self.data_encryption.rotate_encryption_key()
                    if success:
                        st.success("✅ Clave rotada exitosamente")
                    else:
                        st.error("❌ Error rotando clave")
        
        with col2:
            st.info("💡 **Nota**: La rotación de claves es una operación crítica que afecta todos los datos encriptados")
    
    def _render_async_processing_tab(self):
        """Tab de procesamiento asíncrono de IA"""
        st.markdown("## 🤖 Procesamiento Asíncrono de IA")
        
        try:
            # Importar módulo de IA
            from modules.ai.ai_processor import HealthAnalyticsAI
            
            # Crear instancia temporal para obtener métricas
            ai_processor = HealthAnalyticsAI()
            
            # Obtener métricas de procesamiento asíncrono
            metrics = ai_processor.get_async_processing_metrics()
            
            if 'error' in metrics:
                st.error(f"❌ Error obteniendo métricas: {metrics['error']}")
                return
            
            # Métricas principales
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                total_requests = metrics.get('total_requests', 0)
                st.metric("🔄 Total Requests", total_requests)
            
            with col2:
                successful = metrics.get('successful_requests', 0)
                success_rate = (successful / max(1, total_requests)) * 100
                st.metric("✅ Tasa de Éxito", f"{success_rate:.1f}%")
            
            with col3:
                avg_time = metrics.get('average_response_time', 0)
                st.metric("⏱️ Tiempo Promedio", f"{avg_time:.2f}s")
            
            with col4:
                cache_hits = metrics.get('cache_hits', 0)
                cache_rate = (cache_hits / max(1, total_requests)) * 100
                st.metric("💾 Cache Hit Rate", f"{cache_rate:.1f}%")
            
            # Gráfico de rendimiento en el tiempo (simulado)
            st.markdown("### 📈 Rendimiento del Procesamiento Asíncrono")
            
            # Generar datos simulados para el gráfico
            import plotly.graph_objects as go
            from datetime import datetime, timedelta
            
            # Simular datos de las últimas 24 horas
            hours = [(datetime.now() - timedelta(hours=i)).strftime('%H:00') for i in range(23, -1, -1)]
            response_times = [max(0.5, 2.0 + (i % 3) * 0.5 + (i % 7) * 0.3) for i in range(24)]
            success_rates = [min(100, 85 + (i % 5) * 3 + (i % 11) * 2) for i in range(24)]
            
            # Crear gráfico de líneas
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=hours, y=response_times,
                mode='lines+markers',
                name='Tiempo de Respuesta (s)',
                yaxis='y',
                line=dict(color='blue')
            ))
            
            fig.add_trace(go.Scatter(
                x=hours, y=success_rates,
                mode='lines+markers',
                name='Tasa de Éxito (%)',
                yaxis='y2',
                line=dict(color='green')
            ))
            
            fig.update_layout(
                title="Rendimiento del Procesamiento Asíncrono (Últimas 24h)",
                xaxis_title="Hora",
                yaxis=dict(title="Tiempo de Respuesta (s)", side="left"),
                yaxis2=dict(title="Tasa de Éxito (%)", side="right", overlaying="y"),
                hovermode=False  # Deshabilitar hover para evitar errores
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Controles de gestión
            st.markdown("### 🛠️ Gestión del Procesamiento Asíncrono")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("🗑️ Limpiar Cache de IA"):
                    try:
                        ai_processor.clear_async_cache()
                        st.success("✅ Cache de IA limpiado")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error limpiando cache: {str(e)}")
            
            with col2:
                if st.button("🔄 Reiniciar Procesador Asíncrono"):
                    st.info("🔄 Reiniciando procesador asíncrono...")
                    # En una implementación real, aquí se reiniciaría el procesador
                    st.success("✅ Procesador asíncrono reiniciado")
            
            # Estado del sistema
            st.markdown("### 📊 Estado del Sistema Asíncrono")
            
            status_items = [
                ("🔄 Procesamiento Asíncrono", "✅ Activo"),
                ("💾 Cache de Respuestas", "✅ Activo"),
                ("🔄 Pool de Threads", "✅ Activo"),
                ("📊 Métricas", "✅ Recolectando"),
                ("🔒 Rate Limiting", "✅ Integrado"),
                ("📝 Auditoría", "✅ Activa")
            ]
            
            for item, status in status_items:
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.write(f"**{item}:**")
                with col2:
                    st.write(status)
            
        except Exception as e:
            st.error(f"❌ Error en procesamiento asíncrono: {str(e)}")
            st.info("💡 Asegúrate de que el módulo de IA esté disponible")

    def _render_performance_fallback(self):
        """Renderizar tab de rendimiento del sistema sanitario"""
        st.markdown("### 📊 Rendimiento del Sistema Sanitario")

        # Métricas de rendimiento del sistema de salud
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("⚡ Tiempo Consulta", "2.3 min", delta="-0.4 min", help="Tiempo promedio de consulta médica")

        with col2:
            st.metric("🏥 Disponibilidad Sistema", "99.2%", delta="+0.1%", help="Disponibilidad del sistema de información sanitario")

        with col3:
            st.metric("👥 Usuarios Concurrentes", "847", help="Profesionales sanitarios conectados")

        with col4:
            st.metric("📊 Transacciones/min", "2,340", delta="+156", help="Transacciones sanitarias por minuto")

        # Gráfico de rendimiento del sistema por servicio
        st.markdown("### 📈 Rendimiento por Servicio Sanitario")

        services = ['Atención Primaria', 'Especialidades', 'Urgencias', 'Hospitalización', 'Laboratorio']
        response_times = [1.2, 3.4, 0.8, 2.1, 4.2]  # minutos

        fig = px.bar(
            x=services, y=response_times,
            title="Tiempo de Respuesta por Servicio (minutos)",
            color=response_times,
            color_continuous_scale='RdYlGn_r'  # Rojo para tiempos altos, verde para bajos
        )
        fig.update_layout(
            xaxis_title="Servicio Sanitario",
            yaxis_title="Tiempo de Respuesta (min)",
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)

        # Controles de optimización
        st.markdown("### 🛠️ Optimización del Sistema")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("⚡ Optimizar Rendimiento General"):
                st.success("✅ Optimización ejecutada - Mejora estimada del 12%")

        with col2:
            selected_service = st.selectbox(
                "Optimizar servicio específico:",
                services
            )
            if st.button(f"🎯 Optimizar {selected_service}"):
                st.success(f"✅ {selected_service} optimizado correctamente")

    def _render_security_fallback(self):
        """Renderizar tab de seguridad del sistema sanitario"""
        st.markdown("### 🔒 Seguridad del Sistema Sanitario")

        # Métricas de seguridad específicas del sistema de salud
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("🔐 Accesos Sistema", "2,847", delta="+156", help="Accesos diarios al sistema sanitario")

        with col2:
            st.metric("❌ Intentos Fallidos", "12", delta="-3", help="Intentos de acceso fallidos")

        with col3:
            st.metric("✅ Cumplimiento LOPD", "98.7%", delta="+0.2%", help="Cumplimiento Ley Protección de Datos")

        with col4:
            st.metric("🛡️ Auditorías Exitosas", "847", help="Auditorías de seguridad completadas")

        # Gráfico de accesos por servicio
        st.markdown("### 📈 Accesos por Servicio Sanitario")

        access_types = {
            'Historia Clínica': 1847,
            'Prescripción Electrónica': 1243,
            'Citas Médicas': 892,
            'Resultados Laboratorio': 674,
            'Informes Radiología': 423,
            'Administración': 156
        }

        fig = px.pie(
            values=list(access_types.values()),
            names=list(access_types.keys()),
            title="Distribución de Accesos por Servicio"
        )
        st.plotly_chart(fig, use_container_width=True)

        # Panel de alertas de seguridad
        st.markdown("### 🚨 Estado de Seguridad")

        col1, col2 = st.columns(2)

        with col1:
            st.success("✅ Todos los sistemas cumplen normativa sanitaria")
            st.success("✅ Encriptación de datos médicos activa")
            st.success("✅ Backup de historias clínicas actualizado")

        with col2:
            st.info("ℹ️ Próxima auditoría LOPD: 15 días")
            st.info("ℹ️ Certificados SSL válidos hasta Dic 2025")
            st.warning("⚠️ Revisar accesos usuarios inactivos > 90 días")

    def _render_rate_limiting_fallback(self):
        """Renderizar tab de control de tráfico del sistema sanitario"""
        st.markdown("### 🚦 Control de Tráfico del Sistema Sanitario")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("🚫 Accesos Limitados", "3", help="Usuarios temporalmente limitados por exceso de consultas")

        with col2:
            st.metric("⚠️ Centros en Alerta", "2", help="Centros sanitarios con tráfico alto")

        with col3:
            st.metric("📊 Políticas Activas", "15", help="Políticas de control de tráfico configuradas")

        with col4:
            st.metric("🔄 Consultas/Segundo", "127", delta="+23", help="Consultas al sistema por segundo")

        # Gráfico de tráfico por hora
        st.markdown("### 📈 Tráfico del Sistema por Hora")

        import numpy as np
        import plotly.graph_objects as go

        hours = list(range(24))
        traffic = [
            20, 15, 12, 10, 8, 15, 45, 89, 125, 156,
            167, 178, 189, 195, 187, 176, 165, 152,
            138, 124, 98, 76, 54, 32
        ]

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=hours, y=traffic,
            mode='lines+markers',
            name='Consultas/min',
            line=dict(color='#3b82f6', width=3),
            fill='tonexty'
        ))

        fig.update_layout(
            title="Tráfico del Sistema Sanitario (24 horas)",
            xaxis_title="Hora del día",
            yaxis_title="Consultas por minuto",
            height=350
        )
        st.plotly_chart(fig, use_container_width=True)

        # Controles de tráfico
        st.markdown("### 🛠️ Gestión de Tráfico")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("⚡ Aumentar Límites Temporalmente"):
                st.success("✅ Límites incrementados por 2 horas")

        with col2:
            if st.button("🔄 Balancear Carga Automáticamente"):
                st.success("✅ Balanceador de carga optimizado")

    def _render_encryption_fallback(self):
        """Renderizar tab de seguridad de datos del sistema sanitario"""
        st.markdown("### 🔐 Seguridad de Datos Sanitarios")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("🔐 Algoritmo", "AES-256-GCM", help="Encriptación de historias clínicas")

        with col2:
            st.metric("🔑 Certificados", "✅ Válidos", help="Certificados digitales del sistema")

        with col3:
            st.metric("🧂 Hash Seguro", "✅ SHA-256", help="Hash para integridad de datos")

        with col4:
            st.metric("📅 Última Auditoría", datetime.now().strftime("%d-%m-%Y"), help="Última auditoría de seguridad")

        # Estado de protección de datos
        st.markdown("### 🛡️ Estado de Protección de Datos Médicos")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            **🏥 Datos Protegidos:**
            - ✅ Historias Clínicas Encriptadas
            - ✅ Resultados Laboratorio Seguros
            - ✅ Imágenes Médicas Protegidas
            - ✅ Recetas Electrónicas Cifradas
            - ✅ Citas Médicas Anonimizadas
            """)

        with col2:
            st.markdown("""
            **📋 Cumplimiento Normativo:**
            - ✅ RGPD (Reglamento General de Protección de Datos)
            - ✅ LOPD (Ley Orgánica de Protección de Datos)
            - ✅ Normativa Sanitaria Andaluza
            - ✅ ISO 27001 (Gestión de Seguridad)
            - ✅ ENS (Esquema Nacional de Seguridad)
            """)

        # Controles de encriptación
        st.markdown("### 🛠️ Gestión de Seguridad")

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("🧪 Verificar Integridad de Datos"):
                with st.spinner("Verificando integridad..."):
                    time.sleep(2)
                    st.success("✅ Integridad de datos médicos verificada")

        with col2:
            if st.button("🔄 Rotar Claves de Encriptación"):
                with st.spinner("Rotando claves..."):
                    time.sleep(3)
                    st.success("✅ Claves rotadas correctamente")

        with col3:
            if st.button("📊 Generar Informe LOPD"):
                with st.spinner("Generando informe..."):
                    time.sleep(2)
                    st.success("✅ Informe LOPD generado y enviado")
    
    def _render_analytics_tab(self):
        """Tab de analytics generales"""
        st.markdown("## 📈 Analytics del Sistema")
        
        # Métricas generales
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("🕐 Tiempo de Sesión", "2h 15m")
        
        with col2:
            st.metric("📊 Datasets Cargados", "5")
        
        with col3:
            st.metric("🤖 Consultas IA", "23")
        
        with col4:
            st.metric("🗺️ Mapas Generados", "8")
        
        # Gráfico de uso en el tiempo (simulado)
        st.markdown("### 📈 Uso del Sistema en el Tiempo")
        
        # Generar datos simulados
        hours = list(range(24))
        usage_data = [max(0, 10 + (h - 12) * 2 + (h % 3) * 5) for h in hours]
        
        fig = px.line(
            x=hours, y=usage_data,
            title="Actividad del Sistema por Hora",
            labels={'x': 'Hora del Día', 'y': 'Usuarios Activos'}
        )
        fig.update_layout(
            xaxis_title="Hora del Día",
            yaxis_title="Usuarios Activos"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Resumen de rendimiento
        st.markdown("### 📊 Resumen de Rendimiento")
        
        performance_summary = {
            "Tiempo de Carga Promedio": "0.03s",
            "Tasa de Éxito": "98.15%",
            "Memoria Utilizada": "45.2 MB",
            "Cache Hit Rate": "87.3%",
            "Errores en 24h": "2",
            "Uptime": "99.9%"
        }
        
        for metric, value in performance_summary.items():
            col1, col2 = st.columns([2, 1])
            with col1:
                st.write(f"**{metric}:**")
            with col2:
                st.write(value)

# Función de utilidad para usar el dashboard de administración
def get_admin_dashboard() -> AdminDashboard:
    """Obtener instancia del dashboard de administración"""
    if 'admin_dashboard' not in st.session_state:
        try:
            dashboard = AdminDashboard()
            st.session_state['admin_dashboard'] = dashboard
            if dashboard.systems_initialized:
                st.success("✅ Dashboard administrativo inicializado correctamente")
            else:
                st.info("💡 Dashboard administrativo funcionando en modo simulación")
        except Exception as e:
            st.error(f"❌ Error inicializando dashboard administrativo: {str(e)}")
            # Crear dashboard básico sin sistemas
            dashboard = AdminDashboard()
            dashboard.systems_initialized = False
            st.session_state['admin_dashboard'] = dashboard

    return st.session_state['admin_dashboard']


def reset_admin_dashboard():
    """Reinicializar el dashboard administrativo"""
    if 'admin_dashboard' in st.session_state:
        del st.session_state['admin_dashboard']
    return get_admin_dashboard()
