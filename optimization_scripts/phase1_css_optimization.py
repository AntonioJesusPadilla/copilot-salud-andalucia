#!/usr/bin/env python3
"""
FASE 1: OPTIMIZACIÓN DE CSS
============================
Extrae CSS inline de auth_system.py a archivos externos y minifica assets CSS.

Optimizaciones:
1. Extraer CSS inline de render_login_page() a assets/login.css
2. Minificar CSS (usando csscompressor o método simple)
3. Actualizar referencias en el código para usar CSS externo

Ganancia esperada: 4-6 segundos en carga inicial

Uso: python optimization_scripts/phase1_css_optimization.py
"""

import os
import re
from pathlib import Path

# Colores para terminal
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    END = '\033[0m'

def log(message, color=Colors.GREEN):
    """Log con color"""
    print(f"{color}[PHASE 1]{Colors.END} {message}")

def minify_css_simple(css_content):
    """
    Minificación simple de CSS (sin dependencias externas)
    - Elimina comentarios
    - Elimina espacios en blanco innecesarios
    - Elimina saltos de línea
    """
    # Eliminar comentarios CSS (/* ... */)
    css_content = re.sub(r'/\*.*?\*/', '', css_content, flags=re.DOTALL)

    # Eliminar múltiples espacios
    css_content = re.sub(r'\s+', ' ', css_content)

    # Eliminar espacios alrededor de { } : ; ,
    css_content = re.sub(r'\s*{\s*', '{', css_content)
    css_content = re.sub(r'\s*}\s*', '}', css_content)
    css_content = re.sub(r'\s*:\s*', ':', css_content)
    css_content = re.sub(r'\s*;\s*', ';', css_content)
    css_content = re.sub(r'\s*,\s*', ',', css_content)

    # Eliminar último punto y coma antes de }
    css_content = re.sub(r';}', '}', css_content)

    return css_content.strip()

