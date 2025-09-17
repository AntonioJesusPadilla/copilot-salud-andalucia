#!/usr/bin/env python3
"""
Test Asíncrono Mínimo - Solo verificar funcionalidad core
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

def test_basic_async_functionality():
    """Test básico de funcionalidad asíncrona"""
    print("🧪 TEST BÁSICO ASYNC/AWAIT")
    print("=" * 40)
    
    # Verificar GROQ_API_KEY
    groq_key = os.getenv("GROQ_API_KEY")
    if not groq_key or groq_key == "tu_groq_api_key_aqui":
        print("❌ GROQ_API_KEY no configurada correctamente")
        print("💡 Configura tu API key en el archivo .env")
        return False
    
    print(f"✅ GROQ_API_KEY configurada: {groq_key[:10]}...")
    
    # Verificar dependencias
    try:
        import aiohttp
        print(f"✅ aiohttp disponible: {aiohttp.__version__}")
    except ImportError:
        print("❌ aiohttp no instalado")
        return False
    
    return True

async def test_groq_api_direct():
    """Test directo de la API de Groq"""
    print("\n🧪 TEST DIRECTO API GROQ")
    print("=" * 40)
    
    try:
        import aiohttp
        import json
        
        groq_key = os.getenv("GROQ_API_KEY")
        base_url = "https://api.groq.com/openai/v1/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {groq_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "system", "content": "Eres un asistente útil. Responde en español."},
                {"role": "user", "content": "Hola, ¿funciona la conexión?"}
            ],
            "temperature": 0.7,
            "max_tokens": 100
        }
        
        print("   🔄 Enviando petición a Groq API...")
        
        timeout = aiohttp.ClientTimeout(total=30)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(base_url, headers=headers, json=payload) as response:
                if response.status == 200:
                    result = await response.json()
                    content = result['choices'][0]['message']['content']
                    print(f"   ✅ Respuesta recibida: {content[:50]}...")
                    return True
                else:
                    error_text = await response.text()
                    print(f"   ❌ Error API: {response.status} - {error_text}")
                    return False
                    
    except Exception as e:
        print(f"   ❌ Error en petición: {e}")
        return False

async def test_async_data_processing():
    """Test de procesamiento asíncrono de datos"""
    print("\n🧪 TEST PROCESAMIENTO ASÍNCRONO")
    print("=" * 40)
    
    try:
        # Simular procesamiento asíncrono de datos
        async def process_data_async(data):
            await asyncio.sleep(0.1)  # Simular procesamiento
            return {"processed": True, "count": len(data)}
        
        # Test con diferentes tipos de datos
        test_cases = [
            [1, 2, 3, 4, 5],
            {"hospitales": [{"nombre": "Test"}]},
            pd.DataFrame([{"id": 1, "valor": 100}])
        ]
        
        results = []
        for i, test_data in enumerate(test_cases):
            print(f"   🔄 Procesando caso {i+1}...")
            result = await process_data_async(test_data)
            results.append(result)
            print(f"   ✅ Caso {i+1}: {result}")
        
        print(f"   📊 Total casos procesados: {len(results)}")
        return True
        
    except Exception as e:
        print(f"   ❌ Error en procesamiento: {e}")
        return False

async def test_concurrent_processing():
    """Test de procesamiento concurrente"""
    print("\n🧪 TEST PROCESAMIENTO CONCURRENTE")
    print("=" * 40)
    
    try:
        async def mock_ai_request(query, delay=0.1):
            await asyncio.sleep(delay)
            return f"Respuesta para: {query}"
        
        # Crear múltiples tareas concurrentes
        queries = [
            "¿Cuántos hospitales hay?",
            "¿Cuál es la población?",
            "¿Qué servicios están disponibles?"
        ]
        
        print(f"   🔄 Procesando {len(queries)} consultas concurrentemente...")
        
        # Ejecutar todas las tareas en paralelo
        tasks = [mock_ai_request(query) for query in queries]
        results = await asyncio.gather(*tasks)
        
        print(f"   ✅ {len(results)} consultas procesadas:")
        for i, result in enumerate(results):
            print(f"      {i+1}. {result}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error en procesamiento concurrente: {e}")
        return False

def main():
    """Ejecutar tests mínimos"""
    print("🚀 TESTS ASYNC/AWAIT MÍNIMOS")
    print("=" * 50)
    
    # Test síncrono
    if not test_basic_async_functionality():
        print("\n❌ Test básico falló - configurar entorno primero")
        return
    
    # Tests asíncronos
    try:
        results = asyncio.run(test_groq_api_direct())
        results += asyncio.run(test_async_data_processing())
        results += asyncio.run(test_concurrent_processing())
        
        print(f"\n📊 RESULTADOS: {results}/3 tests asíncronos pasaron")
        
        if results == 3:
            print("🎉 ¡Todos los tests asíncronos funcionan correctamente!")
            print("✅ El async/await está funcionando bien en tu proyecto")
        else:
            print("⚠️ Algunos tests fallaron - revisar configuración")
            
    except Exception as e:
        print(f"❌ Error ejecutando tests asíncronos: {e}")

if __name__ == "__main__":
    main()
