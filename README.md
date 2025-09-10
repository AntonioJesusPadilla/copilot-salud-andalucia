# 🏥 Copilot Salud Andalucía

**Sistema Inteligente de Análisis Sanitario con IA para la Provincia de Málaga**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://copilot-salud-andalucia.streamlit.app/)
[![Python](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 👨‍💻 **Autor**
**Antonio Jesús Padilla**

---

## 📋 **Descripción del Proyecto**

**Copilot Salud Andalucía** es una plataforma web avanzada desarrollada con Streamlit que proporciona análisis inteligente del sistema sanitario de la provincia de Málaga. El sistema integra inteligencia artificial, análisis de datos geoespaciales, mapas épicos interactivos, y un robusto sistema de autenticación y autorización basado en roles (RBAC) con **personalización completa por rol** para ofrecer insights estratégicos a diferentes tipos de usuarios del sector sanitario.

### 🎯 **Objetivos Principales**

- **Análisis Predictivo**: Proyecciones demográficas y necesidades sanitarias futuras
- **Optimización de Recursos**: Distribución eficiente de camas, personal y equipamiento
- **Equidad Territorial**: Evaluación de la accesibilidad y equidad en la atención sanitaria
- **Planificación Estratégica**: Herramientas para la toma de decisiones basadas en datos
- **Inteligencia Artificial**: Asistente IA especializado en análisis sociosanitario
- **Personalización Total**: Experiencia única adaptada a cada rol de usuario

---

## 📁 **Estructura del Proyecto**

```
copilot-salud-andalucia/
├── src/                    # Aplicaciones principales
│   ├── app.py             # Aplicación principal Streamlit
│   └── streamlit_app.py   # Aplicación alternativa
├── modules/               # Módulos organizados por funcionalidad
│   ├── core/              # Módulos principales
│   ├── ai/                # Procesamiento IA
│   ├── security/          # Seguridad y auditoría
│   ├── performance/       # Optimización y rendimiento
│   ├── visualization/     # Gráficos y mapas
│   └── admin/             # Administración
├── config/                # Configuración
│   ├── requirements.txt
│   ├── packages.txt
│   └── .streamlit/
├── data/                  # Datos del proyecto
│   ├── raw/              # Datos originales
│   └── processed/        # Datos procesados
├── docs/                  # Documentación completa
├── scripts/               # Scripts de utilidad
├── testing/               # Pruebas y verificación
└── assets/                # Recursos estáticos
```

---

## ⚡ **Instalación Rápida**

### **Opción 1: Instalación Automática (Recomendada)**
```bash
# Clonar el repositorio
git clone https://github.com/AntonioJesusPadilla/copilot-salud-andalucia.git
cd copilot-salud-andalucia

# Instalación automática de dependencias
python scripts/install_dependencies.py

# Configurar secrets (opcional para desarrollo)
cp config/.streamlit/secrets.toml.example config/.streamlit/secrets.toml
# Edita config/.streamlit/secrets.toml con tu GROQ_API_KEY

# Verificar instalación
python testing/check_dependencies.py

# Ejecutar la aplicación
python scripts/start_app.py
# O alternativamente: streamlit run src/app.py
```

### **Opción 2: Instalación Manual**
```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Verificar instalación
python testing/check_dependencies.py

# Ejecutar aplicación
streamlit run src/app.py
```

---

## 🔧 **Características Principales**

### **🚀 Optimización de Rendimiento**
- **Sistema de Caché Inteligente** - Caché por rol de usuario con TTL personalizado
- **Procesamiento Asíncrono de IA** - Consultas IA en segundo plano sin bloqueos
- **Carga Selectiva de Datos** - Solo datasets necesarios según el rol
- **Optimización de Consultas** - Consultas SQL optimizadas y indexación inteligente

### **🔐 Seguridad Avanzada**
- **Auditoría Completa** - Log de todas las acciones del usuario
- **Rate Limiting** - Protección contra ataques de fuerza bruta
- **Encriptación de Datos** - Datos sensibles encriptados con AES-256
- **Autenticación JWT** - Tokens seguros con expiración automática
- **Control de Acceso Basado en Roles (RBAC)** - Permisos granulares por rol

### **🤖 Inteligencia Artificial**
- **Asistente IA Especializado** - Groq API para análisis sociosanitario
- **Procesamiento Asíncrono** - Consultas IA no bloqueantes
- **Análisis Predictivo** - Proyecciones demográficas y sanitarias
- **Recomendaciones Inteligentes** - Sugerencias basadas en datos

### **🗺️ Visualización Avanzada**
- **Mapas Interactivos Épicos** - Folium con capas dinámicas
- **Gráficos Dinámicos** - Plotly con interactividad completa
- **Dashboard Personalizado** - Adaptado a cada rol de usuario
- **Análisis Geoespacial** - GeoPandas para análisis territorial

---

## 👥 **Sistema de Roles y Permisos**

| Rol | Usuario | Contraseña | Permisos |
|-----|---------|------------|----------|
| 🔴 **Administrador** | `admin` | `admin123` | Acceso total |
| 🔵 **Gestor Sanitario** | `gestor.malaga` | `gestor123` | Gestión y planificación |
| 🟢 **Analista** | `analista.datos` | `analista123` | Análisis y reportes |
| 🟣 **Invitado** | `demo` | `demo123` | Solo visualización |

---

## 📊 **Datos del Sistema**

- **Hospitales y Centros Sanitarios** - Red asistencial completa
- **Demografía de Málaga 2025** - Población y proyecciones
- **Indicadores de Salud** - Métricas sanitarias clave
- **Accesibilidad Sanitaria** - Tiempos y costes de acceso
- **Servicios Especializados** - Cobertura de servicios médicos

---

## 🛠️ **Tecnologías Utilizadas**

- **Frontend**: Streamlit 1.29+
- **IA**: Groq API
- **Datos**: Pandas, NumPy
- **Mapas**: Folium, GeoPandas, Geopy
- **Seguridad**: Bcrypt, PyJWT, Cryptography
- **Visualización**: Plotly, Seaborn, Matplotlib
- **Python**: 3.12.7 (última versión estable)

---

## 📚 **Documentación Completa**

- **[Guía de Instalación](docs/README.md)** - Instalación detallada y configuración
- **[Mejoras de Rendimiento](docs/MEJORAS_RENDIMIENTO_SEGURIDAD.md)** - Optimizaciones implementadas
- **[Guía de Despliegue](docs/DEPLOYMENT.md)** - Despliegue en producción
- **[Configuración Streamlit Cloud](docs/STREAMLIT_CLOUD_SETUP.md)** - Despliegue en la nube
- **[Política de Seguridad](docs/SECURITY.md)** - Mejores prácticas de seguridad
- **[Pruebas](testing/README_TESTS.md)** - Guía de testing y verificación

---

## 🚀 **Despliegue en Streamlit Cloud**

1. **Fork del repositorio** en GitHub
2. **Configurar secrets** en Streamlit Cloud:
   - `GROQ_API_KEY`: Tu API key de Groq
   - `JWT_SECRET_KEY`: Clave JWT segura
   - `SECRET_KEY`: Clave secreta de la aplicación
3. **Conectar repositorio** en Streamlit Cloud
4. **Desplegar** automáticamente

[![Deploy to Streamlit Cloud](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/)

---

## 🔧 **Solución de Problemas**

### **Dependencias de Mapas**
Si aparece el warning "geopy no disponible":
```bash
python testing/check_geopy.py
```

### **Verificación de Dependencias**
```bash
python testing/check_dependencies.py
```

### **Logs y Debugging**
```bash
python testing/verify_deployment.py
```

---

## 📈 **Casos de Uso Principales**

### **Para Administradores**
- Gestión integral del sistema sanitario
- Configuración y supervisión de usuarios
- Análisis de equidad territorial completo
- Planificación estratégica avanzada

### **Para Gestores Sanitarios**
- Optimización de recursos hospitalarios
- Análisis de capacidad asistencial
- Evaluación de accesibilidad por distrito
- Planificación de servicios sanitarios

### **Para Analistas**
- Análisis estadísticos avanzados
- Visualizaciones de datos epidemiológicos
- Estudios de correlación demográfica
- Reportes técnicos especializados

### **Para Invitados**
- Información general de hospitales
- Datos demográficos básicos
- Consultas sobre servicios disponibles
- Indicadores generales de salud

---

## 🤝 **Contribución**

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## 📄 **Licencia**

Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.

---

## 📞 **Contacto**

**Antonio Jesús Padilla**
- GitHub: [@AntonioJesusPadilla](https://github.com/AntonioJesusPadilla)
- Email: [email_protegido](antoniojesuspadilla.dev@proton.me)

---

**Versión**: 2.1.0 | **Última actualización**: 10/09/2025