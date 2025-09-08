import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os
import sys
from dotenv import load_dotenv

# Añadir módulos al path de forma más robusta
modules_path = os.path.join(os.path.dirname(__file__), 'modules')
if modules_path not in sys.path:
    sys.path.append(modules_path)

# Importar sistema de autenticación
try:
    from modules.auth_system import (
        check_authentication, render_login_page, logout, 
        render_user_management, render_user_profile, HealthAuthenticator
    )
    AUTH_AVAILABLE = True
except ImportError as e:
    st.error(f"❌ Error importando sistema de autenticación: {str(e)}")
    AUTH_AVAILABLE = False

# Importar módulos IA
try:
    from modules.ai_processor import HealthAnalyticsAI, HealthMetricsCalculator
    from modules.chart_generator import SmartChartGenerator, DataAnalyzer
    AI_AVAILABLE = True
except ImportError as e:
        st.error(f"❌ Error importando módulos IA: {str(e)}")
        AI_AVAILABLE = False

# Importar módulos de mapas
try:
    import importlib
    import sys
    
    # Forzar recarga de módulos si ya están cargados
    if 'modules.map_interface' in sys.modules:
        importlib.reload(sys.modules['modules.map_interface'])
    if 'modules.interactive_maps' in sys.modules:
        importlib.reload(sys.modules['modules.interactive_maps'])
    
    from modules.map_interface import MapInterface
    from modules.interactive_maps import EpicHealthMaps
    MAPS_AVAILABLE = True
except ImportError as e:
    st.error(f"❌ Error importando módulos de mapas: {str(e)}")
    MAPS_AVAILABLE = False

# Importar dashboards personalizados por rol
try:
    from modules.role_dashboards import RoleDashboards
    ROLE_DASHBOARDS_AVAILABLE = True
except ImportError as e:
    st.error(f"❌ Error importando dashboards por rol: {str(e)}")
    ROLE_DASHBOARDS_AVAILABLE = False

# Cargar variables de entorno
load_dotenv()

@st.cache_data(ttl=3600, show_spinner="Cargando datos sanitarios...")
def load_health_datasets():
    """Cargar datasets de salud con optimización para cloud"""
    try:
        datasets = {}
        file_mapping = {
            'hospitales': 'data/raw/hospitales_malaga_2025.csv',
            'demografia': 'data/raw/demografia_malaga_2025.csv', 
            'servicios': 'data/raw/servicios_sanitarios_2025.csv',
            'accesibilidad': 'data/raw/accesibilidad_sanitaria_2025.csv',
            'indicadores': 'data/raw/indicadores_salud_2025.csv'
        }
        
        # Contador de archivos cargados para progreso
        loaded_files = 0
        total_files = len(file_mapping)
        
        for key, filepath in file_mapping.items():
            if os.path.exists(filepath):
                try:
                    # Optimización: usar dtype específicos para reducir memoria
                    if key == 'demografia':
                        datasets[key] = pd.read_csv(filepath, dtype={
                            'municipio': 'string',
                            'poblacion_2025': 'int32',
                            'poblacion_2024': 'int32',
                            'crecimiento_2024_2025': 'int16',
                            'densidad_hab_km2_2025': 'float32',
                            'renta_per_capita_2024': 'float32',
                            'indice_envejecimiento_2025': 'float32'
                        })
                    elif key == 'hospitales':
                        datasets[key] = pd.read_csv(filepath, dtype={
                            'nombre': 'string',
                            'tipo_centro': 'string',
                            'distrito_sanitario': 'string',
                            'camas_funcionamiento_2025': 'int16',
                            'personal_sanitario_2025': 'int16',
                            'poblacion_referencia_2025': 'int32'
                        })
                    else:
                        # Carga estándar para otros archivos
                        datasets[key] = pd.read_csv(filepath)
                    
                    loaded_files += 1
                    
                except Exception as file_error:
                    st.warning(f"⚠️ Error cargando {filepath}: {str(file_error)}")
            else:
                st.warning(f"⚠️ Archivo no encontrado: {filepath}")
        
        if datasets:
            st.success(f"✅ Cargados {loaded_files}/{total_files} datasets correctamente")
            return datasets
        else:
            st.error("❌ No se pudieron cargar los datasets")
            return None
        
    except Exception as e:
        st.error(f"❌ Error crítico cargando datasets: {str(e)}")
        return None

