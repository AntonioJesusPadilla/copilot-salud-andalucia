#!/usr/bin/env python3
"""
Script de Prueba Rápida - Copilot Salud Andalucía
Verifica que la aplicación se puede ejecutar sin errores
"""

import sys
import os
import importlib

def test_imports():
    """Probar importaciones críticas"""
    print("🔍 Probando importaciones críticas...")
    
    critical_modules = [
        "streamlit",
        "pandas",
        "plotly",
        "bcrypt",
        "cryptography",
        "aiohttp"
    ]
    
    maps_modules = [
        "folium",
        "geopy",
        "geopandas",
        "shapely"
    ]
    
    success = True
    
    print("\n📦 Módulos críticos:")
    for module in critical_modules:
        try:
            importlib.import_module(module)
            print(f"   ✅ {module}")
        except ImportError as e:
            print(f"   ❌ {module}: {e}")
            success = False
    
    print("\n🗺️ Módulos de mapas:")
    maps_ok = True
    for module in maps_modules:
        try:
            importlib.import_module(module)
            print(f"   ✅ {module}")
        except ImportError as e:
            print(f"   ❌ {module}: {e}")
            maps_ok = False
    
    if not maps_ok:
        print("   ⚠️ Los mapas no estarán disponibles, pero la app funcionará")
    
    return success

def test_app_structure():
    """Probar estructura de la aplicación"""
    print("\n🏗️ Probando estructura de la aplicación...")
    
    required_files = [
        "app.py",
        "requirements.txt",
        "modules/auth_system.py",
        "modules/ai_processor.py",
        "modules/performance_optimizer.py",
        "modules/security_auditor.py",
        "modules/rate_limiter.py",
        "modules/data_encryption.py",
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

def test_data_files():
    """Probar archivos de datos"""
    print("\n📊 Probando archivos de datos...")
    
    data_files = [
        "data/raw/hospitales_malaga_2025.csv",
        "data/raw/demografia_malaga_2025.csv",
        "data/raw/servicios_sanitarios_2025.csv",
        "data/raw/accesibilidad_sanitaria_2025.csv",
        "data/raw/indicadores_salud_2025.csv"
    ]
    
    success = True
    
    for file_path in data_files:
        if os.path.exists(file_path):
            print(f"   ✅ {file_path}")
        else:
            print(f"   ⚠️ {file_path} - No encontrado (se generará automáticamente)")
    
    return True  # Los datos se pueden generar, no es crítico

def main():
    """Función principal de prueba"""
    print("🧪 PRUEBA RÁPIDA - COPILOT SALUD ANDALUCÍA")
    print("=" * 50)
    
    # Probar importaciones
    imports_ok = test_imports()
    
    # Probar estructura
    structure_ok = test_app_structure()
    
    # Probar datos
    data_ok = test_data_files()
    
    print("\n" + "=" * 50)
    print("📊 RESUMEN DE PRUEBAS:")
    print(f"   Importaciones: {'✅ OK' if imports_ok else '❌ FALLO'}")
    print(f"   Estructura: {'✅ OK' if structure_ok else '❌ FALLO'}")
    print(f"   Datos: {'✅ OK' if data_ok else '⚠️ PARCIAL'}")
    
    if imports_ok and structure_ok:
        print("\n🎉 ¡APLICACIÓN LISTA PARA EJECUTAR!")
        print("🚀 Ejecuta: streamlit run app.py")
        return True
    else:
        print("\n❌ HAY PROBLEMAS QUE RESOLVER")
        print("💡 Ejecuta: python install_dependencies.py")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
