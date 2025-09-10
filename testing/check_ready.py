#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script simple de verificación para Streamlit Cloud"""

import os
import sys

def main():
    print("Verificando archivos para Streamlit Cloud...")
    
    # Archivos críticos
    critical_files = [
        'streamlit_app.py',
        'app.py', 
        'requirements.txt',
        '.streamlit/config.toml',
        '.streamlit/secrets.toml.example'
    ]
    
    missing = []
    for file in critical_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file}")
            missing.append(file)
    
    # Archivos de datos
    data_files = [
        'data/raw/hospitales_malaga_2025.csv',
        'data/raw/demografia_malaga_2025.csv',
        'data/users.json'
    ]
    
    print("\nArchivos de datos:")
    for file in data_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file}")
            missing.append(file)
    
    print("\n" + "="*50)
    if not missing:
        print("🎉 ¡TODO LISTO PARA STREAMLIT CLOUD!")
        print("\nPróximos pasos:")
        print("1. git add . && git commit -m 'Ready for Streamlit Cloud'")
        print("2. git push origin main")
        print("3. Ve a https://share.streamlit.io")
        print("4. Crea nueva app con tu repo")
        print("5. Configura secrets")
        return True
    else:
        print(f"❌ Faltan {len(missing)} archivos")
        print("Ejecuta 'python data_collector_2025.py' si faltan datos")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
