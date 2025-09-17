#!/usr/bin/env python3
"""
Test de Formatos de Datos - Verificar compatibilidad con diferentes formatos
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

async def test_dataframe_format():
    """Test con formato DataFrame (formato correcto)"""
    print("🧪 TEST - FORMATO DATAFRAME")
    print("=" * 40)
    
    try:
        from modules.ai.async_ai_processor import AsyncAIProcessor
        
        processor = AsyncAIProcessor()
        
        # Datos en formato DataFrame (correcto)
        test_data = {
            'hospitales': pd.DataFrame([
                {'nombre': 'Hospital Test 1', 'distrito': 'Centro', 'camas': 100},
                {'nombre': 'Hospital Test 2', 'distrito': 'Norte', 'camas': 150}
            ]),
            'demografia': pd.DataFrame([
                {'municipio': 'Test City 1', 'poblacion_2025': 1000},
                {'municipio': 'Test City 2', 'poblacion_2025': 2000}
            ])
        }
        
        print("   📊 Datos en formato DataFrame")
        print(f"   📊 Hospitales: {len(test_data['hospitales'])} registros")
        print(f"   📊 Demografía: {len(test_data['demografia'])} registros")
        
        result = await processor.process_query_async(
            "¿Cuántos hospitales hay?",
            test_data,
            "invitado"
        )
        
        print(f"   📊 Resultado: {result.get('analysis_type', 'error')}")
        print(f"   📊 Error presente: {'error' in result}")
        
        if 'error' in result:
            print(f"   ❌ Error: {result['error']}")
            return False
        else:
            print("   ✅ Formato DataFrame funciona correctamente")
            return True
            
    except Exception as e:
        print(f"   ❌ Error en test DataFrame: {e}")
        return False

async def test_dict_format():
    """Test con formato diccionario (formato de respaldo)"""
    print("\n🧪 TEST - FORMATO DICCIONARIO")
    print("=" * 40)
    
    try:
        from modules.ai.async_ai_processor import AsyncAIProcessor
        
        processor = AsyncAIProcessor()
        
        # Datos en formato diccionario (respaldo)
        test_data = {
            'hospitales': [
                {'nombre': 'Hospital Test 1', 'distrito': 'Centro'},
                {'nombre': 'Hospital Test 2', 'distrito': 'Norte'}
            ],
            'demografia': {
                'poblacion_2025': [1000, 2000],
                'municipio': ['Test City 1', 'Test City 2']
            }
        }
        
        print("   📊 Datos en formato diccionario")
        print(f"   📊 Hospitales: {len(test_data['hospitales'])} registros")
        print(f"   📊 Demografía: {len(test_data['demografia']['poblacion_2025'])} registros")
        
        result = await processor.process_query_async(
            "¿Cuál es la población total?",
            test_data,
            "invitado"
        )
        
        print(f"   📊 Resultado: {result.get('analysis_type', 'error')}")
        print(f"   📊 Error presente: {'error' in result}")
        
        if 'error' in result:
            print(f"   ❌ Error: {result['error']}")
            return False
        else:
            print("   ✅ Formato diccionario funciona correctamente")
            return True
            
    except Exception as e:
        print(f"   ❌ Error en test diccionario: {e}")
        return False

async def test_mixed_format():
    """Test con formato mixto"""
    print("\n🧪 TEST - FORMATO MIXTO")
    print("=" * 40)
    
    try:
        from modules.ai.async_ai_processor import AsyncAIProcessor
        
        processor = AsyncAIProcessor()
        
        # Datos en formato mixto
        test_data = {
            'hospitales': pd.DataFrame([
                {'nombre': 'Hospital Test', 'distrito': 'Centro'}
            ]),
            'demografia': {
                'poblacion_2025': [1000, 2000]
            }
        }
        
        print("   📊 Datos en formato mixto")
        print(f"   📊 Hospitales: DataFrame con {len(test_data['hospitales'])} registros")
        print(f"   📊 Demografía: Diccionario con {len(test_data['demografia']['poblacion_2025'])} valores")
        
        result = await processor.process_query_async(
            "¿Cuántos hospitales y cuál es la población?",
            test_data,
            "invitado"
        )
        
        print(f"   📊 Resultado: {result.get('analysis_type', 'error')}")
        print(f"   📊 Error presente: {'error' in result}")
        
        if 'error' in result:
            print(f"   ❌ Error: {result['error']}")
            return False
        else:
            print("   ✅ Formato mixto funciona correctamente")
            return True
            
    except Exception as e:
        print(f"   ❌ Error en test mixto: {e}")
        return False

def main():
    """Ejecutar todos los tests de formatos"""
    print("🧪 TESTS DE FORMATOS DE DATOS")
    print("=" * 50)
    
    try:
        # Ejecutar tests asíncronos
        results = asyncio.run(test_dataframe_format())
        results += asyncio.run(test_dict_format())
        results += asyncio.run(test_mixed_format())
        
        print(f"\n📊 RESULTADOS: {results}/3 tests pasaron")
        
        if results == 3:
            print("🎉 ¡Todos los formatos de datos funcionan correctamente!")
            print("✅ El procesador asíncrono es robusto y compatible")
        else:
            print("⚠️ Algunos formatos necesitan ajustes")
            
    except Exception as e:
        print(f"❌ Error ejecutando tests: {e}")

if __name__ == "__main__":
    main()
