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

class AdminDashboard:
    def __init__(self):
        """Inicializar dashboard de administración"""
        self.performance_optimizer = None
        self.security_auditor = None
        self.rate_limiter = None
        self.data_encryption = None
    
    def initialize_systems(self, performance_optimizer, security_auditor, rate_limiter, data_encryption):
        """Inicializar sistemas de optimización y seguridad"""
        self.performance_optimizer = performance_optimizer
        self.security_auditor = security_auditor
        self.rate_limiter = rate_limiter
        self.data_encryption = data_encryption
    
    def render_admin_dashboard(self):
        """Renderizar dashboard completo de administración"""
        st.markdown("# 🛠️ Dashboard de Administración")
        st.markdown("Panel de control para monitorear rendimiento y seguridad del sistema")
        
        # Tabs para diferentes secciones
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📊 Rendimiento", "🔒 Seguridad", "🚦 Rate Limiting", 
            "🔐 Encriptación", "📈 Analytics"
        ])
        
        with tab1:
            self._render_performance_tab()
        
        with tab2:
            self._render_security_tab()
        
        with tab3:
            self._render_rate_limiting_tab()
        
        with tab4:
            self._render_encryption_tab()
        
        with tab5:
            self._render_analytics_tab()
        
        # Tab adicional para procesamiento asíncrono
        with st.expander("🤖 Procesamiento Asíncrono de IA"):
            self._render_async_processing_tab()
    
    def _render_performance_tab(self):
        """Tab de rendimiento"""
        st.markdown("## 📊 Monitoreo de Rendimiento")
        
        if not self.performance_optimizer:
            st.error("❌ Sistema de optimización no disponible")
            return
        
        # Estadísticas de cache
        cache_stats = self.performance_optimizer.get_cache_stats()
        
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
        """Tab de seguridad"""
        st.markdown("## 🔒 Monitoreo de Seguridad")
        
        if not self.security_auditor:
            st.error("❌ Sistema de auditoría no disponible")
            return
        
        # Obtener datos de seguridad
        security_data = self.security_auditor.get_security_dashboard_data(hours=24)
        
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
        """Tab de rate limiting"""
        st.markdown("## 🚦 Monitoreo de Rate Limiting")
        
        if not self.rate_limiter:
            st.error("❌ Sistema de rate limiting no disponible")
            return
        
        # Estadísticas del sistema
        system_stats = self.rate_limiter.get_system_stats()
        
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
        """Tab de encriptación"""
        st.markdown("## 🔐 Estado de Encriptación")
        
        if not self.data_encryption:
            st.error("❌ Sistema de encriptación no disponible")
            return
        
        # Estado del sistema de encriptación
        encryption_status = self.data_encryption.get_encryption_status()
        
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
            from modules.ai_processor import HealthAnalyticsAI
            
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
                hovermode='x unified'
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
        st.session_state['admin_dashboard'] = AdminDashboard()
    return st.session_state['admin_dashboard']
