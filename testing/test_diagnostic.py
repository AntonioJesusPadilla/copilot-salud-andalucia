# Crear archivo: testing/test_diagnostic.py
#!/usr/bin/env python3
"""
Test de Diagnóstico para Async - Identificar problemas específicos
"""

import sys
import os
import asyncio
import traceback
from dotenv import load_dotenv

# Añadir el directorio raíz al path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Cargar variables de entorno desde .env
load_dotenv()

def test_environment():
    """Verificar variables de entorno y configuración"""
    print("🔍 DIAGNÓSTICO - ENTORNO")
    print("=" * 40)
    
    # Verificar que el archivo .env existe
    env_file = os.path.join(project_root, ".env")
    if os.path.exists(env_file):
        print(f"   ✅ Archivo .env encontrado: {env_file}")
    else:
        print(f"   ❌ Archivo .env no encontrado en: {env_file}")
        print("   💡 Solución: Ejecutar python scripts/setup_env.py")
        return False
    
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
    
    # Verificar JWT_SECRET_KEY
    jwt_secret = os.getenv("JWT_SECRET_KEY")
    if jwt_secret and jwt_secret != "tu_clave_jwt_super_segura_de_32_caracteres_o_mas":
        print(f"   ✅ JWT_SECRET_KEY: {jwt_secret[:10]}...")
    else:
        print("   ⚠️ JWT_SECRET_KEY: No configurada o valor por defecto")
    
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
        print(f"   �� Timeout: {processor.request_timeout}")
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
        print("   �� Probando conexión con Groq API...")
        
        # Datos de prueba mínimos (formato correcto con DataFrames)
        import pandas as pd
        
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

def test_streamlit_wrapper():
    """Test del wrapper de Streamlit"""
    print("\n🔍 DIAGNÓSTICO - WRAPPER")
    print("=" * 40)
    
    try:
        from modules.ai.streamlit_async_wrapper import StreamlitAsyncWrapper
        
        wrapper = StreamlitAsyncWrapper()
        print("   ✅ StreamlitAsyncWrapper creado")
        
        # Test de loop
        loop = wrapper._get_or_create_loop()
        if loop and not loop.is_closed():
            print("   ✅ Loop de asyncio creado")
        else:
            print("   ❌ Problema con loop de asyncio")
            return False
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error en wrapper: {e}")
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
        import pandas as pd
        
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

def test_env_loading():
    """Test específico para verificar carga del archivo .env"""
    print("\n🔍 DIAGNÓSTICO - CARGA .ENV")
    print("=" * 40)
    
    # Verificar archivo .env
    env_file = os.path.join(project_root, ".env")
    if not os.path.exists(env_file):
        print(f"   ❌ Archivo .env no existe en: {env_file}")
        return False
    
    print(f"   ✅ Archivo .env existe: {env_file}")
    
    # Leer contenido del archivo .env
    try:
        with open(env_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Verificar que contiene las variables necesarias
        required_vars = ['GROQ_API_KEY', 'JWT_SECRET_KEY', 'SECRET_KEY']
        missing_vars = []
        
        for var in required_vars:
            if f"{var}=" in content:
                print(f"   ✅ {var}: Encontrada en archivo")
            else:
                print(f"   ❌ {var}: No encontrada en archivo")
                missing_vars.append(var)
        
        if missing_vars:
            print(f"   ⚠️ Variables faltantes: {missing_vars}")
            return False
        
        # Verificar que las variables se cargan correctamente
        print("\n   🔄 Verificando carga de variables...")
        
        # Recargar .env para asegurar que se carga
        load_dotenv(override=True)
        
        groq_key = os.getenv("GROQ_API_KEY")
        jwt_secret = os.getenv("JWT_SECRET_KEY")
        secret_key = os.getenv("SECRET_KEY")
        
        if groq_key:
            print(f"   ✅ GROQ_API_KEY cargada: {groq_key[:10]}...")
        else:
            print("   ❌ GROQ_API_KEY no se cargó")
            return False
        
        if jwt_secret:
            print(f"   ✅ JWT_SECRET_KEY cargada: {jwt_secret[:10]}...")
        else:
            print("   ❌ JWT_SECRET_KEY no se cargó")
        
        if secret_key:
            print(f"   ✅ SECRET_KEY cargada: {secret_key[:10]}...")
        else:
            print("   ❌ SECRET_KEY no se cargó")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error leyendo archivo .env: {e}")
        return False

def main():
    """Ejecutar diagnóstico completo"""
    print("🔍 DIAGNÓSTICO COMPLETO - ASYNC/AWAIT")
    print("=" * 60)
    
    tests = [
        ("Carga .env", test_env_loading),
        ("Entorno", test_environment),
        ("Procesador", test_async_processor_creation),
        ("Wrapper", test_streamlit_wrapper)
    ]
    
    passed = 0
    for name, test_func in tests:
        if test_func():
            passed += 1
        else:
            print(f"\n⚠️ Test '{name}' falló - revisar configuración")
    
    # Test asíncrono solo si el entorno está bien
    print(f"\n📊 TESTS SÍNCRONOS: {passed}/{len(tests)}")
    
    if passed >= 2:  # Al menos carga .env y entorno
        try:
            asyncio.run(test_groq_api_connection())
            asyncio.run(test_simple_async_flow())
            print("\n✅ Tests asíncronos completados")
        except Exception as e:
            print(f"\n❌ Error en tests asíncronos: {e}")
    else:
        print("\n⚠️ Saltando tests asíncronos - configurar entorno primero")
    
    print("\n" + "=" * 60)
    print("💡 Si hay errores, revisa la configuración de GROQ_API_KEY")
    print("💡 Ejecuta: python scripts/setup_env.py")

if __name__ == "__main__":
    main()