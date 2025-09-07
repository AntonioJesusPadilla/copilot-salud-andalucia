# Archivo de entrada para Vercel/Streamlit
# Este archivo importa y ejecuta la aplicación principal

import os
import sys
import streamlit as st

# Agregar el directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configuración para producción
os.environ.setdefault('STREAMLIT_SERVER_HEADLESS', 'true')
os.environ.setdefault('STREAMLIT_SERVER_PORT', '8501')
os.environ.setdefault('STREAMLIT_BROWSER_GATHER_USAGE_STATS', 'false')

# Forzar layout de escritorio - CSS adicional para Streamlit Cloud
import streamlit as st
st.markdown("""
<style>
/* FORZAR LAYOUT DE ESCRITORIO EN STREAMLIT CLOUD */
.main .block-container {
    max-width: none !important;
    min-width: 1200px !important;
}

@media screen and (max-width: 768px) {
    .main .block-container {
        min-width: 1200px !important;
        overflow-x: auto !important;
    }
}
</style>
<script>
// Forzar viewport desktop en Streamlit Cloud
var viewport = document.querySelector("meta[name=viewport]");
if (viewport) {
    viewport.setAttribute('content', 'width=1200, initial-scale=1.0, maximum-scale=1.0, user-scalable=no');
}
</script>
""", unsafe_allow_html=True)

# Importar y ejecutar la aplicación principal
try:
    from app import main
    
    if __name__ == "__main__":
        main()
except Exception as e:
    st.error(f"❌ Error iniciando la aplicación: {str(e)}")
    st.info("🔧 Verifica que todas las dependencias estén instaladas correctamente")
