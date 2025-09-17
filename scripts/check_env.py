#!/usr/bin/env python3
"""
Script para verificar y configurar variables de entorno
"""

import os
import sys
from pathlib import Path

# Añadir el directorio raíz al path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

def check_env_file():
    """Verificar si existe el archivo .env"""
    env_file = Path(project_root) / ".env"
    
    print("🔍 VERIFICANDO ARCHIVO .ENV")
    print("=" * 40)
    
    if env_file.exists():
        print(f"✅ Archivo .env encontrado: {env_file}")
        
        # Leer contenido
        try:
            with open(env_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Verificar variables
            required_vars = ['GROQ_API_KEY', 'JWT_SECRET_KEY', 'SECRET_KEY']
            
            print("\n📋 Variables encontradas:")
            for var in required_vars:
                if f"{var}=" in content:
                    # Extraer valor
                    lines = content.split('\n')
                    for line in lines:
                        if line.startswith(f"{var}="):
                            value = line.split('=', 1)[1].strip()
                            if value and value != f"tu_{var.lower()}_aqui":
                                print(f"   ✅ {var}: {value[:10]}...")
                            else:
                                print(f"   ⚠️ {var}: Valor por defecto (necesita configuración)")
                            break
                else:
                    print(f"   ❌ {var}: No encontrada")
            
            return True
            
        except Exception as e:
            print(f"❌ Error leyendo archivo .env: {e}")
            return False
    else:
        print(f"❌ Archivo .env no encontrado en: {env_file}")
        return False

def create_env_file():
    """Crear archivo .env básico"""
    print("\n🔧 CREANDO ARCHIVO .ENV")
    print("=" * 40)
    
    env_file = Path(project_root) / ".env"
    
    # Contenido básico
    env_content = """# Configuración de Variables de Entorno - Copilot Salud Andalucía
GROQ_API_KEY=tu_groq_api_key_aqui
JWT_SECRET_KEY=clave_jwt_generada_automaticamente_32_chars
SECRET_KEY=clave_secreta_generada_automaticamente_32_chars
APP_ENVIRONMENT=development
AI_REQUEST_TIMEOUT=30
MAX_CONCURRENT_AI_REQUESTS=5
AI_RETRY_ATTEMPTS=3
AI_CACHE_TTL=300
"""
    
    try:
        with open(env_file, 'w', encoding='utf-8') as f:
            f.write(env_content)
        
        print(f"✅ Archivo .env creado: {env_file}")
        print("📝 IMPORTANTE: Edita el archivo .env y configura tu GROQ_API_KEY")
        return True
        
    except Exception as e:
        print(f"❌ Error creando archivo .env: {e}")
        return False

def test_env_loading():
    """Probar carga de variables de entorno"""
    print("\n🧪 PROBANDO CARGA DE VARIABLES")
    print("=" * 40)
    
    try:
        from dotenv import load_dotenv
        
        # Cargar .env
        load_dotenv()
        
        # Verificar variables
        groq_key = os.getenv("GROQ_API_KEY")
        jwt_secret = os.getenv("JWT_SECRET_KEY")
        secret_key = os.getenv("SECRET_KEY")
        
        print(f"GROQ_API_KEY: {'✅' if groq_key else '❌'} {groq_key[:10] + '...' if groq_key else 'No encontrada'}")
        print(f"JWT_SECRET_KEY: {'✅' if jwt_secret else '❌'} {jwt_secret[:10] + '...' if jwt_secret else 'No encontrada'}")
        print(f"SECRET_KEY: {'✅' if secret_key else '❌'} {secret_key[:10] + '...' if secret_key else 'No encontrada'}")
        
        return bool(groq_key and jwt_secret and secret_key)
        
    except ImportError:
        print("❌ python-dotenv no instalado")
        print("💡 Ejecuta: pip install python-dotenv")
        return False
    except Exception as e:
        print(f"❌ Error cargando variables: {e}")
        return False

def main():
    """Función principal"""
    print("🔐 VERIFICADOR DE VARIABLES DE ENTORNO")
    print("=" * 50)
    
    # Verificar archivo .env
    if not check_env_file():
        print("\n💡 Creando archivo .env...")
        if create_env_file():
            print("✅ Archivo .env creado exitosamente")
        else:
            print("❌ Error creando archivo .env")
            return
    
    # Probar carga de variables
    if test_env_loading():
        print("\n🎉 ¡Variables de entorno cargadas correctamente!")
        print("💡 Ahora puedes ejecutar: python testing/test_diagnostic.py")
    else:
        print("\n⚠️ Problemas cargando variables de entorno")
        print("💡 Revisa el archivo .env y asegúrate de que tenga el formato correcto")

if __name__ == "__main__":
    main()
