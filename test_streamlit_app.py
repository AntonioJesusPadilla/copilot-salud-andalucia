"""
Test Streamlit App - Diagnóstico
"""

import sys
import os

print("🔍 DIAGNÓSTICO DE STREAMLIT APP")
print("=" * 50)

# Verificar directorio actual
print(f"📁 Directorio actual: {os.getcwd()}")
print(f"📁 Archivo actual: {__file__}")

# Verificar path de Python
print(f"🐍 Python path: {sys.path[:3]}...")

# Añadir directorio raíz del proyecto al path
project_root = os.path.dirname(__file__)
print(f"📁 Project root: {project_root}")

if project_root not in sys.path:
    sys.path.insert(0, project_root)
    print(f"✅ Añadido al path: {project_root}")
else:
    print(f"ℹ️ Ya en path: {project_root}")

# Verificar si existe src/app.py
src_app_path = os.path.join(project_root, "src", "app.py")
print(f"📄 src/app.py existe: {os.path.exists(src_app_path)}")

# Intentar importar
try:
    print("🔄 Intentando importar src.app...")
    from src.app import main
    print("✅ Import exitoso: src.app.main")
    
    # Verificar que main es callable
    print(f"🔧 main es callable: {callable(main)}")
    
except ImportError as e:
    print(f"❌ Error de import: {e}")
except Exception as e:
    print(f"❌ Error general: {e}")

print("=" * 50)
print("🏁 Diagnóstico completado")