def extract_login_css_from_auth_system():
    """
    Extraer CSS inline de render_login_page() en auth_system.py
    """
    base_dir = Path(__file__).parent.parent
    auth_file = base_dir / "modules" / "core" / "auth_system.py"

    log("Leyendo auth_system.py...", Colors.BLUE)

    with open(auth_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Encontrar el CSS inline en render_login_page()
    # El CSS está entre las líneas ~403 y ~1680

    # Patrón para encontrar el bloque de CSS reset
    reset_css_pattern = r'reset_css_content = """<style id="login-reset-TIMESTAMP">(.*?)</style>"""'
    reset_match = re.search(reset_css_pattern, content, re.DOTALL)

    reset_css = ""
    if reset_match:
        reset_css = reset_match.group(1)
        log(f"  ✓ CSS Reset extraído ({len(reset_css)} caracteres)", Colors.GREEN)

    # Patrón para encontrar el CSS principal del login
    # Buscar st.markdown con CSS después del reset
    main_css_pattern = r'st\.markdown\("""[\s\n]*<style>(.*?)</style>[\s\n]*""", unsafe_allow_html=True\)'
    main_css_matches = re.findall(main_css_pattern, content, re.DOTALL)

    main_css = ""
    if main_css_matches:
        # Combinar todos los bloques CSS encontrados
        main_css = "\n".join(main_css_matches)
        log(f"  ✓ CSS Principal extraído ({len(main_css)} caracteres)", Colors.GREEN)

    # Combinar todo el CSS
    combined_css = f"""/* ========================================
   LOGIN PAGE CSS - Extraído de auth_system.py
   Fecha: Optimización Fase 1
   ======================================== */

/* RESET CSS PARA LOGIN */
{reset_css}

/* ESTILOS PRINCIPALES DEL LOGIN */
{main_css}
"""

    # Guardar CSS en archivo externo
    login_css_file = base_dir / "assets" / "login.css"
    with open(login_css_file, 'w', encoding='utf-8') as f:
        f.write(combined_css)

    log(f"  ✓ CSS guardado en: assets/login.css ({len(combined_css)} caracteres)", Colors.GREEN)

    # Crear versión minificada
    minified_css = minify_css_simple(combined_css)
    login_css_min_file = base_dir / "assets" / "login.min.css"
    with open(login_css_min_file, 'w', encoding='utf-8') as f:
        f.write(minified_css)

    reduction = (1 - len(minified_css) / len(combined_css)) * 100
    log(f"  ✓ CSS minificado guardado: assets/login.min.css ({len(minified_css)} caracteres, -{reduction:.1f}%)", Colors.GREEN)

    return combined_css, minified_css

def update_auth_system_to_use_external_css():
    """
    Actualizar auth_system.py para cargar CSS externo en lugar de inline
    """
    base_dir = Path(__file__).parent.parent
    auth_file = base_dir / "modules" / "core" / "auth_system.py"

    log("Actualizando auth_system.py para usar CSS externo...", Colors.BLUE)

    with open(auth_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Encontrar la función render_login_page
    # Reemplazar el bloque de CSS inline por carga de archivo externo

    # Nueva implementación de carga CSS
    new_css_loading = '''    # ===== CARGAR CSS EXTERNO (Optimización Fase 1) =====
    # En lugar de CSS inline, cargar desde archivo externo (cacheable)
    import os
    css_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'assets', 'login.min.css')

    if os.path.exists(css_file):
        with open(css_file, 'r', encoding='utf-8') as f:
            login_css = f.read()
        st.markdown(f'<style>{login_css}</style>', unsafe_allow_html=True)
    else:
        # Fallback: usar CSS básico si el archivo no existe
        st.markdown("""
        <style>
        .login-container { max-width: 400px; margin: 2rem auto; padding: 2rem; }
        .stTextInput input { background: white !important; color: #1a202c !important; }
        </style>
        """, unsafe_allow_html=True)
'''

    # Encontrar y reemplazar el bloque de CSS reset y principal
    # Buscar desde "timestamp = datetime.now()" hasta el final de los bloques CSS

    # Patrón para encontrar todo el bloque CSS (desde timestamp hasta el JS)
    pattern = r'(    timestamp = datetime\.now\(\)\.strftime.*?)(    # JAVASCRIPT SIMPLE PARA FORZAR TEMAS)'

    replacement = new_css_loading + '\n\n    # JAVASCRIPT SIMPLE PARA FORZAR TEMAS'

    content_updated = re.sub(pattern, replacement, content, flags=re.DOTALL)

    if content_updated != content:
        # Guardar archivo actualizado
        with open(auth_file, 'w', encoding='utf-8') as f:
            f.write(content_updated)

        log("  ✓ auth_system.py actualizado correctamente", Colors.GREEN)
        return True
    else:
        log("  ⚠ No se pudo actualizar auth_system.py automáticamente", Colors.YELLOW)
        log("    Se requiere actualización manual", Colors.YELLOW)
        return False

def minify_existing_css_files():
    """
    Minificar archivos CSS existentes
    """
    base_dir = Path(__file__).parent.parent
    assets_dir = base_dir / "assets"

    css_files_to_minify = [
        "style.css",
        "extra_styles.css",
        "extra_styles_cloud.css",
        "theme_light.css",
        "theme_dark.css",
        "theme_light_cloud.css",
        "theme_dark_cloud.css",
    ]

    log("Minificando archivos CSS existentes...", Colors.BLUE)

    for css_file in css_files_to_minify:
        source_file = assets_dir / css_file
        if not source_file.exists():
            log(f"  ⚠ No encontrado: {css_file}", Colors.YELLOW)
            continue

        # Leer CSS original
        with open(source_file, 'r', encoding='utf-8') as f:
            original_css = f.read()

        # Minificar
        minified_css = minify_css_simple(original_css)

        # Guardar versión minificada
        min_file = assets_dir / css_file.replace('.css', '.min.css')
        with open(min_file, 'w', encoding='utf-8') as f:
            f.write(minified_css)

        reduction = (1 - len(minified_css) / len(original_css)) * 100
        log(f"  ✓ {css_file} -> {min_file.name} (-{reduction:.1f}%)", Colors.GREEN)

def update_app_to_use_minified_css():
    """
    Actualizar app.py para cargar versiones minificadas de CSS
    """
    base_dir = Path(__file__).parent.parent
    app_file = base_dir / "src" / "app.py"

    log("Actualizando app.py para usar CSS minificado...", Colors.BLUE)

    with open(app_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Reemplazar referencias a archivos CSS por versiones .min.css
    replacements = [
        ('assets/style.css', 'assets/style.min.css'),
        ('assets/extra_styles.css', 'assets/extra_styles.min.css'),
        ('assets/extra_styles_cloud.css', 'assets/extra_styles_cloud.min.css'),
        ('theme_{st.session_state.theme_mode}_cloud.css', 'theme_{st.session_state.theme_mode}_cloud.min.css'),
        ('theme_{st.session_state.theme_mode}.css', 'theme_{st.session_state.theme_mode}.min.css'),
    ]

    content_updated = content
    for old_ref, new_ref in replacements:
        content_updated = content_updated.replace(old_ref, new_ref)

    if content_updated != content:
        with open(app_file, 'w', encoding='utf-8') as f:
            f.write(content_updated)

        log("  ✓ app.py actualizado correctamente", Colors.GREEN)
        return True
    else:
        log("  ℹ app.py ya está actualizado o no requiere cambios", Colors.BLUE)
        return False

def run_phase1():
    """Ejecutar Fase 1 completa"""
    log("="*60, Colors.BLUE)
    log("FASE 1: OPTIMIZACIÓN DE CSS", Colors.BLUE)
    log("="*60, Colors.BLUE)

    try:
        # Paso 1: Extraer CSS inline
        log("\n[1/4] Extrayendo CSS inline de auth_system.py...", Colors.BLUE)
        extract_login_css_from_auth_system()

        # Paso 2: Actualizar auth_system.py
        log("\n[2/4] Actualizando auth_system.py...", Colors.BLUE)
        update_auth_system_to_use_external_css()

        # Paso 3: Minificar CSS existentes
        log("\n[3/4] Minificando archivos CSS existentes...", Colors.BLUE)
        minify_existing_css_files()

        # Paso 4: Actualizar app.py
        log("\n[4/4] Actualizando app.py para usar CSS minificado...", Colors.BLUE)
        update_app_to_use_minified_css()

        log("\n" + "="*60, Colors.BLUE)
        log("✅ FASE 1 COMPLETADA", Colors.GREEN)
        log("="*60, Colors.BLUE)
        log("\nGanancia esperada: 4-6 segundos en carga inicial", Colors.GREEN)
        log("\nPróximos pasos:", Colors.YELLOW)
        log("1. Probar en local: streamlit run src/app.py", Colors.YELLOW)
        log("2. Verificar que el login funciona correctamente", Colors.YELLOW)
        log("3. Si todo funciona, ejecutar Fase 2", Colors.YELLOW)
        log("\nPara revertir cambios:", Colors.RED)
        log("  python optimization_scripts/restore_snapshot.py", Colors.RED)

    except Exception as e:
        log(f"\n❌ ERROR en Fase 1: {e}", Colors.RED)
        log("Para revertir cambios:", Colors.YELLOW)
        log("  python optimization_scripts/restore_snapshot.py", Colors.YELLOW)
        raise

if __name__ == "__main__":
    run_phase1()