# Configuración de la página
st.set_page_config(
    page_title="Copilot Salud Andalucía - Secure",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Importar CSS externo con tema sanitario avanzado y layout desktop
with open('assets/style.css', 'r', encoding='utf-8') as f:
    css_content = f.read()

with open('assets/desktop_layout.css', 'r', encoding='utf-8') as f:
    desktop_css = f.read()

st.markdown(f"""
<style>
/* Importar fuentes modernas */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Poppins:wght@300;400;500;600;700&display=swap');

{css_content}

{desktop_css}
</style>

<script>
// Forzar viewport de escritorio
(function() {{
    var viewport = document.querySelector("meta[name=viewport]");
    if (viewport) {{
        viewport.setAttribute('content', 'width=1200, initial-scale=1.0, maximum-scale=1.0, user-scalable=no');
    }} else {{
        var meta = document.createElement('meta');
        meta.name = "viewport";
        meta.content = "width=1200, initial-scale=1.0, maximum-scale=1.0, user-scalable=no";
        document.getElementsByTagName('head')[0].appendChild(meta);
    }}
    
    // Forzar layout desktop
    if (window.innerWidth < 1200 && !document.body.classList.contains('desktop-forced')) {{
        document.body.classList.add('desktop-forced');
        document.body.style.minWidth = '1200px';
        document.body.style.overflowX = 'auto';
    }}
}})();
</script>
""", unsafe_allow_html=True)

class SecureHealthAnalyticsApp:
    def __init__(self):
        # Inicializar propiedades por defecto
        self.authenticated = False
        self.user = None
        self.auth = None
        self.role_info = None
        self.data = None
        self.ai_processor = None
        self.chart_generator = None
        self.metrics_calculator = None
        self.map_interface = None
        
        if not AUTH_AVAILABLE:
            st.error("❌ Sistema de autenticación no disponible")
            return
            
        # Verificar autenticación
        self.authenticated = check_authentication()
        
        if self.authenticated:
            try:
                self.user = st.session_state.user
                self.auth = HealthAuthenticator()
                self.role_info = self.auth.get_role_info(self.user['role'])
                self.load_datasets()
                
                # Inicializar IA si está disponible y el usuario tiene permisos
                if AI_AVAILABLE and os.getenv('GROQ_API_KEY') and self.has_permission('analisis_ia'):
                    self.ai_processor = HealthAnalyticsAI()
                    self.chart_generator = SmartChartGenerator()
                    self.metrics_calculator = HealthMetricsCalculator()
                
                # Inicializar mapas si está disponible
                if MAPS_AVAILABLE:
                    try:
                        self.map_interface = MapInterface()
                        # Verificar que el método tenga la signatura correcta
                        import inspect
                        sig = inspect.signature(self.map_interface.render_epic_maps_dashboard)
                        params = list(sig.parameters.keys())
                        print(f"🔧 MapInterface parámetros: {params}")
                    except Exception as e:
                        print(f"❌ Error inicializando MapInterface: {str(e)}")
                        self.map_interface = None
                else:
                    self.map_interface = None
                
                # Inicializar dashboards personalizados
                if ROLE_DASHBOARDS_AVAILABLE:
                    self.role_dashboards = RoleDashboards()
                else:
                    self.role_dashboards = None
                    
            except Exception as e:
                st.error(f"❌ Error inicializando aplicación: {str(e)}")
                self.authenticated = False
    
    def has_permission(self, permission: str) -> bool:
        """Verificar si el usuario tiene un permiso específico"""
        try:
            if not self.authenticated or not self.auth or not self.user:
                return False
            
            user_role = self.user.get('role')
            if not user_role:
                return False
                
            return self.auth.has_permission(user_role, permission)
            
        except Exception as e:
            print(f"❌ Error verificando permisos: {str(e)}")
            return False
    
    def require_permission(self, permission: str) -> bool:
        """Decorador para requerir permisos específicos"""
        if not self.has_permission(permission):
            # Obtener información del rol de forma segura
            role_display = "Usuario desconocido"
            if self.role_info:
                role_display = f"{self.role_info['icon']} {self.role_info['name']}"
            elif self.user and self.user.get('role'):
                role_display = f"👤 {self.user['role']}"
            
            st.markdown(f"""
            <div class="permission-required">
                <h3>🚫 Acceso Restringido</h3>
                <p><strong>Permiso requerido:</strong> {permission}</p>
                <p><strong>Tu rol:</strong> {role_display}</p>
                <p>Contacta al administrador para obtener acceso.</p>
            </div>
            """, unsafe_allow_html=True)
            return False
        return True
        
    def _load_datasets_static(self):
        """Cargar datasets con verificación de permisos"""
        return load_health_datasets()
    
    def load_datasets(self):
        """Inicializar datasets"""
        try:
            if self.has_permission('ver_datos'):
                self.data = self._load_datasets_static()
            else:
                self.data = None
        except Exception as e:
            print(f"❌ Error inicializando datasets: {str(e)}")
            self.data = None
        
    def render_secure_header(self):
        """Cabecera personalizada según el rol del usuario"""
        if not self.authenticated or not self.user or not self.role_info:
            st.error("❌ Error: Información de usuario no disponible")
            return
            
        try:
            user_name = self.user.get('name', 'Usuario')
            user_username = self.user.get('username', 'N/A')
            role_icon = self.role_info.get('icon', '👤')
            role_name = self.role_info.get('name', 'Usuario')
            theme = self.role_info.get('theme', {})
            
            # Personalización por rol
            welcome_message = theme.get('welcome_message', 'Sistema de Análisis Sociosanitario')
            gradient = theme.get('primary_gradient', 'linear-gradient(135deg, #ffffff 0%, #f8fafc 100%)')
            header_style = theme.get('header_style', 'simple')
            
            # Estilos específicos por tipo de header
            if header_style == 'executive':
                header_content = f"""
                <div class="main-header-secure" style="background: {gradient}; color: white;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <h1 style="color: white;">🏛️ {welcome_message}</h1>
                            <h2 style="color: rgba(255,255,255,0.9); font-size: 1.2rem;">Sistema Integrado de Gestión Sanitaria</h2>
                        </div>
                        <div style="text-align: right;">
                            <div class="executive-badge" style="background: rgba(255,255,255,0.2); padding: 1rem; border-radius: 12px;">
                                <div style="font-size: 2rem;">{role_icon}</div>
                                <strong style="color: white;">{user_name}</strong><br>
                                <small style="color: rgba(255,255,255,0.8);">{role_name}</small>
                            </div>
                        </div>
                    </div>
                    <p style="color: rgba(255,255,255,0.8); margin-top: 1rem;">🔐 Acceso Ejecutivo Autorizado | Provincia de Málaga</p>
                </div>
                """
            elif header_style == 'operational':
                header_content = f"""
                <div class="main-header-secure" style="background: {gradient}; color: white;">
                    <h1 style="color: white;">⚙️ {welcome_message}</h1>
                    <h2 style="color: rgba(255,255,255,0.9);">Panel Operativo - Gestión Sanitaria</h2>
                    <div class="user-badge" style="background: rgba(255,255,255,0.2); color: white; border: 1px solid rgba(255,255,255,0.3);">
                        {role_icon} <strong>{user_name}</strong> | {role_name}
                    </div>
                    <p style="color: rgba(255,255,255,0.8);">📊 Sistema Operativo Activo | Málaga</p>
                </div>
                """
            elif header_style == 'analytical':
                header_content = f"""
                <div class="main-header-secure" style="background: {gradient}; color: white;">
                    <h1 style="color: white;">📊 {welcome_message}</h1>
                    <h2 style="color: rgba(255,255,255,0.9);">Plataforma de Análisis Avanzado</h2>
                    <div class="user-badge" style="background: rgba(255,255,255,0.2); color: white; border: 1px solid rgba(255,255,255,0.3);">
                        {role_icon} <strong>{user_name}</strong> | {role_name}
                    </div>
                    <p style="color: rgba(255,255,255,0.8);">📈 Análisis de Datos Activo | Málaga</p>
                </div>
                """
            else:  # simple
                header_content = f"""
                <div class="main-header-secure" style="background: {gradient}; color: white;">
                    <h1 style="color: white;">👁️ {welcome_message}</h1>
                    <h2 style="color: rgba(255,255,255,0.9);">Información Pública Sanitaria</h2>
                    <div class="user-badge" style="background: rgba(255,255,255,0.2); color: white; border: 1px solid rgba(255,255,255,0.3);">
                        {role_icon} <strong>{user_name}</strong>
                    </div>
                    <p style="color: rgba(255,255,255,0.8);">📋 Acceso Público | Málaga</p>
                </div>
                """
            
            st.markdown(header_content, unsafe_allow_html=True)
    
            # Indicador de rol fijo
            st.markdown(f"""
            <div class="role-indicator">
                {role_icon} {user_username} ({role_name})
            </div>
            """, unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"❌ Error renderizando header: {str(e)}")
    
    def render_secure_sidebar(self):
        """Sidebar personalizado según el rol del usuario"""
        with st.sidebar:
            theme = self.role_info.get('theme', {})
            sidebar_style = theme.get('sidebar_style', 'minimal')
            focus_areas = theme.get('focus_areas', ['Información General'])
            
            # Información del usuario personalizada por rol
            st.markdown(f"""
            <div style="background: {theme.get('primary_gradient', 'linear-gradient(135deg, #6b7280 0%, #9ca3af 100%)')}; 
                        padding: 1.5rem; border-radius: 12px; text-align: center; margin-bottom: 1rem; color: white;">
                <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">{self.role_info['icon']}</div>
                <strong style="font-size: 1.1rem;">{self.user['name']}</strong><br>
                <small style="color: rgba(255,255,255,0.8); font-size: 0.9rem;">{self.role_info['name']}</small>
                <div style="margin-top: 0.5rem; padding: 0.5rem; background: rgba(255,255,255,0.1); border-radius: 8px;">
                    <small style="color: rgba(255,255,255,0.9);">{self.user['organization']}</small>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Botón de logout
            if st.button("🚪 Cerrar Sesión", key="logout_sidebar"):
                logout()
            
            # Enlaces rápidos personalizados por rol
            if sidebar_style == 'expanded':
                st.markdown("### 🚀 Panel de Control")
                
                if st.button("🏛️ Vista Ejecutiva", width="stretch"):
                    st.session_state.page = "main"
                    st.rerun()
                    
                if self.has_permission('gestion_usuarios'):
                    if st.button("👥 Gestión de Usuarios", width="stretch"):
                        st.session_state.page = "gestion_usuarios"
                        st.rerun()
                        
                if st.button("📊 Análisis Estratégico", width="stretch"):
                    st.session_state.page = "main"
                    st.rerun()
                    
            elif sidebar_style == 'compact':
                st.markdown("### ⚙️ Gestión")
                
                if st.button("📊 Dashboard", width="stretch"):
                    st.session_state.page = "main"
                    st.rerun()
                    
                if st.button("🗺️ Mapas", width="stretch"):
                    st.session_state.page = "main"
                    st.rerun()
                    
            elif sidebar_style == 'detailed':
                st.markdown("### 📈 Análisis")
                
                if st.button("📊 Dashboard Analítico", width="stretch"):
                    st.session_state.page = "main"
                    st.rerun()
                    
                if st.button("🔍 Exploración de Datos", width="stretch"):
                    st.session_state.page = "main"
                    st.rerun()
                    
            else:  # minimal
                st.markdown("### 📋 Navegación")
                
                if st.button("🏠 Inicio", width="stretch"):
                    st.session_state.page = "main"
                    st.rerun()
            
            # Perfil siempre disponible
            if st.button("👤 Mi Perfil", width="stretch"):
                st.session_state.page = "profile"
                st.rerun()
                
            st.markdown("---")
                
            # Áreas de enfoque personalizadas por rol
            st.markdown(f"### 🎯 Áreas de Enfoque")
            for i, area in enumerate(focus_areas):
                st.markdown(f"**{i+1}.** {area}")
            
            st.markdown("---")
            
            # Información del sistema personalizada por rol
            if self.data and self.has_permission('ver_datos'):
                if sidebar_style == 'expanded':
                    st.markdown("### 📊 KPIs Ejecutivos")
                    total_hospitales = len(self.data['hospitales'])
                    total_poblacion = self.data['demografia']['poblacion_2025'].sum()
                    
                    st.metric("🏥 Centros", total_hospitales)
                    st.metric("👥 Población", f"{total_poblacion/1000:.0f}K")
                    st.metric("🎯 Cobertura", f"{(total_hospitales/total_poblacion*100000):.1f}/100K")
                    
                elif sidebar_style == 'compact':
                    st.markdown("### ⚙️ Métricas Operativas")
                    if 'accesibilidad' in self.data:
                        avg_time = self.data['accesibilidad']['tiempo_coche_minutos'].mean()
                        st.metric("⏱️ Tiempo Medio", f"{avg_time:.0f} min")
                    
                elif sidebar_style == 'detailed':
                    st.markdown("### 📈 Indicadores Analíticos")
                    if 'indicadores' in self.data:
                        avg_ratio = self.data['indicadores']['ratio_medico_1000_hab'].mean()
                        st.metric("👨‍⚕️ Ratio Médicos", f"{avg_ratio:.1f}/1K")
                
                else:  # minimal
                    st.markdown("### 📋 Info Básica")
                    st.info(f"🏥 {len(self.data['hospitales'])} centros disponibles")
                
                # Indicador de acceso a IA
                if self.ai_processor:
                    st.success("🤖 IA Activa")
                else:
                    st.info("🔧 IA Limitada")
            
            st.markdown("---")
            
            # Permisos del usuario
            st.markdown("### 🔐 Mis Permisos")
            permissions = self.role_info['permissions']
            permission_names = {
                # Permisos generales
                'acceso_completo': '🔓 Acceso Total',
                'gestion_usuarios': '👥 Gestión de Usuarios',
                'configuracion_sistema': '⚙️ Configuración del Sistema',
                'analisis_ia': '🤖 Análisis con IA',
                'reportes': '📋 Reportes Avanzados',
                'planificacion': '📈 Planificación Estratégica',
                'ver_datos': '👀 Visualización de Datos',
                'analisis_equidad': '⚖️ Análisis de Equidad',
                
                # Permisos de mapas
                'mapas_todos': '🌟 Todos los Mapas',
                'mapas_estrategicos': '🎯 Mapas Estratégicos',
                'mapas_sensibles': '🔒 Mapas con Datos Sensibles',
                'mapas_operativos': '⚙️ Mapas Operativos',
                'mapas_gestion': '📊 Mapas de Gestión',
                'mapas_analiticos': '📈 Mapas Analíticos',
                'mapas_demograficos': '👥 Mapas Demográficos',
                'mapas_publicos': '🌐 Mapas Públicos'
            }
            
            # Mostrar permisos organizados por categorías
            general_perms = []
            map_perms = []
            
            for perm in permissions:
                perm_display = permission_names.get(perm, f"🔹 {perm}")
                if perm.startswith('mapas_'):
                    map_perms.append(perm_display)
                else:
                    general_perms.append(perm_display)
            
            # Permisos generales
            if general_perms:
                st.markdown("**🔧 Permisos Generales:**")
                for perm_display in general_perms:
                    st.markdown(f"• {perm_display}")
            
            # Permisos de mapas
            if map_perms:
                st.markdown("**🗺️ Permisos de Mapas:**")
                for perm_display in map_perms:
                    st.markdown(f"• {perm_display}")

def main():
    """Función principal con autenticación completa"""
    
    if not AUTH_AVAILABLE:
        st.error("❌ Sistema de autenticación no disponible. Instala: pip install bcrypt PyJWT")
        return
    
    # Verificar autenticación
    if not check_authentication():
        render_login_page()
        return
    
    # Usuario autenticado - inicializar aplicación segura
    app = SecureHealthAnalyticsApp()
    
    if not app.authenticated:
        st.error("❌ Error en la autenticación. Intenta iniciar sesión nuevamente.")
        logout()
        return
    
    # Renderizar aplicación segura
    app.render_secure_header()
    app.render_secure_sidebar()
    
    # Navegación principal
    render_page_navigation(app)
    
    # Footer con información de seguridad y auditoría
    st.markdown("---")
    st.markdown(f"""
    <div style="text-align: center; color: #666; padding: 1rem; background: linear-gradient(135deg, rgba(0,168,107,0.05), rgba(33,150,243,0.05)); border-radius: 10px; border: 1px solid rgba(0,168,107,0.2);">
        <p><strong>🔐 Sistema Seguro v2.0</strong> | 
        <strong>👤 Usuario:</strong> {app.user['name']} ({app.user['username']}) | 
        <strong>🎭 Rol:</strong> {app.role_info['name']} | 
        <strong>🏢 Org:</strong> {app.user['organization']}</p>
        <p><strong>⏰ Sesión:</strong> {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} | 
        <strong>🔑 Permisos:</strong> {len(app.role_info['permissions'])} activos | 
        <strong>🤖 IA:</strong> {'🟢 Disponible' if app.ai_processor else '🔒 Restringida'}</p>
        <p><em>🏥 Sistema de Análisis Sociosanitario de Málaga v2.1 - Acceso Autorizado</em></p>
        </div>
        """, unsafe_allow_html=True)

def render_page_navigation(app):
    """Navegación entre páginas según permisos"""
    
    current_page = st.session_state.get('page', 'main')
    
    if current_page == 'gestion_usuarios' and app.has_permission('gestion_usuarios'):
        render_user_management()
    elif current_page == 'profile':
        render_user_profile()
    else:
        # Página principal con tabs dinámicos
        tabs_available = []
        tab_functions = []
        
        # Dashboard siempre disponible para usuarios con ver_datos
        if app.has_permission('ver_datos'):
            tabs_available.append("📊 Dashboard")
            tab_functions.append(lambda: render_secure_dashboard(app))
        
        if app.has_permission('analisis_ia'):
            tabs_available.append("🤖 Chat IA")
            tab_functions.append(lambda: render_secure_chat(app))
        
        if app.has_permission('reportes'):
            tabs_available.append("📋 Reportes")
            tab_functions.append(lambda: render_secure_reportes(app))
        
        if app.has_permission('planificacion'):
            tabs_available.append("🗺️ Planificación")
            tab_functions.append(lambda: render_secure_planificacion(app))
        
        # Tab de mapas épicos disponible para usuarios con permisos de ver_datos o superior
        if app.has_permission('ver_datos') and MAPS_AVAILABLE:
            tabs_available.append("🗺️ Mapas Épicos")
            tab_functions.append(lambda: render_epic_maps_tab(app))
        
        # Si solo tiene un tab, mostrarlo directamente
        if len(tabs_available) == 1:
            tab_functions[0]()
        elif len(tabs_available) > 1:
            tabs = st.tabs(tabs_available)
            
            for i, tab_function in enumerate(tab_functions):
                with tabs[i]:
                    tab_function()
        else:
            if app.user['role'] == 'invitado':
                st.info("ℹ️ **Usuario Invitado**: Solo tienes acceso al Dashboard básico. Para más funcionalidades, contacta al administrador.")
            else:
                st.error("❌ No tienes permisos para acceder a ninguna funcionalidad")

def render_secure_chat(app):
    """Chat con verificación de permisos"""
    st.markdown("### 🤖 Asistente IA Seguro")
    
    if not app.require_permission('analisis_ia'):
        # Mensaje específico para cada rol sin permisos
        if app.user['role'] == 'invitado':
            st.warning("🔒 **Chat IA no disponible**: Los usuarios invitados no tienen acceso al asistente de IA.")
            st.info("💡 **Sugerencia**: Solicita una cuenta con permisos de 'Analista' o superior para acceder al Chat IA.")
        return
    
    # Estado de IA mejorado
    st.markdown(f"""
    <div class="access-granted">
        <h4>✅ Acceso Autorizado al Análisis con IA</h4>
        <p><strong>Usuario:</strong> {app.user['name']} | <strong>Rol:</strong> {app.role_info['name']}</p>
        <p><strong>Organización:</strong> {app.user['organization']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Inicializar mensajes personalizados por usuario
    user_messages_key = f'secure_messages_{app.user["username"]}'
    if user_messages_key not in st.session_state:
        # Crear saludo personalizado según el rol
        role_specific_content = {
            'admin': {
                'greeting': 'Soy tu asistente de análisis sociosanitario con **acceso administrativo completo**.',
                'analyses': [
                    '• Gestión integral del sistema sanitario',
                    '• Configuración y supervisión de usuarios',
                    '• Análisis de equidad territorial completo',
                    '• Planificación estratégica avanzada',
                    '• Reportes ejecutivos y auditoría',
                    '• Evaluación de recursos a nivel provincial'
                ],
                'suggestion': 'Como administrador, puedes consultar sobre cualquier aspecto del sistema sanitario de Málaga.'
            },
            'gestor': {
                'greeting': 'Soy tu asistente especializado en **gestión sanitaria operacional**.',
                'analyses': [
                    '• Optimización de recursos hospitalarios',
                    '• Análisis de capacidad asistencial',
                    '• Evaluación de accesibilidad por distrito',
                    '• Planificación de servicios sanitarios',
                    '• Reportes operacionales y de gestión',
                    '• Identificación de déficits asistenciales'
                ],
                'suggestion': 'Como gestor sanitario, puedes consultar sobre eficiencia operacional y planificación de recursos.'
            },
            'analista': {
                'greeting': 'Soy tu asistente especializado en **análisis estadístico y de datos sanitarios**.',
                'analyses': [
                    '• Análisis estadísticos avanzados',
                    '• Visualizaciones de datos epidemiológicos',
                    '• Estudios de correlación demográfica',
                    '• Análisis de tendencias poblacionales',
                    '• Reportes técnicos especializados',
                    '• Evaluación de indicadores de salud'
                ],
                'suggestion': 'Como analista, puedes solicitar análisis estadísticos detallados y visualizaciones específicas.'
            },
            'invitado': {
                'greeting': 'Soy tu asistente de consulta para **información básica del sistema sanitario**.',
                'analyses': [
                    '• Información general de hospitales',
                    '• Datos demográficos básicos',
                    '• Consultas sobre servicios disponibles',
                    '• Indicadores generales de salud',
                    '• Información de accesibilidad básica'
                ],
                'suggestion': 'Como usuario invitado, puedes consultar información general del sistema sanitario.'
            }
        }
        
        current_role_content = role_specific_content.get(app.user['role'], role_specific_content['invitado'])
        
        st.session_state[user_messages_key] = [
            {"role": "assistant", "content": f"""¡Hola **{app.user['name']}**! 👋 

{current_role_content['greeting']}

**🔐 Sesión Autenticada:**
- **Usuario:** {app.user['username']}
- **Rol:** {app.role_info['icon']} {app.role_info['name']}
- **Organización:** {app.user['organization']}

**🎯 Análisis Disponibles para tu rol:**

{'  \n'.join(current_role_content['analyses'])}

**💡 {current_role_content['suggestion']}**"""}
        ]
    
    # Mostrar historial específico del usuario
    for message in st.session_state[user_messages_key]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Input del usuario
    if prompt := st.chat_input(f"Consulta como {app.role_info['name']}..."):
        # Añadir contexto de usuario a la consulta
        enhanced_prompt = f"[Usuario: {app.user['name']}, Rol: {app.role_info['name']}, Org: {app.user['organization']}] {prompt}"
        
        st.session_state[user_messages_key].append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Procesar con IA si está disponible
        with st.chat_message("assistant"):
            if app.ai_processor and app.chart_generator:
                with st.spinner("🔒 Procesando consulta segura..."):
                    try:
                        # Procesar consulta con contexto de rol
                        analysis = app.ai_processor.process_health_query(enhanced_prompt, app.data)
                        
                        if analysis.get('analysis_type') != 'error':
                            # Mostrar análisis con información de auditoría
                            st.markdown(f"""
                            <div style="background: rgba(76, 175, 80, 0.1); padding: 1rem; border-radius: 8px; border-left: 4px solid #4CAF50;">
                                <strong>🔍 Análisis Procesado</strong><br>
                                <small>Usuario: {app.user['name']} | Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</small><br>
                                <strong>{analysis.get('main_insight', 'Análisis completado')}</strong>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Ejecutar y mostrar resultados
                            if 'data_query' in analysis:
                                try:
                                    result_data = app.ai_processor.execute_data_query(analysis['data_query'], app.data)
                                    
                                    if not result_data.empty and 'error' not in result_data.columns:
                                        chart_config = analysis.get('chart_config', {})
                                        
                                        # Generar gráfico
                                        if not chart_config.get('type'):
                                            chart_config['type'] = DataAnalyzer.suggest_chart_type(
                                                result_data, analysis.get('analysis_type', 'general')
                                            )
                                        
                                        if not chart_config.get('x_axis'):
                                            key_cols = DataAnalyzer.detect_key_columns(
                                                result_data, analysis.get('analysis_type', 'general')
                                            )
                                            chart_config.update(key_cols)
                                        
                                        fig = app.chart_generator.generate_chart(chart_config, result_data)
                                        st.plotly_chart(fig, width='stretch')
                                    
                                        # Mostrar datos con restricciones por rol
                                        if app.has_permission('acceso_completo'):
                                            with st.expander("📊 Datos completos del análisis"):
                                                st.dataframe(result_data, width='stretch')
                                        elif app.has_permission('analisis_ia'):
                                            with st.expander("📊 Vista resumida de datos"):
                                                st.dataframe(result_data.head(10), width='stretch')
                                                st.info(f"Mostrando 10 de {len(result_data)} registros (limitado por rol)")
                                        else:
                                            st.info("🔒 Vista de datos restringida para tu rol")
                                except Exception as e:
                                    st.error(f"❌ Error ejecutando análisis: {str(e)}")
                            
                            # Métricas y recomendaciones
                            if 'metrics' in analysis and analysis['metrics']:
                                st.markdown("#### 📈 Métricas Clave")
                                cols = st.columns(min(len(analysis['metrics']), 4))
                                for i, metric in enumerate(analysis['metrics'][:4]):
                                    with cols[i]:
                                        st.metric(
                                            metric.get('name', 'Métrica'), 
                                            metric.get('value', 'N/A'),
                                            help=metric.get('unit', '')
                                        )
                        
                            if 'recommendations' in analysis and analysis['recommendations']:
                                st.markdown(f"""
                                <div style="background: rgba(156, 39, 176, 0.1); padding: 1rem; border-radius: 8px; border-left: 4px solid #9c27b0;">
                                    <h4>🎯 Recomendaciones para {app.role_info['name']}</h4>
                                    <ul>
                                        {''.join([f'<li>{rec}</li>' for rec in analysis['recommendations']])}
                                    </ul>
                                </div>
                                """, unsafe_allow_html=True)
                            
                            response = f"✅ **Análisis autorizado completado** por {app.user['name']}: {analysis.get('main_insight', 'Consulta procesada')}"
                        else:
                            response = f"❌ **Error en análisis**: {analysis.get('main_insight', 'No se pudo procesar')}"
                        
                    except Exception as e:
                        response = f"⚠️ **Error de sistema**: {str(e)}"
                        st.error(response)
            else:
                response = "🔒 **IA requiere configuración** o permisos insuficientes."
                st.warning(response)
            
            st.session_state[user_messages_key].append({"role": "assistant", "content": response})

def render_secure_dashboard(app):
    """Dashboard personalizado según el rol del usuario"""
    
    if not app.require_permission('ver_datos'):
        return
    
    if not app.data:
        st.error("❌ No hay datos disponibles. Ejecuta data_collector_2025.py")
        return
    
    # Usar dashboard personalizado si está disponible
    if app.role_dashboards and ROLE_DASHBOARDS_AVAILABLE:
        try:
            app.role_dashboards.render_personalized_dashboard(
                app.user['role'], 
                app.data, 
                app.role_info
            )
            return
        except Exception as e:
            st.error(f"❌ Error en dashboard personalizado: {str(e)}")
            st.info("🔄 Usando dashboard por defecto...")
    
    # Dashboard por defecto si no hay personalización
    st.markdown("### 📊 Dashboard Seguro")
    
    # Información de acceso
    st.markdown(f"""
    <div class="access-granted">
        ✅ <strong>Acceso Autorizado a Dashboard</strong> | Usuario: {app.user['name']} | Rol: {app.role_info['name']}
        </div>
        """, unsafe_allow_html=True)
    
    # Métricas básicas (todos los roles con ver_datos)
    col1, col2, col3, col4 = st.columns(4)
    
    total_pop = app.data['demografia']['poblacion_2025'].sum()
    total_hospitals = len(app.data['hospitales'])
    total_beds = app.data['hospitales']['camas_funcionamiento_2025'].sum()
    
    with col1:
        st.metric("👥 Población", f"{total_pop/1000:.0f}K")
    with col2:
        st.metric("🏥 Centros", total_hospitals)
    with col3:
        st.metric("🛏️ Camas", f"{total_beds:,}")
    with col4:
        bed_ratio = (total_beds / total_pop) * 1000
        st.metric("Camas/1000 hab", f"{bed_ratio:.1f}")
    
    # Contenido adicional basado en permisos
    if app.has_permission('analisis_ia'):
        st.markdown("---")
        st.markdown("#### 📈 Análisis Avanzado (Autorizado)")
    elif app.user['role'] == 'invitado':
        st.markdown("---")
        st.markdown("#### 📊 Dashboard Básico")
        st.info("🔒 **Usuario Invitado**: Acceso limitado a métricas generales. Para análisis avanzados, contacta al administrador.")
        
        tab1, tab2, tab3 = st.tabs(["🏥 Infraestructura", "👥 Demografía", "🔬 Servicios"])
        
        with tab1:
            # Gráfico de hospitales por tipo
            tipo_counts = app.data['hospitales']['tipo_centro'].value_counts()
            fig_tipos = px.pie(
                values=tipo_counts.values,
                names=tipo_counts.index,
                title="🏥 Distribución de Centros por Tipo",
                hole=0.4
            )
            fig_tipos.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_tipos, width='stretch')
            
            # Capacidad hospitalaria
            fig_hospitales = px.bar(
                app.data['hospitales'],
                x='nombre',
                y='camas_funcionamiento_2025',
                title="🛏️ Capacidad Hospitalaria",
                color='tipo_centro',
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig_hospitales.update_xaxes(tickangle=45)
            st.plotly_chart(fig_hospitales, width='stretch')
        
        with tab2:
            # Top municipios por población
            top_pop = app.data['demografia'].nlargest(12, 'poblacion_2025')
            fig_demo = px.bar(
                top_pop,
                x='municipio',
                y='poblacion_2025',
                title="👥 Top 12 Municipios por Población",
                color='crecimiento_2024_2025',
                color_continuous_scale='Viridis'
            )
            fig_demo.update_xaxes(tickangle=45)
            st.plotly_chart(fig_demo, width='stretch')
            
            # Análisis de densidad vs renta
            fig_scatter = px.scatter(
                app.data['demografia'],
                x='densidad_hab_km2_2025',
                y='renta_per_capita_2024',
                size='poblacion_2025',
                color='indice_envejecimiento_2025',
                hover_data=['municipio'],
                title="🏘️ Densidad vs Renta per Cápita",
                color_continuous_scale='Spectral_r'
            )
            st.plotly_chart(fig_scatter, width='stretch')
        
        with tab3:
            # Análisis de servicios
            servicios_bool = app.data['servicios'].select_dtypes(include=['bool'])
            if not servicios_bool.empty:
                # Estadísticas de cobertura
                coverage_stats = (servicios_bool.mean() * 100).round(1).sort_values(ascending=False)
                
                fig_coverage = px.bar(
                    x=coverage_stats.index,
                    y=coverage_stats.values,
                    title="📊 Cobertura de Servicios (%)",
                    color=coverage_stats.values,
                    color_continuous_scale='RdYlGn'
                )
                fig_coverage.update_xaxes(tickangle=45)
                fig_coverage.add_hline(y=75, line_dash="dash", line_color="red", 
                                     annotation_text="Objetivo mínimo 75%")
                st.plotly_chart(fig_coverage, width='stretch')
                
                # Matriz de servicios
                services_matrix = servicios_bool.astype(int)
                services_matrix.index = app.data['servicios']['centro_sanitario']
                
                fig_heatmap = px.imshow(
                    services_matrix.T,
                    title="🔬 Matriz de Servicios Disponibles",
                    color_continuous_scale='RdYlGn',
                    aspect='auto'
                )
                fig_heatmap.update_layout(height=400)
                st.plotly_chart(fig_heatmap, width='stretch')
                    
            else:
                st.info("📊 Análisis avanzado disponible con permisos de 'analisis_ia'")

def render_secure_reportes(app):
    """Sistema de reportes con control de acceso"""
    st.markdown("### 📋 Reportes Seguros")
    
    if not app.require_permission('reportes'):
        # Mensaje específico para cada rol sin permisos
        if app.user['role'] == 'invitado':
            st.warning("🔒 **Reportes no disponibles**: Los usuarios invitados no tienen acceso a reportes avanzados.")
            st.info("💡 **Sugerencia**: Solicita una cuenta con permisos de 'Analista' o superior para acceder a los reportes.")
        return
    
    st.markdown(f"""
    <div class="access-granted">
        ✅ <strong>Acceso Autorizado a Reportes</strong> | Usuario: {app.user['name']}
    </div>
    """, unsafe_allow_html=True)
    
    # Selector de tipo de reporte
    report_types = ["📈 Reporte Ejecutivo", "🏥 Análisis de Infraestructura", "👥 Reporte Demográfico"]
    
    # Solo administradores pueden acceder al análisis de equidad
    if app.has_permission('analisis_equidad'):
        report_types.append("⚖️ Evaluación de Equidad")
    
    # Análisis completo solo para administradores
    if app.has_permission('acceso_completo'):
        report_types.append("🔍 Análisis Completo")
    
    selected_report = st.selectbox("Tipo de Reporte:", report_types)
    
    if "Ejecutivo" in selected_report:
        render_executive_report_secure(app)
    elif "Infraestructura" in selected_report:
        render_infrastructure_report_secure(app)
    elif "Demográfico" in selected_report:
        render_demographic_report_secure(app)
    elif "Equidad" in selected_report:
        render_equity_report_secure(app)
    elif "Análisis Completo" in selected_report:
        render_complete_analysis_secure(app)

def render_executive_report_secure(app):
    """Reporte ejecutivo con auditoría"""
    st.markdown("#### 📈 Reporte Ejecutivo Seguro")
    
    report_date = datetime.now().strftime("%d de %B de %Y")
    user_info = f"Generado por: {app.user['name']} ({app.role_info['name']}) - {app.user['organization']}"
    
    if not app.data:
        st.error("❌ Datos no disponibles")
        return
    
    executive_summary = f"""
    # 🏥 REPORTE EJECUTIVO - SISTEMA SANITARIO MÁLAGA
    **Fecha de análisis:** {report_date}  
    **{user_info}**
    
    ---
    
    ## 📊 INDICADORES PRINCIPALES
    - **Población total atendida:** {app.data['demografia']['poblacion_2025'].sum():,} habitantes
    - **Red asistencial:** {len(app.data['hospitales'])} centros sanitarios  
    - **Capacidad hospitalaria:** {app.data['hospitales']['camas_funcionamiento_2025'].sum():,} camas
    - **Personal sanitario:** {app.data['hospitales']['personal_sanitario_2025'].sum():,} profesionales
    - **Ratio camas/1000 hab:** {(app.data['hospitales']['camas_funcionamiento_2025'].sum() / app.data['demografia']['poblacion_2025'].sum() * 1000):.1f}
    
    ## 🗺️ DISTRIBUCIÓN TERRITORIAL
    - **Distritos sanitarios:** {len(app.data['hospitales']['distrito_sanitario'].unique())}
    - **Municipios cubiertos:** {len(app.data['demografia'])}
    - **Tiempo medio acceso:** {app.data['accesibilidad']['tiempo_coche_minutos'].mean():.1f} minutos
    
    ## 🎯 RECOMENDACIONES ESTRATÉGICAS
    1. **Prioridad Alta:** Evaluar equidad en distritos con menor ratio de recursos
    2. **Accesibilidad:** Mejorar conexiones en municipios con >60 min de acceso
    3. **Capacidad:** Monitorear ocupación en hospitales regionales
    4. **Personal:** Reforzar plantillas en áreas de alta demanda
    
    ---
    **Clasificación:** Uso Interno | **Acceso:** {app.role_info['name']} | **Timestamp:** {datetime.now().isoformat()}
    """
    
    st.markdown(executive_summary)
    
    # Botón de descarga con auditoría
    st.download_button(
        f"📥 Descargar Reporte Ejecutivo ({app.user['username']})",
        executive_summary,
        file_name=f"reporte_ejecutivo_{app.user['username']}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
        mime="text/plain"
    )

def render_infrastructure_report_secure(app):
    """Reporte de infraestructura con permisos"""
    st.markdown("#### 🏥 Reporte de Infraestructura")
    
    if not app.data:
        return
    
    # Análisis básico
    total_beds = app.data['hospitales']['camas_funcionamiento_2025'].sum()
    total_population = app.data['demografia']['poblacion_2025'].sum()
    bed_ratio = (total_beds / total_population) * 1000
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🛏️ Total Camas", f"{total_beds:,}")
    with col2:
        st.metric("📊 Ratio Camas/1K hab", f"{bed_ratio:.1f}")
    with col3:
        status = "✅ Adecuado" if bed_ratio >= 3 else "⚠️ Por debajo OMS"
        st.metric("🎯 Estado vs OMS", status)
    
    # Gráfico de distribución
    tipo_analysis = app.data['hospitales'].groupby('tipo_centro', observed=False).agg({
        'camas_funcionamiento_2025': ['sum', 'mean'],
        'personal_sanitario_2025': 'sum',
        'poblacion_referencia_2025': 'sum'
    }).round(1)
    
    st.markdown("##### 📊 Análisis por Tipo de Centro")
    st.dataframe(tipo_analysis, width='stretch')

def render_demographic_report_secure(app):
    """Reporte demográfico seguro"""
    st.markdown("#### 👥 Reporte Demográfico")
    
    if not app.data:
        return
    
    # Estadísticas de crecimiento
    total_growth = app.data['demografia']['crecimiento_2024_2025'].sum()
    total_pop_2024 = app.data['demografia']['poblacion_2024'].sum()
    growth_rate = (total_growth / total_pop_2024) * 100
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📈 Crecimiento 2024-2025", f"+{total_growth:,}")
    with col2:
        st.metric("📊 Tasa Crecimiento", f"{growth_rate:.2f}%")
    with col3:
        growing_munic = len(app.data['demografia'][app.data['demografia']['crecimiento_2024_2025'] > 0])
        st.metric("🏘️ Municipios en Crecimiento", growing_munic)
    
    # Top municipios
    st.markdown("##### 🏆 Top 5 Municipios en Crecimiento")
    top_growth = app.data['demografia'].nlargest(5, 'crecimiento_2024_2025')
    
    for _, row in top_growth.iterrows():
        growth_pct = (row['crecimiento_2024_2025'] / row['poblacion_2024']) * 100
        st.write(f"• **{row['municipio']}**: +{row['crecimiento_2024_2025']:,} hab ({growth_pct:.1f}%)")

def render_equity_report_secure(app):
    """Reporte de equidad (solo usuarios autorizados)"""
    st.markdown("#### ⚖️ Reporte de Equidad")
    
    if not app.has_permission('analisis_equidad'):
        st.warning("🔒 Reporte de equidad requiere permisos de administrador")
        return
    
    if app.metrics_calculator and app.data:
        try:
            equity_data = app.metrics_calculator.calculate_equity_index(app.data)
            if not equity_data.empty:
                st.markdown("##### 📊 Índices de Equidad por Distrito")
                
                equity_summary = equity_data[['distrito', 'score_equidad', 'ratio_camas_1000hab', 'ratio_personal_1000hab']].round(2)
                st.dataframe(equity_summary, width='stretch')
                
                # Alertas automáticas
                low_equity = equity_data[equity_data['score_equidad'] < 50]
                if not low_equity.empty:
                    st.error(f"🚨 **ALERTA**: {len(low_equity)} distritos con equidad crítica (<50 puntos)")
                    for _, district in low_equity.iterrows():
                        st.write(f"• **{district['distrito']}**: {district['score_equidad']:.0f}/100")
        except Exception as e:
            st.error(f"Error calculando equidad: {str(e)}")

def render_secure_planificacion(app):
    """Módulo de planificación con permisos"""
    st.markdown("### 🗺️ Planificación Estratégica Segura")
    
    if not app.require_permission('planificacion'):
        # Mensaje específico para cada rol sin permisos
        if app.user['role'] == 'invitado':
            st.warning("🔒 **Planificación no disponible**: Los usuarios invitados no tienen acceso a herramientas de planificación.")
            st.info("💡 **Sugerencia**: Solicita una cuenta con permisos de 'Gestor' o superior para acceder a la planificación.")
        elif app.user['role'] == 'analista':
            st.warning("🔒 **Planificación restringida**: Los analistas no tienen acceso a herramientas de planificación estratégica.")
            st.info("💡 **Sugerencia**: Contacta a un Gestor Sanitario o Administrador para funciones de planificación.")
        return
    
    st.markdown(f"""
    <div class="access-granted">
        ✅ <strong>Acceso Autorizado a Planificación</strong> | {app.user['name']} ({app.role_info['name']})
    </div>
    """, unsafe_allow_html=True)
    
    if not app.data:
        st.error("❌ Datos no disponibles")
        return
    
    # Análisis de planificación
    planificacion_options = st.selectbox(
        "🎯 Tipo de Análisis de Planificación:",
        [
            "🏥 Ubicación Óptima de Nuevos Centros",
            "📈 Proyección de Demanda Sanitaria", 
            "⚖️ Redistribución de Recursos",
            "🚗 Optimización de Rutas de Acceso"
        ]
    )
    
    if "Ubicación" in planificacion_options:
        render_location_planificacion(app)
    elif "Proyección" in planificacion_options:
        render_demand_projection(app)
    elif "Redistribución" in planificacion_options:
        render_resource_redistribution(app)
    elif "Optimización" in planificacion_options:
        render_route_optimization(app)

def render_location_planificacion(app):
    """Análisis de ubicación óptima"""
    st.markdown("#### 🏥 Análisis de Ubicación Óptima")
    
    # Simular análisis de planificación
    planificacion_metrics = []
    
    for _, municipio_data in app.data['demografia'].iterrows():
        municipio = municipio_data['municipio']
        pop_growth = municipio_data['crecimiento_2024_2025']
        population = municipio_data['poblacion_2025']
        
        # Tiempo de acceso promedio
        access_data = app.data['accesibilidad'][app.data['accesibilidad']['municipio_origen'] == municipio]
        avg_access_time = access_data['tiempo_coche_minutos'].mean() if not access_data.empty else 60
        
        # Score de necesidad
        need_score = (
            (pop_growth / 1000) * 0.3 +
            (population / 10000) * 0.4 +
            (avg_access_time / 10) * 0.3
        )
        
        planificacion_metrics.append({
            'municipio': municipio,
            'poblacion': population,
            'crecimiento': pop_growth,
            'tiempo_acceso_promedio': avg_access_time,
            'score_necesidad': need_score,
            'prioridad': 'Alta' if need_score > 15 else 'Media' if need_score > 8 else 'Baja'
        })
    
    planificacion_df = pd.DataFrame(planificacion_metrics).sort_values('score_necesidad', ascending=False)
    
    # Visualización
    fig_planificacion = px.scatter(
        planificacion_df,
        x='tiempo_acceso_promedio',
        y='poblacion',
        size='crecimiento',
        color='score_necesidad',
        hover_data=['municipio', 'prioridad'],
        title="🎯 Análisis de Ubicaciones Prioritarias",
        color_continuous_scale='Reds'
    )
    st.plotly_chart(fig_planificacion, width='stretch')
    
    # Top 5 recomendaciones
    st.markdown("##### 🏆 Top 5 Ubicaciones Recomendadas")
    top_5 = planificacion_df.head(5)
    
    for i, (_, row) in enumerate(top_5.iterrows()):
        priority_emoji = "🔴" if row['prioridad'] == 'Alta' else "🟡" if row['prioridad'] == 'Media' else "🟢"
        
        with st.expander(f"{i+1}. {priority_emoji} {row['municipio']} - Prioridad {row['prioridad']}"):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Población actual:** {row['poblacion']:,}")
                st.write(f"**Crecimiento esperado:** +{row['crecimiento']:,}")
            with col2:
                st.write(f"**Tiempo acceso actual:** {row['tiempo_acceso_promedio']:.1f} min")
                st.write(f"**Score de necesidad:** {row['score_necesidad']:.1f}")

def render_demand_projection(app):
    """Proyección de demanda"""
    st.markdown("#### 📈 Proyección de Demanda Sanitaria")
    
    # Proyección basada en crecimiento poblacional
    current_pop = app.data['demografia']['poblacion_2025'].sum()
    growth_rate = (app.data['demografia']['crecimiento_2024_2025'].sum() / app.data['demografia']['poblacion_2024'].sum()) * 100
    
    years = [2025, 2026, 2027, 2028, 2029, 2030]
    projected_pop = []
    projected_demand = []
    
    for year in years:
        years_ahead = year - 2025
        pop_projection = current_pop * ((1 + growth_rate/100) ** years_ahead)
        demand_projection = pop_projection * 0.15  # Estimación 15% necesita atención sanitaria anual
        
        projected_pop.append(pop_projection)
        projected_demand.append(demand_projection)
    
    projection_df = pd.DataFrame({
        'año': years,
        'poblacion_proyectada': projected_pop,
        'demanda_sanitaria': projected_demand
    })
    
    fig_projection = px.line(
        projection_df,
        x='año',
        y=['poblacion_proyectada', 'demanda_sanitaria'],
        title="📈 Proyección de Población y Demanda Sanitaria 2025-2030"
    )
    st.plotly_chart(fig_projection, width='stretch')
    
    # Métricas de proyección
    col1, col2, col3 = st.columns(3)
    with col1:
        pop_2030 = projected_pop[-1]
        st.metric("👥 Población 2030", f"{pop_2030/1000:.0f}K")
    with col2:
        demand_2030 = projected_demand[-1]
        st.metric("🏥 Demanda 2030", f"{demand_2030/1000:.0f}K")
    with col3:
        growth_total = ((pop_2030 - current_pop) / current_pop) * 100
        st.metric("📊 Crecimiento Total", f"{growth_total:.1f}%")

def render_resource_redistribution(app):
    """Análisis de redistribución de recursos"""
    st.markdown("#### ⚖️ Redistribución Óptima de Recursos")
    
    if app.metrics_calculator:
        try:
            equity_data = app.metrics_calculator.calculate_equity_index(app.data)
            if not equity_data.empty:
                # Identificar distritos con desequilibrios
                avg_ratio_camas = equity_data['ratio_camas_1000hab'].mean()
                avg_ratio_personal = equity_data['ratio_personal_1000hab'].mean()
                
                redistribution_needs = []
                for _, district in equity_data.iterrows():
                    camas_deficit = avg_ratio_camas - district['ratio_camas_1000hab']
                    personal_deficit = avg_ratio_personal - district['ratio_personal_1000hab']
                    
                    redistribution_needs.append({
                        'distrito': district['distrito'],
                        'deficit_camas': camas_deficit,
                        'deficit_personal': personal_deficit,
                        'prioridad_redistribucion': abs(camas_deficit) + abs(personal_deficit)
                    })
                
                redistrib_df = pd.DataFrame(redistribution_needs).sort_values('prioridad_redistribucion', ascending=False)
                
                # Visualizar necesidades de redistribución
                fig_redistrib = px.bar(
                    redistrib_df,
                    x='distrito',
                    y=['deficit_camas', 'deficit_personal'],
                    title="⚖️ Déficits por Distrito (valores negativos = exceso)",
                    barmode='group'
                )
                st.plotly_chart(fig_redistrib, width='stretch')
                
                # Recomendaciones de redistribución
                st.markdown("##### 🎯 Recomendaciones de Redistribución")
                top_needs = redistrib_df.head(3)
                
                for _, row in top_needs.iterrows():
                    if row['deficit_camas'] > 0:
                        st.warning(f"**{row['distrito']}**: Necesita +{row['deficit_camas']:.1f} camas/1000 hab")
                    if row['deficit_personal'] > 0:
                        st.info(f"**{row['distrito']}**: Necesita +{row['deficit_personal']:.1f} personal/1000 hab")
        
        except Exception as e:
            st.error(f"Error en análisis de redistribución: {str(e)}")

def render_route_optimization(app):
    """Optimización de rutas de acceso"""
    st.markdown("#### 🚗 Optimización de Rutas de Acceso")
    
    # Análisis de tiempos de acceso
    access_analysis = app.data['accesibilidad'].groupby('municipio_origen', observed=False).agg({
        'tiempo_coche_minutos': ['mean', 'min', 'max'],
        'coste_transporte_euros': 'mean'
    }).round(1)
    
    access_analysis.columns = ['tiempo_promedio', 'tiempo_minimo', 'tiempo_maximo', 'coste_promedio']
    access_analysis = access_analysis.reset_index()
    
    # Identificar rutas problemáticas
    problematic_routes = access_analysis[access_analysis['tiempo_promedio'] > 60]
    
    if not problematic_routes.empty:
        st.error(f"🚨 **{len(problematic_routes)} municipios** con tiempo de acceso >60 minutos")
        
        fig_routes = px.bar(
            problematic_routes,
            x='municipio_origen',
            y='tiempo_promedio',
            title="⚠️ Municipios con Acceso Deficiente (>60 min)",
            color='tiempo_promedio',
            color_continuous_scale='Reds'
        )
        st.plotly_chart(fig_routes, width='stretch')
        
        # Recomendaciones de mejora
        st.markdown("##### 🛣️ Recomendaciones de Mejora")
        for _, route in problematic_routes.iterrows():
            st.write(f"• **{route['municipio_origen']}**: Mejorar conexión (actual: {route['tiempo_promedio']:.0f} min)")
    else:
        st.success("✅ Todos los municipios tienen acceso adecuado (<60 min)")





def render_complete_analysis_secure(app):
    """Análisis completo del sistema (solo administradores)"""
    st.markdown("#### 🔍 Análisis Completo del Sistema")
    
    if not app.has_permission('acceso_completo'):
        st.error("🔒 Este análisis requiere permisos de administrador")
        return
    
    st.markdown(f"""
    <div class="access-granted">
        ✅ <strong>Análisis Completo Autorizado</strong> | Administrador: {app.user['name']}
    </div>
    """, unsafe_allow_html=True)
    
    if not app.data:
        st.error("❌ No hay datos disponibles para el análisis")
        return
    
    # Análisis integral de todos los componentes
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🏥 Infraestructura", "👥 Demografía", "⚖️ Equidad", 
        "🗺️ Accesibilidad", "📊 Resumen Ejecutivo"
    ])
    
    with tab1:
        st.markdown("##### 🏥 Análisis de Infraestructura Hospitalaria")
        
        # Métricas clave
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            total_hospitals = len(app.data['hospitales'])
            st.metric("🏥 Total Hospitales", total_hospitals)
        with col2:
            total_beds = app.data['hospitales']['camas_funcionamiento_2025'].sum()
            st.metric("🛏️ Camas Totales", f"{total_beds:,}")
        with col3:
            total_staff = app.data['hospitales']['personal_sanitario_2025'].sum()
            st.metric("👨‍⚕️ Personal Sanitario", f"{total_staff:,}")
        with col4:
            total_population = app.data['demografia']['poblacion_2025'].sum()
            bed_ratio = (total_beds / total_population) * 1000
            st.metric("Camas/1000 hab", f"{bed_ratio:.1f}")
        
        # Distribución por tipo de centro
        tipo_dist = app.data['hospitales']['tipo_centro'].value_counts()
        fig_tipos = px.pie(values=tipo_dist.values, names=tipo_dist.index, 
                          title="Distribución de Centros por Tipo")
        st.plotly_chart(fig_tipos, width='stretch')
    
    with tab2:
        st.markdown("##### 👥 Análisis Demográfico Detallado")
        
        # Proyecciones demográficas
        total_pop_2025 = app.data['demografia']['poblacion_2025'].sum()
        total_growth = app.data['demografia']['crecimiento_2024_2025'].sum()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("👥 Población 2025", f"{total_pop_2025:,}")
        with col2:
            st.metric("📈 Crecimiento 2024-25", f"+{total_growth:,}")
        with col3:
            growth_rate = (total_growth / total_pop_2025) * 100
            st.metric("📊 Tasa Crecimiento", f"{growth_rate:.2f}%")
        
        # Top municipios por crecimiento
        top_growth = app.data['demografia'].nlargest(10, 'crecimiento_2024_2025')
        fig_growth = px.bar(top_growth, x='municipio', y='crecimiento_2024_2025',
                           title="Top 10 Municipios por Crecimiento Poblacional")
        fig_growth.update_xaxes(tickangle=45)
        st.plotly_chart(fig_growth, width='stretch')
    
    with tab3:
        st.markdown("##### ⚖️ Análisis de Equidad Territorial")
        
        if app.metrics_calculator:
            try:
                equity_data = app.metrics_calculator.calculate_equity_index(app.data)
                if not equity_data.empty:
                    # Métricas de equidad
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        avg_score = equity_data['score_equidad'].mean()
                        st.metric("📊 Score Promedio", f"{avg_score:.1f}/100")
                    with col2:
                        max_score = equity_data['score_equidad'].max()
                        best_district = equity_data[equity_data['score_equidad'] == max_score]['distrito'].iloc[0]
                        st.metric("🏆 Mejor Distrito", f"{best_district} ({max_score:.1f})")
                    with col3:
                        min_score = equity_data['score_equidad'].min()
                        worst_district = equity_data[equity_data['score_equidad'] == min_score]['distrito'].iloc[0]
                        st.metric("⚠️ Distrito con Menor Score", f"{worst_district} ({min_score:.1f})")
                    
                    # Gráfico de equidad
                    fig_equity = px.bar(equity_data, x='distrito', y='score_equidad',
                                       title="Score de Equidad por Distrito Sanitario",
                                       color='score_equidad', color_continuous_scale='RdYlGn',
                                       labels={'score_equidad': 'Score de Equidad (0-100)', 'distrito': 'Distrito Sanitario'})
                    fig_equity.update_xaxes(tickangle=45)
                    st.plotly_chart(fig_equity, width='stretch')
                    
                    # Tabla detallada de equidad
                    st.markdown("##### 📋 Detalle por Distrito")
                    st.dataframe(equity_data, width='stretch')
                else:
                    st.info("No se pudieron calcular los índices de equidad")
            except Exception as e:
                st.error(f"Error calculando equidad: {str(e)}")
        else:
            st.warning("Calculadora de métricas no disponible")
    
    with tab4:
        st.markdown("##### 🗺️ Análisis de Accesibilidad")
        
        if 'accesibilidad' in app.data:
            # Tiempos de acceso promedio
            avg_time = app.data['accesibilidad']['tiempo_coche_minutos'].mean()
            max_time = app.data['accesibilidad']['tiempo_coche_minutos'].max()
            min_time = app.data['accesibilidad']['tiempo_coche_minutos'].min()
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("⏱️ Tiempo Promedio", f"{avg_time:.1f} min")
            with col2:
                st.metric("⏱️ Tiempo Máximo", f"{max_time:.1f} min")
            with col3:
                st.metric("⏱️ Tiempo Mínimo", f"{min_time:.1f} min")
            
            # Distribución de tiempos de acceso
            fig_access = px.histogram(app.data['accesibilidad'], x='tiempo_coche_minutos',
                                     title="Distribución de Tiempos de Acceso",
                                     nbins=20)
            st.plotly_chart(fig_access, width='stretch')
    
    with tab5:
        st.markdown("##### 📊 Resumen Ejecutivo Completo")
        
        # Alertas y recomendaciones críticas
        st.markdown("**🚨 Alertas del Sistema:**")
        
        # Verificar ratios críticos
        alerts = []
        total_population = app.data['demografia']['poblacion_2025'].sum()
        total_beds = app.data['hospitales']['camas_funcionamiento_2025'].sum()
        bed_ratio = (total_beds / total_population) * 1000
        avg_time = app.data['accesibilidad']['tiempo_coche_minutos'].mean()
        
        if bed_ratio < 3.0:
            alerts.append("⚠️ Ratio de camas por habitante por debajo del estándar (3.0/1000)")
        
        if avg_time > 45:
            alerts.append("⚠️ Tiempo de acceso promedio superior a 45 minutos")
        
        long_access = app.data['accesibilidad'][app.data['accesibilidad']['tiempo_coche_minutos'] > 60]
        if not long_access.empty:
            alerts.append(f"⚠️ {len(long_access)} rutas con tiempo de acceso superior a 60 minutos")
        
        if alerts:
            for alert in alerts:
                st.warning(alert)
        else:
            st.success("✅ Todos los indicadores dentro de parámetros normales")
        
        # Recomendaciones estratégicas
        st.markdown("**💡 Recomendaciones Estratégicas:**")
        
        recommendations = [
            "🏥 Evaluar la creación de nuevos centros de salud en zonas de alto crecimiento poblacional",
            "🚑 Optimizar rutas de transporte sanitario para reducir tiempos de acceso",
            "👨‍⚕️ Planificar contratación de personal sanitario según proyecciones demográficas",
            "⚖️ Implementar medidas de equidad territorial en distritos con menores recursos",
            "📊 Establecer sistema de monitoreo continuo de indicadores clave"
        ]
        
        for rec in recommendations:
            st.info(rec)

def render_epic_maps_tab(app):
    """Tab de mapas épicos con verificación de permisos"""
    st.markdown("### 🗺️ Mapas Interactivos Épicos")
    
    if not app.require_permission('ver_datos'):
        return
    
    # Verificar disponibilidad de mapas
    if not MAPS_AVAILABLE:
        st.error("❌ Sistema de mapas no disponible. Instala: pip install folium streamlit-folium")
        return
    
    if not app.map_interface:
        st.error("❌ Interface de mapas no inicializada")
        return
    
    # Información de acceso
    st.markdown(f"""
    <div class="access-granted">
        ✅ <strong>Acceso Autorizado a Mapas Épicos</strong> | Usuario: {app.user['name']} | Rol: {app.role_info['name']}
    </div>
    """, unsafe_allow_html=True)
    
    if not app.data:
        st.error("❌ No hay datos disponibles para generar mapas. Ejecuta data_collector_2025.py")
        return
    
    # Renderizar dashboard de mapas épicos con permisos del usuario
    try:
        user_permissions = app.role_info['permissions']
        
        # Verificar si el método acepta user_permissions
        try:
            app.map_interface.render_epic_maps_dashboard(app.data, user_permissions)
        except TypeError as te:
            if "takes 2 positional arguments but 3 were given" in str(te):
                st.warning("⚠️ Usando versión de mapas sin permisos diferenciados")
                app.map_interface.render_epic_maps_dashboard(app.data)
            else:
                raise te
    except Exception as e:
        st.error(f"❌ Error renderizando mapas épicos: {str(e)}")
        
        # Información de depuración para administradores
        if app.has_permission('acceso_completo'):
            with st.expander("🔧 Información de Depuración (Solo Administradores)"):
                st.code(f"Error: {str(e)}")
                st.write("**Datos disponibles:**")
                st.write(f"- Hospitales: {len(app.data.get('hospitales', []))}")
                st.write(f"- Demografia: {len(app.data.get('demografia', []))}")
                st.write(f"- Servicios: {len(app.data.get('servicios', []))}")
                st.write(f"- Accesibilidad: {len(app.data.get('accesibilidad', []))}")

if __name__ == "__main__":
    main()