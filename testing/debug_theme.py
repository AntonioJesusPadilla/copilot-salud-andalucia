"""
Script de depuración para verificar que los estilos CSS se están generando correctamente
"""

# Simular session_state
class MockSessionState:
    def __init__(self, theme='dark'):
        self.theme_mode = theme

    def get(self, key, default):
        return getattr(self, key, default)

# Probar ambos temas
for theme in ['light', 'dark']:
    st_session_state = MockSessionState(theme)
    current_theme = st_session_state.get('theme_mode', 'light')

    # Colores de texto principales según tema
    if current_theme == 'light':
        text_color = '#0f172a'
        secondary_text = '#334155'
        muted_text = '#64748b'
    else:
        text_color = '#f8fafc'
        secondary_text = '#cbd5e1'
        muted_text = '#94a3b8'

    sidebar_text_color = '#0f172a'

    print(f"\n{'='*60}")
    print(f"TEMA: {current_theme.upper()}")
    print(f"{'='*60}")
    print(f"text_color: {text_color}")
    print(f"sidebar_text_color: {sidebar_text_color}")

    # Verificar que las reglas CSS se generan correctamente
    print(f"\n--- Expanders CSS ---")
    print(f"div[data-testid=\"stExpander\"] {{")
    print(f"    color: {text_color} !important;")
    print(f"}}")

    print(f"\n--- Métricas CSS ---")
    print(f"div[data-testid=\"stMetric\"] * {{")
    print(f"    color: {text_color} !important;")
    print(f"}}")

    print(f"\n--- Badge CSS para {current_theme} ---")
    if current_theme == 'dark':
        print("Fondos: #10b981 (verde), #fbbf24 (amarillo), #fca5a5 (rojo), #7dd3fc (azul)")
        print(f"Texto en badges: #0f172a (oscuro)")
    else:
        print(f"Texto en badges: #0f172a (oscuro)")

print("\n✅ Generación de CSS completada")