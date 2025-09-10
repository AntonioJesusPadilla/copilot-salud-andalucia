#!/usr/bin/env python3
"""
Verificador de Dependencias de Mapas
Comprueba que geopy y dependencias geoespaciales estén disponibles
"""

def check_geopy_dependencies():
    """Verificar dependencias de mapas"""
    print("🗺️ VERIFICADOR DE DEPENDENCIAS DE MAPAS")
    print("=" * 50)
    
    dependencies = {
        'geopy': 'Geocoding y cálculos geográficos',
        'folium': 'Mapas interactivos',
        'streamlit_folium': 'Integración con Streamlit',
        'geopandas': 'Análisis geoespacial',
        'shapely': 'Geometrías espaciales',
        'pyproj': 'Proyecciones cartográficas'
    }
    
    results = {}
    
    for dep, description in dependencies.items():
        try:
            if dep == 'streamlit_folium':
                import streamlit_folium
                results[dep] = {'status': '✅', 'version': getattr(streamlit_folium, '__version__', 'N/A')}
            elif dep == 'geopy':
                import geopy
                results[dep] = {'status': '✅', 'version': getattr(geopy, '__version__', 'N/A')}
            elif dep == 'folium':
                import folium
                results[dep] = {'status': '✅', 'version': getattr(folium, '__version__', 'N/A')}
            elif dep == 'geopandas':
                import geopandas
                results[dep] = {'status': '✅', 'version': getattr(geopandas, '__version__', 'N/A')}
            elif dep == 'shapely':
                import shapely
                results[dep] = {'status': '✅', 'version': getattr(shapely, '__version__', 'N/A')}
            elif dep == 'pyproj':
                import pyproj
                results[dep] = {'status': '✅', 'version': getattr(pyproj, '__version__', 'N/A')}
        except ImportError as e:
            results[dep] = {'status': '❌', 'error': str(e)}
    
    print("📊 RESULTADOS:")
    print("-" * 30)
    
    for dep, info in results.items():
        if info['status'] == '✅':
            print(f"{info['status']} {dep:<20} v{info['version']:<10} - {dependencies[dep]}")
        else:
            print(f"{info['status']} {dep:<20} {'ERROR':<10} - {dependencies[dep]}")
            print(f"   Error: {info['error']}")
    
    print()
    
    # Verificar funcionalidad específica
    print("🔧 PRUEBAS DE FUNCIONALIDAD:")
    print("-" * 30)
    
    try:
        from geopy.geocoders import Nominatim
        geolocator = Nominatim(user_agent="copilot_salud_test")
        print("✅ Geocoding disponible")
    except Exception as e:
        print(f"❌ Geocoding no disponible: {e}")
    
    try:
        import folium
        m = folium.Map(location=[36.7213, -4.4214], zoom_start=10)
        print("✅ Folium mapas básicos disponibles")
    except Exception as e:
        print(f"❌ Folium no disponible: {e}")
    
    try:
        from shapely.geometry import Point
        point = Point(0, 0)
        print("✅ Shapely geometrías disponibles")
    except Exception as e:
        print(f"❌ Shapely no disponible: {e}")
    
    print()
    print("🎯 RECOMENDACIONES:")
    print("-" * 30)
    
    failed_deps = [dep for dep, info in results.items() if info['status'] == '❌']
    
    if not failed_deps:
        print("✅ Todas las dependencias de mapas están disponibles")
        print("✅ Las funciones de mapas deberían funcionar correctamente")
    else:
        print(f"⚠️ {len(failed_deps)} dependencias faltantes:")
        for dep in failed_deps:
            print(f"   - {dep}: {dependencies[dep]}")
        print()
        print("💡 Para instalar las dependencias faltantes:")
        print("   pip install geopy folium streamlit-folium geopandas shapely pyproj")

if __name__ == "__main__":
    check_geopy_dependencies()
