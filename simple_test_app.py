"""
Test Simple para Streamlit Cloud
"""

import streamlit as st

st.title("🏥 Test Simple - Copilot Salud Andalucía")
st.write("✅ Aplicación funcionando correctamente")

st.write("**Información del sistema:**")
st.write(f"- Streamlit version: {st.__version__}")
st.write(f"- Directorio actual: {os.getcwd()}")

import os
st.write(f"- Archivos en directorio: {len(os.listdir('.'))}")

st.success("🎉 ¡Test completado exitosamente!")
