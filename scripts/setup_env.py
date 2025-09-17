#!/usr/bin/env python3
"""
Script para configurar variables de entorno - Copilot Salud Andalucía
Genera claves seguras y crea archivo .env
"""

import os
import secrets
import string
from pathlib import Path

def generate_secure_key(length=32):
    """Generar clave segura aleatoria"""
    alphabet = string.ascii_letters + string.digits + "_-"
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def create_env_file():
    """Crear archivo .env con configuración"""
    print("🔐 CONFIGURANDO VARIABLES DE ENTORNO")
    print("=" * 50)
    
    # Generar claves seguras
    jwt_secret = generate_secure_key(32)
    secret_key = generate_secure_key(32)
    
    # Contenido del archivo .env
    env_content = f"""# Configuración de Variables de Entorno - Copilot Salud Andalucía
# IMPORTANTE: No subir este archivo a GitHub (está en .gitignore)

# ===========================================
# API KEYS - CONFIGURAR CON TUS CLAVES REALES
# ===========================================

# API Key de Groq para funcionalidad de IA
# Obtener en: https://console.groq.com/keys
GROQ_API_KEY=tu_groq_api_key_aqui

# Clave secreta JWT para autenticación (generada automáticamente)
JWT_SECRET_KEY={jwt_secret}

# Clave secreta de la aplicación (generada automáticamente)
SECRET_KEY={secret_key}

# ===========================================
# CONFIGURACIÓN DE LA APLICACIÓN
# ===========================================

# Entorno de ejecución (development, production)
APP_ENVIRONMENT=development

# Puerto de Streamlit (por defecto 8501)
STREAMLIT_SERVER_PORT=8501

# Modo headless para producción
STREAMLIT_SERVER_HEADLESS=false

# ===========================================
# CONFIGURACIÓN DE IA ASÍNCRONA
# ===========================================

# Tiempo de timeout para peticiones IA (segundos)
AI_REQUEST_TIMEOUT=30

# Número máximo de peticiones concurrentes
MAX_CONCURRENT_AI_REQUESTS=5

# Número de reintentos para peticiones fallidas
AI_RETRY_ATTEMPTS=3

# TTL del cache de respuestas IA (segundos)
AI_CACHE_TTL=300

# ===========================================
# CONFIGURACIÓN DE SEGURIDAD
# ===========================================

# Habilitar autenticación de dos factores
ENABLE_2FA=false

# Tiempo de expiración de sesión (horas)
SESSION_TIMEOUT_HOURS=24

# Límite de consultas IA por hora por usuario
MAX_AI_QUERIES_PER_HOUR=50

# ===========================================
# CONFIGURACIÓN DE CACHE
# ===========================================

# TTL del cache para administradores (segundos)
CACHE_TTL_ADMIN=600

# TTL del cache para usuarios normales (segundos)
CACHE_TTL_USER=300

# ===========================================
# CONFIGURACIÓN DE LOGS
# ===========================================

# Nivel de logging (DEBUG, INFO, WARNING, ERROR)
LOG_LEVEL=INFO

# Habilitar logs de auditoría
ENABLE_AUDIT_LOGS=true

# ===========================================
# INSTRUCCIONES DE CONFIGURACIÓN
# ===========================================

# 1. Reemplaza 'tu_groq_api_key_aqui' con tu API key real de Groq
# 2. Las claves JWT_SECRET_KEY y SECRET_KEY ya están generadas
# 3. Ajusta la configuración según tu entorno
# 4. Para producción, cambia APP_ENVIRONMENT=production
# 5. Para Streamlit Cloud, usa la interfaz de secrets en lugar de este archivo
"""
    
    # Crear archivo .env
    env_path = Path(".env")
    
    if env_path.exists():
        print("⚠️ Archivo .env ya existe")
        response = input("¿Sobrescribir? (s/n): ").lower()
        if response != 's':
            print("❌ Operación cancelada")
            return False
    
    try:
        with open(env_path, 'w', encoding='utf-8') as f:
            f.write(env_content)
        
        print("✅ Archivo .env creado exitosamente")
        print(f"🔑 JWT_SECRET_KEY generada: {jwt_secret[:10]}...")
        print(f"🔑 SECRET_KEY generada: {secret_key[:10]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creando archivo .env: {e}")
        return False

def check_groq_api_key():
    """Verificar si GROQ_API_KEY está configurada"""
    groq_key = os.getenv("GROQ_API_KEY")
    
    if groq_key and groq_key != "tu_groq_api_key_aqui":
        print("✅ GROQ_API_KEY ya está configurada")
        return True
    else:
        print("⚠️ GROQ_API_KEY no está configurada")
        print("💡 Para configurar:")
        print("   1. Ve a https://console.groq.com/keys")
        print("   2. Crea una nueva API key")
        print("   3. Edita el archivo .env y reemplaza 'tu_groq_api_key_aqui'")
        return False

def main():
    """Función principal"""
    print("🚀 CONFIGURADOR DE VARIABLES DE ENTORNO")
    print("=" * 60)
    
    # Crear archivo .env
    if create_env_file():
        print("\n📋 PRÓXIMOS PASOS:")
        print("1. Configura tu GROQ_API_KEY en el archivo .env")
        print("2. Ejecuta: python testing/test_diagnostic.py")
        print("3. Si todo está bien, ejecuta: streamlit run app.py")
        
        # Verificar GROQ_API_KEY
        print("\n🔍 VERIFICANDO CONFIGURACIÓN:")
        check_groq_api_key()
        
    else:
        print("❌ Error en la configuración")

if __name__ == "__main__":
    main()
