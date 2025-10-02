#!/usr/bin/env python3
"""
Script para verificar el contraste de colores según WCAG AA/AAA
Copilot Salud Andalucía - Sistema de Temas
"""

def hex_to_rgb(hex_color):
    """Convertir color hexadecimal a RGB"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def relative_luminance(rgb):
    """Calcular luminancia relativa según WCAG"""
    r, g, b = [x / 255.0 for x in rgb]

    def adjust(color):
        if color <= 0.03928:
            return color / 12.92
        return ((color + 0.055) / 1.055) ** 2.4

    r = adjust(r)
    g = adjust(g)
    b = adjust(b)

    return 0.2126 * r + 0.7152 * g + 0.0722 * b

def contrast_ratio(color1, color2):
    """Calcular ratio de contraste entre dos colores"""
    lum1 = relative_luminance(hex_to_rgb(color1))
    lum2 = relative_luminance(hex_to_rgb(color2))

    lighter = max(lum1, lum2)
    darker = min(lum1, lum2)

    return (lighter + 0.05) / (darker + 0.05)

def check_wcag_compliance(ratio, text_size='normal'):
    """Verificar cumplimiento WCAG"""
    if text_size == 'large':  # 18pt+ o 14pt+ bold
        aa_threshold = 3.0
        aaa_threshold = 4.5
    else:  # texto normal
        aa_threshold = 4.5
        aaa_threshold = 7.0

    if ratio >= aaa_threshold:
        return 'AAA', '✅'
    elif ratio >= aa_threshold:
        return 'AA', '✅'
    else:
        return 'FAIL', '❌'

# ========== COLORES DEL SISTEMA ==========

# Modo Claro
light_theme = {
    'bg': '#ffffff',
    'text_primary': '#0f172a',
    'text_secondary': '#334155',
    'text_muted': '#64748b',
    'bg_surface': '#f8fafc',
    'bg_elevated': '#f1f5f9',
    'interactive_primary': '#0284c7',
}

# Modo Oscuro
dark_theme = {
    'bg': '#0f172a',
    'text_primary': '#f8fafc',
    'text_secondary': '#cbd5e1',
    'text_muted': '#94a3b8',
    'bg_surface': '#1e293b',
    'bg_elevated': '#334155',
    'interactive_primary': '#38bdf8',
}

# Paleta de gráficos - Modo Claro
chart_colors_light = {
    'chart-1': '#0369a1',  # Azul sanitario
    'chart-2': '#047857',  # Verde salud
    'chart-3': '#b91c1c',  # Rojo médico
    'chart-4': '#6d28d9',  # Púrpura datos
    'chart-5': '#c2410c',  # Naranja terracota
    'chart-6': '#0e7490',  # Cyan profesional
    'chart-7': '#be123c',  # Rosa sanitario
    'chart-8': '#475569',  # Gris corporativo
}

# Paleta de gráficos - Modo Oscuro
chart_colors_dark = {
    'chart-1': '#7dd3fc',  # Azul cielo brillante
    'chart-2': '#6ee7b7',  # Verde menta
    'chart-3': '#fca5a5',  # Rojo coral
    'chart-4': '#c4b5fd',  # Púrpura lavanda
    'chart-5': '#fdba74',  # Naranja melocotón
    'chart-6': '#67e8f9',  # Cyan aguamarina
    'chart-7': '#f9a8d4',  # Rosa pastel
    'chart-8': '#cbd5e1',  # Gris plata
}

# ========== VERIFICACIÓN DE CONTRASTE ==========

def verify_theme(theme_name, theme_colors):
    """Verificar contraste de un tema"""
    print(f"\n{'='*70}")
    print(f"  {theme_name.upper()}")
    print(f"{'='*70}\n")

    # Verificar textos sobre fondo principal
    bg = theme_colors['bg']

    print("📝 TEXTOS SOBRE FONDO PRINCIPAL:")
    print(f"{'Elemento':<25} {'Ratio':<10} {'WCAG':<8} {'Status'}")
    print("-" * 70)

    for text_type in ['text_primary', 'text_secondary', 'text_muted']:
        ratio = contrast_ratio(theme_colors[text_type], bg)
        wcag, status = check_wcag_compliance(ratio)
        print(f"{text_type:<25} {ratio:>6.2f}:1   {wcag:<8} {status}")

    # Verificar textos sobre superficie elevada
    print(f"\n📊 TEXTOS SOBRE SUPERFICIE ELEVADA (bg_surface):")
    print(f"{'Elemento':<25} {'Ratio':<10} {'WCAG':<8} {'Status'}")
    print("-" * 70)

    bg_surface = theme_colors['bg_surface']
    for text_type in ['text_primary', 'text_secondary', 'text_muted']:
        ratio = contrast_ratio(theme_colors[text_type], bg_surface)
        wcag, status = check_wcag_compliance(ratio)
        print(f"{text_type:<25} {ratio:>6.2f}:1   {wcag:<8} {status}")

    # Verificar interactivos
    print(f"\n🔵 ELEMENTOS INTERACTIVOS:")
    print(f"{'Elemento':<25} {'Ratio':<10} {'WCAG':<8} {'Status'}")
    print("-" * 70)

    ratio = contrast_ratio(theme_colors['interactive_primary'], bg)
    wcag, status = check_wcag_compliance(ratio, 'large')  # Botones son texto grande
    print(f"interactive_primary       {ratio:>6.2f}:1   {wcag:<8} {status}")

def verify_chart_colors(theme_name, chart_colors, bg_color):
    """Verificar contraste de colores de gráficos"""
    print(f"\n{'='*70}")
    print(f"  PALETA DE GRÁFICOS - {theme_name.upper()}")
    print(f"{'='*70}\n")

    print(f"📊 COLORES DE GRÁFICOS SOBRE FONDO:")
    print(f"{'Color':<15} {'Hex':<12} {'Ratio':<10} {'WCAG':<8} {'Status'}")
    print("-" * 70)

    for name, color in chart_colors.items():
        ratio = contrast_ratio(color, bg_color)
        wcag, status = check_wcag_compliance(ratio, 'large')  # Gráficos son elementos grandes
        print(f"{name:<15} {color:<12} {ratio:>6.2f}:1   {wcag:<8} {status}")

# Colores de badges Streamlit - Modo Oscuro
streamlit_badges_dark = {
    'success': '#10b981',   # Verde
    'warning': '#fbbf24',   # Amarillo
    'error': '#fca5a5',     # Rojo coral
    'info': '#7dd3fc',      # Azul cielo
}

# Colores de badges Streamlit - Modo Claro
streamlit_badges_light = {
    'success': '#d4edda',   # Verde claro
    'warning': '#fff3cd',   # Amarillo claro
    'error': '#f8d7da',     # Rojo claro
    'info': '#d1ecf1',      # Azul claro
}

def verify_streamlit_badges(theme_name, badge_colors, text_color, bg_color):
    """Verificar contraste de badges de Streamlit"""
    print(f"\n{'='*70}")
    print(f"  BADGES STREAMLIT - {theme_name.upper()}")
    print(f"{'='*70}\n")

    print(f"🏷️ TEXTO EN BADGES (color: {text_color}):")
    print(f"{'Badge':<15} {'BG Color':<12} {'Ratio':<10} {'WCAG':<8} {'Status'}")
    print("-" * 70)

    for name, color in badge_colors.items():
        ratio = contrast_ratio(text_color, color)
        wcag, status = check_wcag_compliance(ratio, 'large')
        print(f"{name:<15} {color:<12} {ratio:>6.2f}:1   {wcag:<8} {status}")

# ========== EJECUCIÓN ==========

if __name__ == "__main__":
    print("\n" + "="*70)
    print("  VERIFICACIÓN DE CONTRASTE WCAG - COPILOT SALUD ANDALUCÍA")
    print("="*70)
    print("\n📌 Criterios WCAG 2.1:")
    print("   • AA Normal Text:  ≥ 4.5:1")
    print("   • AAA Normal Text: ≥ 7.0:1")
    print("   • AA Large Text:   ≥ 3.0:1")
    print("   • AAA Large Text:  ≥ 4.5:1")

    # Verificar temas
    verify_theme("Modo Claro", light_theme)
    verify_theme("Modo Oscuro", dark_theme)

    # Verificar paletas de gráficos
    verify_chart_colors("Modo Claro", chart_colors_light, light_theme['bg'])
    verify_chart_colors("Modo Oscuro", chart_colors_dark, dark_theme['bg'])

    # Verificar badges de Streamlit
    verify_streamlit_badges("Modo Claro", streamlit_badges_light, '#0f5132', light_theme['bg'])
    verify_streamlit_badges("Modo Oscuro", streamlit_badges_dark, '#0f172a', dark_theme['bg'])

    print(f"\n{'='*70}")
    print("  ✅ VERIFICACIÓN COMPLETADA")
    print(f"{'='*70}\n")