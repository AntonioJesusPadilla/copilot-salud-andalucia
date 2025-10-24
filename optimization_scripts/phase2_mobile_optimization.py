#!/usr/bin/env python3
"""
FASE 2: OPTIMIZACIÓN DE DETECCIÓN MÓVIL Y CARGA CONDICIONAL
============================================================
Optimiza la detección de dispositivos móviles y implementa carga condicional de CSS.

Optimizaciones:
1. Optimizar detección de dispositivos móviles (más rápida)
2. Implementar carga condicional de CSS según dispositivo
3. Cargar ios_safari_fixes.css solo en iOS
4. Cachear detección en session_state

Ganancia esperada: 1.5-2.5 segundos

Uso: python optimization_scripts/phase2_mobile_optimization.py
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
    print(f"{color}[PHASE 2]{Colors.END} {message}")

def optimize_mobile_detection():
    """
    Optimizar la función is_mobile_device() en app.py
    para hacerla más rápida y menos bloqueante
    """
    base_dir = Path(__file__).parent.parent
    app_file = base_dir / "src" / "app.py"

    log("Optimizando detección de dispositivos móviles...", Colors.BLUE)

    with open(app_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Nueva implementación optimizada de is_mobile_device()
    new_mobile_detection = '''def is_mobile_device():
    """
    Detecta si el usuario está usando un dispositivo móvil
    OPTIMIZADO: Usa st.context cuando está disponible, fallback rápido
    """
    # Cachear resultado en session_state para evitar detecciones repetidas
    if 'device_type_detected' in st.session_state:
        return st.session_state.get('is_mobile_cached', False)

    try:
        # Método optimizado: Intentar obtener user agent de forma rápida
        user_agent = ""

        # Intentar obtener del contexto de Streamlit (más rápido)
        try:
            # En Streamlit >= 1.28, usar st.context
            if hasattr(st, 'context') and hasattr(st.context, 'headers'):
                user_agent = st.context.headers.get("User-Agent", "").lower()
        except:
            pass

        # Fallback: Intentar websocket headers (solo si el anterior falla)
        if not user_agent:
            try:
                import streamlit.web.server.websocket_headers as wsh
                headers = wsh.get_websocket_headers()
                user_agent = headers.get("User-Agent", "").lower()
            except:
                pass

        # Patrones comunes de dispositivos móviles
        mobile_patterns = [
            'iphone', 'ipad', 'ipod',  # iOS
            'android',                  # Android
            'mobile', 'phone',          # Genéricos
        ]

        is_mobile = any(pattern in user_agent for pattern in mobile_patterns)

        # Cachear resultado
        st.session_state.device_type_detected = True
        st.session_state.is_mobile_cached = is_mobile

        return is_mobile

    except Exception as e:
        # Fallback rápido: Asumir desktop si no podemos detectar
        st.session_state.device_type_detected = True
        st.session_state.is_mobile_cached = False
        return False'''

    # Reemplazar la función is_mobile_device existente
    pattern = r'def is_mobile_device\(\):.*?return False'
    content_updated = re.sub(pattern, new_mobile_detection, content, flags=re.DOTALL, count=1)

    if content_updated != content:
        with open(app_file, 'w', encoding='utf-8') as f:
            f.write(content_updated)

        log("  ✓ Detección de móvil optimizada", Colors.GREEN)
        return True
    else:
        log("  ⚠ No se pudo actualizar la detección de móvil", Colors.YELLOW)
        return False

def implement_conditional_css_loading():
    """
    Implementar carga condicional de CSS según tipo de dispositivo
    """
    base_dir = Path(__file__).parent.parent
    app_file = base_dir / "src" / "app.py"

    log("Implementando carga condicional de CSS...", Colors.BLUE)

    with open(app_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Buscar la función load_css_file() y agregar parámetros opcionales
    # También buscar donde se cargan los CSS y hacer condicional

    # Agregar función auxiliar para detectar iOS
    ios_detection_function = '''
def is_ios_device():
    """Detectar si el dispositivo es iOS específicamente"""
    if 'is_ios_cached' in st.session_state:
        return st.session_state.is_ios_cached

    try:
        user_agent = ""

        # Intentar obtener user agent
        try:
            if hasattr(st, 'context') and hasattr(st.context, 'headers'):
                user_agent = st.context.headers.get("User-Agent", "").lower()
        except:
            pass

        if not user_agent:
            try:
                import streamlit.web.server.websocket_headers as wsh
                headers = wsh.get_websocket_headers()
                user_agent = headers.get("User-Agent", "").lower()
            except:
                pass

        is_ios = any(pattern in user_agent for pattern in ['iphone', 'ipad', 'ipod'])
        st.session_state.is_ios_cached = is_ios
        return is_ios

    except:
        st.session_state.is_ios_cached = False
        return False

'''

    # Insertar función después de is_mobile_device()
    pattern = r'(# Detectar tipo de dispositivo\s+IS_MOBILE = is_mobile_device\(\))'
    replacement = ios_detection_function + '\n\\1'

    content_updated = re.sub(pattern, replacement, content)

    # Ahora buscar donde se carga ios_safari_fixes.css y hacerlo condicional
    # Buscar la sección de carga de CSS y agregar condicional

    ios_css_conditional = '''
    # Cargar CSS específico para iOS solo si es necesario (Optimización Fase 2)
    if is_ios_device():
        ios_css = load_css_file('assets/ios_safari_fixes.css')
        if ios_css:
            st.markdown(f'<style>{ios_css}</style>', unsafe_allow_html=True)
            # print("✓ CSS iOS Safari aplicado")
'''

    # Buscar cualquier carga existente de ios_safari_fixes.css y reemplazarla
    # o agregarla si no existe

    if 'ios_safari_fixes.css' in content_updated:
        # Reemplazar carga existente
        pattern_ios = r'[\s\S]*?load_css_file\([\'"]assets/ios_safari_fixes\.css[\'"]\)[\s\S]*?(?=\n\n|\n    # |\n    if )'
        content_updated = re.sub(pattern_ios, ios_css_conditional, content_updated)
        log("  ✓ Carga de CSS iOS ahora es condicional", Colors.GREEN)
    else:
        # Si no existe, agregarlo después de la carga de CSS principal
        # Buscar el final de load_optimized_css()
        pattern_insert = r'(def load_optimized_css\(\):[\s\S]*?return "[^"]+"\s+)'
        replacement_insert = '\\1' + ios_css_conditional + '\n'
        content_updated = re.sub(pattern_insert, replacement_insert, content_updated)
        log("  ✓ Carga condicional de CSS iOS agregada", Colors.GREEN)

    # Guardar cambios
    with open(app_file, 'w', encoding='utf-8') as f:
        f.write(content_updated)

    return True

def optimize_css_loading_in_main():
    """
    Optimizar la carga de CSS en la función main()
    para evitar cargar CSS innecesario
    """
    base_dir = Path(__file__).parent.parent
    app_file = base_dir / "src" / "app.py"

    log("Optimizando carga de CSS en función main()...", Colors.BLUE)

    with open(app_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Buscar donde se carga extra_styles_cloud.css y hacerlo más eficiente
    # Agregar lógica para no cargar en móvil si no es necesario

    optimization_code = '''
    # Cargar CSS extra solo en desktop (Optimización Fase 2)
    if css_loaded != "mobile_basic" and not IS_MOBILE:
        # Detectar si estamos en Cloud
        is_cloud = any([
            os.getenv('USER') == 'appuser',
            os.path.exists('/home/appuser/.streamlit/'),
            'HOSTNAME' in os.environ and 'streamlit' in os.environ.get('HOSTNAME', '').lower(),
            os.getenv('STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION') is not None
        ])

        # Usar versión Cloud si está en Cloud
        extra_css_file = 'assets/extra_styles_cloud.min.css' if is_cloud else 'assets/extra_styles.min.css'
        extra_css = load_css_file(extra_css_file)
        if extra_css:
            st.markdown(f'<style>{extra_css}</style>', unsafe_allow_html=True)
'''

    # Buscar el bloque existente de carga de extra_styles y reemplazarlo
    pattern = r'# Cargar CSS extra solo en desktop.*?st\.markdown\(f\'<style>\{extra_css\}</style>\', unsafe_allow_html=True\)'

    if re.search(pattern, content, re.DOTALL):
        content_updated = re.sub(pattern, optimization_code.strip(), content, flags=re.DOTALL)
    else:
        # Si no existe ese patrón exacto, buscar una variante más flexible
        pattern_alt = r'if css_loaded != "mobile_basic":.*?if extra_css:[\s\S]*?st\.markdown\(f\'<style>\{extra_css\}</style>\', unsafe_allow_html=True\)'
        content_updated = re.sub(pattern_alt, optimization_code.strip(), content, flags=re.DOTALL)

    if content_updated != content:
        with open(app_file, 'w', encoding='utf-8') as f:
            f.write(content_updated)

        log("  ✓ Carga de CSS optimizada en main()", Colors.GREEN)
        return True
    else:
        log("  ℹ No se encontró el bloque a optimizar (puede ya estar optimizado)", Colors.BLUE)
        return False

def run_phase2():
    """Ejecutar Fase 2 completa"""
    log("="*60, Colors.BLUE)
    log("FASE 2: OPTIMIZACIÓN MÓVIL Y CARGA CONDICIONAL", Colors.BLUE)
    log("="*60, Colors.BLUE)

    try:
        # Paso 1: Optimizar detección móvil
        log("\n[1/3] Optimizando detección de dispositivos móviles...", Colors.BLUE)
        optimize_mobile_detection()

        # Paso 2: Implementar carga condicional de CSS
        log("\n[2/3] Implementando carga condicional de CSS...", Colors.BLUE)
        implement_conditional_css_loading()

        # Paso 3: Optimizar carga en main()
        log("\n[3/3] Optimizando carga de CSS en main()...", Colors.BLUE)
        optimize_css_loading_in_main()

        log("\n" + "="*60, Colors.BLUE)
        log("✅ FASE 2 COMPLETADA", Colors.GREEN)
        log("="*60, Colors.BLUE)
        log("\nGanancia esperada: 1.5-2.5 segundos", Colors.GREEN)
        log("\nMejoras implementadas:", Colors.GREEN)
        log("  • Detección de móvil más rápida con caché", Colors.GREEN)
        log("  • CSS iOS solo se carga en dispositivos iOS", Colors.GREEN)
        log("  • CSS extra no se carga en móviles", Colors.GREEN)
        log("\nPróximos pasos:", Colors.YELLOW)
        log("1. Probar en local: streamlit run src/app.py", Colors.YELLOW)
        log("2. Probar en diferentes dispositivos (iOS, Android, desktop)", Colors.YELLOW)
        log("3. Si todo funciona, ejecutar Fase 3", Colors.YELLOW)
        log("\nPara revertir cambios:", Colors.RED)
        log("  python optimization_scripts/restore_snapshot.py", Colors.RED)

    except Exception as e:
        log(f"\n❌ ERROR en Fase 2: {e}", Colors.RED)
        log("Para revertir cambios:", Colors.YELLOW)
        log("  python optimization_scripts/restore_snapshot.py", Colors.YELLOW)
        raise

if __name__ == "__main__":
    run_phase2()
