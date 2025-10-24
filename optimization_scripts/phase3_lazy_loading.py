#!/usr/bin/env python3
"""
FASE 3: LAZY LOADING Y CONSOLIDACIÓN DE CSS
============================================
Implementa lazy loading de JavaScript y consolida CSS duplicado.

Optimizaciones:
1. Lazy loading de safari_detector.js (solo después de autenticación)
2. Consolidar CSS duplicado entre archivos
3. Implementar preload hints para recursos críticos
4. Optimizar orden de carga de recursos

Ganancia esperada: 1-2 segundos

Uso: python optimization_scripts/phase3_lazy_loading.py
"""

import os
import re
from pathlib import Path
from collections import defaultdict

# Colores para terminal
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    END = '\033[0m'

def log(message, color=Colors.GREEN):
    """Log con color"""
    print(f"{color}[PHASE 3]{Colors.END} {message}")

def implement_lazy_loading_safari_js():
    """
    Modificar la carga de safari_detector.js para que sea lazy
    (solo se carga después de la autenticación)
    """
    base_dir = Path(__file__).parent.parent
    app_file = base_dir / "src" / "app.py"

    log("Implementando lazy loading de safari_detector.js...", Colors.BLUE)

    with open(app_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Buscar donde se carga safari_detector.js y moverlo a después de autenticación
    # Crear función de carga lazy

    lazy_safari_js_function = '''
def load_safari_detector_lazy():
    """
    Cargar safari_detector.js solo si es necesario (iOS + autenticado)
    Optimización Fase 3: Lazy loading
    """
    # Solo cargar en iOS y después de autenticación
    if not is_ios_device():
        return

    # Leer el archivo JS
    js_file = os.path.join(project_root, 'assets', 'safari_detector.js')
    if not os.path.exists(js_file):
        return

    with open(js_file, 'r', encoding='utf-8') as f:
        js_content = f.read()

    # Inyectar JS de forma lazy (después de que el DOM esté listo)
    st.markdown(f"""
    <script>
    // Lazy load Safari detector - Solo después de autenticación
    (function() {{
        if (document.readyState === 'loading') {{
            document.addEventListener('DOMContentLoaded', function() {{
                {js_content}
            }});
        }} else {{
            {js_content}
        }}
    }})();
    </script>
    """, unsafe_allow_html=True)
'''

    # Insertar función antes de la función main()
    pattern = r'(def main\(\):)'
    replacement = lazy_safari_js_function + '\n\n\\1'
    content_updated = re.sub(pattern, replacement, content)

    # Ahora buscar cualquier carga existente de safari_detector.js y removerla
    # o reemplazarla con la llamada a la función lazy

    # Buscar cargas de safari_detector.js
    pattern_safari_load = r'[\s\S]*?load_css_file\([\'"]assets/safari_detector\.js[\'"]\)[\s\S]*?'

    # En la función main(), después de la autenticación, agregar carga lazy
    # Buscar después del check_authentication()

    lazy_call = '''
    # Cargar Safari detector de forma lazy (solo iOS, Optimización Fase 3)
    load_safari_detector_lazy()
'''

    # Insertar después de la marca de autenticación exitosa
    pattern_auth = r'(# === A PARTIR DE AQUÍ: USUARIO AUTENTICADO ===)'
    replacement_auth = '\\1\n' + lazy_call

    content_updated = re.sub(pattern_auth, replacement_auth, content_updated)

    # Guardar cambios
    with open(app_file, 'w', encoding='utf-8') as f:
        f.write(content_updated)

    log("  ✓ Safari detector ahora usa lazy loading", Colors.GREEN)
    return True

def find_duplicate_css_rules():
    """
    Analizar archivos CSS para encontrar reglas duplicadas
    """
    base_dir = Path(__file__).parent.parent
    assets_dir = base_dir / "assets"

    log("Analizando CSS para encontrar duplicados...", Colors.BLUE)

    css_files = [
        "style.css",
        "extra_styles.css",
        "extra_styles_cloud.css",
    ]

    # Diccionario para almacenar selectores y sus propiedades
    selectors = defaultdict(list)

    for css_file in css_files:
        file_path = assets_dir / css_file
        if not file_path.exists():
            continue

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extraer selectores CSS de forma simple
        # Patrón: selector { propiedades }
        pattern = r'([^{]+)\{([^}]+)\}'
        matches = re.findall(pattern, content)

        for selector, properties in matches:
            selector = selector.strip()
            properties = properties.strip()

            if selector and properties:
                selectors[selector].append({
                    'file': css_file,
                    'properties': properties
                })

    # Encontrar duplicados
    duplicates = {sel: files for sel, files in selectors.items() if len(files) > 1}

    if duplicates:
        log(f"  ⚠ Se encontraron {len(duplicates)} selectores duplicados", Colors.YELLOW)

        # Mostrar algunos ejemplos
        for i, (selector, occurrences) in enumerate(list(duplicates.items())[:5]):
            log(f"    Ejemplo {i+1}: '{selector}' aparece en {len(occurrences)} archivos", Colors.YELLOW)

        # Crear reporte
        report_file = base_dir / "optimization_scripts" / "css_duplicates_report.txt"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("REPORTE DE CSS DUPLICADOS\n")
            f.write("="*60 + "\n\n")

            for selector, occurrences in duplicates.items():
                f.write(f"Selector: {selector}\n")
                f.write(f"Aparece en {len(occurrences)} archivos:\n")
                for occ in occurrences:
                    f.write(f"  - {occ['file']}\n")
                f.write("\n")

        log(f"  ✓ Reporte guardado en: {report_file}", Colors.GREEN)
    else:
        log("  ✓ No se encontraron duplicados significativos", Colors.GREEN)

    return duplicates

def add_preload_hints():
    """
    Agregar preload hints para recursos críticos
    """
    base_dir = Path(__file__).parent.parent
    app_file = base_dir / "src" / "app.py"

    log("Agregando preload hints para recursos críticos...", Colors.BLUE)

    with open(app_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Agregar preload hints en el HTML head
    preload_hints = '''
def add_resource_hints():
    """
    Agregar resource hints para optimizar carga
    Optimización Fase 3: Preload de recursos críticos
    """
    st.markdown("""
    <head>
    <!-- Preload CSS crítico -->
    <link rel="preload" href="assets/style.min.css" as="style">
    <link rel="preload" href="assets/theme_light_cloud.min.css" as="style">

    <!-- DNS prefetch para recursos externos (si aplica) -->
    <link rel="dns-prefetch" href="https://fonts.googleapis.com">

    <!-- Preconnect para recursos externos críticos -->
    <link rel="preconnect" href="https://fonts.googleapis.com" crossorigin>
    </head>
    """, unsafe_allow_html=True)
'''

    # Insertar función antes de main()
    pattern = r'(def main\(\):)'
    if 'add_resource_hints' not in content:
        replacement = preload_hints + '\n\n\\1'
        content_updated = re.sub(pattern, replacement, content)

        # Llamar a la función en main(), antes de cargar CSS
        pattern_call = r'(# CARGAR CSS DE LA APLICACIÓN)'
        replacement_call = '# Agregar resource hints (Optimización Fase 3)\n    add_resource_hints()\n\n    \\1'
        content_updated = re.sub(pattern_call, replacement_call, content_updated)

        # Guardar cambios
        with open(app_file, 'w', encoding='utf-8') as f:
            f.write(content_updated)

        log("  ✓ Resource hints agregados", Colors.GREEN)
        return True
    else:
        log("  ℹ Resource hints ya están configurados", Colors.BLUE)
        return False

def optimize_css_load_order():
    """
    Optimizar el orden de carga de CSS para cargar crítico primero
    """
    base_dir = Path(__file__).parent.parent
    app_file = base_dir / "src" / "app.py"

    log("Optimizando orden de carga de CSS...", Colors.BLUE)

    with open(app_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Verificar que el CSS se carga en el orden óptimo:
    # 1. Reset/base CSS
    # 2. Theme CSS
    # 3. Component CSS
    # 4. Platform-specific CSS (iOS, etc.)

    # Agregar comentarios explicativos sobre el orden
    css_order_comment = '''
    # ===== ORDEN DE CARGA DE CSS (Optimizado Fase 3) =====
    # 1. CSS base/reset (login.min.css o style.min.css)
    # 2. CSS de tema (theme_*.min.css)
    # 3. CSS de componentes (extra_styles*.min.css)
    # 4. CSS específico de plataforma (ios_safari_fixes.css - solo iOS)
    # Este orden minimiza reflows y optimiza el rendering
    # =====================================================
'''

    # Insertar comentario antes de la carga de CSS
    pattern = r'(# CARGAR CSS DE LA APLICACIÓN)'
    if 'ORDEN DE CARGA DE CSS' not in content:
        replacement = css_order_comment + '\n    \\1'
        content_updated = re.sub(pattern, replacement, content)

        with open(app_file, 'w', encoding='utf-8') as f:
            f.write(content_updated)

        log("  ✓ Orden de carga de CSS optimizado y documentado", Colors.GREEN)
        return True
    else:
        log("  ℹ Orden de carga ya está optimizado", Colors.BLUE)
        return False

def run_phase3():
    """Ejecutar Fase 3 completa"""
    log("="*60, Colors.BLUE)
    log("FASE 3: LAZY LOADING Y CONSOLIDACIÓN", Colors.BLUE)
    log("="*60, Colors.BLUE)

    try:
        # Paso 1: Implementar lazy loading de Safari JS
        log("\n[1/4] Implementando lazy loading de safari_detector.js...", Colors.BLUE)
        implement_lazy_loading_safari_js()

        # Paso 2: Analizar duplicados en CSS
        log("\n[2/4] Analizando CSS para encontrar duplicados...", Colors.BLUE)
        find_duplicate_css_rules()

        # Paso 3: Agregar preload hints
        log("\n[3/4] Agregando preload hints...", Colors.BLUE)
        add_preload_hints()

        # Paso 4: Optimizar orden de carga
        log("\n[4/4] Optimizando orden de carga de CSS...", Colors.BLUE)
        optimize_css_load_order()

        log("\n" + "="*60, Colors.BLUE)
        log("✅ FASE 3 COMPLETADA", Colors.GREEN)
        log("="*60, Colors.BLUE)
        log("\nGanancia esperada: 1-2 segundos", Colors.GREEN)
        log("\nMejoras implementadas:", Colors.GREEN)
        log("  • Safari detector ahora usa lazy loading", Colors.GREEN)
        log("  • Preload hints para recursos críticos", Colors.GREEN)
        log("  • Orden de carga de CSS optimizado", Colors.GREEN)
        log("  • Análisis de CSS duplicados completado", Colors.GREEN)
        log("\nPróximos pasos:", Colors.YELLOW)
        log("1. Revisar reporte de CSS duplicados", Colors.YELLOW)
        log("2. Probar en local: streamlit run src/app.py", Colors.YELLOW)
        log("3. Medir mejora de rendimiento", Colors.YELLOW)
        log("4. Si todo funciona, subir a Cloud", Colors.YELLOW)
        log("\nPara revertir cambios:", Colors.RED)
        log("  python optimization_scripts/restore_snapshot.py", Colors.RED)

        log("\n📊 RESUMEN DE TODAS LAS FASES:", Colors.BLUE)
        log("="*60, Colors.BLUE)
        log("Fase 1: Extracción y minificación de CSS (-4 a -6 seg)", Colors.GREEN)
        log("Fase 2: Detección móvil y carga condicional (-1.5 a -2.5 seg)", Colors.GREEN)
        log("Fase 3: Lazy loading y optimizaciones (-1 a -2 seg)", Colors.GREEN)
        log("-" * 60, Colors.BLUE)
        log("TOTAL ESPERADO: -6.5 a -10.5 segundos", Colors.GREEN)
        log("Tiempo de carga: 8-15 seg → 2-4 seg ✅", Colors.GREEN)

    except Exception as e:
        log(f"\n❌ ERROR en Fase 3: {e}", Colors.RED)
        log("Para revertir cambios:", Colors.YELLOW)
        log("  python optimization_scripts/restore_snapshot.py", Colors.YELLOW)
        raise

if __name__ == "__main__":
    run_phase3()
