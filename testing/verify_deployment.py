#!/usr/bin/env python3
"""
Script de Verificación de Despliegue - Streamlit Cloud
Verifica que la aplicación esté funcionando correctamente en producción
"""

import sys
import os
import importlib
from typing import List, Tuple

def check_critical_imports() -> Tuple[bool, List[str]]:
    """Verificar importaciones críticas para Streamlit Cloud"""
    print("🔍 Verificando importaciones críticas...")
    
    critical_modules = [
        "streamlit",
        "pandas", 
        "plotly",
        "bcrypt",
        "cryptography",
        "aiohttp"
    ]
    
    success = True
    failed_modules = []
    
    for module in critical_modules:
        try:
            importlib.import_module(module)
            print(f"   ✅ {module}")
        except ImportError as e:
            print(f"   ❌ {module}: {e}")
            success = False
            failed_modules.append(module)
    
    return success, failed_modules

def check_optional_imports() -> Tuple[bool, List[str]]:
    """Verificar importaciones opcionales (mapas)"""
    print("\n🗺️ Verificando importaciones opcionales...")
    
    optional_modules = [
        "folium",
        "streamlit_folium"
    ]
    
    success = True
    failed_modules = []
    
    for module in optional_modules:
        try:
            importlib.import_module(module)
            print(f"   ✅ {module}")
        except ImportError as e:
            print(f"   ⚠️ {module}: {e} (opcional)")
            failed_modules.append(module)
    
    # Los mapas son opcionales, no fallan el despliegue
    return True, failed_modules

def check_app_structure() -> bool:
    """Verificar estructura de la aplicación"""
    print("\n🏗️ Verificando estructura de la aplicación...")
    
    required_files = [
        "app.py",
        "requirements.txt",
        "modules/auth_system.py",
        "modules/ai_processor.py",
        "data/users.json"
    ]
    
    success = True
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"   ✅ {file_path}")
        else:
            print(f"   ❌ {file_path} - FALTANTE")
            success = False
    
    return success

def check_environment_variables() -> bool:
    """Verificar variables de entorno críticas"""
    print("\n🔐 Verificando variables de entorno...")
    
    # Verificar que GROQ_API_KEY esté configurada
    groq_key = os.getenv("GROQ_API_KEY")
    if groq_key and groq_key != "demo_key_for_testing":
        print("   ✅ GROQ_API_KEY configurada")
        return True
    else:
        print("   ⚠️ GROQ_API_KEY no configurada o es demo")
        print("   💡 La funcionalidad de IA estará limitada")
        return True  # No es crítico para el despliegue

def check_streamlit_config() -> bool:
    """Verificar configuración de Streamlit"""
    print("\n⚙️ Verificando configuración de Streamlit...")
    
    config_files = [
        ".streamlit/config.toml",
        ".streamlit/secrets.toml"
    ]
    
    success = True
    
    for config_file in config_files:
        if os.path.exists(config_file):
            print(f"   ✅ {config_file}")
        else:
            print(f"   ⚠️ {config_file} - No encontrado")
            if config_file == ".streamlit/secrets.toml":
                print("   💡 Configura secrets en Streamlit Cloud")
    
    return success

def main():
    """Función principal de verificación"""
    print("🚀 VERIFICACIÓN DE DESPLIEGUE - STREAMLIT CLOUD")
    print("=" * 60)
    
    # Verificar importaciones críticas
    critical_ok, critical_failed = check_critical_imports()
    
    # Verificar importaciones opcionales
    optional_ok, optional_failed = check_optional_imports()
    
    # Verificar estructura
    structure_ok = check_app_structure()
    
    # Verificar variables de entorno
    env_ok = check_environment_variables()
    
    # Verificar configuración
    config_ok = check_streamlit_config()
    
    # Resumen
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE VERIFICACIÓN:")
    print(f"   Importaciones críticas: {'✅ OK' if critical_ok else '❌ FALLO'}")
    print(f"   Importaciones opcionales: {'✅ OK' if optional_ok else '⚠️ PARCIAL'}")
    print(f"   Estructura de app: {'✅ OK' if structure_ok else '❌ FALLO'}")
    print(f"   Variables de entorno: {'✅ OK' if env_ok else '⚠️ PARCIAL'}")
    print(f"   Configuración: {'✅ OK' if config_ok else '⚠️ PARCIAL'}")
    
    # Determinar estado final
    if critical_ok and structure_ok:
        print("\n🎉 ¡DESPLIEGUE VERIFICADO EXITOSAMENTE!")
        print("✅ La aplicación está lista para producción")
        
        if optional_failed:
            print(f"\n⚠️ Funcionalidades opcionales no disponibles: {', '.join(optional_failed)}")
            print("💡 Los mapas pueden no funcionar correctamente")
        
        return True
    else:
        print("\n❌ VERIFICACIÓN FALLIDA")
        print("💡 Revisa los errores anteriores")
        
        if critical_failed:
            print(f"❌ Módulos críticos faltantes: {', '.join(critical_failed)}")
            print("💡 Ejecuta: pip install -r requirements.txt")
        
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)