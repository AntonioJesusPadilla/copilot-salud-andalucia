"""
Streamlit Cloud Entry Point
Punto de entrada principal para Streamlit Cloud
"""

import sys
import os

# Añadir el directorio raíz del proyecto al path
project_root = os.path.dirname(__file__)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Importar y ejecutar la aplicación principal
try:
    from src.app import main
    main()
except Exception as e:
    import streamlit as st
    st.error(f"❌ Error cargando aplicación: {str(e)}")
    st.write("**Información de debug:**")
    st.write(f"- Error: {str(e)}")
    st.write(f"- Directorio: {os.getcwd()}")
    st.write(f"- Archivos: {os.listdir('.')}")
