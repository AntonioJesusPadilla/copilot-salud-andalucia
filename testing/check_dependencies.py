#!/usr/bin/env python3
"""
Verificador de Dependencias - Copilot Salud Andalucía
Verifica que todas las dependencias estén instaladas correctamente
"""

import sys
import importlib
from typing import List, Tuple

def check_module(module_name: str, package_name: str = None) -> Tuple[bool, str]:
    """Verificar si un módulo está disponible"""
    try:
        importlib.import_module(module_name)
        return True, f"✅ {package_name or module_name}"
    except ImportError as e:
        return False, f"❌ {package_name or module_name}: {str(e)}"

def check_dependencies():
    """Verificar todas las dependencias del proyecto"""
    print("🔍 VERIFICADOR DE DEPENDENCIAS - COPILOT SALUD ANDALUCÍA")
    print("=" * 60)
    
    # Dependencias críticas
    critical_deps = [
        ("streamlit", "Streamlit"),
        ("pandas", "Pandas"),
        ("numpy", "NumPy"),
        ("plotly", "Plotly"),
        ("bcrypt", "Bcrypt"),
        ("jwt", "PyJWT"),
        ("cryptography", "Cryptography"),
        ("aiohttp", "aiohttp"),
        ("dotenv", "python-dotenv"),
        ("requests", "Requests"),
        ("bs4", "BeautifulSoup4"),
        ("seaborn", "Seaborn"),
        ("matplotlib", "Matplotlib"),
        ("watchdog", "Watchdog"),
        ("PIL", "Pillow"),
        ("pytz", "pytz"),
    ]
    
    # Dependencias de mapas
    maps_deps = [
        ("folium", "Folium"),
        ("geopandas", "GeoPandas"),
        ("shapely", "Shapely"),
        ("geopy", "GeoPy"),
        ("pyproj", "PyProj"),
    ]
    
    # Dependencias de IA
    ai_deps = [
        ("groq", "Groq"),
    ]
    
    print("📦 DEPENDENCIAS CRÍTICAS:")
    critical_ok = 0
    for module, name in critical_deps:
        success, message = check_module(module, name)
        print(f"   {message}")
        if success:
            critical_ok += 1
    
    print(f"\n📊 Críticas: {critical_ok}/{len(critical_deps)} instaladas")
    
    print("\n🗺️ DEPENDENCIAS DE MAPAS:")
    maps_ok = 0
    for module, name in maps_deps:
        success, message = check_module(module, name)
        print(f"   {message}")
        if success:
            maps_ok += 1
    
    print(f"\n📊 Mapas: {maps_ok}/{len(maps_deps)} instaladas")
    
    print("\n🤖 DEPENDENCIAS DE IA:")
    ai_ok = 0
    for module, name in ai_deps:
        success, message = check_module(module, name)
        print(f"   {message}")
        if success:
            ai_ok += 1
    
    print(f"\n📊 IA: {ai_ok}/{len(ai_deps)} instaladas")
    
    # Resumen final
    total_deps = len(critical_deps) + len(maps_deps) + len(ai_deps)
    total_ok = critical_ok + maps_ok + ai_ok
    
    print("\n" + "=" * 60)
    print(f"📊 RESUMEN TOTAL: {total_ok}/{total_deps} dependencias instaladas")
    
    if total_ok == total_deps:
        print("🎉 ¡TODAS LAS DEPENDENCIAS ESTÁN INSTALADAS!")
        print("✅ El proyecto está listo para ejecutarse")
        return True
    else:
        print("⚠️ ALGUNAS DEPENDENCIAS FALTAN")
        print("💡 Ejecuta: python install_dependencies.py")
        return False

def check_python_version():
    """Verificar versión de Python"""
    print(f"🐍 Python {sys.version}")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 9):
        print("❌ Se requiere Python 3.9 o superior")
        return False
    print("✅ Versión de Python compatible")
    return True

def main():
    """Función principal"""
    print("🚀 VERIFICADOR DE DEPENDENCIAS")
    print("=" * 60)
    
    # Verificar versión de Python
    if not check_python_version():
        sys.exit(1)
    
    # Verificar dependencias
    if check_dependencies():
        print("\n🚀 Para ejecutar la aplicación:")
        print("   streamlit run app.py")
        sys.exit(0)
    else:
        print("\n❌ Instala las dependencias faltantes antes de continuar")
        sys.exit(1)

if __name__ == "__main__":
    main()
