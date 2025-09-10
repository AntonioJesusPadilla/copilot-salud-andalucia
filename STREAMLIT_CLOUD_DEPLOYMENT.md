# 🚀 Guía de Despliegue en Streamlit Cloud

## 📋 **Preparación Completada**

El proyecto **Copilot Salud Andalucía** está listo para desplegar en Streamlit Cloud con la nueva estructura reorganizada.

---

## 🔧 **Archivos de Configuración**

### **✅ Archivos en la Raíz (Requeridos por Streamlit Cloud)**
- `app.py` - Punto de entrada principal
- `requirements.txt` - Dependencias de Python
- `packages.txt` - Dependencias del sistema
- `runtime.txt` - Versión de Python
- `.streamlit/config.toml` - Configuración de Streamlit

### **📁 Estructura del Proyecto**
```
copilot-salud-andalucia/
├── app.py                    # ✅ Punto de entrada
├── requirements.txt          # ✅ Dependencias
├── packages.txt              # ✅ Sistema
├── runtime.txt               # ✅ Python 3.11
├── .streamlit/
│   ├── config.toml          # ✅ Configuración
│   └── secrets.toml         # ✅ Secrets (ejemplo)
├── src/
│   └── app.py               # ✅ Aplicación principal
├── modules/                 # ✅ Módulos organizados
├── data/                    # ✅ Datos del proyecto
├── docs/                    # ✅ Documentación
└── testing/                 # ✅ Pruebas
```

---

## 🚀 **Pasos para Desplegar**

### **1. Subir a GitHub**
```bash
git add .
git commit -m "🚀 Preparar para despliegue en Streamlit Cloud"
git push origin main
```

### **2. Conectar con Streamlit Cloud**
1. Ir a [share.streamlit.io](https://share.streamlit.io)
2. Iniciar sesión con GitHub
3. Seleccionar repositorio: `copilot-salud-andalucia`
4. Configurar:
   - **Main file path**: `app.py`
   - **Python version**: `3.11`
   - **Dependencies**: `requirements.txt`

### **3. Configurar Secrets**
En la interfaz de Streamlit Cloud, añadir en "Secrets":

```toml
GROQ_API_KEY = "tu_api_key_de_groq_aqui"
```

### **4. Variables de Entorno (Opcional)**
- `GROQ_API_KEY`: API key de Groq para funcionalidad IA
- `STREAMLIT_SERVER_PORT`: 8501 (por defecto)
- `STREAMLIT_SERVER_HEADLESS`: true

---

## ⚙️ **Configuración Específica**

### **📦 Dependencias del Sistema (packages.txt)**
```
libgeos-dev
libproj-dev
libgdal-dev
libspatialite-dev
libsqlite3-mod-spatialite
build-essential
libffi-dev
libssl-dev
```

### **🐍 Dependencias de Python (requirements.txt)**
```
streamlit>=1.29.0
pandas>=2.1.0
numpy>=1.24.0
plotly>=5.17.0
groq>=0.4.0
folium>=0.15.0
geopandas>=0.14.0
shapely>=2.0.0
geopy>=2.4.0
pyproj>=3.6.0
bcrypt>=4.1.0
PyJWT>=2.8.0
cryptography>=41.0.0
aiohttp>=3.8.0
```

### **⚡ Configuración de Streamlit (.streamlit/config.toml)**
```toml
[server]
port = 8501
headless = true
enableCORS = false
enableXsrfProtection = false

[browser]
gatherUsageStats = false

[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
```

---

## 🔍 **Verificación Post-Despliegue**

### **✅ Checklist de Verificación**
- [ ] Aplicación carga correctamente
- [ ] Autenticación funciona
- [ ] Mapas interactivos se muestran
- [ ] IA responde a consultas
- [ ] Dashboards por rol funcionan
- [ ] Datos se cargan correctamente

### **🌐 URLs de Acceso**
- **Streamlit Cloud**: `https://tu-app.streamlit.app`
- **Logs**: Disponibles en la interfaz de Streamlit Cloud
- **Métricas**: Monitoreo automático

---

## 🛠️ **Solución de Problemas**

### **❌ Error: "No module named 'modules'"**
- **Solución**: Verificar que `app.py` está en la raíz
- **Verificar**: Path de importación en `app.py`

### **❌ Error: "Dependencies not found"**
- **Solución**: Verificar `requirements.txt` y `packages.txt`
- **Verificar**: Versión de Python en `runtime.txt`

### **❌ Error: "Secrets not found"**
- **Solución**: Configurar `GROQ_API_KEY` en secrets
- **Verificar**: Formato TOML en secrets

### **❌ Error: "Mapas no disponibles"**
- **Solución**: Verificar dependencias de mapas en `packages.txt`
- **Verificar**: Instalación de `folium`, `geopandas`

---

## 📊 **Características del Despliegue**

### **🚀 Optimizaciones Incluidas**
- ✅ Estructura modular organizada
- ✅ Imports optimizados
- ✅ Cache inteligente
- ✅ Rate limiting
- ✅ Seguridad mejorada
- ✅ Mapas interactivos
- ✅ IA asíncrona

### **📈 Escalabilidad**
- ✅ Módulos independientes
- ✅ Configuración centralizada
- ✅ Logs estructurados
- ✅ Monitoreo integrado

---

## 🎯 **Estado del Despliegue**

**✅ LISTO PARA DESPLEGAR**

- **Estructura**: ✅ Reorganizada y optimizada
- **Configuración**: ✅ Preparada para Streamlit Cloud
- **Dependencias**: ✅ Verificadas y compatibles
- **Secrets**: ✅ Configurados
- **Documentación**: ✅ Completa

---

*Preparado el 10 de Septiembre de 2025*
