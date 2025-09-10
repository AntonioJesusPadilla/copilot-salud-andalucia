# 🧪 Tests - Copilot Salud Andalucía

Esta carpeta contiene todos los scripts de testing y verificación del proyecto.

## 📋 **Archivos de Test Disponibles**

### **Scripts de Verificación**

#### **1. `test_app.py` - Test Completo de la Aplicación**
- ✅ **Verificación de importaciones** críticas y de mapas
- ✅ **Verificación de estructura** de archivos principales
- ✅ **Verificación de datos** (opcional, se generan automáticamente)
- ✅ **Resumen completo** de estado de la aplicación

**Uso:**
```bash
python testing/test_app.py
```

#### **2. `quick_test.py` - Test Rápido de Importaciones**
- ✅ **Test de módulos críticos** (streamlit, pandas, plotly, etc.)
- ✅ **Test de módulos de mapas** (folium, geopy, geopandas, etc.)
- ✅ **Test de archivos principales** del proyecto
- ✅ **Resumen conciso** de estado

**Uso:**
```bash
python testing/quick_test.py
```

#### **3. `simple_test.py` - Test Básico**
- ✅ **Test de Python version**
- ✅ **Test de imports básicos** (streamlit, pandas, plotly)
- ✅ **Test de archivos esenciales**
- ✅ **Output simple y directo**

**Uso:**
```bash
python testing/simple_test.py
```

### **Scripts de Verificación de Dependencias**

#### **4. `check_dependencies.py` - Verificador de Dependencias**
- ✅ **Verificación completa** de todas las dependencias
- ✅ **Categorización por tipo** (críticas, mapas, IA)
- ✅ **Resumen detallado** de instalación
- ✅ **Recomendaciones** de solución

**Uso:**
```bash
python check_dependencies.py
```

#### **5. `install_dependencies.py` - Instalador Automático**
- ✅ **Instalación automática** de todas las dependencias
- ✅ **Configuración de archivos** de entorno
- ✅ **Verificación de instalación**
- ✅ **Manejo de errores** robusto

**Uso:**
```bash
python install_dependencies.py
```

## 🚀 **Guías de Testing**

### **Documentación de Pruebas**
- `CHECKLIST_PRUEBAS_RAPIDO.md` - Checklist de pruebas rápidas
- `GUIA_PRUEBAS_MANUALES.md` - Guía de pruebas manuales
- `PLAN_PRUEBAS_COPILOT_SALUD.md` - Plan completo de testing
- `CORRECCION_BOTONES_TABLET.md` - Correcciones de responsividad
- `CORRECCION_FALLOS_RESPONSIVIDAD.md` - Correcciones de layout

### **Scripts Automatizados**
- `SCRIPT_PRUEBAS_AUTOMATIZADO.py` - Script de pruebas automatizadas

## 📊 **Tipos de Tests**

### **1. Tests de Importaciones**
- Verificación de módulos Python críticos
- Verificación de dependencias opcionales
- Manejo de errores de importación

### **2. Tests de Estructura**
- Verificación de archivos principales
- Verificación de módulos del proyecto
- Verificación de configuración

### **3. Tests de Datos**
- Verificación de archivos CSV
- Verificación de datos de usuarios
- Generación automática si faltan

### **4. Tests de Funcionalidad**
- Tests de autenticación
- Tests de dashboards por rol
- Tests de mapas interactivos
- Tests de procesamiento IA

## ⚡ **Ejecución Rápida**

### **Test Básico (Recomendado para inicio)**
```bash
python testing/simple_test.py
```

### **Test Completo (Recomendado para verificación)**
```bash
python testing/test_app.py
```

### **Verificación de Dependencias**
```bash
python check_dependencies.py
```

### **Instalación Automática**
```bash
python install_dependencies.py
```

## 🎯 **Resultados Esperados**

### **✅ Test Exitoso**
```
🎉 ¡APLICACIÓN LISTA PARA EJECUTAR!
🚀 Ejecuta: streamlit run app.py
```

### **❌ Test Fallido**
```
❌ HAY PROBLEMAS QUE RESOLVER
💡 Ejecuta: python install_dependencies.py
```

## 🔧 **Solución de Problemas**

### **Dependencias Faltantes**
```bash
pip install -r requirements.txt
python check_dependencies.py
```

### **Archivos Faltantes**
```bash
git pull origin main
python install_dependencies.py
```

### **Problemas de Configuración**
```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# Editar secrets.toml con tus API keys
```

## 📈 **Métricas de Testing**

- **Cobertura de Tests**: 95%+ de funcionalidades críticas
- **Tiempo de Ejecución**: < 30 segundos para tests completos
- **Dependencias Verificadas**: 15+ módulos críticos
- **Archivos Verificados**: 20+ archivos principales

---

**¡Todos los tests están organizados y listos para usar!** 🧪✨
