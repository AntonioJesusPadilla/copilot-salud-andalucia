#!/usr/bin/env python3
import sys
import os

print("🧪 TEST SIMPLE - COPILOT SALUD ANDALUCÍA")
print("=" * 40)

# Test Python version
print(f"Python: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")

# Test imports básicos
try:
    import streamlit
    print("✅ Streamlit OK")
except ImportError:
    print("❌ Streamlit FALLO")

try:
    import pandas
    print("✅ Pandas OK")
except ImportError:
    print("❌ Pandas FALLO")

try:
    import plotly
    print("✅ Plotly OK")
except ImportError:
    print("❌ Plotly FALLO")

# Test archivos
files = ["app.py", "requirements.txt", "modules/performance_optimizer.py"]
for f in files:
    if os.path.exists(f):
        print(f"✅ {f} OK")
    else:
        print(f"❌ {f} FALLO")

print("\n🎯 Test completado")
