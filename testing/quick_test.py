#!/usr/bin/env python3
"""
Test Rápido - Verificación de Importaciones
"""

def test_imports():
    """Test de importaciones críticas"""
    print("🧪 TEST RÁPIDO - COPILOT SALUD ANDALUCÍA")
    print("=" * 50)
    
    # Módulos críticos
    critical_modules = [
        "streamlit",
        "pandas", 
        "plotly",
        "bcrypt",
        "cryptography",
        "aiohttp"
    ]
    
    # Módulos de mapas
    maps_modules = [
        "folium",
        "geopy",
        "geopandas",
        "shapely"
    ]
    
    print("\n📦 MÓDULOS CRÍTICOS:")
    critical_ok = 0
    for module in critical_modules:
        try:
            __import__(module)
            print(f"   ✅ {module}")
            critical_ok += 1
        except ImportError as e:
            print(f"   ❌ {module}: {e}")
    
    print(f"\n📊 Críticos: {critical_ok}/{len(critical_modules)}")
    
    print("\n🗺️ MÓDULOS DE MAPAS:")
    maps_ok = 0
    for module in maps_modules:
        try:
            __import__(module)
            print(f"   ✅ {module}")
            maps_ok += 1
        except ImportError as e:
            print(f"   ❌ {module}: {e}")
    
    print(f"\n📊 Mapas: {maps_ok}/{len(maps_modules)}")
    
    # Test de archivos
    print("\n🏗️ ARCHIVOS PRINCIPALES:")
    import os
    files = [
        "app.py",
        "requirements.txt",
        "modules/performance_optimizer.py",
        "modules/security_auditor.py",
        "modules/rate_limiter.py",
        "modules/data_encryption.py",
        "modules/async_ai_processor.py",
        "modules/streamlit_async_wrapper.py"
    ]
    
    files_ok = 0
    for file in files:
        if os.path.exists(file):
            print(f"   ✅ {file}")
            files_ok += 1
        else:
            print(f"   ❌ {file}")
    
    print(f"\n📊 Archivos: {files_ok}/{len(files)}")
    
    # Resumen
    total_critical = critical_ok + files_ok
    total_possible = len(critical_modules) + len(files)
    
    print("\n" + "=" * 50)
    print(f"📊 RESUMEN: {total_critical}/{total_possible} elementos OK")
    
    if critical_ok == len(critical_modules) and files_ok == len(files):
        print("🎉 ¡TODAS LAS PRUEBAS PASARON!")
        print("🚀 La aplicación está lista para ejecutar")
        return True
    else:
        print("⚠️ Algunas pruebas fallaron")
        print("💡 Ejecuta: python install_dependencies.py")
        return False

if __name__ == "__main__":
    test_imports()
