#!/usr/bin/env python3
"""
Script para eliminar CSS duplicados de archivos
FASE 3 - OPCIÓN A: Limpieza Agresiva

Este script elimina selectores CSS duplicados que ya están en common.css
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
    CYAN = '\033[96m'
    END = '\033[0m'

def log(message, color=Colors.GREEN):
    """Log con color"""
    print(f"{color}[CSS CLEANUP]{Colors.END} {message}")

# Definir selectores a eliminar por archivo
DUPLICATES_TO_REMOVE = {
    'adaptive_theme.css': [
        # Categoría 1: Clases Utilitarias (eliminar TODAS)
        '.d-flex',
        '.align-center',
        '.justify-between',
        '.gap-05',
        '.gap-1',
        '.mb-1',
        '.mb-2',
        '.mt-1',
        '.mt-2',
        '.p-1',
        '.p-2',
        '.rounded',
        '.shadow',
        '.text-left',
        '.text-right',
        # Categoría 2: Componentes de Chat
        '.chat-title',
        '.chat-messages::-webkit-scrollbar-thumb',
        '.chat-messages::-webkit-scrollbar-thumb:hover',
        '.chat-messages::-webkit-scrollbar-track',
        # Categoría 3: Componentes Comunes
        '.chart-container',
        '.chart-container:hover',
        '.chart-title',
        '.metric-card',
        '.metric-value',
        '.metric-label',
        '.info-box',
        '.warning-box',
        # Categoría 4: Header y Sidebar
        '.main-header h1',
        '.main-header h3',
        '.main-header p',
        '.main-header::after',
        '.sidebar-content h3',
        # Streamlit Components
        '.stSidebar',
        '.stDataFrame tbody tr:nth-child(even)',
        '.stDataFrame td',
        '.stSelectbox > div > div:hover',
        '.stTextInput > div > div:hover',
        '.stSelectbox > div > div:focus-within',
        '.stTextInput > div > div:focus-within',
        '.stTabs [data-baseweb="tab"]',
        '.stTabs [data-baseweb="tab"]:hover',
        '.stTabs [data-baseweb="tab"][aria-selected="true"]',
        '.stButton > button',
        '.stButton > button:hover',
        '.stDataFrame tbody tr:hover',
        '.stChatMessage .stMarkdown p',
        '.stChatMessage .stMarkdown div',
        '.stChatMessage .stMarkdown span',
        'div[data-testid="column"]',
        '.fade-in'
    ],

    'theme_light.css': [
        # Categoría 2: Componentes de Chat
        '.chat-title',
        '.chat-messages::-webkit-scrollbar-thumb',
        '.chat-messages::-webkit-scrollbar-thumb:hover',
        '.chat-messages::-webkit-scrollbar-track',
        # Categoría 3: Componentes Comunes
        '.chart-container',
        '.chart-title',
        '.metric-card',
        '.metric-value',
        '.metric-label',
        '.info-box',
        '.warning-box',
        # Categoría 4: Header y Sidebar
        '.main-header h1',
        '.main-header h3',
        '.main-header p',
        '.main-header::after',
        '.sidebar-content h3',
        # Streamlit Components
        '.stSidebar',
        '.stDataFrame tbody tr:nth-child(even)',
        '.stDataFrame td',
        '.stSelectbox > div > div:hover',
        '.stTextInput > div > div:hover',
        '.stSelectbox > div > div:focus-within',
        '.stTextInput > div > div:focus-within',
        '.stTabs [data-baseweb="tab"]',
        '.stTabs [data-baseweb="tab"]:hover',
        '.stTabs [data-baseweb="tab"][aria-selected="true"]',
        '.stButton > button',
        '.stButton > button:hover',
        '.stDataFrame tbody tr:hover',
        '.stChatMessage .stMarkdown p',
        '.stChatMessage .stMarkdown div',
        '.stChatMessage .stMarkdown span',
        'div[data-testid="column"]'
    ],

    'theme_dark.css': [
        # Categoría 2: Componentes de Chat
        '.chat-title',
        '.chat-messages::-webkit-scrollbar-thumb',
        '.chat-messages::-webkit-scrollbar-thumb:hover',
        '.chat-messages::-webkit-scrollbar-track',
        # Categoría 3: Componentes Comunes
        '.chart-container',
        '.chart-title',
        '.metric-card',
        '.metric-value',
        '.metric-label',
        # Categoría 4: Header y Sidebar
        '.main-header h1',
        '.main-header h3',
        '.main-header p',
        '.main-header::after',
        '.sidebar-content h3',
        # Streamlit Components
        '.stSidebar',
        '.stDataFrame tbody tr:nth-child(even)',
        '.stDataFrame td',
        '.stSelectbox > div > div:hover',
        '.stTextInput > div > div:hover',
        '.stTabs [data-baseweb="tab"]',
        '.stButton > button',
        '.stChatMessage .stMarkdown p',
        '.stChatMessage .stMarkdown div',
        '.stChatMessage .stMarkdown span',
        'div[data-testid="column"]'
    ],

    'style.css': [
        # Solo eliminar duplicados con adaptive_theme
        '.chat-messages::-webkit-scrollbar-thumb',
        '.chat-messages::-webkit-scrollbar-thumb:hover',
        '.main-header::after',
        '.sidebar-content h3'
    ]
}

def remove_css_rule(css_content, selector):
    """
    Eliminar una regla CSS específica del contenido
    """
    # Escapar caracteres especiales del selector para regex
    escaped_selector = re.escape(selector)

    # Patrón para encontrar: selector { ... }
    # Incluye manejo de selectores multi-línea
    pattern = rf'{escaped_selector}\s*\{{[^}}]*\}}'

    # Eliminar la regla
    css_content = re.sub(pattern, '', css_content, flags=re.MULTILINE | re.DOTALL)

    return css_content

def clean_empty_lines(css_content):
    """Limpiar líneas vacías múltiples"""
    # Reducir múltiples líneas vacías a máximo 2
    css_content = re.sub(r'\n\s*\n\s*\n+', '\n\n', css_content)
    return css_content

def process_file(file_path, selectors_to_remove):
    """Procesar un archivo CSS eliminando selectores duplicados"""
    log(f"Procesando: {file_path.name}", Colors.CYAN)

    try:
        # Leer archivo original
        with open(file_path, 'r', encoding='utf-8') as f:
            original_content = f.read()

        original_size = len(original_content)
        modified_content = original_content
        removed_count = 0

        # Eliminar cada selector
        for selector in selectors_to_remove:
            before_size = len(modified_content)
            modified_content = remove_css_rule(modified_content, selector)
            after_size = len(modified_content)

            if before_size != after_size:
                removed_count += 1
                log(f"  ✓ Eliminado: {selector}", Colors.GREEN)

        # Limpiar líneas vacías
        modified_content = clean_empty_lines(modified_content)

        final_size = len(modified_content)
        bytes_saved = original_size - final_size
        percentage = (bytes_saved / original_size * 100) if original_size > 0 else 0

        # Guardar archivo modificado
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(modified_content)

        log(f"  📊 Selectores eliminados: {removed_count}", Colors.YELLOW)
        log(f"  💾 Bytes ahorrados: {bytes_saved} ({percentage:.1f}%)", Colors.YELLOW)
        log(f"  ✅ Archivo actualizado: {file_path.name}", Colors.GREEN)

        return {
            'file': file_path.name,
            'removed_count': removed_count,
            'bytes_saved': bytes_saved,
            'original_size': original_size,
            'final_size': final_size
        }

    except Exception as e:
        log(f"  ❌ Error procesando {file_path.name}: {e}", Colors.RED)
        return None

def main():
    """Función principal"""
    base_dir = Path(__file__).parent.parent
    assets_dir = base_dir / "assets"

    log("=" * 70, Colors.BLUE)
    log("ELIMINACIÓN DE CSS DUPLICADOS - FASE 3 OPCIÓN A", Colors.BLUE)
    log("=" * 70, Colors.BLUE)
    log("")

    log("⚠️  IMPORTANTE: Los archivos originales están respaldados en:", Colors.YELLOW)
    log("   optimization_backups/css_cleanup_backup_20251026_082702/", Colors.YELLOW)
    log("")

    results = []

    for filename, selectors in DUPLICATES_TO_REMOVE.items():
        file_path = assets_dir / filename

        if not file_path.exists():
            log(f"⚠️  Archivo no encontrado: {filename}", Colors.YELLOW)
            continue

        log(f"\n{'='*70}", Colors.BLUE)
        result = process_file(file_path, selectors)
        if result:
            results.append(result)

    # Resumen final
    log("\n" + "=" * 70, Colors.BLUE)
    log("RESUMEN DE LIMPIEZA", Colors.BLUE)
    log("=" * 70, Colors.BLUE)

    total_removed = sum(r['removed_count'] for r in results)
    total_bytes_saved = sum(r['bytes_saved'] for r in results)
    total_original = sum(r['original_size'] for r in results)

    log(f"\nArchivos procesados: {len(results)}", Colors.CYAN)
    log(f"Selectores eliminados: {total_removed}", Colors.CYAN)
    log(f"Bytes ahorrados: {total_bytes_saved} bytes ({total_bytes_saved/1024:.2f} KB)", Colors.GREEN)
    log(f"Reducción total: {(total_bytes_saved/total_original*100):.1f}%", Colors.GREEN)

    log("\n📋 Desglose por archivo:", Colors.BLUE)
    for r in results:
        percentage = (r['bytes_saved'] / r['original_size'] * 100) if r['original_size'] > 0 else 0
        log(f"  {r['file']:25} - {r['removed_count']:2} selectores | -{r['bytes_saved']:5} bytes ({percentage:4.1f}%)", Colors.CYAN)

    log("\n✅ LIMPIEZA COMPLETADA", Colors.GREEN)
    log("\nPróximos pasos:", Colors.YELLOW)
    log("1. Verificar sintaxis: python -m py_compile src/app.py", Colors.YELLOW)
    log("2. Probar aplicación: streamlit run src/app.py", Colors.YELLOW)
    log("3. Si falla algo: python optimization_scripts/restore_css_cleanup.py", Colors.YELLOW)
    log("")

if __name__ == "__main__":
    main()
