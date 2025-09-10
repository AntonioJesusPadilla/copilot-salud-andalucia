#!/usr/bin/env python3
"""
Script de Inicio Rápido - Copilot Salud Andalucía
Inicia la aplicación con la configuración correcta
"""

import os
import sys
import subprocess
from pathlib import Path

def check_environment():
    """Verificar que el entorno esté configurado correctamente"""
    print("🔍 Verificando entorno...")
    
    # Verificar Python
    if sys.version_info < (3, 9):
        print("❌ Se requiere Python 3.9 o superior")
        return False
    
    # Verificar archivos críticos
    required_files = [
        "src/app.py",
        "config/requirements.txt",
        "config/.streamlit/config.toml"
    ]
    
    for file_path in required_files:
        if not os.path.exists(file_path):
            print(f"❌ Archivo requerido no encontrado: {file_path}")
            return False
    
    print("✅ Entorno verificado")
    return True

def check_dependencies():
    """Verificar dependencias críticas"""
    print("📦 Verificando dependencias...")
    
    try:
        import streamlit
        import pandas
        import plotly
        print("✅ Dependencias críticas disponibles")
        return True
    except ImportError as e:
        print(f"❌ Dependencias faltantes: {e}")
        print("💡 Ejecuta: python install_dependencies.py")
        return False

def check_secrets():
    """Verificar configuración de secrets"""
    print("🔐 Verificando configuración...")
    
    secrets_file = ".streamlit/secrets.toml"
    example_file = ".streamlit/secrets.toml.example"
    
    if os.path.exists(secrets_file):
        print("✅ Archivo de secrets encontrado")
        return True
    elif os.path.exists(example_file):
        print("⚠️ Archivo de ejemplo encontrado")
        print("💡 Copia .streamlit/secrets.toml.example a .streamlit/secrets.toml")
        print("   y configura tu GROQ_API_KEY")
        return False
    else:
        print("⚠️ Archivo de secrets no encontrado")
        print("💡 Crea .streamlit/secrets.toml con tu GROQ_API_KEY")
        return False

def start_application():
    """Iniciar la aplicación Streamlit"""
    print("🚀 Iniciando Copilot Salud Andalucía...")
    
    # Comando para iniciar Streamlit
    cmd = [
        sys.executable, "-m", "streamlit", "run", "src/app.py",
        "--server.port", "8501",
        "--server.headless", "true",
        "--browser.gatherUsageStats", "false"
    ]
    
    try:
        print("🌐 Abriendo en: http://localhost:8501")
        print("⏹️ Presiona Ctrl+C para detener la aplicación")
        print("=" * 50)
        
        # Ejecutar Streamlit
        subprocess.run(cmd, check=True)
        
    except KeyboardInterrupt:
        print("\n👋 Aplicación detenida por el usuario")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error iniciando la aplicación: {e}")
        return False
    except FileNotFoundError:
        print("❌ Streamlit no encontrado")
        print("💡 Instala con: pip install streamlit")
        return False
    
    return True

def main():
    """Función principal"""
    print("🏥 COPILOT SALUD ANDALUCÍA - INICIO RÁPIDO")
    print("=" * 50)
    
    # Verificar entorno
    if not check_environment():
        print("\n❌ Entorno no configurado correctamente")
        sys.exit(1)
    
    # Verificar dependencias
    if not check_dependencies():
        print("\n❌ Dependencias faltantes")
        sys.exit(1)
    
    # Verificar secrets (opcional para desarrollo)
    secrets_ok = check_secrets()
    if not secrets_ok:
        print("\n⚠️ Configuración de secrets incompleta")
        print("💡 La aplicación funcionará en modo limitado")
        response = input("¿Continuar de todos modos? (s/n): ").lower()
        if response != 's':
            sys.exit(1)
    
    # Iniciar aplicación
    print("\n" + "=" * 50)
    start_application()

if __name__ == "__main__":
    main()
