#!/usr/bin/env python3
"""
Test Asíncrono Standalone - Sin dependencias de Streamlit
"""

import sys
import os
import asyncio
import traceback
import pandas as pd

# Añadir el directorio raíz al path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Cargar variables de entorno
from dotenv import load_dotenv
load_dotenv()

class MockStreamlitSessionState:
    """Mock de session_state para evitar dependencias de Streamlit"""
    def __init__(self):
        self._state = {}
    
    def __getitem__(self, key):
        return self._state[key]
    
    def __setitem__(self, key, value):
        self._state[key] = value
    
    def __contains__(self, key):
        return key in self._state

# Mock de streamlit para evitar warnings
class MockStreamlit:
    def __init__(self):
        self.session_state = MockStreamlitSessionState()

# Reemplazar streamlit con mock
sys.modules['streamlit'] = MockStreamlit()

def test_environment():
    """Verificar variables de entorno y configuración"""
    print("🔍 DIAGNÓSTICO - ENTORNO")
    print("=" * 40)
    
    # Verificar GROQ_API_KEY
    groq_key = os.getenv("GROQ_API_KEY")
    if groq_key and groq_key != "tu_groq_api_key_aqui":
        print(f"   ✅ GROQ_API_KEY: {groq_key[:10]}...")
    elif groq_key == "tu_groq_api_key_aqui":
        print("   ⚠️ GROQ_API_KEY: Configurada pero con valor por defecto")
        print("   💡 Solución: Reemplazar con tu API key real de Groq")
        return False
    else:
        print("   ❌ GROQ_API_KEY: No encontrada")
        print("   💡 Solución: Configurar variable de entorno")
        return False
    
    # Verificar dependencias
    try:
        import aiohttp
        print(f"   ✅ aiohttp: {aiohttp.__version__}")
    except ImportError as e:
        print(f"   ❌ aiohttp: {e}")
        return False
    
    try:
        import asyncio
        print(f"   ✅ asyncio: Disponible")
    except ImportError as e:
        print(f"   ❌ asyncio: {e}")
        return False
    
    try:
        from dotenv import load_dotenv
        print(f"   ✅ python-dotenv: Disponible")
    except ImportError as e:
        print(f"   ❌ python-dotenv: {e}")
        return False
    
    return True

def test_async_processor_creation():
    """Test de creación del procesador asíncrono"""
    print("\n🔍 DIAGNÓSTICO - PROCESADOR")
    print("=" * 40)
    
    try:
        from modules.ai.async_ai_processor import AsyncAIProcessor
        
        processor = AsyncAIProcessor()
        print("   ✅ AsyncAIProcessor creado")
        
        # Verificar configuración
        print(f"   📊 Modelo: {processor.model}")
        print(f"   📊 Max concurrent: {processor.max_concurrent_requests}")
        print(f"   📊 Timeout: {processor.request_timeout}")
        print(f"   📊 Retry attempts: {processor.retry_attempts}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error creando procesador: {e}")
        traceback.print_exc()
        return False

async def test_groq_api_connection():
    """Test de conexión con Groq API"""
    print("\n🔍 DIAGNÓSTICO - API GROQ")
    print("=" * 40)
    
    try:
        from modules.ai.async_ai_processor import AsyncAIProcessor
        
        processor = AsyncAIProcessor()
        
        # Test de conexión simple
        print("   🔄 Probando conexión con Groq API...")
        
        # Datos de prueba mínimos (formato correcto con DataFrames)
        test_data = {
            'hospitales': pd.DataFrame([{'nombre': 'Test Hospital', 'distrito': 'Centro'}]),
            'demografia': pd.DataFrame([{'municipio': 'Test City', 'poblacion_2025': 1000}])
        }
        
        result = await processor.process_query_async(
            "Hola, ¿funciona la conexión?",
            test_data,
            "invitado"
        )
        
        print(f"   📊 Resultado: {result.get('analysis_type', 'error')}")
        
        if 'error' in result:
            print(f"   ❌ Error en API: {result['error']}")
            return False
        else:
            print("   ✅ Conexión con Groq API exitosa")
            return True
            
    except Exception as e:
        print(f"   ❌ Error en conexión API: {e}")
        traceback.print_exc()
        return False

