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
from src.app import main

if __name__ == "__main__":
    main()
