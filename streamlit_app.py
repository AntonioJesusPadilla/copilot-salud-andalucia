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

# Test simple primero
try:
    import streamlit as st
    
    st.title("🏥 Copilot Salud Andalucía - Test")
    st.write("✅ Aplicación cargando correctamente")
    
    # Verificar imports críticos
    st.write("**Verificando dependencias:**")
    
    try:
        import pandas as pd
        st.write("✅ pandas")
    except ImportError as e:
        st.error(f"❌ pandas: {e}")
    
    try:
        import plotly.express as px
        st.write("✅ plotly")
    except ImportError as e:
        st.error(f"❌ plotly: {e}")
    
    try:
        from modules.core.auth_system import HealthAuthenticator
        st.write("✅ auth_system")
    except ImportError as e:
        st.error(f"❌ auth_system: {e}")
    
    # Intentar cargar la aplicación principal
    st.write("**Cargando aplicación principal...**")
    try:
        from src.app import main
        st.success("✅ Aplicación principal importada correctamente")
        
        # Ejecutar la aplicación principal
        main()
        
    except Exception as e:
        st.error(f"❌ Error cargando aplicación principal: {str(e)}")
        st.write("**Información de debug:**")
        st.write(f"- Directorio actual: {os.getcwd()}")
        st.write(f"- Archivos disponibles: {os.listdir('.')}")
        st.write(f"- Python path: {sys.path[:3]}")

except Exception as e:
    st.error(f"❌ Error crítico: {str(e)}")
    st.write("**Información de debug:**")
    st.write(f"- Error: {str(e)}")
    st.write(f"- Tipo: {type(e).__name__}")
