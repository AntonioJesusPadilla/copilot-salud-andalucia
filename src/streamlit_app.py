#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Archivo de entrada limpio para Streamlit
Este archivo importa y ejecuta la aplicación principal
"""

import os
import sys
import streamlit as st

# Configurar paths
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)

# Asegurar que tanto la raíz como src están en el path
for path in [project_root, current_dir]:
    if path not in sys.path:
        sys.path.insert(0, path)

print(f"Streamlit app paths:")
print(f"Current dir: {current_dir}")
print(f"Project root: {project_root}")
print(f"Python path: {sys.path}")

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
    
    # Información adicional de debug
    import traceback
    st.code(traceback.format_exc())
