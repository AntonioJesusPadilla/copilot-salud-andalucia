#!/usr/bin/env python3
"""
Script de Instalación de Dependencias - Copilot Salud Andalucía
Instala todas las dependencias necesarias para el proyecto
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Ejecutar comando y mostrar resultado"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completado")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error en {description}: {e}")
        print(f"   Salida: {e.stdout}")
        print(f"   Error: {e.stderr}")
        return False

def check_python_version():
    """Verificar versión de Python"""
    print("🐍 Verificando versión de Python...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 9):
        print(f"❌ Python {version.major}.{version.minor} detectado. Se requiere Python 3.9+")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
    return True

def install_dependencies():
    """Instalar dependencias del proyecto"""
    print("📦 Instalando dependencias de Copilot Salud Andalucía...")
    print("=" * 60)
    
    # Verificar que requirements.txt existe
    if not os.path.exists("config/requirements.txt"):
        print("❌ Archivo config/requirements.txt no encontrado")
        return False
    
    # Comandos de instalación
    commands = [
        ("pip install --upgrade pip", "Actualizando pip"),
        ("pip install -r config/requirements.txt", "Instalando dependencias principales"),
        ("pip install --upgrade geopy folium geopandas shapely pyproj", "Instalando dependencias de mapas"),
        ("pip install --upgrade cryptography aiohttp", "Instalando dependencias de seguridad"),
    ]
    
    success_count = 0
    for command, description in commands:
        if run_command(command, description):
            success_count += 1
        else:
            print(f"⚠️ Continuando con la siguiente dependencia...")
    
    print("=" * 60)
    print(f"📊 Resumen: {success_count}/{len(commands)} comandos ejecutados exitosamente")
    
    return success_count == len(commands)

def verify_installation():
    """Verificar que las dependencias se instalaron correctamente"""
    print("\n🔍 Verificando instalación...")
    
    critical_modules = [
        "streamlit",
        "pandas", 
        "plotly",
        "folium",
        "geopy",
        "geopandas",
        "shapely",
        "bcrypt",
        "cryptography",
        "aiohttp"
    ]
    
    failed_modules = []
    
    for module in critical_modules:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError:
            print(f"❌ {module}")
            failed_modules.append(module)
    
    if failed_modules:
        print(f"\n⚠️ Módulos no instalados: {', '.join(failed_modules)}")
        return False
    else:
        print("\n🎉 ¡Todas las dependencias instaladas correctamente!")
        return True

def create_venv():
    """Crear entorno virtual si no existe"""
    if not os.path.exists("venv"):
        print("🔄 Creando entorno virtual...")
        if run_command("python -m venv venv", "Creando entorno virtual"):
            print("✅ Entorno virtual creado")
            print("💡 Para activar el entorno virtual:")
            print("   Windows: venv\\Scripts\\activate")
            print("   Linux/Mac: source venv/bin/activate")
            return True
    else:
        print("✅ Entorno virtual ya existe")
        return True

def setup_config_files():
    """Configurar archivos de configuración"""
    print("⚙️ Configurando archivos de configuración...")
    
    # Crear directorio config/.streamlit si no existe
    os.makedirs("config/.streamlit", exist_ok=True)
    
    # Verificar si secrets.toml existe
    if not os.path.exists("config/.streamlit/secrets.toml"):
        if os.path.exists("config/.streamlit/secrets.toml.example"):
            print("📋 Archivo de ejemplo de secrets encontrado")
            print("💡 Copia config/.streamlit/secrets.toml.example a config/.streamlit/secrets.toml")
            print("   y configura tus API keys")
        else:
            print("⚠️ Archivo de secrets no encontrado")
            print("💡 Crea config/.streamlit/secrets.toml con tu GROQ_API_KEY")
    
    print("✅ Configuración de archivos completada")
    return True

def main():
    """Función principal"""
    print("🚀 INSTALADOR DE DEPENDENCIAS - COPILOT SALUD ANDALUCÍA")
    print("=" * 60)
    
    # Verificar versión de Python
    if not check_python_version():
        sys.exit(1)
    
    # Crear entorno virtual
    create_venv()
    
    # Configurar archivos
    setup_config_files()
    
    # Instalar dependencias
    if not install_dependencies():
        print("\n❌ Error instalando dependencias")
        print("💡 Intenta instalar manualmente: pip install -r config/requirements.txt")
        sys.exit(1)
    
    # Verificar instalación
    if not verify_installation():
        print("\n⚠️ Algunas dependencias no se instalaron correctamente")
        print("💡 Revisa los errores anteriores e instala manualmente las dependencias faltantes")
        sys.exit(1)
    
    print("\n🎉 ¡INSTALACIÓN COMPLETADA EXITOSAMENTE!")
    print("=" * 60)
    print("📋 Próximos pasos:")
    print("1. Activa el entorno virtual:")
    print("   Windows: venv\\Scripts\\activate")
    print("   Linux/Mac: source venv/bin/activate")
    print("2. Ejecuta la aplicación:")
    print("   streamlit run app.py")
    print("3. Abre tu navegador en: http://localhost:8501")
    print("=" * 60)

if __name__ == "__main__":
    main()
