# scripts/update_and_run.py
import subprocess
import sys
import os

def update_and_run():
    print("🔄 Actualizando desde GitHub...")
    subprocess.run(["git", "pull"], check=True)
    
    print("🚀 Iniciando Streamlit...")
    subprocess.run([
        sys.executable, "-m", "streamlit", "run", 
        "src/app.py", "--server.runOnSave", "true"
    ])

if __name__ == "__main__":
    update_and_run()