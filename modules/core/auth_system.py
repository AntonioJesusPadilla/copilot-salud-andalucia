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
        self.secret_key = os.getenv("JWT_SECRET", "health_copilot_secret_2025")
        self.users_db = self.load_users()
        
        # Roles del sistema sanitario con permisos específicos y personalización
        self.roles = {
            "admin": {
                "name": "Administrador del Sistema",
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
    
    # CSS para la página de login
    st.markdown("""
    <style>
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
    </style>
    """, unsafe_allow_html=True)
    
    # Centrar la página de login
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div class="login-container">
            <div class="login-header">
                <h1>🏥 Copilot Salud</h1>
                <h3>Sistema de Análisis Sociosanitario</h3>
                <p>Provincia de Málaga - Andalucía</p>
            </div>
            <div class="login-form-container">
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

def render_user_management():
    """Panel de gestión de usuarios (solo admin)"""
    
    if not st.session_state.get('authenticated') or st.session_state.user['role'] != 'admin':
        st.error("❌ Acceso denegado. Solo administradores pueden gestionar usuarios.")
        return
    
    st.markdown("### 👥 Gestión de Usuarios")
    
    auth = HealthAuthenticator()
    
    tab1, tab2, tab3 = st.tabs(["📋 Lista de Usuarios", "➕ Crear Usuario", "⚙️ Configuración"])
    
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
        st.markdown("#### ⚙️ Configuración del Sistema")
        
        st.info("🔧 Funcionalidades de configuración avanzada (próximamente)")
        
        # Estadísticas del sistema
        users = auth.get_all_users()
        total_users = len(users)
        active_users = len([u for u in users.values() if u.get('active', True)])
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("👥 Total Usuarios", total_users)
        with col2:
            st.metric("🟢 Usuarios Activos", active_users)
        with col3:
            st.metric("📊 Roles Disponibles", len(auth.roles))

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
        
        st.markdown("#### 🔐 Permisos")
        permissions = role_info['permissions']
        for perm in permissions:
            permission_names = {
                'full_access': '🔓 Acceso Completo',
                'user_management': '👥 Gestión de Usuarios',
                'system_config': '⚙️ Configuración del Sistema',
                'analytics': '📊 Análisis Avanzado',
                'reports': '📋 Reportes',
                'planning': '🗺️ Planificación',
                'view_data': '👀 Visualización de Datos',
                'basic_analytics': '📈 Análisis Básico',
                'analisis_equidad': '⚖️ Análisis de Equidad'
            }
            st.write(f"✅ {permission_names.get(perm, perm)}")

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
    st.rerun()