#!/usr/bin/env python3
"""
Test Asíncrono Simple - Versión robusta y fácil de usar
"""

import sys
import os
import asyncio
import pandas as pd

# Añadir el directorio raíz al path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Cargar variables de entorno
from dotenv import load_dotenv
load_dotenv()

def test_environment():
    """Verificar entorno básico"""
    print("🔍 VERIFICANDO ENTORNO")
    print("=" * 30)
    
    # Verificar GROQ_API_KEY
    groq_key = os.getenv("GROQ_API_KEY")
    if groq_key and groq_key != "tu_groq_api_key_aqui":
        print(f"✅ GROQ_API_KEY: {groq_key[:10]}...")
        return True
    else:
        print("❌ GROQ_API_KEY no configurada")
        print("💡 Edita el archivo .env y configura tu API key")
        return False

def test_dependencies():
    """Verificar dependencias"""
    print("\n🔍 VERIFICANDO DEPENDENCIAS")
    print("=" * 30)
    
    deps = ['aiohttp', 'pandas', 'dotenv']
    all_ok = True
    
    for dep in deps:
        try:
            __import__(dep)
            print(f"✅ {dep}")
        except ImportError:
            print(f"❌ {dep} - Instalar con: pip install {dep}")
            all_ok = False
    
    return all_ok

async def test_groq_api():
    """Test directo de Groq API"""
    print("\n🔍 PROBANDO GROQ API")
    print("=" * 30)
    
    try:
        import aiohttp
        import json
        
        groq_key = os.getenv("GROQ_API_KEY")
        url = "https://api.groq.com/openai/v1/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {groq_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "user", "content": "Responde solo 'OK' si funciona"}
            ],
            "max_tokens": 10
        }
        
        print("🔄 Enviando petición...")
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=data) as response:
                if response.status == 200:
                    result = await response.json()
                    content = result['choices'][0]['message']['content']
                    print(f"✅ Respuesta: {content}")
                    return True
                else:
                    error = await response.text()
                    print(f"❌ Error {response.status}: {error}")
                    return False
                    
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

async def test_async_processor():
    """Test del procesador asíncrono"""
    print("\n🔍 PROBANDO PROCESADOR ASÍNCRONO")
    print("=" * 30)
    
    try:
        # Mock de streamlit para evitar warnings
        class MockStreamlit:
            class SessionState:
                def __init__(self):
                    self._state = {}
                def __getitem__(self, key):
                    return self._state[key]
                def __setitem__(self, key, value):
                    self._state[key] = value
                def __contains__(self, key):
                    return key in self._state
            
            def __init__(self):
                self.session_state = self.SessionState()
        
        # Reemplazar streamlit temporalmente
        original_streamlit = sys.modules.get('streamlit')
        sys.modules['streamlit'] = MockStreamlit()
        
        try:
            from modules.ai.async_ai_processor import AsyncAIProcessor
            
            processor = AsyncAIProcessor()
            print("✅ Procesador creado")
            
            # Datos de prueba
            test_data = {
                'hospitales': pd.DataFrame([{'nombre': 'Test Hospital'}]),
                'demografia': pd.DataFrame([{'poblacion_2025': 1000}])
            }
            
            print("🔄 Procesando consulta...")
            result = await processor.process_query_async(
                "¿Cuántos hospitales hay?",
                test_data,
                "invitado"
            )
            
            if 'error' in result:
                print(f"❌ Error: {result['error']}")
                return False
            else:
                print("✅ Procesamiento exitoso")
                return True
                
        finally:
            # Restaurar streamlit original
            if original_streamlit:
                sys.modules['streamlit'] = original_streamlit
            else:
                del sys.modules['streamlit']
                
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

async def test_concurrent_processing():
    """Test de procesamiento concurrente"""
    print("\n🔍 PROBANDO PROCESAMIENTO CONCURRENTE")
    print("=" * 30)
    
    try:
        async def mock_task(task_id, delay=0.1):
            await asyncio.sleep(delay)
            return f"Tarea {task_id} completada"
        
        print("🔄 Ejecutando 3 tareas concurrentes...")
        
        tasks = [mock_task(i) for i in range(1, 4)]
        results = await asyncio.gather(*tasks)
        
        print(f"✅ {len(results)} tareas completadas:")
        for result in results:
            print(f"   - {result}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

async def main():
    """Función principal asíncrona"""
    print("🚀 TEST ASYNC/AWAIT SIMPLE")
    print("=" * 50)
    
    # Tests síncronos
    env_ok = test_environment()
    deps_ok = test_dependencies()
    
    if not env_ok or not deps_ok:
        print("\n❌ Configuración básica falló")
        return
    
    # Tests asíncronos
    print("\n🔄 Ejecutando tests asíncronos...")
    
    results = []
    results.append(await test_groq_api())
    results.append(await test_async_processor())
    results.append(await test_concurrent_processing())
    
    passed = sum(results)
    total = len(results)
    
    print(f"\n📊 RESULTADOS: {passed}/{total} tests pasaron")
    
    if passed == total:
        print("🎉 ¡Todos los tests pasaron!")
        print("✅ El async/await funciona correctamente en tu proyecto")
    else:
        print("⚠️ Algunos tests fallaron")
        print("💡 Revisa la configuración y dependencias")

if __name__ == "__main__":
    asyncio.run(main())
