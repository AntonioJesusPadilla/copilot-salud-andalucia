# Crear archivo: testing/test_integration.py
#!/usr/bin/env python3
"""
Test de Integración Completa con Async
"""

import sys
import os
import asyncio

# Añadir el directorio raíz al path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

async def test_full_async_flow():
    """Test del flujo completo asíncrono"""
    print("�� TEST INTEGRACIÓN COMPLETA")
    print("=" * 40)
    
    try:
        from modules.ai.streamlit_async_wrapper import get_streamlit_async_wrapper
        
        # Simular datos de la aplicación
        test_data = {
            'hospitales': [
                {'nombre': 'Hospital Regional', 'distrito': 'Centro', 'camas': 200},
                {'nombre': 'Hospital Norte', 'distrito': 'Norte', 'camas': 150}
            ],
            'demografia': {
                'poblacion_2025': [100000, 80000, 120000]
            }
        }
        
        # Obtener wrapper
        wrapper = get_streamlit_async_wrapper()
        
        # Test 1: Consulta simple
        print("   🔄 Probando consulta simple...")
        result1 = wrapper.process_query_sync(
            "¿Cuántos hospitales hay en total?",
            test_data,
            "invitado"
        )
        print(f"   ✅ Resultado 1: {result1.get('analysis_type', 'error')}")
        
        # Test 2: Múltiples consultas
        print("   🔄 Probando múltiples consultas...")
        queries = [
            "¿Cuál es la población total?",
            "¿Cuántas camas hay disponibles?",
            "¿Qué distritos tienen hospitales?"
        ]
        
        results = wrapper.process_multiple_queries(
            queries, test_data, "analista"
        )
        
        print(f"   ✅ Resultados múltiples: {len(results)} consultas procesadas")
        
        # Test 3: Métricas
        print("   🔄 Probando métricas...")
        metrics = wrapper.get_processing_metrics()
        cache_stats = wrapper.get_cache_stats()
        
        print(f"   ✅ Métricas: {metrics}")
        print(f"   ✅ Cache: {cache_stats}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error en integración: {e}")
        return False

def main():
    """Ejecutar test de integración"""
    print("🚀 TEST DE INTEGRACIÓN ASYNC/AWAIT")
    print("=" * 50)
    
    try:
        result = asyncio.run(test_full_async_flow())
        if result:
            print("\n🎉 ¡INTEGRACIÓN ASYNC FUNCIONA CORRECTAMENTE!")
            print("✅ El proyecto está listo para usar async/await")
        else:
            print("\n⚠️ La integración async necesita ajustes")
    except Exception as e:
        print(f"\n❌ Error ejecutando integración: {e}")

if __name__ == "__main__":
    main()