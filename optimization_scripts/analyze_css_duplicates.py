#!/usr/bin/env python3
"""
Script para analizar CSS duplicados
Genera reporte de selectores CSS que aparecen en múltiples archivos
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
    CYAN = '\033[96m'
    END = '\033[0m'

def log(message, color=Colors.GREEN):
    """Log con color"""
    print(f"{color}[CSS ANALYZER]{Colors.END} {message}")

def analyze_css_files():
    """Analizar archivos CSS para encontrar duplicados"""
    base_dir = Path(__file__).parent.parent
    assets_dir = base_dir / "assets"

    log("🔍 Analizando archivos CSS...", Colors.BLUE)

    # Archivos CSS a analizar (excluimos .min.css ya que son versiones minificadas)
    css_files = [
        "style.css",
        "extra_styles.css",
        "extra_styles_cloud.css",
        "theme_light.css",
        "theme_dark.css",
        "theme_light_cloud.css",
        "theme_dark_cloud.css",
        "adaptive_theme.css",
        "desktop_layout.css",
        "ios_safari_fixes.css",
        "login.css"
    ]

    # Diccionario para almacenar selectores y sus propiedades
    selectors = defaultdict(list)
    file_stats = {}

    log(f"Archivos a analizar: {len(css_files)}", Colors.CYAN)

    for css_file in css_files:
        file_path = assets_dir / css_file
        if not file_path.exists():
            log(f"  ⚠ {css_file} no encontrado", Colors.YELLOW)
            continue

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            file_size = len(content)
            file_stats[css_file] = {
                'size': file_size,
                'selectors': 0
            }

            # Extraer selectores CSS de forma simple
            # Patrón: selector { propiedades }
            pattern = r'([^{]+)\{([^}]+)\}'
            matches = re.findall(pattern, content, re.MULTILINE)

            for selector, properties in matches:
                selector = selector.strip()
                properties = properties.strip()

                # Ignorar comentarios y selectores vacíos
                if not selector or selector.startswith('/*') or not properties:
                    continue

                # Normalizar selector (quitar espacios múltiples)
                selector = ' '.join(selector.split())

                # Normalizar propiedades (quitar espacios y saltos de línea)
                properties_normalized = ' '.join(properties.split())

                if selector and properties_normalized:
                    selectors[selector].append({
                        'file': css_file,
                        'properties': properties_normalized,
                        'properties_raw': properties
                    })
                    file_stats[css_file]['selectors'] += 1

            log(f"  ✓ {css_file}: {file_stats[css_file]['selectors']} selectores ({file_size} bytes)", Colors.GREEN)

        except Exception as e:
            log(f"  ❌ Error leyendo {css_file}: {e}", Colors.RED)

    return selectors, file_stats

def generate_report(selectors, file_stats):
    """Generar reporte de duplicados"""
    base_dir = Path(__file__).parent.parent

    log("\n📊 Generando reporte...", Colors.BLUE)

    # Encontrar duplicados
    duplicates = {sel: files for sel, files in selectors.items() if len(files) > 1}

    # Encontrar duplicados exactos (mismo selector, mismas propiedades)
    exact_duplicates = {}
    partial_duplicates = {}

    for selector, occurrences in duplicates.items():
        # Agrupar por propiedades
        props_groups = defaultdict(list)
        for occ in occurrences:
            props_groups[occ['properties']].append(occ['file'])

        # Si hay grupos con más de un archivo, es duplicado exacto
        for props, files in props_groups.items():
            if len(files) > 1:
                if selector not in exact_duplicates:
                    exact_duplicates[selector] = []
                exact_duplicates[selector].append({
                    'files': files,
                    'properties': props
                })

        # Si hay diferentes propiedades, es duplicado parcial
        if len(props_groups) > 1:
            partial_duplicates[selector] = occurrences

    # Crear reporte
    report_file = base_dir / "optimization_scripts" / "css_duplicates_report.txt"

    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("REPORTE DE ANÁLISIS DE CSS DUPLICADOS\n")
        f.write("=" * 80 + "\n")
        f.write(f"Generado: {Path(__file__).name}\n")
        f.write("\n")

        # Resumen de archivos
        f.write("ARCHIVOS ANALIZADOS:\n")
        f.write("-" * 80 + "\n")
        total_size = 0
        total_selectors = 0
        for file, stats in sorted(file_stats.items()):
            f.write(f"  {file:40} {stats['selectors']:5} selectores | {stats['size']:8} bytes\n")
            total_size += stats['size']
            total_selectors += stats['selectors']
        f.write("-" * 80 + "\n")
        f.write(f"  {'TOTAL':40} {total_selectors:5} selectores | {total_size:8} bytes\n")
        f.write("\n\n")

        # Duplicados exactos
        f.write("=" * 80 + "\n")
        f.write(f"DUPLICADOS EXACTOS: {len(exact_duplicates)}\n")
        f.write("=" * 80 + "\n")
        f.write("(Mismo selector con las mismas propiedades en múltiples archivos)\n")
        f.write("Estos pueden ser eliminados moviendo el código a un archivo común.\n")
        f.write("\n")

        if exact_duplicates:
            for i, (selector, groups) in enumerate(sorted(exact_duplicates.items()), 1):
                f.write(f"\n[{i}] SELECTOR: {selector}\n")
                f.write("-" * 80 + "\n")
                for group in groups:
                    f.write(f"  Aparece en {len(group['files'])} archivos:\n")
                    for file in group['files']:
                        f.write(f"    • {file}\n")
                    f.write(f"\n  Propiedades:\n")
                    # Mostrar propiedades de forma legible
                    props = group['properties'].split(';')
                    for prop in props[:5]:  # Mostrar solo las primeras 5
                        if prop.strip():
                            f.write(f"    {prop.strip()}\n")
                    if len(props) > 5:
                        f.write(f"    ... y {len(props) - 5} propiedades más\n")
                    f.write("\n")
        else:
            f.write("  ✓ No se encontraron duplicados exactos\n")

        # Duplicados parciales
        f.write("\n\n")
        f.write("=" * 80 + "\n")
        f.write(f"DUPLICADOS PARCIALES: {len(partial_duplicates)}\n")
        f.write("=" * 80 + "\n")
        f.write("(Mismo selector pero con propiedades diferentes en distintos archivos)\n")
        f.write("Estos pueden ser consolidados o necesitar refactorización.\n")
        f.write("\n")

        if partial_duplicates:
            # Mostrar solo los primeros 20
            for i, (selector, occurrences) in enumerate(sorted(partial_duplicates.items())[:20], 1):
                f.write(f"\n[{i}] SELECTOR: {selector}\n")
                f.write("-" * 80 + "\n")
                f.write(f"  Aparece en {len(occurrences)} archivos con diferentes estilos:\n")
                for occ in occurrences:
                    f.write(f"    • {occ['file']}\n")
                f.write("\n")

            if len(partial_duplicates) > 20:
                f.write(f"\n... y {len(partial_duplicates) - 20} selectores parcialmente duplicados más\n")
        else:
            f.write("  ✓ No se encontraron duplicados parciales significativos\n")

        # Resumen final
        f.write("\n\n")
        f.write("=" * 80 + "\n")
        f.write("RESUMEN DE OPTIMIZACIÓN\n")
        f.write("=" * 80 + "\n")
        f.write(f"Total de selectores únicos:        {len(selectors)}\n")
        f.write(f"Selectores con duplicación:        {len(duplicates)}\n")
        f.write(f"Duplicados exactos (eliminar):     {len(exact_duplicates)}\n")
        f.write(f"Duplicados parciales (revisar):    {len(partial_duplicates)}\n")
        f.write("\n")
        f.write("RECOMENDACIONES:\n")
        f.write("-" * 80 + "\n")
        if exact_duplicates:
            f.write(f"1. Eliminar {len(exact_duplicates)} duplicados exactos moviendo código a archivo común\n")
            f.write(f"   Ahorro estimado: ~{len(exact_duplicates) * 150} bytes\n")
        if partial_duplicates:
            f.write(f"2. Revisar {len(partial_duplicates)} duplicados parciales para refactorización\n")
        if not exact_duplicates and not partial_duplicates:
            f.write("✓ El código CSS está bien optimizado, sin duplicaciones significativas\n")
        f.write("\n")

    log(f"✅ Reporte generado: {report_file}", Colors.GREEN)

    # Mostrar resumen en consola
    log("\n📊 RESUMEN:", Colors.BLUE)
    log(f"  Total selectores únicos: {len(selectors)}", Colors.CYAN)
    log(f"  Duplicados exactos: {len(exact_duplicates)}", Colors.YELLOW if exact_duplicates else Colors.GREEN)
    log(f"  Duplicados parciales: {len(partial_duplicates)}", Colors.YELLOW if partial_duplicates else Colors.GREEN)

    if exact_duplicates or partial_duplicates:
        log(f"\n⚠ Se encontraron {len(duplicates)} selectores duplicados", Colors.YELLOW)
        log(f"  Revisar: {report_file}", Colors.YELLOW)
    else:
        log("\n✓ No se encontraron duplicaciones significativas", Colors.GREEN)

    return report_file

if __name__ == "__main__":
    log("=" * 60, Colors.BLUE)
    log("ANÁLISIS DE CSS DUPLICADOS - FASE 3", Colors.BLUE)
    log("=" * 60, Colors.BLUE)
    log("")

    try:
        # Analizar archivos
        selectors, file_stats = analyze_css_files()

        # Generar reporte
        report_file = generate_report(selectors, file_stats)

        log("\n" + "=" * 60, Colors.BLUE)
        log("✅ ANÁLISIS COMPLETADO", Colors.GREEN)
        log("=" * 60, Colors.BLUE)
        log(f"\nReporte guardado en:", Colors.GREEN)
        log(f"  {report_file}", Colors.CYAN)
        log("\nPróximos pasos:", Colors.YELLOW)
        log("1. Revisar el reporte de duplicados", Colors.YELLOW)
        log("2. Decidir qué duplicados eliminar (con supervisión)", Colors.YELLOW)
        log("3. Crear archivo CSS común para código compartido", Colors.YELLOW)

    except Exception as e:
        log(f"\n❌ ERROR: {e}", Colors.RED)
        raise