async def test_simple_async_flow():
    """Test de flujo asíncrono simple"""
    print("\n🔍 DIAGNÓSTICO - FLUJO SIMPLE")
    print("=" * 40)
    
    try:
        from modules.ai.async_ai_processor import AsyncAIProcessor
        
        processor = AsyncAIProcessor()
        
        # Test muy simple
        print("   🔄 Probando flujo asíncrono simple...")
        
        # Simular datos mínimos (formato correcto con DataFrames)
        test_data = {
            'hospitales': pd.DataFrame([{'nombre': 'Hospital Test', 'distrito': 'Centro'}]),
            'demografia': pd.DataFrame([{'municipio': 'Test City', 'poblacion_2025': 1000}])
        }
        
        # Test directo del procesador
        result = await processor.process_query_async(
            "Test simple",
            test_data,
            "invitado"
        )
        
        print(f"   📊 Tipo de análisis: {result.get('analysis_type', 'error')}")
        print(f"   📊 Error presente: {'error' in result}")
        
        if 'error' in result:
            print(f"   ❌ Error específico: {result['error']}")
            return False
        else:
            print("   ✅ Flujo asíncrono funciona")
            return True
            
    except Exception as e:
        print(f"   ❌ Error en flujo asíncrono: {e}")
        traceback.print_exc()
        return False

async def test_data_format_compatibility():
    """Test de compatibilidad con diferentes formatos de datos"""
    print("\n🔍 DIAGNÓSTICO - COMPATIBILIDAD DATOS")
    print("=" * 40)
    
    try:
        from modules.ai.async_ai_processor import AsyncAIProcessor
        
        processor = AsyncAIProcessor()
        
        # Test 1: Formato DataFrame (correcto)
        print("   🔄 Probando formato DataFrame...")
        test_data_df = {
            'hospitales': pd.DataFrame([{'nombre': 'Hospital DF', 'distrito': 'Centro'}]),
            'demografia': pd.DataFrame([{'municipio': 'City DF', 'poblacion_2025': 1000}])
        }
        
        result_df = await processor.process_query_async(
            "¿Cuántos hospitales hay?",
            test_data_df,
            "invitado"
        )
        
        print(f"   📊 DataFrame: {result_df.get('analysis_type', 'error')}")
        
        # Test 2: Formato diccionario (respaldo)
        print("   🔄 Probando formato diccionario...")
        test_data_dict = {
            'hospitales': [{'nombre': 'Hospital Dict', 'distrito': 'Centro'}],
            'demografia': {'poblacion_2025': [1000], 'municipio': ['City Dict']}
        }
        
        result_dict = await processor.process_query_async(
            "¿Cuál es la población?",
            test_data_dict,
            "invitado"
        )
        
        print(f"   📊 Diccionario: {result_dict.get('analysis_type', 'error')}")
        
        # Verificar que ambos funcionan
        df_ok = 'error' not in result_df
        dict_ok = 'error' not in result_dict
        
        if df_ok and dict_ok:
            print("   ✅ Ambos formatos funcionan correctamente")
            return True
        else:
            print("   ⚠️ Algunos formatos tienen problemas")
            return False
            
    except Exception as e:
        print(f"   ❌ Error en test de compatibilidad: {e}")
        traceback.print_exc()
        return False

def main():
    """Ejecutar diagnóstico completo sin Streamlit"""
    print("🔍 DIAGNÓSTICO COMPLETO - ASYNC/AWAIT (STANDALONE)")
    print("=" * 70)
    
    tests = [
        ("Entorno", test_environment),
        ("Procesador", test_async_processor_creation)
    ]
    
    passed = 0
    for name, test_func in tests:
        if test_func():
            passed += 1
        else:
            print(f"\n⚠️ Test '{name}' falló - revisar configuración")
    
    # Tests asíncronos
    print(f"\n📊 TESTS SÍNCRONOS: {passed}/{len(tests)}")
    
    if passed >= 1:  # Al menos entorno
        try:
            print("\n🔄 Ejecutando tests asíncronos...")
            
            # Ejecutar tests asíncronos usando asyncio.run
            async def run_async_tests():
                results = []
                results.append(await test_groq_api_connection())
                results.append(await test_simple_async_flow())
                results.append(await test_data_format_compatibility())
                return results
            
            async_results = asyncio.run(run_async_tests())
            async_passed = sum(async_results)
            print(f"\n📊 TESTS ASÍNCRONOS: {async_passed}/{len(async_results)}")
            
            if async_passed == len(async_results):
                print("✅ Todos los tests asíncronos completados exitosamente")
            else:
                print("⚠️ Algunos tests asíncronos fallaron")
                
        except Exception as e:
            print(f"\n❌ Error en tests asíncronos: {e}")
    else:
        print("\n⚠️ Saltando tests asíncronos - configurar entorno primero")
    
    print("\n" + "=" * 70)
    print("💡 Si hay errores, revisa la configuración de GROQ_API_KEY")
    print("💡 Ejecuta: python scripts/setup_env.py")

if __name__ == "__main__":
    main()
