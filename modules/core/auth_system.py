import streamlit as st
import pandas as pd
import bcrypt
import json
import os
from datetime import datetime, timedelta
from typing import Dict, Optional
import jwt

class HealthAuthenticator:
    def __init__(self):
        self.users_file = "data/users.json"
        self.secret_key = os.getenv("JWT_SECRET_KEY", os.getenv("JWT_SECRET", None))
        if not self.secret_key:
            raise ValueError("JWT_SECRET_KEY no configurada. Configura la variable de entorno JWT_SECRET_KEY")
        self.users_db = self.load_users()
        
        # Roles del sistema sanitario con permisos específicos y personalización
        self.roles = {
            "admin": {
                "name": "Administrador del Sistema",
                "description": "Acceso completo al sistema con capacidades de supervisión, gestión de usuarios y configuración del sistema. Puede acceder a todos los datos, funcionalidades y configuraciones.",
                "permissions": [
                    "acceso_completo",        # ✅ Acceso total
                    "gestion_usuarios",       # ✅ Gestión de usuarios
                    "configuracion_sistema",  # ✅ Configuración del sistema
                    "analisis_ia",           # ✅ Chat IA completo con Groq
                    "ver_datos",             # ✅ Dashboard con análisis avanzado
                    "reportes",              # ✅ Reportes ejecutivos completos
                    "planificacion",         # ✅ Planificación estratégica
                    "analisis_equidad",      # ✅ Análisis de equidad detallado
                    "mapas_todos",           # ✅ Todos los mapas épicos
                    "mapas_estrategicos",    # ✅ Mapas con datos estratégicos
                    "mapas_sensibles"        # ✅ Mapas con datos sensibles
                ],
                "color": "#1a365d",
                "color_secondary": "#2d3748",
                "color_accent": "#e53e3e",
                "icon": "👨‍💼",
                "theme": {
                    "primary_gradient": "linear-gradient(135deg, #1a365d 0%, #2d3748 100%)",
                    "header_style": "executive",
                    "dashboard_layout": "comprehensive",
                    "preferred_charts": ["executive_summary", "strategic_kpis", "system_overview"],
                    "sidebar_style": "expanded",
                    "welcome_message": "Panel de Control Ejecutivo",
                    "focus_areas": ["Supervisión General", "Gestión de Usuarios", "Análisis Estratégico", "Auditoría del Sistema"]
                }
            },
            "gestor": {
                "name": "Gestor Sanitario",
                "description": "Responsable de la gestión operativa del sistema sanitario. Enfocado en la planificación de recursos, análisis de capacidad hospitalaria y optimización de servicios sanitarios.",
                "permissions": [
                    "analisis_ia",           # ✅ Chat IA especializado en gestión
                    "ver_datos",             # ✅ Dashboard con métricas clave
                    "reportes",              # ✅ Reportes ejecutivos y operacionales
                    "planificacion",         # ✅ Planificación de recursos
                    "mapas_operativos",      # ✅ Mapas operativos (hospitales, cobertura)
                    "mapas_gestion"          # ✅ Mapas de gestión (tiempos, capacidad)
                    # ❌ gestion_usuarios (restringida)
                    # ❌ mapas_estrategicos (datos estratégicos)
                ],
                "color": "#2b6cb0",
                "color_secondary": "#3182ce", 
                "color_accent": "#4299e1",
                "icon": "👩‍⚕️",
                "theme": {
                    "primary_gradient": "linear-gradient(135deg, #2b6cb0 0%, #3182ce 100%)",
                    "header_style": "operational",
                    "dashboard_layout": "management",
                    "preferred_charts": ["operational_metrics", "capacity_management", "service_coverage"],
                    "sidebar_style": "compact",
                    "welcome_message": "Centro de Gestión Sanitaria",
                    "focus_areas": ["Capacidad Hospitalaria", "Tiempos de Acceso", "Cobertura de Servicios", "Planificación Operativa"]
                }
            },
            "analista": {
                "name": "Analista de Datos",
                "description": "Especialista en análisis estadístico y visualización de datos sanitarios. Enfocado en el análisis de tendencias demográficas, correlaciones y generación de insights basados en datos.",
                "permissions": [
                    "analisis_ia",           # ✅ Chat IA para análisis estadísticos
                    "ver_datos",             # ✅ Dashboard con visualizaciones avanzadas
                    "reportes",              # ✅ Reportes técnicos y estadísticos
                    "mapas_analiticos",      # ✅ Mapas estadísticos y heatmaps
                    "mapas_demograficos"     # ✅ Mapas demográficos y correlaciones
                    # ❌ planificacion (restringida)
                    # ❌ mapas_operativos (datos operativos sensibles)
                ],
                "color": "#059669",
                "color_secondary": "#10b981",
                "color_accent": "#34d399",
                "icon": "📊",
                "theme": {
                    "primary_gradient": "linear-gradient(135deg, #059669 0%, #10b981 100%)",
                    "header_style": "analytical",
                    "dashboard_layout": "data_focused",
                    "preferred_charts": ["statistical_analysis", "demographic_trends", "correlation_matrices", "data_quality"],
                    "sidebar_style": "detailed",
                    "welcome_message": "Laboratorio de Análisis de Datos",
                    "focus_areas": ["Análisis Estadístico", "Tendencias Demográficas", "Correlaciones", "Calidad de Datos"]
                }
            },
            "invitado": {
                "name": "Usuario Invitado",
                "description": "Acceso limitado a información pública del sistema sanitario. Puede visualizar datos generales y mapas públicos, pero sin acceso a análisis avanzados o datos sensibles.",
                "permissions": [
                    "ver_datos",          # ✅ Dashboard básico con métricas generales
                    "mapas_publicos"      # ✅ Mapas públicos básicos
                    # ❌ analisis_ia (sin acceso a Chat IA)
                    # ❌ reportes (sin reportes avanzados)
                    # ❌ planificacion (sin planificación)
                    # ❌ mapas_operativos (sin datos internos)
                ],
                "color": "#6b7280",
                "color_secondary": "#9ca3af",
                "color_accent": "#d1d5db",
                "icon": "👤",
                "theme": {
                    "primary_gradient": "linear-gradient(135deg, #6b7280 0%, #9ca3af 100%)",
                    "header_style": "simple",
                    "dashboard_layout": "basic",
                    "preferred_charts": ["basic_overview", "public_metrics"],
                    "sidebar_style": "minimal",
                    "welcome_message": "Portal de Información Pública",
                    "focus_areas": ["Información General", "Ubicaciones", "Datos Públicos"]
                }
            }
        }
    
    def load_users(self) -> Dict:
        """Cargar base de datos de usuarios"""
        try:
            if os.path.exists(self.users_file):
                with open(self.users_file, 'r', encoding='utf-8') as f:
                    users_data = json.load(f)
                    # Verificar que los datos son válidos
                    if isinstance(users_data, dict) and users_data:
                        return users_data
                    else:
                        print("❌ Archivo de usuarios vacío o corrupto, creando usuarios por defecto")
            
            # Crear usuarios por defecto si no existe o está corrupto
            print("🔧 Creando usuarios por defecto...")
            default_users = self.create_default_users()
            self.save_users(default_users)
            print("✅ Usuarios por defecto creados exitosamente")
            return default_users
            
        except json.JSONDecodeError as e:
            print(f"❌ Error JSON en archivo de usuarios: {str(e)}")
            # Archivo corrupto, crear backup y recrear
            if os.path.exists(self.users_file):
                backup_file = f"{self.users_file}.backup"
                os.rename(self.users_file, backup_file)
                print(f"📁 Archivo corrupto respaldado como: {backup_file}")
            
            default_users = self.create_default_users()
            self.save_users(default_users)
            return default_users
            
        except Exception as e:
            print(f"❌ Error inesperado cargando usuarios: {str(e)}")
            # Como último recurso, devolver usuarios por defecto sin guardar
            return self.create_default_users()
    
    def save_users(self, users: Dict):
        """Guardar base de datos de usuarios"""
        try:
            # Crear directorio si no existe
            os.makedirs(os.path.dirname(self.users_file), exist_ok=True)
            
            # Verificar que los datos son válidos antes de guardar
            if not isinstance(users, dict):
                raise ValueError("Los datos de usuarios deben ser un diccionario")
            
            # Guardar con formato legible
            with open(self.users_file, 'w', encoding='utf-8') as f:
                json.dump(users, f, indent=2, ensure_ascii=False)
                
            print(f"✅ Usuarios guardados exitosamente en: {self.users_file}")
            
        except Exception as e:
            error_msg = f"❌ Error guardando usuarios: {str(e)}"
            print(error_msg)
            # Solo mostrar error en Streamlit si está disponible
            try:
                st.error(error_msg)
            except:
                pass
    
    def create_default_users(self) -> Dict:
        """Crear usuarios por defecto del sistema"""
        default_users = {
            "admin": {
                "name": "Administrador Sistema",
                "email": "admin@salud-malaga.es",
                "password": self.hash_password("admin123"),
                "role": "admin",
                "organization": "Consejería de Salud",
                "created_date": datetime.now().isoformat(),
                "last_login": None,
                "active": True
            },
            "gestor.malaga": {
                "name": "Gestor Sanitario Málaga",
                "email": "gestor@sas-malaga.es", 
                "password": self.hash_password("gestor123"),
                "role": "gestor",
                "organization": "SAS Málaga",
                "created_date": datetime.now().isoformat(),
                "last_login": None,
                "active": True
            },
            "analista.datos": {
                "name": "Analista de Datos",
                "email": "analista@salud-andalucia.es",
                "password": self.hash_password("analista123"),
                "role": "analista", 
                "organization": "IECA - Instituto de Estadística",
                "created_date": datetime.now().isoformat(),
                "last_login": None,
                "active": True
            },
            "demo": {
                "name": "Usuario Demo",
                "email": "demo@demo.com",
                "password": self.hash_password("demo123"),
                "role": "invitado",
                "organization": "Demostración",
                "created_date": datetime.now().isoformat(),
                "last_login": None,
                "active": True
            }
        }
        return default_users
    
    def hash_password(self, password: str) -> str:
        """Hashear contraseña con bcrypt"""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def verify_password(self, password: str, hashed: str) -> bool:
        """Verificar contraseña"""
        try:
            return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
        except:
            return False
    
    def authenticate_user(self, username: str, password: str) -> Optional[Dict]:
        """Autenticar usuario"""
        if username in self.users_db:
            user = self.users_db[username]
            if user.get('active', True) and self.verify_password(password, user['password']):
                # Actualizar último login
                self.users_db[username]['last_login'] = datetime.now().isoformat()
                self.save_users(self.users_db)
                
                # Retornar datos del usuario sin contraseña
                user_data = user.copy()
                del user_data['password']
                user_data['username'] = username
                return user_data
        return None
    
    def create_jwt_token(self, user_data: Dict) -> str:
        """Crear token JWT para el usuario"""
        payload = {
            'username': user_data['username'],
            'role': user_data['role'],
            'exp': datetime.utcnow() + timedelta(hours=8),  # Token válido por 8 horas
            'iat': datetime.utcnow()
        }
        return jwt.encode(payload, self.secret_key, algorithm='HS256')
    
    def verify_jwt_token(self, token: str) -> Optional[Dict]:
        """Verificar token JWT"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    def has_permission(self, user_role: str, required_permission: str) -> bool:
        """Verificar si el usuario tiene un permiso específico"""
        if user_role not in self.roles:
            return False
        return required_permission in self.roles[user_role]['permissions']
    
    def get_role_info(self, role: str) -> Dict:
        """Obtener información del rol"""
        return self.roles.get(role, self.roles['invitado'])
    
    def register_user(self, username: str, user_data: Dict) -> bool:
        """Registrar nuevo usuario (solo admin)"""
        try:
            if username not in self.users_db:
                user_data['password'] = self.hash_password(user_data['password'])
                user_data['created_date'] = datetime.now().isoformat()
                user_data['last_login'] = None
                user_data['active'] = True
                
                self.users_db[username] = user_data
                self.save_users(self.users_db)
                return True
            return False
        except Exception as e:
            st.error(f"Error registrando usuario: {str(e)}")
            return False
    
    def update_user(self, username: str, updates: Dict) -> bool:
        """Actualizar datos de usuario"""
        try:
            if username in self.users_db:
                for key, value in updates.items():
                    if key == 'password':
                        value = self.hash_password(value)
                    self.users_db[username][key] = value
                
                self.save_users(self.users_db)
                return True
            return False
        except Exception as e:
            st.error(f"Error actualizando usuario: {str(e)}")
            return False
    
    def deactivate_user(self, username: str) -> bool:
        """Desactivar usuario"""
        return self.update_user(username, {'active': False})

    def activate_user(self, username: str) -> bool:
        """Activar usuario"""
        return self.update_user(username, {'active': True})

    def delete_user(self, username: str) -> bool:
        """Eliminar usuario permanentemente"""
        try:
            if username in self.users_db:
                # No permitir eliminar el último admin
                if self.users_db[username].get('role') == 'admin':
                    admin_count = sum(1 for user in self.users_db.values() if user.get('role') == 'admin' and user.get('active', True))
                    if admin_count <= 1:
                        st.error("❌ No se puede eliminar el último administrador del sistema")
                        return False

                del self.users_db[username]
                self.save_users(self.users_db)
                return True
            return False
        except Exception as e:
            st.error(f"Error eliminando usuario: {str(e)}")
            return False
    
    def get_all_users(self) -> Dict:
        """Obtener todos los usuarios (sin contraseñas)"""
        users_safe = {}
        for username, user_data in self.users_db.items():
            user_safe = user_data.copy()
            del user_safe['password']
            user_safe['username'] = username
            users_safe[username] = user_safe
        return users_safe

def render_login_page():
    """Renderizar página de login"""

    # FORZAR RECARGA COMPLETA si viene de logout (para limpiar CSS del DOM)
    # Simplemente mostrar mensaje y dejar que el usuario haga login de nuevo
    # El CSS ya se carga solo cuando está autenticado, así que el login debería verse limpio
    if st.session_state.get('force_reload_after_logout', False):
        # Limpiar la flag
        del st.session_state['force_reload_after_logout']

        # Mensaje opcional indicando que se cerró sesión
        # (El login normal se renderizará después)

    # Inicializar tema si no existe
    if 'theme_mode' not in st.session_state:
        st.session_state.theme_mode = 'light'

    current_theme = st.session_state.get('theme_mode', 'light')

    # CSS para la página de login
    from datetime import datetime
    # ===== CARGAR CSS EXTERNO (Optimización Fase 1) =====
    # En lugar de CSS inline, cargar desde archivo externo (cacheable)
    import os
    css_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'assets', 'login.min.css')

    if os.path.exists(css_file):
        with open(css_file, 'r', encoding='utf-8') as f:
            login_css = f.read()
        # Agregar marca de tiempo para forzar recarga de CSS (evitar caché navegador)
        import time
        cache_buster = f"/* CSS Version: {int(time.time())} - Padding Fix Applied */"
        st.markdown(f'<style>{cache_buster}\n{login_css}</style>', unsafe_allow_html=True)
    else:
        # Fallback: usar CSS básico si el archivo no existe
        st.markdown("""
        <style>
        .login-container { max-width: 400px; margin: 2rem auto; padding: 2rem; }
        .stTextInput input { background: white !important; color: #1a202c !important; }
        </style>
        """, unsafe_allow_html=True)

    # CSS INLINE ADICIONAL para sobrescribir padding (máxima prioridad)
    st.markdown("""
    <style>
    /* FIX URGENTE: Limitar ancho del contenedor principal del login */
    .stMainBlockContainer,
    [class*="block-container"] {
        max-width: 460px !important;
        margin: 0 auto !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        padding-top: 1rem !important;
    }

    /* Asegurar que el login-container esté centrado con ancho correcto */
    .login-container {
        max-width: 420px !important;
        margin: 0 auto !important;
    }
    </style>
    <script>
    // JAVASCRIPT PARA FORZAR ANCHO CORRECTO DEL LOGIN - Ejecutar después de carga
    (function() {
        function fixLoginWidth() {
            console.log('🔧 Aplicando fix de ancho del login...');

            // Seleccionar el contenedor principal (Streamlit usa .stMainBlockContainer)
            const blockContainer = document.querySelector('.stMainBlockContainer') ||
                                 document.querySelector('[class*="block-container"]');

            if (blockContainer) {
                blockContainer.style.setProperty('max-width', '460px', 'important');
                blockContainer.style.setProperty('margin', '0 auto', 'important');
                blockContainer.style.setProperty('padding-left', '1rem', 'important');
                blockContainer.style.setProperty('padding-right', '1rem', 'important');
                blockContainer.style.setProperty('padding-top', '1rem', 'important');
                console.log('✅ Ancho limitado a 460px en .stMainBlockContainer');
            } else {
                console.warn('⚠️ No se encontró .stMainBlockContainer');
            }

            // Asegurar login container centrado
            const loginContainer = document.querySelector('.login-container');
            if (loginContainer) {
                loginContainer.style.setProperty('max-width', '420px', 'important');
                loginContainer.style.setProperty('margin', '0 auto', 'important');
                console.log('✅ Estilos aplicados a .login-container');
            }

            // Forzar ancho en todos los elementos hijos directos del block-container
            if (blockContainer) {
                const blockContainerChildren = blockContainer.querySelectorAll(':scope > *');
                blockContainerChildren.forEach(child => {
                    child.style.setProperty('max-width', '100%', 'important');
                });
                console.log('✅ Ancho aplicado a hijos del contenedor');
            }
        }

        // Ejecutar inmediatamente
        fixLoginWidth();

        // Ejecutar cuando el DOM esté listo
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', fixLoginWidth);
        } else {
            fixLoginWidth();
        }

        // Ejecutar después de delays (por si Streamlit carga después)
        setTimeout(fixLoginWidth, 100);
        setTimeout(fixLoginWidth, 500);
        setTimeout(fixLoginWidth, 1000);
        setTimeout(fixLoginWidth, 2000);

        // Observar cambios en el DOM por si Streamlit reenderiza
        const observer = new MutationObserver(fixLoginWidth);
        observer.observe(document.body, { childList: true, subtree: true });
    })();
    </script>
    """, unsafe_allow_html=True)

    # JAVASCRIPT SIMPLE PARA FORZAR TEMAS
    st.markdown("""
        <script>
        function applyThemeStyles() {
            const isDark = document.body.getAttribute('data-theme') === 'dark' ||
                          document.documentElement.getAttribute('data-theme') === 'dark';

            // Obtener TODOS los elementos
            const allElements = document.querySelectorAll('*');

            allElements.forEach(el => {
                const tagName = el.tagName.toLowerCase();

                if (isDark) {
                    // MODO OSCURO - TEXTO BLANCO
                    if (tagName === 'input' || tagName === 'textarea' || tagName === 'select') {
                        el.style.setProperty('background', '#334155', 'important');
                        el.style.setProperty('color', '#ffffff', 'important');
                        el.style.setProperty('border', '1px solid #6b7280', 'important');
                    } else {
                        el.style.setProperty('color', '#ffffff', 'important');
                    }
                } else {
                    // MODO CLARO - TEXTO NEGRO
                    if (tagName === 'input' || tagName === 'textarea' || tagName === 'select') {
                        el.style.setProperty('background', '#ffffff', 'important');
                        el.style.setProperty('color', '#000000', 'important');
                        el.style.setProperty('border', '1px solid #d1d5db', 'important');
                    } else {
                        el.style.setProperty('color', '#000000', 'important');
                    }
                }
            });
        }

        // Ejecutar inmediatamente
        applyThemeStyles();

        // Ejecutar cuando cargue el DOM
        document.addEventListener('DOMContentLoaded', applyThemeStyles);

        // Detectar cambios en el atributo data-theme
        try {
            const observer = new MutationObserver(function(mutations) {
                let themeChanged = false;
                mutations.forEach(function(mutation) {
                    if (mutation.type === 'attributes' &&
                        mutation.attributeName === 'data-theme') {
                        themeChanged = true;
                    }
                });
                if (themeChanged) {
                    setTimeout(applyThemeStyles, 50);
                }
            });

            // Observar cambios en body y html (validar que existen)
            if (document.body && document.body.nodeType === 1) {
                observer.observe(document.body, { attributes: true, attributeFilter: ['data-theme'] });
            }
            if (document.documentElement && document.documentElement.nodeType === 1) {
                observer.observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });
            }
        } catch(e) {
            console.warn('⚠️ No se pudo inicializar MutationObserver en login:', e);
        }
        </script>
        """, unsafe_allow_html=True)

    # ===== FORMULARIO DE LOGIN =====
    # Crear contenedor con estilos inline para temas
    if current_theme == 'dark':
        container_bg = '#1e293b'
        container_shadow = '0 10px 40px rgba(0, 0, 0, 0.3), 0 2px 8px rgba(0, 0, 0, 0.2)'
        container_border = '1px solid #374151'
        header_bg = 'linear-gradient(135deg, #1e293b 0%, #0f172a 100%)'
        header_color = '#ffffff'
        subtitle_color = '#ffffff'
        text_color = '#ffffff'
        form_bg = '#1e293b'
    else:
        container_bg = '#ffffff'
        container_shadow = '0 10px 40px rgba(0, 0, 0, 0.1), 0 2px 8px rgba(0, 0, 0, 0.06)'
        container_border = '1px solid rgba(0, 0, 0, 0.05)'
        header_bg = 'linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%)'
        header_color = '#1a202c'
        subtitle_color = '#4a5568'
        text_color = '#718096'
        form_bg = '#ffffff'

    st.markdown(f"""
    <div class="login-container" style="max-width: 420px; margin: 0 auto; background: {container_bg}; border-radius: 24px; box-shadow: {container_shadow}; border: {container_border};">
        <div class="login-header" style="background: {header_bg}; padding: 32px; border-radius: 24px 24px 0 0; text-align: center;">
            <div style="color: {header_color} !important; font-size: 32px; font-weight: 700; margin-bottom: 8px;">🏥 Copilot Salud</div>
            <div style="color: {subtitle_color} !important; font-size: 18px; font-weight: 500; margin: 8px 0;">Sistema de Análisis Sociosanitario</div>
            <div style="color: {text_color} !important; font-size: 14px; margin-top: 8px;">Provincia de Málaga - Andalucía</div>
        </div>
        <div class="login-form-container" style="padding: 32px; background: {form_bg};">
    """, unsafe_allow_html=True)

    # Título "Iniciar Sesión" con botón de tema a la derecha
    col_title, col_theme = st.columns([5, 1])
    with col_title:
        st.markdown("#### 🔐 Iniciar Sesión")
    with col_theme:
        theme_icon = "🌙" if current_theme == 'light' else "☀️"
        if st.button(theme_icon, key="login_theme_toggle", help="Cambiar tema", use_container_width=True):
            new_theme = 'dark' if current_theme == 'light' else 'light'
            st.session_state.theme_mode = new_theme
            st.rerun()

    # Formulario de login
    with st.form("login_form"):
        username = st.text_input("👤 Usuario", placeholder="Ingresa tu usuario")
        password = st.text_input("🔑 Contraseña", type="password", placeholder="Ingresa tu contraseña")

        col1, col2 = st.columns(2)
        with col1:
            login_button = st.form_submit_button("🚀 Iniciar Sesión", use_container_width=True)
        with col2:
            demo_button = st.form_submit_button("👤 Acceso Demo", use_container_width=True)

    # Procesar login
    if login_button or demo_button:
        auth = HealthAuthenticator()

        # Si es demo, usar credenciales demo
        if demo_button:
            username = "demo"
            password = "demo123"

        if username and password:
            user = auth.authenticate_user(username, password)
            if user:
                # Crear token y guardar en session state
                token = auth.create_jwt_token(user)
                st.session_state.auth_token = token
                st.session_state.user = user
                st.session_state.authenticated = True

                # Mensaje de éxito
                role_info = auth.get_role_info(user['role'])
                st.success(f"✅ Bienvenido **{user['name']}** | Rol: {role_info['icon']} {role_info['name']}")
                st.rerun()
            else:
                st.error("❌ Usuario o contraseña incorrectos")
        else:
            st.warning("⚠️ Por favor ingresa usuario y contraseña")

    # Mostrar credenciales demo
    st.markdown("""
    <div class="demo-credentials">
        <h4>🎯 Credenciales de Demostración</h4>
        <p><strong>Administrador:</strong> admin / admin123</p>
        <p><strong>Gestor:</strong> gestor.malaga / gestor123</p>
        <p><strong>Analista:</strong> analista.datos / analista123</p>
        <p><strong>Demo:</strong> demo / demo123</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("</div></div>", unsafe_allow_html=True)

    # Información de roles
    st.markdown('<div class="roles-section">', unsafe_allow_html=True)
    st.markdown("### 👥 Roles del Sistema")

    auth = HealthAuthenticator()

    # Diccionario de traducción de permisos para la pantalla de login
    permission_translations = {
        'full_access': 'Acceso Total',
        'user_management': 'Gestión de Usuarios',
        'system_config': 'Configuración del Sistema',
        'analytics': 'Análisis Avanzado',
        'reports': 'Reportes',
        'planning': 'Planificación',
        'view_data': 'Visualización de Datos',
        'basic_analytics': 'Análisis Básico',
        'analisis_equidad': 'Análisis de Equidad'
    }

    for role_key, role_info in auth.roles.items():
        # Traducir permisos al español
        translated_permissions = [permission_translations.get(perm, perm) for perm in role_info['permissions']]
        permissions_text = ", ".join(translated_permissions)

        st.markdown(f"""
        <div style="background: #ffffff; padding: 1rem; border-radius: 12px; margin: 0.75rem 0; border: 1px solid rgba(0, 0, 0, 0.1); box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);">
            <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                <span style="font-size: 1.2rem; margin-right: 0.5rem;">{role_info['icon']}</span>
                <strong style="color: {role_info['color']}; font-size: 0.95rem;">{role_info['name']}</strong>
            </div>
            <small style="color: #4a5568; font-size: 0.8rem;">Permisos: {permissions_text}</small>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

def render_user_management():
    """Panel de gestión de usuarios (solo admin)"""

    if not st.session_state.get('authenticated') or st.session_state.user['role'] != 'admin':
        st.error("❌ Acceso denegado. Solo administradores pueden gestionar usuarios.")
        return

    st.markdown("### 👥 Gestión de Usuarios")

    auth = HealthAuthenticator()

    tab1, tab2, tab3, tab4 = st.tabs(["📋 Lista de Usuarios", "➕ Crear Usuario", "✏️ Editar Usuario", "🗑️ Eliminar Usuario"])

    with tab1:
        st.markdown("#### 📋 Usuarios Registrados")

        try:
            users = auth.get_all_users()
            users_data = []

            if not users:
                st.warning("⚠️ No hay usuarios registrados en el sistema.")
                return

            for username, user in users.items():
                try:
                    role_info = auth.get_role_info(user.get('role', 'viewer'))
                    users_data.append({
                        'Usuario': username,
                        'Nombre': user.get('name', 'N/A'),
                        'Email': user.get('email', 'N/A'),
                        'Rol': f"{role_info['icon']} {role_info['name']}",
                        'Organización': user.get('organization', 'N/A'),
                        'Último Acceso': user['last_login'][:10] if user.get('last_login') else 'Nunca',
                        'Estado': '🟢 Activo' if user.get('active', True) else '🔴 Inactivo'
                    })
                except Exception as e:
                    st.error(f"❌ Error procesando usuario {username}: {str(e)}")
                    continue

            if users_data:
                users_df = pd.DataFrame(users_data)
                st.dataframe(users_df, width="stretch")

                # Mostrar estadísticas
                st.markdown("##### 📊 Estadísticas")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("👥 Total Usuarios", len(users_data))
                with col2:
                    active_users = len([u for u in users_data if u['Estado'] == '🟢 Activo'])
                    st.metric("🟢 Usuarios Activos", active_users)
                with col3:
                    roles_count = len(set([u['Rol'] for u in users_data]))
                    st.metric("🎭 Roles Únicos", roles_count)
            else:
                st.warning("⚠️ No se pudieron cargar los datos de usuarios.")

        except Exception as e:
            st.error(f"❌ Error cargando usuarios: {str(e)}")
            st.info("💡 Verifica que el archivo de usuarios esté correctamente configurado.")

    with tab2:
        st.markdown("#### ➕ Crear Nuevo Usuario")

        with st.form("create_user_form"):
            col1, col2 = st.columns(2)

            with col1:
                new_username = st.text_input("👤 Usuario")
                new_name = st.text_input("📝 Nombre Completo")
                new_email = st.text_input("📧 Email")

            with col2:
                new_role = st.selectbox("👔 Rol", list(auth.roles.keys()),
                                       format_func=lambda x: f"{auth.roles[x]['icon']} {auth.roles[x]['name']}")
                new_organization = st.text_input("🏢 Organización")
                new_password = st.text_input("🔑 Contraseña", type="password")

            if st.form_submit_button("➕ Crear Usuario"):
                if all([new_username, new_name, new_email, new_password]):
                    user_data = {
                        'name': new_name,
                        'email': new_email,
                        'role': new_role,
                        'organization': new_organization,
                        'password': new_password
                    }

                    if auth.register_user(new_username, user_data):
                        st.success(f"✅ Usuario {new_username} creado exitosamente")
                        st.rerun()
                    else:
                        st.error("❌ Error creando usuario. Puede que ya exista.")
                else:
                    st.warning("⚠️ Por favor completa todos los campos")

    with tab3:
        st.markdown("#### ✏️ Editar Usuario Existente")

        users = auth.get_all_users()
        if not users:
            st.warning("⚠️ No hay usuarios para editar.")
            return

        # Selector de usuario a editar
        user_to_edit = st.selectbox(
            "👤 Seleccionar Usuario a Editar",
            list(users.keys()),
            format_func=lambda x: f"{x} - {users[x]['name']}"
        )

        if user_to_edit:
            current_user = users[user_to_edit]

            st.markdown(f"##### Editando usuario: **{user_to_edit}**")

            with st.form("edit_user_form"):
                col1, col2 = st.columns(2)

                with col1:
                    edit_name = st.text_input("📝 Nombre Completo", value=current_user.get('name', ''))
                    edit_email = st.text_input("📧 Email", value=current_user.get('email', ''))
                    edit_organization = st.text_input("🏢 Organización", value=current_user.get('organization', ''))

                with col2:
                    current_role_index = list(auth.roles.keys()).index(current_user.get('role', 'invitado'))
                    edit_role = st.selectbox(
                        "👔 Rol",
                        list(auth.roles.keys()),
                        index=current_role_index,
                        format_func=lambda x: f"{auth.roles[x]['icon']} {auth.roles[x]['name']}"
                    )

                    edit_active = st.checkbox("✅ Usuario Activo", value=current_user.get('active', True))
                    edit_password = st.text_input("🔑 Nueva Contraseña (dejar vacío para mantener)", type="password", placeholder="Solo si quieres cambiarla")

                col_save, col_cancel = st.columns(2)
                with col_save:
                    save_changes = st.form_submit_button("💾 Guardar Cambios", type="primary")
                with col_cancel:
                    reset_password = st.form_submit_button("🔑 Solo Cambiar Contraseña")

                if save_changes:
                    updates = {
                        'name': edit_name,
                        'email': edit_email,
                        'role': edit_role,
                        'organization': edit_organization,
                        'active': edit_active
                    }

                    if edit_password:
                        updates['password'] = edit_password

                    if auth.update_user(user_to_edit, updates):
                        st.success(f"✅ Usuario {user_to_edit} actualizado exitosamente")
                        st.rerun()
                    else:
                        st.error("❌ Error actualizando usuario")

                if reset_password:
                    if edit_password:
                        if auth.update_user(user_to_edit, {'password': edit_password}):
                            st.success(f"✅ Contraseña de {user_to_edit} actualizada exitosamente")
                            st.rerun()
                        else:
                            st.error("❌ Error actualizando contraseña")
                    else:
                        st.warning("⚠️ Ingresa una nueva contraseña")

    with tab4:
        st.markdown("#### 🗑️ Eliminar Usuario")

        users = auth.get_all_users()
        if not users:
            st.warning("⚠️ No hay usuarios para eliminar.")
            return

        st.warning("⚠️ **ATENCIÓN**: Esta acción es irreversible. El usuario será eliminado permanentemente del sistema.")

        # Selector de usuario a eliminar
        user_to_delete = st.selectbox(
            "👤 Seleccionar Usuario a Eliminar",
            [""] + list(users.keys()),
            format_func=lambda x: f"{x} - {users[x]['name']}" if x and x in users else "-- Seleccionar Usuario --"
        )

        if user_to_delete:
            current_user = users[user_to_delete]
            role_info = auth.get_role_info(current_user.get('role', 'invitado'))

            # Mostrar información del usuario a eliminar
            st.markdown(f"""
            <div style="background: #fff5f5; padding: 1rem; border-radius: 10px; border: 2px solid #fc8181; margin: 1rem 0;">
                <h4>🗑️ Usuario a Eliminar</h4>
                <p><strong>👤 Usuario:</strong> {user_to_delete}</p>
                <p><strong>📝 Nombre:</strong> {current_user.get('name', 'N/A')}</p>
                <p><strong>📧 Email:</strong> {current_user.get('email', 'N/A')}</p>
                <p><strong>👔 Rol:</strong> {role_info['icon']} {role_info['name']}</p>
                <p><strong>🏢 Organización:</strong> {current_user.get('organization', 'N/A')}</p>
                <p><strong>📅 Último Acceso:</strong> {current_user.get('last_login', 'Nunca')[:10] if current_user.get('last_login') else 'Nunca'}</p>
            </div>
            """, unsafe_allow_html=True)

            # Verificar si es administrador
            if current_user.get('role') == 'admin':
                admin_count = sum(1 for user in users.values() if user.get('role') == 'admin' and user.get('active', True))
                if admin_count <= 1:
                    st.error("❌ No se puede eliminar el último administrador del sistema")
                    return
                else:
                    st.warning(f"⚠️ Hay {admin_count} administradores. Se puede eliminar este usuario.")

            # Confirmación de eliminación
            st.markdown("##### ✋ Confirmación de Eliminación")
            confirmation_text = st.text_input(
                f"Escribe **{user_to_delete}** para confirmar la eliminación:",
                placeholder=f"Escribe: {user_to_delete}"
            )

            col1, col2 = st.columns(2)

            with col1:
                if st.button("🗑️ ELIMINAR USUARIO", type="primary", disabled=(confirmation_text != user_to_delete)):
                    if confirmation_text == user_to_delete:
                        if auth.delete_user(user_to_delete):
                            st.success(f"✅ Usuario {user_to_delete} eliminado exitosamente")
                            st.balloons()
                            st.rerun()
                        else:
                            st.error("❌ Error eliminando usuario")
                    else:
                        st.error("❌ Confirmación incorrecta")

            with col2:
                # Opción alternativa: desactivar en lugar de eliminar
                if st.button("🔒 Solo Desactivar Usuario"):
                    if auth.deactivate_user(user_to_delete):
                        st.success(f"✅ Usuario {user_to_delete} desactivado exitosamente")
                        st.rerun()
                    else:
                        st.error("❌ Error desactivando usuario")

def render_user_profile():
    """Renderizar perfil de usuario"""
    if not st.session_state.get('authenticated'):
        return
    
    user = st.session_state.user
    auth = HealthAuthenticator()
    role_info = auth.get_role_info(user['role'])
    
    st.markdown("### 👤 Mi Perfil")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown(f"""
        <div style="text-align: center; padding: 1rem; background: linear-gradient(135deg, {role_info['color']}20, {role_info['color']}10); border-radius: 15px; border: 2px solid {role_info['color']}40;">
            <div style="font-size: 4rem;">{role_info['icon']}</div>
            <h3>{user['name']}</h3>
            <p style="color: {role_info['color']}; font-weight: bold;">{role_info['name']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### 📊 Información del Usuario")
        st.write(f"**👤 Usuario:** {user['username']}")
        st.write(f"**📧 Email:** {user['email']}")
        st.write(f"**🏢 Organización:** {user['organization']}")
        st.write(f"**📅 Último Acceso:** {user['last_login'][:16] if user['last_login'] else 'Primer acceso'}")
        
        # Información específica del rol
        st.markdown("#### 🎭 Información del Rol")
        st.write(f"**🎯 Descripción:** {role_info.get('description', 'Sin descripción disponible')}")
        
        # Áreas de enfoque del rol
        theme = role_info.get('theme', {})
        focus_areas = theme.get('focus_areas', [])
        if focus_areas:
            st.markdown("**🎯 Áreas de Enfoque:**")
            for i, area in enumerate(focus_areas, 1):
                st.write(f"{i}. {area}")
        
        # Mensaje de bienvenida personalizado
        welcome_msg = theme.get('welcome_message', 'Bienvenido al sistema')
        st.info(f"💬 {welcome_msg}")
        
        st.markdown("#### 🔐 Permisos")
        permissions = role_info['permissions']
        
        # Mapeo de permisos con iconos y descripciones
        permission_names = {
            # Permisos generales
            'acceso_completo': '🔓 Acceso Total',
            'gestion_usuarios': '👥 Gestión de Usuarios',
            'configuracion_sistema': '⚙️ Configuración del Sistema',
            'analisis_ia': '🤖 Análisis con IA',
            'ver_datos': '👀 Visualización de Datos',
            'reportes': '📋 Reportes Avanzados',
            'planificacion': '🗺️ Planificación Estratégica',
            'analisis_equidad': '⚖️ Análisis de Equidad',
            
            # Permisos de mapas
            'mapas_todos': '🌟 Todos los Mapas',
            'mapas_estrategicos': '🎯 Mapas Estratégicos',
            'mapas_sensibles': '🔒 Mapas con Datos Sensibles',
            'mapas_operativos': '🏥 Mapas Operativos',
            'mapas_gestion': '📊 Mapas de Gestión',
            'mapas_analiticos': '📈 Mapas Analíticos',
            'mapas_demograficos': '👥 Mapas Demográficos',
            'mapas_publicos': '🌐 Mapas Públicos'
        }
        
        # Separar permisos generales y de mapas
        general_perms = []
        map_perms = []
        
        for perm in permissions:
            if perm.startswith('mapas_'):
                display_name = permission_names.get(perm, perm)
                map_perms.append(display_name)
            else:
                display_name = permission_names.get(perm, perm)
                general_perms.append(display_name)
        
        # Mostrar permisos generales
        if general_perms:
            st.markdown("**🔧 Permisos Generales:**")
            for perm_display in general_perms:
                st.markdown(f"• {perm_display}")
        
        # Mostrar permisos de mapas
        if map_perms:
            st.markdown("**🗺️ Permisos de Mapas:**")
            for perm_display in map_perms:
                st.markdown(f"• {perm_display}")

def check_authentication():
    """Verificar si el usuario está autenticado"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    if 'auth_token' in st.session_state and not st.session_state.authenticated:
        # Verificar token JWT
        auth = HealthAuthenticator()
        token_data = auth.verify_jwt_token(st.session_state.auth_token)
        
        if token_data:
            # Token válido, restaurar sesión
            username = token_data['username']
            if username in auth.users_db:
                user = auth.users_db[username].copy()
                del user['password']
                user['username'] = username
                st.session_state.user = user
                st.session_state.authenticated = True
        else:
            # Token expirado o inválido
            if 'auth_token' in st.session_state:
                del st.session_state.auth_token
            st.session_state.authenticated = False
    
    return st.session_state.authenticated

def logout():
    """Cerrar sesión y limpiar completamente el estado"""
    # LIMPIAR TODO el session_state para eliminar CSS residual
    keys_to_delete = list(st.session_state.keys())
    for key in keys_to_delete:
        del st.session_state[key]

    # FORZAR tema LIGHT SIEMPRE al hacer logout
    st.session_state.theme_mode = 'light'
    st.session_state.authenticated = False
    st.session_state.user = None

    # Marcar que se hizo logout para aplicar reset CSS
    st.session_state['force_reload_after_logout'] = True

    # Forzar rerun para aplicar CSS de reset
    st.rerun()