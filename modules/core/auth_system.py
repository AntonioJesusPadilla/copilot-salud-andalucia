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

    # Inicializar tema si no existe
    if 'theme_mode' not in st.session_state:
        st.session_state.theme_mode = 'light'

    current_theme = st.session_state.get('theme_mode', 'light')

    # Botón de tema en login - parte superior derecha
    theme_icon = "🌙" if current_theme == 'light' else "☀️"
    theme_text = "Oscuro" if current_theme == 'light' else "Claro"

    col1, col2, col3 = st.columns([1, 4, 1])
    with col3:
        if st.button(f"{theme_icon} {theme_text}", key="login_theme_btn", use_container_width=True):
            new_theme = 'dark' if current_theme == 'light' else 'light'
            st.session_state.theme_mode = new_theme
            st.rerun()

    # CSS para la página de login
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")

    # Aplicar CSS básico primero
    st.markdown("""
    <style>
    /* CSS ACTUALIZADO - {timestamp} */
        /* ========== OCULTAR SIDEBAR EN LOGIN ========== */
        [data-testid="stSidebar"],
        .stSidebar,
        section[data-testid="stSidebar"] {
            display: none !important;
            visibility: hidden !important;
            width: 0 !important;
        }

        /* Expandir el contenido principal para ocupar todo el ancho */
        .main .block-container {
            max-width: 100% !important;
            padding-left: 5rem !important;
            padding-right: 5rem !important;
        }

        .login-container {
            max-width: 420px;
            margin: 0 auto;
            padding: 0;
            background: #ffffff;
            border-radius: 24px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1), 0 2px 8px rgba(0, 0, 0, 0.06);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(0, 0, 0, 0.05);
            overflow: hidden;
        }
        
        .login-header {
            text-align: center;
            color: #1a202c;
            padding: 2.5rem 2rem 1.5rem 2rem;
            background: linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%);
            position: relative;
        }
        
        .login-header::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 50%;
            transform: translateX(-50%);
            width: 60px;
            height: 3px;
            background: linear-gradient(135deg, #00a86b 0%, #4CAF50 100%);
            border-radius: 2px;
        }
        
        .login-header h1 {
            font-size: 2rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
            color: #1a202c;
            letter-spacing: -0.01em;
        }
        
        .login-header h3 {
            font-size: 1rem;
            font-weight: 400;
            margin-bottom: 0.25rem;
            color: #4a5568;
            opacity: 0.8;
        }
        
        .login-header p {
            font-size: 0.85rem;
            color: #718096;
            margin: 0;
            font-weight: 400;
        }
        
        .login-form-container {
            padding: 2rem;
        }
        
        .demo-credentials {
            background: linear-gradient(135deg, #f0fff4 0%, #e6fffa 100%);
            padding: 1.5rem;
            border-radius: 12px;
            color: #1a202c;
            margin-top: 1.5rem;
            border: 1px solid rgba(76, 175, 80, 0.2);
            position: relative;
        }
        
        .demo-credentials::before {
            content: '🎯';
            position: absolute;
            top: 1rem;
            right: 1rem;
            font-size: 1.2rem;
            opacity: 0.6;
        }
        
        .demo-credentials h4 {
            color: #00a86b;
            margin-bottom: 1rem;
            font-size: 0.95rem;
            font-weight: 600;
        }
        
        .demo-credentials p {
            margin: 0.5rem 0;
            font-size: 0.85rem;
            color: #4a5568;
        }
        
        .user-role-badge {
            display: inline-block;
            padding: 0.5rem 1rem;
            border-radius: 12px;
            font-size: 0.8rem;
            font-weight: 500;
            margin: 0.25rem;
            border: 1px solid rgba(0, 0, 0, 0.1);
            background: #ffffff;
        }
        
        .roles-section {
            margin-top: 2rem;
            padding: 1.5rem;
            background: #fafafa;
            border-radius: 12px;
        }
        
        .roles-section h3 {
            color: #1a202c;
            font-size: 1.1rem;
            font-weight: 600;
            margin-bottom: 1rem;
            text-align: center;
        }

        /* ========== MODO OSCURO ========== */
        [data-theme="dark"] .login-container,
        body[data-theme="dark"] .login-container {
            background: #1e293b !important;
            border: 1px solid #374151 !important;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3), 0 2px 8px rgba(0, 0, 0, 0.2) !important;
        }

        [data-theme="dark"] .login-header,
        body[data-theme="dark"] .login-header {
            background: linear-gradient(135deg, #334155 0%, #1e293b 100%) !important;
            color: #f9fafb !important;
        }

        [data-theme="dark"] .login-header h1,
        body[data-theme="dark"] .login-header h1 {
            color: #f9fafb !important;
        }

        [data-theme="dark"] .login-header h3,
        body[data-theme="dark"] .login-header h3 {
            color: #d1d5db !important;
        }

        [data-theme="dark"] .login-header p,
        body[data-theme="dark"] .login-header p {
            color: #9ca3af !important;
        }

        [data-theme="dark"] .login-form-container,
        body[data-theme="dark"] .login-form-container {
            background: #1e293b !important;
        }

        [data-theme="dark"] .demo-credentials,
        body[data-theme="dark"] .demo-credentials {
            background: linear-gradient(135deg, #065f46 0%, #047857 100%) !important;
            border: 1px solid rgba(52, 211, 153, 0.3) !important;
            color: #f9fafb !important;
        }

        [data-theme="dark"] .demo-credentials h4,
        body[data-theme="dark"] .demo-credentials h4 {
            color: #34d399 !important;
        }

        [data-theme="dark"] .demo-credentials p,
        body[data-theme="dark"] .demo-credentials p {
            color: #e5e7eb !important;
        }

        [data-theme="dark"] .roles-section,
        body[data-theme="dark"] .roles-section {
            background: #334155 !important;
        }

        [data-theme="dark"] .roles-section h3,
        body[data-theme="dark"] .roles-section h3 {
            color: #f9fafb !important;
        }

        [data-theme="dark"] .user-role-badge,
        body[data-theme="dark"] .user-role-badge {
            background: #1e293b !important;
            border: 1px solid #4b5563 !important;
            color: #e5e7eb !important;
        }

        /* Estilos para elementos de Streamlit en modo oscuro */
        [data-theme="dark"] .login-container .stButton > button,
        body[data-theme="dark"] .login-container .stButton > button {
            background: #334155 !important;
            color: #f9fafb !important;
            border: 1px solid #4b5563 !important;
        }

        [data-theme="dark"] .login-container .stButton > button:hover,
        body[data-theme="dark"] .login-container .stButton > button:hover {
            background: #4b5563 !important;
            border-color: #6b7280 !important;
        }

        [data-theme="dark"] .login-container .stTextInput > div > div > input,
        body[data-theme="dark"] .login-container .stTextInput > div > div > input {
            background: #334155 !important;
            color: #f9fafb !important;
            border: 1px solid #4b5563 !important;
        }

        [data-theme="dark"] .login-container .stTextInput > div > div > input:focus,
        body[data-theme="dark"] .login-container .stTextInput > div > div > input:focus {
            border-color: #6b7280 !important;
        }

        [data-theme="dark"] .login-container label,
        body[data-theme="dark"] .login-container label {
            color: #f9fafb !important;
        }

        [data-theme="dark"] .login-container .stMarkdown h4,
        body[data-theme="dark"] .login-container .stMarkdown h4 {
            color: #f9fafb !important;
        }

        /* TARJETAS DE ROLES EN MODO OSCURO - MÁS AGRESIVO */
        [data-theme="dark"] div[style*="background: #ffffff"],
        [data-theme="dark"] div[style*="background:#ffffff"],
        [data-theme="dark"] .role-card-login,
        body[data-theme="dark"] div[style*="background: #ffffff"],
        body[data-theme="dark"] div[style*="background:#ffffff"],
        body[data-theme="dark"] .role-card-login {
            background: #334155 !important;
            border: 2px solid #6b7280 !important;
            color: #f9fafb !important;
            box-shadow: 0 4px 8px rgba(0,0,0,0.3) !important;
        }

        [data-theme="dark"] div[style*="background: #ffffff"] *,
        [data-theme="dark"] div[style*="background:#ffffff"] *,
        [data-theme="dark"] .role-card-login *,
        body[data-theme="dark"] div[style*="background: #ffffff"] *,
        body[data-theme="dark"] div[style*="background:#ffffff"] *,
        body[data-theme="dark"] .role-card-login * {
            color: #f9fafb !important;
        }

        [data-theme="dark"] div[style*="background: #ffffff"] strong,
        [data-theme="dark"] div[style*="background:#ffffff"] strong,
        body[data-theme="dark"] div[style*="background: #ffffff"] strong,
        body[data-theme="dark"] div[style*="background:#ffffff"] strong {
            color: #ffffff !important;
            font-weight: 700 !important;
        }

        [data-theme="dark"] div[style*="background: #ffffff"] small,
        [data-theme="dark"] div[style*="background:#ffffff"] small,
        body[data-theme="dark"] div[style*="background: #ffffff"] small,
        body[data-theme="dark"] div[style*="background:#ffffff"] small {
            color: #e5e7eb !important;
            opacity: 0.9 !important;
        }

        /* FORZAR TODOS LOS DIV CON ESTILOS INLINE EN MODO OSCURO */
        [data-theme="dark"] div[style],
        body[data-theme="dark"] div[style] {
            background: #334155 !important;
            color: #f9fafb !important;
        }

        /* FORZAR VISIBILIDAD DE ELEMENTOS STREAMLIT EN MODO OSCURO */
        [data-theme="dark"] .login-container *,
        body[data-theme="dark"] .login-container * {
            color: #f9fafb !important;
        }

        [data-theme="dark"] .login-container input,
        [data-theme="dark"] .login-container textarea,
        [data-theme="dark"] .login-container select,
        body[data-theme="dark"] .login-container input,
        body[data-theme="dark"] .login-container textarea,
        body[data-theme="dark"] .login-container select {
            background: #334155 !important;
            color: #f9fafb !important;
            border: 1px solid #6b7280 !important;
        }

        [data-theme="dark"] .login-container .stTextInput input,
        [data-theme="dark"] .login-container [data-testid="textInput"] input,
        body[data-theme="dark"] .login-container .stTextInput input,
        body[data-theme="dark"] .login-container [data-testid="textInput"] input {
            background: #334155 !important;
            color: #f9fafb !important;
            border: 1px solid #6b7280 !important;
        }

        /* BOTONES ESPECÍFICOS CON MEJOR CONTRASTE */
        [data-theme="dark"] .login-container button,
        [data-theme="dark"] .login-container .stButton > button,
        body[data-theme="dark"] .login-container button,
        body[data-theme="dark"] .login-container .stButton > button {
            background: #334155 !important;
            color: #ffffff !important;
            border: 2px solid #6b7280 !important;
            font-weight: 600 !important;
            text-shadow: 0 1px 2px rgba(0,0,0,0.5) !important;
        }

        [data-theme="dark"] .login-container button:hover,
        [data-theme="dark"] .login-container .stButton > button:hover,
        body[data-theme="dark"] .login-container button:hover,
        body[data-theme="dark"] .login-container .stButton > button:hover {
            background: #4b5563 !important;
            border-color: #9ca3af !important;
            color: #ffffff !important;
            transform: translateY(-1px) !important;
            box-shadow: 0 4px 8px rgba(0,0,0,0.3) !important;
        }

        /* Forzar placeholder text en modo oscuro */
        [data-theme="dark"] .login-container input::placeholder,
        [data-theme="dark"] .login-container textarea::placeholder,
        body[data-theme="dark"] .login-container input::placeholder,
        body[data-theme="dark"] .login-container textarea::placeholder {
            color: #9ca3af !important;
            opacity: 0.8 !important;
        }

        /* Específico para elementos de form de Streamlit */
        [data-theme="dark"] .login-container .stForm,
        [data-theme="dark"] .login-container [data-testid="stForm"],
        body[data-theme="dark"] .login-container .stForm,
        body[data-theme="dark"] .login-container [data-testid="stForm"] {
            background: transparent !important;
        }

        [data-theme="dark"] .login-container .stMarkdown,
        body[data-theme="dark"] .login-container .stMarkdown {
            color: #f9fafb !important;
        }

        [data-theme="dark"] .login-container .stMarkdown h1,
        [data-theme="dark"] .login-container .stMarkdown h2,
        [data-theme="dark"] .login-container .stMarkdown h3,
        [data-theme="dark"] .login-container .stMarkdown h4,
        [data-theme="dark"] .login-container .stMarkdown h5,
        [data-theme="dark"] .login-container .stMarkdown h6,
        body[data-theme="dark"] .login-container .stMarkdown h1,
        body[data-theme="dark"] .login-container .stMarkdown h2,
        body[data-theme="dark"] .login-container .stMarkdown h3,
        body[data-theme="dark"] .login-container .stMarkdown h4,
        body[data-theme="dark"] .login-container .stMarkdown h5,
        body[data-theme="dark"] .login-container .stMarkdown h6 {
            color: #f9fafb !important;
        }

        /* FORZAR TEMA OSCURO GLOBALMENTE CUANDO ESTÁ ACTIVO */
        body[data-theme="dark"] {
            background-color: #0f172a !important;
            color: #f9fafb !important;
        }

        body[data-theme="dark"] .stApp,
        body[data-theme="dark"] .main {
            background-color: #0f172a !important;
            color: #f9fafb !important;
        }

        body[data-theme="dark"] .stButton > button {
            background: #4b5563 !important;
            color: #f9fafb !important;
            border: 1px solid #6b7280 !important;
        }

        body[data-theme="dark"] .stTextInput > div > div > input {
            background: #334155 !important;
            color: #f9fafb !important;
            border: 1px solid #6b7280 !important;
        }

        body[data-theme="dark"] label {
            color: #f9fafb !important;
        }

        body[data-theme="dark"] .stMarkdown {
            color: #f9fafb !important;
        }

        body[data-theme="dark"] .stMarkdown h1,
        body[data-theme="dark"] .stMarkdown h2,
        body[data-theme="dark"] .stMarkdown h3,
        body[data-theme="dark"] .stMarkdown h4 {
            color: #f9fafb !important;
        }

        /* TOGGLE BUTTON STYLING EN MODO OSCURO */
        [data-theme="dark"] button[key="theme_toggle_v6_positioned"],
        body[data-theme="dark"] button[key="theme_toggle_v6_positioned"] {
            background: #334155 !important;
            color: #ffffff !important;
            border: 2px solid #6b7280 !important;
            font-weight: 600 !important;
            text-shadow: 0 1px 2px rgba(0,0,0,0.5) !important;
        }

        [data-theme="dark"] button[key="theme_toggle_v6_positioned"]:hover,
        body[data-theme="dark"] button[key="theme_toggle_v6_positioned"]:hover {
            background: #4b5563 !important;
            border-color: #9ca3af !important;
            transform: translateY(-1px) !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.4) !important;
        }

        /* ========== FORZAR MODO CLARO ========== */
        body[data-theme="light"],
        body:not([data-theme="dark"]) {
            background-color: #ffffff !important;
            color: #1a202c !important;
        }

        body[data-theme="light"] .stApp,
        body[data-theme="light"] .main,
        body:not([data-theme="dark"]) .stApp,
        body:not([data-theme="dark"]) .main {
            background-color: #ffffff !important;
            color: #1a202c !important;
        }

        body[data-theme="light"] .stButton > button,
        body:not([data-theme="dark"]) .stButton > button {
            background: #ffffff !important;
            color: #1a202c !important;
            border: 1px solid #d1d5db !important;
        }

        body[data-theme="light"] .stTextInput > div > div > input,
        body:not([data-theme="dark"]) .stTextInput > div > div > input {
            background: #ffffff !important;
            color: #1a202c !important;
            border: 1px solid #d1d5db !important;
        }

        body[data-theme="light"] label,
        body:not([data-theme="dark"]) label {
            color: #1a202c !important;
        }

        body[data-theme="light"] .stMarkdown,
        body:not([data-theme="dark"]) .stMarkdown {
            color: #1a202c !important;
        }

        body[data-theme="light"] .stMarkdown h1,
        body[data-theme="light"] .stMarkdown h2,
        body[data-theme="light"] .stMarkdown h3,
        body[data-theme="light"] .stMarkdown h4,
        body:not([data-theme="dark"]) .stMarkdown h1,
        body:not([data-theme="dark"]) .stMarkdown h2,
        body:not([data-theme="dark"]) .stMarkdown h3,
        body:not([data-theme="dark"]) .stMarkdown h4 {
            color: #1a202c !important;
        }

        /* SIDEBAR EN MODO CLARO */
        body[data-theme="light"] .stSidebar,
        body[data-theme="light"] [data-testid="stSidebar"],
        body:not([data-theme="dark"]) .stSidebar,
        body:not([data-theme="dark"]) [data-testid="stSidebar"] {
            background-color: #f8fafc !important;
            color: #1a202c !important;
        }

        body[data-theme="light"] .stSidebar *,
        body[data-theme="light"] [data-testid="stSidebar"] *,
        body:not([data-theme="dark"]) .stSidebar *,
        body:not([data-theme="dark"]) [data-testid="stSidebar"] * {
            color: #1a202c !important;
        }

        /* FORZAR ELEMENTOS GENERALES EN MODO CLARO */
        body[data-theme="light"] *,
        body:not([data-theme="dark"]) * {
            color: #1a202c !important;
        }

        body[data-theme="light"] button,
        body:not([data-theme="dark"]) button {
            background: #ffffff !important;
            color: #1a202c !important;
            border: 1px solid #d1d5db !important;
        }

        body[data-theme="light"] input,
        body[data-theme="light"] textarea,
        body[data-theme="light"] select,
        body:not([data-theme="dark"]) input,
        body:not([data-theme="dark"]) textarea,
        body:not([data-theme="dark"]) select {
            background: #ffffff !important;
            color: #1a202c !important;
            border: 1px solid #d1d5db !important;
        }
    </style>
    """, unsafe_allow_html=True)

    # Aplicar atributo data-theme para el modo oscuro
    if 'theme_mode' in st.session_state:
        current_theme = st.session_state.theme_mode
    else:
        current_theme = 'light'  # Valor por defecto

    # CSS inmediato para modo oscuro si está activo
    if current_theme == 'dark':
        st.markdown("""
        <style>
        /* FORZAR MODO OSCURO INMEDIATO */
            html, body, .stApp, .main {
                background-color: #0f172a !important;
                color: #f9fafb !important;
            }

            .stButton > button {
                background: #4b5563 !important;
                color: #f9fafb !important;
                border: 1px solid #6b7280 !important;
            }

            .stTextInput > div > div > input {
                background: #334155 !important;
                color: #f9fafb !important;
                border: 1px solid #6b7280 !important;
            }

            label, .stMarkdown, .stMarkdown * {
                color: #f9fafb !important;
            }

            .login-container {
                background: #1e293b !important;
                border: 1px solid #374151 !important;
            }

            .login-header {
                background: linear-gradient(135deg, #334155 0%, #1e293b 100%) !important;
                color: #f9fafb !important;
            }

            .login-header,
            .login-header *,
            .login-header h1,
            .login-header h2,
            .login-header h3,
            .login-header p {
                color: #f9fafb !important;
            }

            .demo-credentials {
                background: linear-gradient(135deg, #065f46 0%, #047857 100%) !important;
                color: #ffffff !important;
                border: 2px solid rgba(52, 211, 153, 0.5) !important;
                box-shadow: 0 4px 12px rgba(0,0,0,0.3) !important;
            }

            .demo-credentials * {
                color: #ffffff !important;
            }

            .demo-credentials h4 {
                color: #4ade80 !important;
                font-weight: 700 !important;
            }
            </style>
            """, unsafe_allow_html=True)

        st.markdown(f"""
        <script>
        document.body.setAttribute('data-theme', '{current_theme}');
        document.documentElement.setAttribute('data-theme', '{current_theme}');

        // También aplicar a elementos principales de Streamlit
        setTimeout(function() {{
            const stApp = document.querySelector('.stApp');
            if (stApp) {{
                stApp.setAttribute('data-theme', '{current_theme}');
            }}
            const main = document.querySelector('.main');
            if (main) {{
                main.setAttribute('data-theme', '{current_theme}');
            }}

            // APLICAR ESTILOS SEGÚN TEMA
            if ('{current_theme}' === 'dark') {{
                // FORZAR ESTILOS DE MODO OSCURO
                const buttons = document.querySelectorAll('button');
                buttons.forEach(btn => {{
                    btn.style.background = '#334155';
                    btn.style.color = '#ffffff';
                    btn.style.border = '2px solid #6b7280';
                    btn.style.fontWeight = '600';
                }});

                // Forzar divs con estilos inline (tarjetas)
                const divs = document.querySelectorAll('div[style*="background"]');
                divs.forEach(div => {{
                    if (div.style.background && div.style.background.includes('#ffffff')) {{
                        div.style.background = '#334155';
                        div.style.color = '#ffffff';
                        div.style.border = '2px solid #6b7280';

                        // Forzar todos los elementos hijos
                        const children = div.querySelectorAll('*');
                        children.forEach(child => {{
                            child.style.color = '#ffffff';
                        }});
                    }}
                }});

                // Forzar inputs
                const inputs = document.querySelectorAll('input');
                inputs.forEach(input => {{
                    input.style.background = '#334155';
                    input.style.color = '#ffffff';
                    input.style.border = '1px solid #6b7280';
                }});

                // Forzar labels
                const labels = document.querySelectorAll('label');
                labels.forEach(label => {{
                    label.style.color = '#ffffff';
                }});

                // Forzar toggle button específico
                const toggleBtn = document.querySelector('button[key="theme_toggle_v6_positioned"]');
                if (toggleBtn) {{
                    toggleBtn.style.background = '#334155';
                    toggleBtn.style.color = '#ffffff';
                    toggleBtn.style.border = '2px solid #6b7280';
                }}
            }} else {{
                // FORZAR ESTILOS DE MODO CLARO - RESETEAR DARK MODE
                const buttons = document.querySelectorAll('button');
                buttons.forEach(btn => {{
                    btn.style.background = '#ffffff';
                    btn.style.color = '#1a202c';
                    btn.style.border = '1px solid #d1d5db';
                    btn.style.fontWeight = 'normal';
                }});

                // Resetear divs con estilos inline
                const divs = document.querySelectorAll('div[style*="background"]');
                divs.forEach(div => {{
                    if (div.style.background && div.style.background.includes('#334155')) {{
                        div.style.background = '#ffffff';
                        div.style.color = '#1a202c';
                        div.style.border = '1px solid #e5e7eb';

                        // Resetear todos los elementos hijos
                        const children = div.querySelectorAll('*');
                        children.forEach(child => {{
                            child.style.color = '#1a202c';
                        }});
                    }}
                }});

                // Resetear inputs
                const inputs = document.querySelectorAll('input');
                inputs.forEach(input => {{
                    input.style.background = '#ffffff';
                    input.style.color = '#1a202c';
                    input.style.border = '1px solid #d1d5db';
                }});

                // Resetear labels
                const labels = document.querySelectorAll('label');
                labels.forEach(label => {{
                    label.style.color = '#1a202c';
                }});

                // Resetear sidebar
                const sidebar = document.querySelector('.stSidebar, [data-testid="stSidebar"]');
                if (sidebar) {{
                    sidebar.style.backgroundColor = '#f8fafc';
                    const sidebarElements = sidebar.querySelectorAll('*');
                    sidebarElements.forEach(el => {{
                        el.style.color = '#1a202c';
                    }});
                }}

                // Resetear toggle button específico
                const toggleBtn = document.querySelector('button[key="theme_toggle_v6_positioned"]');
                if (toggleBtn) {{
                    toggleBtn.style.background = '#ffffff';
                    toggleBtn.style.color = '#1a202c';
                    toggleBtn.style.border = '1px solid #d1d5db';
                }}
            }}
        }}, 200);

        // Ejecutar nuevamente después de 1 segundo por si hay elementos que se cargan tarde
        setTimeout(function() {{
            if ('{current_theme}' === 'dark') {{
                const buttons = document.querySelectorAll('button');
                buttons.forEach(btn => {{
                    if (!btn.style.background || btn.style.background.includes('rgb(255')) {{
                        btn.style.background = '#334155';
                        btn.style.color = '#ffffff';
                        btn.style.border = '2px solid #6b7280';
                    }}
                }});
            }} else {{
                // Asegurar modo claro
                const buttons = document.querySelectorAll('button');
                buttons.forEach(btn => {{
                    if (btn.style.background && btn.style.background.includes('#334155')) {{
                        btn.style.background = '#ffffff';
                        btn.style.color = '#1a202c';
                        btn.style.border = '1px solid #d1d5db';
                    }}
                }});

                // Asegurar sidebar en modo claro
                const sidebar = document.querySelector('.stSidebar, [data-testid="stSidebar"]');
                if (sidebar) {{
                    const sidebarElements = sidebar.querySelectorAll('*');
                    sidebarElements.forEach(el => {{
                        if (el.style.color && el.style.color.includes('#f9fafb')) {{
                            el.style.color = '#1a202c';
                        }}
                    }});
                }}
            }}
        }}, 1000);
        </script>
        """, unsafe_allow_html=True)

    # CSS FINAL SUPER AGRESIVO para modo oscuro
    if 'theme_mode' in st.session_state and st.session_state.theme_mode == 'dark':
        final_timestamp = datetime.now().strftime("%H%M%S%f")
        st.markdown(f"""
        <style>
        /* ULTRA AGGRESSIVE DARK MODE ONLY - {final_timestamp} */

        /* APLICAR SOLO CUANDO data-theme="dark" */
        [data-theme="dark"] button,
        body[data-theme="dark"] button,
        [data-theme="dark"] .stButton > button,
        body[data-theme="dark"] .stButton > button,
        [data-theme="dark"] input[type="submit"],
        body[data-theme="dark"] input[type="submit"] {{
            background: #334155 !important;
            color: #ffffff !important;
            border: 2px solid #6b7280 !important;
            font-weight: 600 !important;
        }}

        /* DIVS CON BACKGROUND BLANCO SOLO EN MODO OSCURO */
        [data-theme="dark"] div[style*="#ffffff"],
        [data-theme="dark"] div[style*="rgb(255, 255, 255)"],
        [data-theme="dark"] div[style*="white"],
        body[data-theme="dark"] div[style*="#ffffff"],
        body[data-theme="dark"] div[style*="rgb(255, 255, 255)"],
        body[data-theme="dark"] div[style*="white"] {{
            background: #334155 !important;
            color: #ffffff !important;
            border: 2px solid #6b7280 !important;
        }}

        /* INPUTS SOLO EN MODO OSCURO */
        [data-theme="dark"] input,
        [data-theme="dark"] textarea,
        [data-theme="dark"] select,
        body[data-theme="dark"] input,
        body[data-theme="dark"] textarea,
        body[data-theme="dark"] select {{
            background: #334155 !important;
            color: #ffffff !important;
            border: 1px solid #6b7280 !important;
        }}

        /* LABELS SOLO EN MODO OSCURO */
        [data-theme="dark"] label,
        body[data-theme="dark"] label {{
            color: #ffffff !important;
        }}

        /* MARKDOWN SOLO EN MODO OSCURO */
        [data-theme="dark"] .stMarkdown,
        [data-theme="dark"] .stMarkdown *,
        body[data-theme="dark"] .stMarkdown,
        body[data-theme="dark"] .stMarkdown * {{
            color: #ffffff !important;
        }}

        /* CONTAINERS SOLO EN MODO OSCURO */
        [data-theme="dark"] .login-container,
        [data-theme="dark"] .demo-credentials,
        [data-theme="dark"] .roles-section,
        body[data-theme="dark"] .login-container,
        body[data-theme="dark"] .demo-credentials,
        body[data-theme="dark"] .roles-section {{
            background: #1e293b !important;
            color: #ffffff !important;
        }}

        /* ELEMENTOS CON ESTILOS INLINE SOLO EN MODO OSCURO */
        [data-theme="dark"] div[style],
        body[data-theme="dark"] div[style] {{
            background: #334155 !important;
            color: #ffffff !important;
        }}

        [data-theme="dark"] div[style] *,
        body[data-theme="dark"] div[style] * {{
            color: #ffffff !important;
        }}
        </style>
        """, unsafe_allow_html=True)

    # CSS para asegurar modo claro correcto
    else:
        # Asegurar que en modo claro el texto sea negro
        light_timestamp = datetime.now().strftime("%H%M%S%f")
        st.markdown(f"""
        <style>
        /* FORCE LIGHT MODE COLORS - {light_timestamp} */

        /* ASEGURAR TEXTO NEGRO EN MODO CLARO */
        [data-theme="light"] *,
        body[data-theme="light"] *,
        body:not([data-theme="dark"]) *,
        html:not([data-theme="dark"]) * {{
            color: #1f2937 !important;
        }}

        /* BOTONES EN MODO CLARO */
        [data-theme="light"] button,
        body[data-theme="light"] button,
        body:not([data-theme="dark"]) button {{
            background: #ffffff !important;
            color: #1f2937 !important;
            border: 1px solid #d1d5db !important;
        }}

        /* INPUTS EN MODO CLARO */
        [data-theme="light"] input,
        [data-theme="light"] textarea,
        [data-theme="light"] select,
        body[data-theme="light"] input,
        body[data-theme="light"] textarea,
        body[data-theme="light"] select,
        body:not([data-theme="dark"]) input,
        body:not([data-theme="dark"]) textarea,
        body:not([data-theme="dark"]) select {{
            background: #ffffff !important;
            color: #1f2937 !important;
            border: 1px solid #d1d5db !important;
        }}

        /* SIDEBAR EN MODO CLARO */
        [data-theme="light"] .stSidebar,
        [data-theme="light"] .stSidebar *,
        body[data-theme="light"] .stSidebar,
        body[data-theme="light"] .stSidebar *,
        body:not([data-theme="dark"]) .stSidebar,
        body:not([data-theme="dark"]) .stSidebar * {{
            color: #1f2937 !important;
            background: #ffffff !important;
        }}

        /* MARKDOWN EN MODO CLARO */
        [data-theme="light"] .stMarkdown,
        [data-theme="light"] .stMarkdown *,
        body[data-theme="light"] .stMarkdown,
        body[data-theme="light"] .stMarkdown *,
        body:not([data-theme="dark"]) .stMarkdown,
        body:not([data-theme="dark"]) .stMarkdown * {{
            color: #1f2937 !important;
        }}

        /* ========== CHAT INPUT FORZADO EN MODO OSCURO ========== */
        [data-theme="dark"] .stChatInput textarea,
        [data-theme="dark"] .stChatInput input,
        [data-theme="dark"] [data-testid="stChatInput"] textarea,
        [data-theme="dark"] [data-testid="stChatInput"] input,
        [data-theme="dark"] .stChatInput,
        [data-theme="dark"] [data-testid="stChatInput"],
        body[data-theme="dark"] .stChatInput textarea,
        body[data-theme="dark"] .stChatInput input,
        body[data-theme="dark"] [data-testid="stChatInput"] textarea,
        body[data-theme="dark"] [data-testid="stChatInput"] input {{
            background: #334155 !important;
            color: #f8fafc !important;
            border: 1px solid #6b7280 !important;
        }}

        [data-theme="dark"] .stChatInput textarea::placeholder,
        [data-theme="dark"] .stChatInput input::placeholder,
        [data-theme="dark"] [data-testid="stChatInput"] textarea::placeholder,
        [data-theme="dark"] [data-testid="stChatInput"] input::placeholder,
        body[data-theme="dark"] .stChatInput textarea::placeholder,
        body[data-theme="dark"] .stChatInput input::placeholder {{
            color: #9ca3af !important;
            opacity: 1 !important;
        }}

        /* ========== ALERTAS FORZADAS EN MODO OSCURO ========== */
        [data-theme="dark"] .alert-card,
        body[data-theme="dark"] .alert-card {{
            background: #1e293b !important;
            border-color: #475569 !important;
            box-shadow: 0 2px 8px rgba(0,0,0,0.3) !important;
        }}

        [data-theme="dark"] .alert-message,
        body[data-theme="dark"] .alert-message {{
            color: #f8fafc !important;
        }}

        /* ========== SELECTBOX Y DROPDOWNS EN MODO OSCURO ========== */
        [data-theme="dark"] .stSelectbox,
        [data-theme="dark"] [data-baseweb="select"],
        [data-theme="dark"] [data-testid="stSelectbox"],
        body[data-theme="dark"] .stSelectbox,
        body[data-theme="dark"] [data-baseweb="select"] {{
            background: #334155 !important;
            color: #f8fafc !important;
        }}

        [data-theme="dark"] .stSelectbox > div,
        [data-theme="dark"] [data-baseweb="select"] > div,
        body[data-theme="dark"] .stSelectbox > div,
        body[data-theme="dark"] [data-baseweb="select"] > div {{
            background: #334155 !important;
            color: #f8fafc !important;
            border-color: #6b7280 !important;
        }}

        /* Opciones del dropdown cuando se despliega */
        [data-theme="dark"] [role="listbox"],
        [data-theme="dark"] [data-baseweb="menu"],
        [data-theme="dark"] ul[role="listbox"],
        body[data-theme="dark"] [role="listbox"],
        body[data-theme="dark"] [data-baseweb="menu"] {{
            background: #1e293b !important;
            border: 1px solid #6b7280 !important;
        }}

        [data-theme="dark"] [role="option"],
        [data-theme="dark"] li[role="option"],
        body[data-theme="dark"] [role="option"],
        body[data-theme="dark"] li[role="option"] {{
            background: #1e293b !important;
            color: #f8fafc !important;
        }}

        [data-theme="dark"] [role="option"]:hover,
        [data-theme="dark"] li[role="option"]:hover,
        body[data-theme="dark"] [role="option"]:hover,
        body[data-theme="dark"] li[role="option"]:hover {{
            background: #334155 !important;
            color: #ffffff !important;
        }}

        /* Texto seleccionado en el selectbox */
        [data-theme="dark"] .stSelectbox input,
        [data-theme="dark"] [data-baseweb="select"] input,
        [data-theme="dark"] .stSelectbox div[data-baseweb="select"] > div,
        body[data-theme="dark"] .stSelectbox input,
        body[data-theme="dark"] [data-baseweb="select"] input {{
            color: #f8fafc !important;
            background: #334155 !important;
        }}

        /* ========== BOTONES GENERALES EN MODO OSCURO ========== */
        [data-theme="dark"] .stButton > button,
        [data-theme="dark"] button[kind="primary"],
        [data-theme="dark"] button[kind="secondary"],
        body[data-theme="dark"] .stButton > button,
        body[data-theme="dark"] button[kind="primary"],
        body[data-theme="dark"] button[kind="secondary"] {{
            background: #334155 !important;
            color: #f8fafc !important;
            border: 1px solid #6b7280 !important;
        }}

        [data-theme="dark"] .stButton > button:hover,
        [data-theme="dark"] button[kind="primary"]:hover,
        [data-theme="dark"] button[kind="secondary"]:hover,
        body[data-theme="dark"] .stButton > button:hover,
        body[data-theme="dark"] button[kind="primary"]:hover,
        body[data-theme="dark"] button[kind="secondary"]:hover {{
            background: #475569 !important;
            color: #ffffff !important;
            border-color: #9ca3af !important;
        }}

        /* ========== TARJETAS DE ESTADO OPERATIVO ========== */
        .status-card {{
            text-align: center;
            padding: 1.3rem;
            border-radius: 12px;
            border-width: 3px;
            border-style: solid;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}

        .status-card-title {{
            font-weight: 700;
            color: #1a202c;
            font-size: 1.1rem;
            margin-bottom: 0.3rem;
        }}

        .status-card-subtitle {{
            font-size: 1rem;
            color: #2d3748;
            font-weight: 600;
        }}

        /* Modo oscuro para tarjetas de estado */
        [data-theme="dark"] .status-card,
        body[data-theme="dark"] .status-card {{
            box-shadow: 0 2px 8px rgba(0,0,0,0.3);
        }}

        [data-theme="dark"] .status-card-title,
        body[data-theme="dark"] .status-card-title {{
            color: #f8fafc !important;
        }}

        [data-theme="dark"] .status-card-subtitle,
        body[data-theme="dark"] .status-card-subtitle {{
            color: #cbd5e1 !important;
        }}
        </style>
        """, unsafe_allow_html=True)

    # Centrar la página de login
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Usar f-string para interpolar variables según el tema
        if current_theme == 'dark':
            header_color = '#f9fafb'
            subtitle_color = '#d1d5db'
            text_color = '#9ca3af'
            container_bg = '#1e293b'
            container_border = '1px solid #374151'
            container_shadow = '0 10px 40px rgba(0,0,0,0.3)'
            header_bg = 'linear-gradient(135deg, #334155 0%, #1e293b 100%)'
            form_bg = '#1e293b'
        else:
            header_color = '#1a202c'
            subtitle_color = '#4a5568'
            text_color = '#718096'
            container_bg = '#ffffff'
            container_border = '1px solid rgba(0, 0, 0, 0.05)'
            container_shadow = '0 10px 40px rgba(0, 0, 0, 0.1), 0 2px 8px rgba(0, 0, 0, 0.06)'
            header_bg = 'linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%)'
            form_bg = '#ffffff'

        st.markdown(f"""
        <div class="login-container" style="max-width: 420px; margin: 0 auto; background: {container_bg}; border-radius: 24px; box-shadow: {container_shadow}; border: {container_border};">
            <div class="login-header" style="background: {header_bg}; padding: 32px; border-radius: 24px 24px 0 0; text-align: center;">
                <div style="color: {header_color}; font-size: 32px; font-weight: 700; margin-bottom: 8px;">🏥 Copilot Salud</div>
                <div style="color: {subtitle_color}; font-size: 18px; font-weight: 500; margin: 8px 0;">Sistema de Análisis Sociosanitario</div>
                <div style="color: {text_color}; font-size: 14px; margin-top: 8px;">Provincia de Málaga - Andalucía</div>
            </div>
            <div class="login-form-container" style="padding: 32px; background: {form_bg};">
        """, unsafe_allow_html=True)
        
        st.markdown("#### 🔐 Iniciar Sesión")
        
        # Formulario de login
        with st.form("login_form"):
            username = st.text_input("👤 Usuario", placeholder="Ingresa tu usuario")
            password = st.text_input("🔑 Contraseña", type="password", placeholder="Ingresa tu contraseña")
            
            col1, col2 = st.columns(2)
            with col1:
                login_button = st.form_submit_button("🚀 Iniciar Sesión", width="stretch")
            with col2:
                demo_button = st.form_submit_button("👤 Acceso Demo", width="stretch")
        
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

        # JAVASCRIPT SIMPLE PARA FORZAR TEMAS
        st.markdown("""
        <script>
        function applyThemeStyles() {
            const isDark = document.body.getAttribute('data-theme') === 'dark' ||
                          document.documentElement.getAttribute('data-theme') === 'dark';

            console.log('🎨 Aplicando tema:', isDark ? 'OSCURO' : 'CLARO');

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

            console.log('✅ Tema aplicado correctamente a', allElements.length, 'elementos');
        }

        // Ejecutar inmediatamente
        applyThemeStyles();

        // Ejecutar cuando cargue el DOM
        document.addEventListener('DOMContentLoaded', applyThemeStyles);

        // Detectar cambios en el atributo data-theme
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

        // Observar cambios en body y html
        observer.observe(document.body, { attributes: true, attributeFilter: ['data-theme'] });
        observer.observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });

        // Ejecutar cada 2 segundos como respaldo
        setInterval(applyThemeStyles, 2000);
        </script>
        """, unsafe_allow_html=True)

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
    """Cerrar sesión"""
    for key in ['authenticated', 'user', 'auth_token']:
        if key in st.session_state:
            del st.session_state[key]
    # Resetear tema a claro al cerrar sesión
    st.session_state.theme_mode = 'light'
    st.rerun()