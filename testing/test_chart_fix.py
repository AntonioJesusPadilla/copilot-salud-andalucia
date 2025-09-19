#!/usr/bin/env python3
"""
TEST DE VERIFICACIÓN DE LAS CORRECCIONES EN CHART_GENERATOR
==========================================================

Este script prueba que las correcciones aplicadas al chart_generator.py
funcionen correctamente y no produzcan errores de 'showrangeslider'.
"""

import sys
import os
import pandas as pd

# Añadir el directorio raíz al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules.visualization.chart_generator import SmartChartGenerator

def test_basic_chart_creation():
    """Test básico de creación de gráficos"""
    print("🧪 TEST 1: Creación básica de gráficos")

    generator = SmartChartGenerator()
    generator.debug_mode = True  # Activar debug para ver detalles

    # Datos de prueba
    data = pd.DataFrame({
        'distrito': ['Norte', 'Sur', 'Este', 'Oeste', 'Centro'],
        'camas_funcionamiento_2025': [250, 180, 320, 210, 280],
        'personal_sanitario_2025': [450, 320, 580, 410, 520],
        'poblacion_referencia_2025': [150000, 200000, 120000, 180000, 160000]
    })

    # Configuraciones de prueba
    test_configs = [
        {
            'type': 'bar',
            'title': 'Test Gráfico de Barras',
            'x_axis': 'distrito',
            'y_axis': 'camas_funcionamiento_2025'
        },
        {
            'type': 'scatter',
            'title': 'Test Gráfico de Dispersión',
            'x_axis': 'camas_funcionamiento_2025',
            'y_axis': 'personal_sanitario_2025'
        },
        {
            'type': 'line',
            'title': 'Test Gráfico de Líneas',
            'x_axis': 'distrito',
            'y_axis': 'poblacion_referencia_2025'
        },
        {
            'type': 'pie',
            'title': 'Test Gráfico Circular'
        }
    ]

    results = []

    for i, config in enumerate(test_configs):
        try:
            print(f"\n--- Probando configuración {i+1}: {config['type']} ---")

            fig = generator.generate_chart(config, data, 'light')

            # Verificar que la figura no es None
            if fig is None:
                print(f"❌ ERROR: generate_chart devolvió None para {config['type']}")
                results.append(False)
                continue

            # Intentar serializar (aquí es donde solían fallar)
            try:
                fig_json = fig.to_json()
                print(f"✅ ÉXITO: {config['type']} creado y serializado correctamente")
                results.append(True)
            except Exception as e:
                print(f"❌ ERROR al serializar {config['type']}: {str(e)}")
                results.append(False)

        except Exception as e:
            print(f"❌ ERROR creando {config['type']}: {str(e)}")
            results.append(False)

    return results

def test_subplot_creation():
    """Test específico para subplots (que era donde fallaba)"""
    print("\n🧪 TEST 2: Creación de subplots (equity dashboard)")

    generator = SmartChartGenerator()
    generator.debug_mode = True

    # Datos similares a los del equity dashboard
    equity_data = pd.DataFrame({
        'distrito': ['Norte', 'Sur', 'Este', 'Oeste'],
        'ratio_camas_1000hab': [2.5, 1.8, 3.2, 2.1],
        'score_equidad': [75, 45, 85, 60],
        'poblacion': [150000, 200000, 120000, 180000],
        'personal_total': [450, 320, 580, 410]
    })

    try:
        # Esto antes fallaba debido a showrangeslider inválido
        equity_fig = generator._create_equity_dashboard(equity_data)

        if equity_fig is None:
            print("❌ ERROR: _create_equity_dashboard devolvió None")
            return False

        # Aplicar tema (otro punto de falla)
        themed_fig = generator._apply_health_theme(equity_fig, 'light')

        if themed_fig is None:
            print("❌ ERROR: _apply_health_theme devolvió None")
            return False

        # Intentar serializar
        fig_json = themed_fig.to_json()
        print("✅ ÉXITO: Equity dashboard creado, tematizado y serializado correctamente")
        return True

    except Exception as e:
        print(f"❌ ERROR en equity dashboard: {str(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return False

def test_theme_application():
    """Test específico para aplicación de temas"""
    print("\n🧪 TEST 3: Aplicación de temas")

    generator = SmartChartGenerator()
    generator.debug_mode = True

    data = pd.DataFrame({
        'x': [1, 2, 3, 4, 5],
        'y': [1, 4, 2, 8, 5]
    })

    config = {
        'type': 'scatter',
        'title': 'Test Aplicación de Tema',
        'x_axis': 'x',
        'y_axis': 'y'
    }

    themes = ['light', 'dark']
    results = []

    for theme in themes:
        try:
            print(f"\n--- Probando tema: {theme} ---")

            fig = generator.generate_chart(config, data, theme)

            if fig is None:
                print(f"❌ ERROR: generate_chart devolvió None para tema {theme}")
                results.append(False)
                continue

            # Serializar
            fig_json = fig.to_json()
            print(f"✅ ÉXITO: Tema {theme} aplicado correctamente")
            results.append(True)

        except Exception as e:
            print(f"❌ ERROR con tema {theme}: {str(e)}")
            results.append(False)

    return results

def main():
    """Función principal de testing"""
    print("🚀 INICIANDO TESTS DE VERIFICACIÓN DE CORRECCIONES")
    print("=" * 60)

    all_results = []

    # Test 1: Creación básica
    basic_results = test_basic_chart_creation()
    all_results.extend(basic_results)

    # Test 2: Subplots
    subplot_result = test_subplot_creation()
    all_results.append(subplot_result)

    # Test 3: Temas
    theme_results = test_theme_application()
    all_results.extend(theme_results)

    # Reporte final
    print("\n" + "=" * 60)
    print("📋 REPORTE FINAL")
    print("=" * 60)

    total_tests = len(all_results)
    passed_tests = sum(all_results)
    failed_tests = total_tests - passed_tests

    print(f"Total de tests: {total_tests}")
    print(f"Tests pasados: {passed_tests}")
    print(f"Tests fallados: {failed_tests}")
    print(f"Porcentaje de éxito: {(passed_tests/total_tests)*100:.1f}%")

    if failed_tests == 0:
        print("\n🎉 ¡TODOS LOS TESTS PASARON!")
        print("✅ Las correcciones funcionaron correctamente")
        print("✅ No hay más errores de 'showrangeslider'")
    else:
        print(f"\n⚠️ Hay {failed_tests} tests que aún fallan")
        print("❌ Revisar los errores reportados arriba")

    print("=" * 60)

if __name__ == "__main__":
    main()