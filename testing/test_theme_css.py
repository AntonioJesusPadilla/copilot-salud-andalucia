"""
Script de diagnóstico para verificar la generación de CSS de temas
"""

# Simular el estado del tema
class MockSessionState:
    def __init__(self):
        self.theme_mode = 'dark'

    def get(self, key, default):
        return getattr(self, key, default)

st_session_state = MockSessionState()

# Simular la lógica del app.py
current_theme = st_session_state.get('theme_mode', 'light')

# Colores de texto principales según tema
if current_theme == 'light':
    text_color = '#0f172a'  # Texto muy oscuro para modo claro
    secondary_text = '#334155'
    muted_text = '#64748b'
else:
    text_color = '#f8fafc'  # Texto muy claro para modo oscuro
    secondary_text = '#cbd5e1'
    muted_text = '#94a3b8'

sidebar_text_color = '#0f172a'

# Generar badge CSS
if current_theme == 'dark':
    badge_css = """
    /* MODO OSCURO: Badges con fondos brillantes y texto oscuro para contraste */

    [data-testid="stAlert"],
    div[data-baseweb="notification"] {
        background-color: #10b981 !important;
        border-left: 4px solid #059669 !important;
    }

    [data-testid="stAlert"] *,
    div[data-baseweb="notification"] * {
        color: #0f172a !important;
    }
    """
else:
    badge_css = """
    /* MODO CLARO: Badges con texto oscuro para buen contraste */
    [data-testid="stAlert"] *,
    div[data-baseweb="notification"] * {
        color: #0f172a !important;
    }
    """

print(f"=== DIAGNÓSTICO DE TEMA: {current_theme.upper()} ===\n")
print(f"text_color: {text_color}")
print(f"secondary_text: {secondary_text}")
print(f"muted_text: {muted_text}")
print(f"sidebar_text_color: {sidebar_text_color}")
print(f"\n=== BADGE CSS GENERADO ===")
print(badge_css)
print("\n=== CSS PRINCIPAL ===")
print(f"""
.main .block-container,
.stMarkdown,
.stMetric {{
    color: {text_color} !important;
}}
""")

# Cambiar a modo claro y probar
print("\n\n" + "="*60)
st_session_state.theme_mode = 'light'
current_theme = st_session_state.get('theme_mode', 'light')

if current_theme == 'light':
    text_color = '#0f172a'
    secondary_text = '#334155'
    muted_text = '#64748b'
else:
    text_color = '#f8fafc'
    secondary_text = '#cbd5e1'
    muted_text = '#94a3b8'

print(f"=== DIAGNÓSTICO DE TEMA: {current_theme.upper()} ===\n")
print(f"text_color: {text_color}")
print(f"secondary_text: {secondary_text}")
print(f"muted_text: {muted_text}")