#!/usr/bin/env python3
"""
🔍 Script de Verificación para Despliegue en Streamlit Cloud
Verifica que todos los archivos y configuraciones estén listos.
"""

import os
import sys
import json
from pathlib import Path

def check_file_exists(filepath, description):
    """Verificar si un archivo existe"""
    if os.path.exists(filepath):
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ {description}: {filepath} - NO ENCONTRADO")
        return False

def check_requirements():
    """Verificar requirements.txt"""
    if not os.path.exists('requirements.txt'):
        print("❌ requirements.txt no encontrado")
        return False
    
    with open('requirements.txt', 'r', encoding='utf-8') as f:
        content = f.read()
    
    required_packages = [
        'streamlit',
        'pandas', 
        'plotly',
        'folium',
        'streamlit-folium',
        'groq',
        'bcrypt',
        'PyJWT'
    ]
    
    missing = []
    for package in required_packages:
        if package.lower() not in content.lower():
            missing.append(package)
    
    if missing:
        print(f"❌ Paquetes faltantes en requirements.txt: {missing}")
        return False
    else:
        print("✅ requirements.txt contiene todos los paquetes necesarios")
        return True

def check_data_files():
    """Verificar archivos de datos"""
    data_files = [
        'data/raw/hospitales_malaga_2025.csv',
        'data/raw/demografia_malaga_2025.csv',
        'data/raw/servicios_sanitarios_2025.csv',
        'data/raw/accesibilidad_sanitaria_2025.csv',
        'data/raw/indicadores_salud_2025.csv'
    ]
    
    all_exist = True
    for file in data_files:
        if not check_file_exists(file, "Archivo de datos"):
            all_exist = False
    
    return all_exist

def check_config_files():
    """Verificar archivos de configuración"""
    config_files = [
        ('.streamlit/config.toml', 'Configuración de Streamlit'),
        ('.streamlit/secrets.toml.example', 'Template de secrets'),
        ('streamlit_app.py', 'Punto de entrada principal'),
        ('app.py', 'Aplicación principal'),
        ('runtime.txt', 'Versión de Python')
    ]
    
    all_exist = True
    for file, desc in config_files:
        if not check_file_exists(file, desc):
            all_exist = False
    
    return all_exist

def check_users_file():
    """Verificar archivo de usuarios"""
    if not os.path.exists('data/users.json'):
        print("❌ data/users.json no encontrado")
        return False
    
    try:
        with open('data/users.json', 'r', encoding='utf-8') as f:
            users = json.load(f)
        
        required_roles = ['admin', 'gestor', 'analista', 'invitado']
        existing_roles = []
        
        for username, user_data in users.items():
            if 'role' in user_data:
                existing_roles.append(user_data['role'])
        
        missing_roles = [role for role in required_roles if role not in existing_roles]
        
        if missing_roles:
            print(f"⚠️  Roles faltantes en users.json: {missing_roles}")
        else:
            print("✅ Archivo de usuarios contiene todos los roles necesarios")
        
        return True
        
    except json.JSONDecodeError:
        print("❌ data/users.json tiene formato JSON inválido")
        return False

def check_modules():
    """Verificar módulos de la aplicación"""
    modules = [
        'modules/auth_system.py',
        'modules/ai_processor.py', 
        'modules/chart_generator.py',
        'modules/interactive_maps.py',
        'modules/map_interface.py',
        'modules/role_dashboards.py'
    ]
    
    all_exist = True
    for module in modules:
        if not check_file_exists(module, "Módulo"):
            all_exist = False
    
    return all_exist

def main():
    """Función principal de verificación"""
    print("🔍 VERIFICACIÓN DE DESPLIEGUE - Copilot Salud Andalucía")
    print("=" * 60)
    
    checks = [
        ("Archivos de configuración", check_config_files),
        ("Requirements.txt", check_requirements),
        ("Archivos de datos", check_data_files),
        ("Archivo de usuarios", check_users_file),
        ("Módulos de la aplicación", check_modules)
    ]
    
    all_passed = True
    results = []
    
    for check_name, check_func in checks:
        print(f"\n📋 Verificando: {check_name}")
        print("-" * 40)
        result = check_func()
        results.append((check_name, result))
        if not result:
            all_passed = False
    
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE VERIFICACIÓN")
    print("=" * 60)
    
    for check_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {check_name}")
    
    print("\n" + "=" * 60)
    
    if all_passed:
        print("🎉 ¡VERIFICACIÓN COMPLETA! El proyecto está listo para Streamlit Cloud")
        print("\n📝 Próximos pasos:")
        print("1. Sube todos los cambios a GitHub")
        print("2. Ve a https://share.streamlit.io")
        print("3. Crea nueva app con tu repositorio")
        print("4. Configura secrets según .streamlit/secrets.toml.example")
        print("5. ¡Despliega y disfruta!")
        return True
    else:
        print("⚠️  VERIFICACIÓN INCOMPLETA - Corrige los errores antes de desplegar")
        print("\n🔧 Acciones recomendadas:")
        print("- Ejecuta 'python data_collector_2025.py' si faltan datos")
        print("- Verifica que todos los archivos estén en el repositorio")
        print("- Revisa la documentación en DEPLOYMENT.md")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
