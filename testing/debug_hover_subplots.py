#!/usr/bin/env python3
"""
ARCHIVO DEBUG PARA RASTREAR PROBLEMAS DE HOVER EN SUBPLOTS
==========================================================

Este archivo está diseñado para identificar específicamente el problema
que ocurre en chat AI con hoversubplots y rangesliders.

Problema identificado en chart_generator.py:
- El error ocurre cuando Plotly intenta renderizar gráficos con configuraciones específicas
- La línea 787 desactiva hovermode=False pero el problema puede venir de subplots
- Hay protecciones extremas contra rangeslider pero el problema persiste

ÁREAS PROBLEMÁTICAS IDENTIFICADAS:
1. hovermode=False en línea 787 puede no ser suficiente
2. Subplots creados en _create_equity_dashboard() línea 488-493
3. Posible conflicto entre rangeslider protection y subplot configuration
4. Layout update en _apply_health_theme() puede introducir configuraciones problemáticas
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import sys
import traceback
from typing import Dict, Any, Optional
import json

class HoverSubplotDebugger:
    """Debugger especializado para problemas de hover en subplots"""

    def __init__(self):
        self.debug_log = []
        self.error_log = []

    def log(self, message: str, level: str = "INFO"):
        """Log de debug con timestamp"""
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
        entry = f"[{timestamp}] {level}: {message}"
        self.debug_log.append(entry)
        print(entry)

    def log_error(self, message: str, exception: Exception = None):
        """Log de errores con traceback completo"""
        self.log(f"ERROR: {message}", "ERROR")
        if exception:
            tb = traceback.format_exc()
            self.error_log.append({
                'message': message,
                'exception': str(exception),
                'traceback': tb
            })
            self.log(f"Exception: {str(exception)}", "ERROR")
            self.log(f"Traceback: {tb}", "ERROR")

    def inspect_figure_layout(self, fig: go.Figure, stage: str = ""):
        """Inspección profunda del layout de la figura"""
        self.log(f"=== INSPECCIÓN LAYOUT {stage} ===")

        try:
            if hasattr(fig, 'layout'):
                layout_dict = fig.layout.to_dict()

                # Inspeccionar todas las propiedades del layout
                for key, value in layout_dict.items():
                    if 'axis' in key:
                        self.log(f"AXIS FOUND: {key} = {type(value)}")
                        if isinstance(value, dict):
                            for subkey, subvalue in value.items():
                                if 'hover' in subkey.lower() or 'range' in subkey.lower():
                                    self.log(f"  🚨 CRITICAL: {key}.{subkey} = {subvalue}")

                    elif 'hover' in key.lower():
                        self.log(f"🚨 HOVER CONFIG: {key} = {value}")

                    elif 'range' in key.lower():
                        self.log(f"🚨 RANGE CONFIG: {key} = {value}")

                # Verificar configuraciones específicas problemáticas
                problematic_keys = [
                    'hovermode', 'hoverdistance', 'spikedistance',
                    'hoversubplots', 'showrangeslider', 'rangeslider'
                ]

                for key in problematic_keys:
                    if key in layout_dict:
                        value = layout_dict[key]
                        self.log(f"🎯 PROBLEMATIC KEY: {key} = {value} (type: {type(value)})")

        except Exception as e:
            self.log_error("Error inspeccionando layout", e)

    def inspect_figure_data(self, fig: go.Figure, stage: str = ""):
        """Inspección de los datos de la figura"""
        self.log(f"=== INSPECCIÓN DATA {stage} ===")

        try:
            if hasattr(fig, 'data'):
                self.log(f"Número de traces: {len(fig.data)}")

                for i, trace in enumerate(fig.data):
                    self.log(f"Trace {i}: {type(trace).__name__}")

                    # Verificar propiedades hover específicas del trace
                    trace_dict = trace.to_dict()
                    hover_props = [key for key in trace_dict.keys() if 'hover' in key.lower()]

                    if hover_props:
                        self.log(f"  Hover properties en trace {i}: {hover_props}")
                        for prop in hover_props:
                            self.log(f"    {prop}: {trace_dict[prop]}")

        except Exception as e:
            self.log_error("Error inspeccionando data", e)

    def test_basic_subplot_creation(self):
        """Test 1: Crear subplot básico sin hover"""
        self.log("TEST 1: Subplot básico sin hover")

        try:
            # Crear subplot simple
            fig = make_subplots(
                rows=2, cols=2,
                subplot_titles=('Plot 1', 'Plot 2', 'Plot 3', 'Plot 4')
            )

            # Datos de prueba
            x = [1, 2, 3, 4, 5]
            y = [1, 4, 2, 8, 5]

            # Añadir traces simples
            fig.add_trace(go.Scatter(x=x, y=y, name='Serie 1'), row=1, col=1)
            fig.add_trace(go.Bar(x=x, y=y, name='Serie 2'), row=1, col=2)
            fig.add_trace(go.Scatter(x=x, y=[i*2 for i in y], name='Serie 3'), row=2, col=1)
            fig.add_trace(go.Bar(x=x, y=[i*1.5 for i in y], name='Serie 4'), row=2, col=2)

            # CONFIGURACIÓN CRÍTICA: Desactivar TODAS las opciones hover
            fig.update_layout(
                hovermode=False,  # Completamente desactivado
                showrangeslider=False
            )

            # Desactivar hover en todos los ejes
            for i in range(1, 5):  # 4 subplots
                if i == 1:
                    fig.update_xaxes(showrangeslider=False, rangeslider=dict(visible=False))
                    fig.update_yaxes(showrangeslider=False)
                else:
                    fig.update_xaxes(showrangeslider=False, rangeslider=dict(visible=False), row=1 if i <= 2 else 2, col=i if i <= 2 else i-2)
                    fig.update_yaxes(showrangeslider=False, row=1 if i <= 2 else 2, col=i if i <= 2 else i-2)

            self.inspect_figure_layout(fig, "BASIC_SUBPLOT_AFTER_CONFIG")
            self.inspect_figure_data(fig, "BASIC_SUBPLOT_AFTER_CONFIG")

            # Intentar serializar (esto es donde suele fallar)
            fig_json = fig.to_json()
            self.log("✅ Subplot básico serializado correctamente")

            return fig

        except Exception as e:
            self.log_error("ERROR en subplot básico", e)
            return None

    def test_equity_dashboard_recreation(self):
        """Test 2: Recrear el dashboard de equidad que causa problemas"""
        self.log("TEST 2: Recreación de equity dashboard problemático")

        try:
            # Datos de prueba similares a los reales
            equity_data = pd.DataFrame({
                'distrito': ['Norte', 'Sur', 'Este', 'Oeste'],
                'ratio_camas_1000hab': [2.5, 1.8, 3.2, 2.1],
                'score_equidad': [75, 45, 85, 60],
                'poblacion': [150000, 200000, 120000, 180000],
                'personal_total': [450, 320, 580, 410]
            })

            # Recrear exactamente el método problemático
            fig = make_subplots(
                rows=2, cols=2,
                subplot_titles=('Ratio Camas/1000 hab', 'Score de Equidad', 'Población por Distrito', 'Personal Sanitario'),
                specs=[[{"secondary_y": False}, {"secondary_y": False}],
                       [{"secondary_y": False}, {"secondary_y": False}]]
            )

            self.inspect_figure_layout(fig, "EQUITY_DASHBOARD_AFTER_CREATION")

            # Añadir traces uno por uno
            self.log("Añadiendo trace 1: Ratio camas")
            fig.add_trace(
                go.Bar(x=equity_data['distrito'], y=equity_data['ratio_camas_1000hab'],
                       name='Camas/1000 hab', marker_color='#00a86b'),
                row=1, col=1
            )
            self.inspect_figure_layout(fig, "EQUITY_DASHBOARD_AFTER_TRACE1")

            self.log("Añadiendo trace 2: Score equidad")
            colors = ['red' if score < 50 else 'orange' if score < 75 else 'green'
                      for score in equity_data['score_equidad']]
            fig.add_trace(
                go.Bar(x=equity_data['distrito'], y=equity_data['score_equidad'],
                       name='Score Equidad', marker_color=colors),
                row=1, col=2
            )
            self.inspect_figure_layout(fig, "EQUITY_DASHBOARD_AFTER_TRACE2")

            self.log("Añadiendo trace 3: Población")
            fig.add_trace(
                go.Scatter(x=equity_data['distrito'], y=equity_data['poblacion'],
                          mode='markers+lines', name='Población',
                          marker_color='#42a5f5'),
                row=2, col=1
            )
            self.inspect_figure_layout(fig, "EQUITY_DASHBOARD_AFTER_TRACE3")

            self.log("Añadiendo trace 4: Personal")
            fig.add_trace(
                go.Bar(x=equity_data['distrito'], y=equity_data['personal_total'],
                       name='Personal Total', marker_color='#66bb6a'),
                row=2, col=2
            )
            self.inspect_figure_layout(fig, "EQUITY_DASHBOARD_AFTER_ALL_TRACES")

            # Aplicar layout básico
            self.log("Aplicando layout básico")
            fig.update_layout(
                title_text="Dashboard de Equidad Sanitaria",
                showlegend=False,
                height=600,
                hovermode=False,  # CRÍTICO
                showrangeslider=False
            )
            self.inspect_figure_layout(fig, "EQUITY_DASHBOARD_AFTER_BASIC_LAYOUT")

            # Intentar serializar antes del tema
            try:
                fig_json = fig.to_json()
                self.log("✅ Dashboard serializado correctamente ANTES del tema")
            except Exception as e:
                self.log_error("❌ Dashboard FALLA al serializar ANTES del tema", e)
                return None

            return fig

        except Exception as e:
            self.log_error("ERROR en equity dashboard", e)
            return None

    def test_theme_application(self, fig: go.Figure):
        """Test 3: Aplicar tema y ver dónde falla"""
        self.log("TEST 3: Aplicación de tema donde puede fallar")

        if fig is None:
            self.log("No se puede aplicar tema - figura es None")
            return None

        try:
            self.log("Aplicando tema adaptativo...")

            # Colores de tema claro (como en el original)
            plot_bg = 'rgba(255, 255, 255, 0.95)'
            paper_bg = 'rgba(248, 250, 252, 0.98)'
            text_color = '#1f2937'
            title_color = '#059669'
            grid_color = 'rgba(156, 163, 175, 0.3)'
            line_color = 'rgba(75, 85, 99, 0.5)'

            self.log("Aplicando layout de tema...")
            fig.update_layout(
                # Fondo adaptativo según tema
                plot_bgcolor=plot_bg,
                paper_bgcolor=paper_bg,

                # Tipografía con colores adaptativos
                font=dict(family="Inter, Arial, sans-serif", size=12, color=text_color),
                title_font=dict(size=16, color=title_color, family="Inter"),

                # Márgenes y espaciado
                margin=dict(l=60, r=60, t=80, b=60),

                # Grid y ejes con colores adaptativos
                xaxis=dict(
                    showgrid=True,
                    gridcolor=grid_color,
                    linecolor=line_color,
                    tickfont=dict(color=text_color),
                    title=dict(font=dict(color=text_color)),
                    rangeslider=dict(visible=False),
                    showrangeslider=False
                ),
                yaxis=dict(
                    showgrid=True,
                    gridcolor=grid_color,
                    linecolor=line_color,
                    tickfont=dict(color=text_color),
                    title=dict(font=dict(color=text_color))
                ),

                # ESTA ES LA LÍNEA PROBLEMÁTICA POTENCIAL:
                hovermode=False,  # En lugar de 'closest' o True

                # Leyenda con tema adaptativo
                legend=dict(
                    bgcolor='rgba(255, 255, 255, 0.9)',
                    bordercolor='rgba(156, 163, 175, 0.3)',
                    font=dict(color=text_color)
                ),

                # PROTECCIONES ADICIONALES PARA STREAMLIT
                showrangeslider=False,
                rangeslider=dict(visible=False)
            )

            self.inspect_figure_layout(fig, "AFTER_THEME_APPLICATION")

            # Intentar serializar después del tema
            try:
                fig_json = fig.to_json()
                self.log("✅ Figura serializada correctamente DESPUÉS del tema")
                return fig
            except Exception as e:
                self.log_error("❌ Figura FALLA al serializar DESPUÉS del tema", e)

                # Analizar el error específico
                if 'hoversubplots' in str(e).lower():
                    self.log("🎯 ERROR CONFIRMADO: Problema con hoversubplots")
                elif 'rangeslider' in str(e).lower():
                    self.log("🎯 ERROR CONFIRMADO: Problema con rangeslider")
                elif 'hover' in str(e).lower():
                    self.log("🎯 ERROR CONFIRMADO: Problema general de hover")

                return None

        except Exception as e:
            self.log_error("ERROR aplicando tema", e)
            return None

    def test_minimal_failing_case(self):
        """Test 4: Caso mínimo que reproduce el error"""
        self.log("TEST 4: Caso mínimo para reproducir el error")

        try:
            # Crear el caso más simple posible que falle
            fig = make_subplots(rows=1, cols=2)

            # Añadir datos mínimos
            fig.add_trace(go.Scatter(x=[1, 2, 3], y=[1, 2, 3]), row=1, col=1)
            fig.add_trace(go.Bar(x=[1, 2, 3], y=[3, 2, 1]), row=1, col=2)

            # Probar diferentes configuraciones una a la vez
            configs_to_test = [
                {"hovermode": False},
                {"hovermode": None},
                {"hovermode": "closest"},
                {"showrangeslider": False},
                {"rangeslider": {"visible": False}},
                {"hovermode": False, "showrangeslider": False},
            ]

            for i, config in enumerate(configs_to_test):
                try:
                    self.log(f"Probando configuración {i+1}: {config}")
                    test_fig = go.Figure(fig)  # Copia
                    test_fig.update_layout(**config)

                    # Intentar serializar
                    test_json = test_fig.to_json()
                    self.log(f"✅ Configuración {i+1} OK")

                except Exception as e:
                    self.log_error(f"❌ Configuración {i+1} FALLA", e)

        except Exception as e:
            self.log_error("ERROR en caso mínimo", e)

    def run_comprehensive_debug(self):
        """Ejecutar todos los tests de debug"""
        self.log("🚀 INICIANDO DEBUG COMPREHENSIVO DE HOVER SUBPLOTS")
        self.log("="*60)

        # Test 1: Subplot básico
        basic_fig = self.test_basic_subplot_creation()

        # Test 2: Dashboard de equidad
        equity_fig = self.test_equity_dashboard_recreation()

        # Test 3: Aplicación de tema
        if equity_fig:
            themed_fig = self.test_theme_application(equity_fig)

        # Test 4: Caso mínimo
        self.test_minimal_failing_case()

        # Generar reporte final
        self.generate_final_report()

    def generate_final_report(self):
        """Generar reporte final de debug"""
        self.log("="*60)
        self.log("📋 REPORTE FINAL DE DEBUG")
        self.log("="*60)

        self.log("RESUMEN DE LOGS:")
        for entry in self.debug_log[-20:]:  # Últimos 20 logs
            print(entry)

        if self.error_log:
            self.log("\n❌ ERRORES ENCONTRADOS:")
            for error in self.error_log:
                self.log(f"Error: {error['message']}")
                self.log(f"Exception: {error['exception']}")
                self.log("---")

        self.log("\n🎯 RECOMENDACIONES:")
        self.log("1. Verificar si el problema es específico de 'hoversubplots'")
        self.log("2. Revisar configuraciones de rangeslider en subplots")
        self.log("3. Considerar usar hovermode=None en lugar de hovermode=False")
        self.log("4. Verificar compatibilidad de Plotly con Streamlit")

        # Guardar reporte en archivo
        try:
            with open('hover_debug_report.txt', 'w', encoding='utf-8') as f:
                f.write("REPORTE DEBUG HOVER SUBPLOTS\n")
                f.write("="*50 + "\n\n")

                f.write("LOGS COMPLETOS:\n")
                for entry in self.debug_log:
                    f.write(entry + "\n")

                if self.error_log:
                    f.write("\nERRORES DETALLADOS:\n")
                    for error in self.error_log:
                        f.write(f"Error: {error['message']}\n")
                        f.write(f"Exception: {error['exception']}\n")
                        f.write(f"Traceback:\n{error['traceback']}\n")
                        f.write("-" * 30 + "\n")

            self.log("✅ Reporte guardado en 'hover_debug_report.txt'")
        except Exception as e:
            self.log_error("Error guardando reporte", e)

def main():
    """Función principal para ejecutar el debug"""
    debugger = HoverSubplotDebugger()
    debugger.run_comprehensive_debug()

    print("\n" + "="*60)
    print("🔍 DEBUG COMPLETADO")
    print("📁 Revisar 'hover_debug_report.txt' para detalles completos")
    print("="*60)

if __name__ == "__main__":
    main()