#!/usr/bin/env python3
"""
Generador de secretos seguros para Copilot Salud Andalucía
Genera claves seguras para SECRET_KEY y JWT_SECRET_KEY
"""

import secrets
import string
import os
from pathlib import Path

def generate_secret_key(length=32):
    """Genera una clave secreta segura"""
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{}|;:,.<>?"
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def generate_jwt_secret(length=64):
    """Genera una clave JWT segura"""
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{}|;:,.<>?"
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def create_secrets_file(file_path, secret_key, jwt_secret):
    """Crea un archivo secrets.toml con las claves generadas"""
    content = f"""# Configuración de secrets generada automáticamente
# Generado el: {os.popen('date').read().strip()}

# Clave secreta para la aplicación
SECRET_KEY = "{secret_key}"

# Clave para tokens JWT
JWT_SECRET_KEY = "{jwt_secret}"

# API Key de Groq (reemplazar con tu clave real)
# GROQ_API_KEY = "tu_groq_api_key_aqui"

# Configuración adicional (opcional)
DATABASE_URL = "sqlite:///health_analytics.db"
ENABLE_METRICS = true
LOG_LEVEL = "INFO"

# Configuración de email (opcional)
# SMTP_SERVER = "smtp.gmail.com"
# SMTP_PORT = 587
# EMAIL_USER = "tu_email@gmail.com"
# EMAIL_PASSWORD = "tu_password_de_aplicacion"

# Configuración de mapas
# MAPBOX_TOKEN = "tu_mapbox_token_aqui"  # Opcional para mapas avanzados
"""
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    print("🔐 GENERADOR DE SECRETOS SEGUROS")
    print("=" * 50)
    
    # Generar claves
    secret_key = generate_secret_key(32)
    jwt_secret = generate_jwt_secret(64)
    
    print(f"✅ SECRET_KEY generada: {secret_key[:8]}...")
    print(f"✅ JWT_SECRET_KEY generada: {jwt_secret[:8]}...")
    
    # Crear archivos secrets.toml
    project_root = Path(__file__).parent.parent
    
    # Para desarrollo local
    local_secrets = project_root / "config" / ".streamlit" / "secrets.toml"
    create_secrets_file(local_secrets, secret_key, jwt_secret)
    print(f"✅ Archivo creado: {local_secrets}")
    
    # Para Streamlit Cloud
    cloud_secrets = project_root / ".streamlit" / "secrets.toml"
    create_secrets_file(cloud_secrets, secret_key, jwt_secret)
    print(f"✅ Archivo creado: {cloud_secrets}")
    
    print("\n🔒 IMPORTANTE:")
    print("- Los archivos secrets.toml están en .gitignore")
    print("- NO hagas commit de estos archivos")
    print("- Configura tu GROQ_API_KEY manualmente")
    print("- Para Streamlit Cloud, usa la interfaz de secrets")
    
    print("\n📝 PRÓXIMOS PASOS:")
    print("1. Configura tu GROQ_API_KEY en los archivos secrets.toml")
    print("2. Para Streamlit Cloud, configura los secrets en la interfaz web")
    print("3. Ejecuta: python scripts/start_app.py")

if __name__ == "__main__":
    main()
