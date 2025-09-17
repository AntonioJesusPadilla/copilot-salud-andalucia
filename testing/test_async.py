# Crear archivo: testing/test_async.py
#!/usr/bin/env python3
"""
Test Específico para Funcionamiento Asíncrono
"""

import asyncio
import sys
import os

# Añadir el directorio raíz al path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

def test_async_imports():
    """Test de importaciones asíncronas"""
    print("🧪 TEST ASYNC - IMPORTACIONES")
    print("=" * 40)
    
    async_modules = [
        "asyncio",
        "aiohttp", 
        "threading"
    ]
    
    for module in async_modules:
        try:
            __import__(module)
            print(f"   ✅ {module}")
        except ImportError as e:
            print(f"   ❌ {module}: {e}")
            return False
    
    return True

def test_async_processor():
    """Test del procesador asíncrono"""
    print("\n�� TEST ASYNC - PROCESADOR")
    print("=" * 40)
    
    try:
        from modules.ai.async_ai_processor import AsyncAIProcessor
        processor = AsyncAIProcessor()
        print("   ✅ AsyncAIProcessor creado")
        
        # Test de métodos
        metrics = processor.get_metrics()
        print(f"   ✅ Métricas: {metrics}")
        
        cache_stats = processor.get_cache_stats()
        print(f"   ✅ Cache stats: {cache_stats}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_streamlit_wrapper():
    """Test del wrapper de Streamlit"""
    print("\n🔄 TEST ASYNC - WRAPPER")
    print("=" * 40)
    
    try:
        from modules.ai.streamlit_async_wrapper import StreamlitAsyncWrapper
        wrapper = StreamlitAsyncWrapper()
        print("   ✅ StreamlitAsyncWrapper creado")
        
        # Test de métricas
        metrics = wrapper.get_processing_metrics()
        print(f"   ✅ Métricas wrapper: {metrics}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

async def test_async_functionality():
    """Test de funcionalidad asíncrona real"""
    print("\n⚡ TEST ASYNC - FUNCIONALIDAD")
    print("=" * 40)
    
    try:
        from modules.ai.async_ai_processor import AsyncAIProcessor
        
        processor = AsyncAIProcessor()
        
        # Datos de prueba
        test_data = {
            'hospitales': [{'nombre': 'Hospital Test', 'distrito': 'Centro'}],
            'demografia': {'poblacion_2025': [100000]}
        }
        
        # Test de procesamiento asíncrono
        print("   �� Probando procesamiento asíncrono...")
        result = await processor.process_query_async(
            "¿Cuántos hospitales hay?", 
            test_data, 
            "invitado"
        )
        
        print(f"   ✅ Resultado: {result.get('analysis_type', 'error')}")
        return True
        
    except Exception as e:
        print(f"   ❌ Error en funcionalidad: {e}")
        return False

def main():
    """Ejecutar todos los tests"""
    print("🚀 INICIANDO TESTS ASYNC/AWAIT")
    print("=" * 50)
    
    tests = [
        test_async_imports,
        test_async_processor,
        test_streamlit_wrapper
    ]
    
    passed = 0
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n📊 TESTS SÍNCRONOS: {passed}/{len(tests)}")
    
    # Test asíncrono
    print("\n⚡ Ejecutando test asíncrono...")
    try:
        asyncio.run(test_async_functionality())
        print("   ✅ Test asíncrono completado")
        passed += 1
    except Exception as e:
        print(f"   ❌ Test asíncrono falló: {e}")
    
    print("\n" + "=" * 50)
    print(f"�� TOTAL: {passed}/{len(tests) + 1} tests pasaron")
    
    if passed == len(tests) + 1:
        print("🎉 ¡TODOS LOS TESTS ASYNC PASARON!")
        return True
    else:
        print("⚠️ Algunos tests fallaron")
        return False

if __name__ == "__main__":
    main()