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

# Importar y ejecutar la aplicación principal
try:
    from app import main
    
    if __name__ == "__main__":
        main()
except Exception as e:
    st.error(f"❌ Error iniciando la aplicación: {str(e)}")
    st.info("🔧 Verifica que todas las dependencias estén instaladas correctamente")
