# Archivo de entrada para Vercel/Streamlit
# Este archivo importa y ejecuta la aplicación principal

import os
import sys

# Agregar el directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importar y ejecutar la aplicación principal
from app import main

if __name__ == "__main__":
    main()
