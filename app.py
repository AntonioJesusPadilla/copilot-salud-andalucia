#!/usr/bin/env python3
"""
Punto de entrada principal para Streamlit Cloud
Copilot Salud Andalucía - Sistema de análisis sociosanitario
"""

import os
import sys

# Añadir directorio raíz del proyecto al path
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Importar y ejecutar la aplicación principal
from src.app import main

if __name__ == "__main__":
    main()
