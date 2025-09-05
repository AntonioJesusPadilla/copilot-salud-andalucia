# 🏥 Copilot Salud Andalucía

**Sistema Inteligente de Análisis Sanitario con IA para la Provincia de Málaga**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://copilot-salud-andalucia.streamlit.app/)
[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
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

## 🚀 **Funcionalidades Principales**

### 🤖 **1. Asistente de Inteligencia Artificial**
- **Chat IA Especializado** powered by Groq (Llama 3.3 70B)
- Análisis automatizado de datos sanitarios
- Generación automática de visualizaciones
- Recomendaciones estratégicas personalizadas
- Consultas en lenguaje natural sobre datos de salud

### 🎨 **2. Dashboards Personalizados por Rol**
- **Dashboard Ejecutivo**: Vista comprensiva para administradores con KPIs estratégicos
- **Dashboard Operativo**: Panel de gestión para gestores sanitarios
- **Dashboard Analítico**: Laboratorio de datos para analistas con correlaciones
- **Dashboard Público**: Vista básica para usuarios invitados
- **Métricas Personalizadas**: Indicadores específicos según el rol del usuario
- **Temas Visuales**: Colores y estilos únicos para cada tipo de usuario

### 🗺️ **3. Mapas Épicos Interactivos**
- **Mapas con Control de Acceso**: Diferentes mapas según permisos del usuario
- **Geolocalización Avanzada**: Integración con Folium para mapas interactivos
- **Capas Dinámicas**: Hospitales, demografía, accesibilidad, especialidades
- **Análisis Geoespacial**: Heatmaps y rutas optimizadas
- **Persistencia de Estado**: Los mapas se mantienen al interactuar con ellos

### 📋 **4. Sistema de Reportes Avanzado**
- **Reporte Ejecutivo**: Métricas clave para directivos
- **Análisis de Infraestructura**: Evaluación de centros sanitarios
- **Reporte Demográfico**: Tendencias poblacionales y proyecciones
- **Evaluación de Equidad**: Análisis de equidad territorial (solo administradores)
- **Análisis Completo**: Reporte integral del sistema (solo administradores)

### 🗺️ **5. Planificación Estratégica**
- **Planificación de Ubicaciones**: Análisis para nuevos centros sanitarios
- **Proyección de Demanda**: Predicción de necesidades futuras
- **Redistribución de Recursos**: Optimización de personal y equipamiento
- **Optimización de Rutas**: Mejora de tiempos de acceso y transporte sanitario

### 👥 **6. Gestión de Usuarios y Roles**
- **Sistema RBAC Completo**: Control de acceso basado en roles
- **Gestión de Usuarios**: Creación, modificación y desactivación de cuentas
- **Auditoría de Accesos**: Registro de actividades y accesos
- **Perfiles Personalizados**: Diferentes niveles de acceso según el rol
- **Personalización Total**: UI, colores, métricas y funcionalidades por rol

---

## 🔐 **Sistema de Seguridad y Autorización**

### 🛡️ **Arquitectura de Seguridad**

El sistema implementa múltiples capas de seguridad:

1. **Autenticación JWT**: Tokens seguros para sesiones de usuario
2. **Hashing de Contraseñas**: Encriptación bcrypt para almacenamiento seguro
3. **Control de Sesiones**: Gestión automática de timeouts y renovación
4. **Validación de Permisos**: Verificación en cada operación crítica
5. **Auditoría de Accesos**: Logging completo de actividades de usuario

### 👥 **Roles y Permisos del Sistema**

#### 🔴 **ADMINISTRADOR** (`admin`)
**Acceso Total al Sistema**
- ✅ **Chat IA Completo** con Groq
- ✅ **Dashboard** con análisis avanzado
- ✅ **Todos los Reportes** incluido análisis de equidad
- ✅ **Planificación Estratégica** completa
- ✅ **Gestión de Usuarios** (crear/modificar/desactivar)
- ✅ **Análisis de Equidad** detallado
- ✅ **Configuración del Sistema**

**Credenciales Demo**: `admin` / `admin123`

#### 🔵 **GESTOR SANITARIO** (`gestor`)
**Gestión y Planificación**
- ✅ **Chat IA** especializado en gestión
- ✅ **Dashboard** con métricas clave
- ✅ **Reportes** ejecutivos y operacionales
- ✅ **Planificación** de recursos
- ❌ Gestión de usuarios (restringida)

**Credenciales Demo**: `gestor.malaga` / `gestor123`

#### 🟢 **ANALISTA DE DATOS** (`analista`)
**Análisis y Estadísticas**
- ✅ **Chat IA** para análisis estadísticos
- ✅ **Dashboard** con visualizaciones avanzadas
- ✅ **Reportes** técnicos y estadísticos
- ❌ Planificación estratégica (restringida)

**Credenciales Demo**: `analista.datos` / `analista123`

#### 🟣 **USUARIO INVITADO** (`invitado`)
**Visualización Básica**
- ✅ **Dashboard Básico** con métricas generales
- ❌ Chat IA (sin acceso)
- ❌ Reportes avanzados
- ❌ Planificación

**Credenciales Demo**: `demo` / `demo123`

---

## 🎨 **Personalización por Rol**

### 🏛️ **Administrador - Tema Ejecutivo**
- **Colores**: Azul ejecutivo (#1a365d)
- **Header**: Panel de Control Ejecutivo
- **Dashboard**: Vista comprensiva con KPIs estratégicos
- **Sidebar**: Expandido con gestión completa
- **Enfoque**: Supervisión general y análisis estratégico

### ⚙️ **Gestor - Tema Operativo**
- **Colores**: Azul gestión (#2b6cb0)
- **Header**: Centro de Gestión Sanitaria
- **Dashboard**: Métricas operativas y de capacidad
- **Sidebar**: Compacto con accesos directos
- **Enfoque**: Capacidad hospitalaria y operaciones

### 📊 **Analista - Tema Analítico**
- **Colores**: Verde analítico (#059669)
- **Header**: Laboratorio de Análisis de Datos
- **Dashboard**: Correlaciones y análisis estadístico
- **Sidebar**: Detallado con herramientas analíticas
- **Enfoque**: Estadísticas y tendencias demográficas

### 👁️ **Invitado - Tema Público**
- **Colores**: Gris público (#6b7280)
- **Header**: Portal de Información Pública
- **Dashboard**: Vista básica con información pública
- **Sidebar**: Mínimo con navegación esencial
- **Enfoque**: Información general accesible

---

## 🗺️ **Mapas Épicos - Sistema Avanzado**

### 🌟 **Tipos de Mapas Disponibles**

1. **🌟 Mapa Completo Épico**: Todas las capas (solo admin)
2. **🏥 Hospitales y Centros**: Ubicaciones y capacidad
3. **🏘️ Municipios y Demografía**: Datos poblacionales
4. **🔥 Heatmap de Accesibilidad**: Análisis de tiempos
5. **💊 Cobertura de Especialidades**: Servicios médicos
6. **🛣️ Rutas y Conexiones**: Optimización de trayectos
7. **📊 Análisis Demográfico**: Tendencias poblacionales
8. **🏥 Ubicaciones Básicas**: Información pública

### 🔒 **Control de Acceso por Mapas**
- **Administrador**: Acceso a todos los mapas incluyendo datos sensibles
- **Gestor**: Mapas operativos y de gestión
- **Analista**: Mapas analíticos y demográficos
- **Invitado**: Solo mapas con información pública

### 🗺️ **Mapas y Geolocalización**
- **Folium**: Mapas interactivos avanzados
- **Streamlit-Folium**: Integración de mapas en Streamlit
- **Geopandas**: Análisis geoespacial (preparado para futuras mejoras)

### 👥 **Permisos de Mapas en Español**
- ✅ `mapas_todos` - **🌟 Todos los Mapas**
- ✅ `mapas_estrategicos` - **🎯 Mapas Estratégicos**
- ✅ `mapas_sensibles` - **🔒 Mapas con Datos Sensibles**
- ✅ `mapas_operativos` - **⚙️ Mapas Operativos**
- ✅ `mapas_gestion` - **📊 Mapas de Gestión**
- ✅ `mapas_analiticos` - **📈 Mapas Analíticos**
- ✅ `mapas_demograficos` - **👥 Mapas Demográficos**
- ✅ `mapas_publicos` - **🌐 Mapas Públicos**

### 🔒 **Medidas de Seguridad Implementadas**

- **Validación de Entrada**: Sanitización de todos los inputs de usuario
- **Control de Acceso Granular**: Permisos específicos por funcionalidad
- **Sesiones Seguras**: Tokens JWT con expiración automática
- **Encriptación de Datos**: Hashing bcrypt para contraseñas
- **Logs de Auditoría**: Registro completo de accesos y operaciones
- **Backup de Usuarios**: Respaldo automático de la base de datos de usuarios

---

## 📊 **Datos y Análisis**

### 📈 **Datasets Integrados**

1. **🏥 Hospitales Málaga 2025** (10 centros)
   - Información completa de hospitales y centros sanitarios
   - Capacidad de camas, personal sanitario, especialidades
   - Geolocalización y áreas de cobertura

2. **👥 Demografía Málaga 2025** (20 municipios)
   - Proyecciones poblacionales actualizadas
   - Análisis de crecimiento y tendencias demográficas
   - Datos socioeconómicos por municipio

3. **🔬 Servicios Sanitarios 2025** (9 centros)
   - Catálogo completo de especialidades médicas
   - Disponibilidad y capacidad por servicio
   - Indicadores de calidad y rendimiento

4. **🗺️ Accesibilidad Sanitaria 2025** (15 rutas)
   - Tiempos de acceso entre municipios y hospitales
   - Análisis de rutas y transporte sanitario
   - Identificación de zonas con acceso limitado

5. **📈 Indicadores de Salud 2025** (6 distritos)
   - Métricas de salud por distrito sanitario
   - Ratios de profesionales por población
   - Indicadores de calidad asistencial

### 🧮 **Métricas y Análisis Calculados**

- **Ratio Camas/1000 habitantes**: Indicador de capacidad hospitalaria
- **Índice de Equidad Territorial**: Score 0-100 por distrito
- **Tiempo de Acceso Promedio**: Análisis de accesibilidad geográfica
- **Proyecciones de Demanda**: Predicciones basadas en crecimiento poblacional
- **Optimización de Recursos**: Recomendaciones de redistribución

---

## 🛠️ **Tecnologías Utilizadas**

### 🐍 **Backend y Framework Principal**
- **Python 3.9+**: Lenguaje principal del proyecto (optimizado para cloud)
- **Streamlit**: Framework web para aplicaciones de datos
- **Pandas**: Manipulación y análisis de datos
- **NumPy**: Computación numérica

### 🤖 **Inteligencia Artificial**
- **Groq API**: Plataforma de IA con modelo Llama 3.3 70B
- **LangChain**: Framework para aplicaciones con LLM
- **JSON**: Intercambio de datos estructurados con IA

### 📊 **Visualización y Gráficos**
- **Plotly Express**: Gráficos interactivos
- **Plotly Graph Objects**: Visualizaciones avanzadas
- **Matplotlib**: Gráficos estáticos complementarios

### 🔐 **Seguridad y Autenticación**
- **bcrypt**: Hashing seguro de contraseñas
- **PyJWT**: Manejo de tokens JSON Web Token
- **python-dotenv**: Gestión de variables de entorno
- **JSON**: Almacenamiento de datos de usuarios

### 🎨 **Frontend y Diseño**
- **HTML5 + CSS3**: Estructura y estilos personalizados
- **Google Fonts**: Tipografías modernas (Inter, Poppins)
- **CSS Grid/Flexbox**: Layouts responsivos
- **Custom CSS**: Temas personalizados y componentes
- **Responsive Design**: Optimizado para PC, tablets y móviles
- **Touch-Friendly**: Botones ≥44px (tablets), ≥48px (móviles)
- **Cross-Device**: Probado en múltiples resoluciones y dispositivos

### 📁 **Gestión de Datos**
- **CSV**: Almacenamiento de datasets
- **JSON**: Configuración y datos de usuario
- **OS/Path**: Manipulación de archivos y rutas

### 🔧 **Herramientas de Desarrollo**
- **Git**: Control de versiones
- **Virtual Environment**: Aislamiento de dependencias
- **Requirements.txt**: Gestión de paquetes Python

### ☁️ **Optimización para Cloud**
- **Streamlit Cloud**: Despliegue nativo optimizado
- **Cache Inteligente**: TTL de 1 hora para datasets
- **Compresión de Datos**: Tipos específicos para reducir memoria
- **Configuración de Producción**: Settings optimizados para cloud
- **Variables de Entorno**: Gestión segura con Streamlit Secrets

---

## 📁 **Estructura del Proyecto**

```
copilot-salud-andalucia/
├── 📄 streamlit_app.py              # Punto de entrada para Streamlit Cloud
├── 📄 app.py                        # Aplicación principal Streamlit
├── 📄 data_collector_2025.py        # Generador de datasets
├── 📄 requirements.txt              # Dependencias optimizadas para cloud
├── 📄 runtime.txt                   # Versión de Python para cloud
├── 📄 README.md                     # Documentación del proyecto
├── 📄 DEPLOYMENT.md                 # Guía completa de despliegue
├── 📄 STREAMLIT_CLOUD_SETUP.md     # Configuración rápida para cloud
├── 📁 .streamlit/                   # Configuración de Streamlit
│   ├── ⚙️ config.toml              # Configuración de producción
│   └── 🔑 secrets.toml.example     # Template de variables de entorno
├── 📁 modules/                       # Módulos del sistema
│   ├── 🔐 auth_system.py            # Sistema de autenticación y roles
│   ├── 🤖 ai_processor.py           # Procesador de IA con Groq
│   ├── 📊 chart_generator.py        # Generador de gráficos inteligentes
│   ├── 🗺️ map_interface.py          # Interfaz de mapas épicos
│   ├── 🌍 interactive_maps.py       # Mapas interactivos con Folium
│   └── 🎨 role_dashboards.py        # Dashboards personalizados por rol
├── 📁 data/                         # Datos del sistema
│   ├── 👥 users.json               # Base de datos de usuarios
│   └── 📁 raw/                     # Datasets CSV
│       ├── hospitales_malaga_2025.csv
│       ├── demografia_malaga_2025.csv
│       ├── servicios_sanitarios_2025.csv
│       ├── accesibilidad_sanitaria_2025.csv
│       └── indicadores_salud_2025.csv
├── 📁 assets/                       # Recursos estáticos
│   └── 🎨 style.css               # Estilos CSS responsivos optimizados
├── 📁 testing/                      # 🧪 Sistema de Pruebas Integral
│   ├── 📄 PLAN_PRUEBAS_COPILOT_SALUD.md      # Plan completo (60+ páginas)
│   ├── ✅ CHECKLIST_PRUEBAS_RAPIDO.md        # Checklist rápido (1 hora)
│   ├── 🤖 SCRIPT_PRUEBAS_AUTOMATIZADO.py    # Script automatizado
│   ├── 📋 GUIA_PRUEBAS_MANUALES.md          # Guía manual detallada
│   ├── 🔧 CORRECCION_BOTONES_TABLET.md      # Corrección tablets portrait
│   └── 📱 CORRECCION_FALLOS_RESPONSIVIDAD.md # Correcciones responsividad
└── 📁 venv/                        # Entorno virtual Python
```

---

## 🚀 **Despliegue y Configuración**

### 🌐 **Opción 1: Despliegue en Streamlit Cloud (Recomendado)**

#### 📋 **Prerrequisitos**
- Cuenta de GitHub
- Cuenta de Streamlit Cloud (gratuita)
- API Key de Groq AI (para funcionalidades de IA)

#### ⚙️ **Despliegue Paso a Paso**

1. **Fork o Clonar el Repositorio**
```bash
git clone [URL_DEL_REPOSITORIO]
cd copilot-salud-andalucia
```

2. **Subir a tu GitHub**
```bash
git add .
git commit -m "Preparado para Streamlit Cloud"
git push origin main
```

3. **Crear App en Streamlit Cloud**
- Ve a [share.streamlit.io](https://share.streamlit.io)
- Inicia sesión con GitHub
- Clic en "New app"
- Selecciona tu repositorio
- **Main file path**: `streamlit_app.py`

4. **Configurar Variables de Entorno (Secrets)**
En Advanced Settings → Secrets, añade:
```toml
GROQ_API_KEY = "tu_groq_api_key_aqui"
JWT_SECRET_KEY = 'tu_jwt_secret_super_segura'
APP_ENVIRONMENT = "production"
SYSTEM_NAME = "Copilot Salud Andalucía"
```

5. **¡Desplegar!**
- La app estará lista en 2-5 minutos
- URL: `https://tu-app.streamlit.app`

### 🖥️ **Opción 2: Instalación Local**

#### 📋 **Prerrequisitos**
- Python 3.9 o superior
- pip (gestor de paquetes Python)
- Cuenta en Groq AI (para funcionalidades de IA)

#### ⚙️ **Instalación Local Paso a Paso**

1. **Clonar el Repositorio**
```bash
git clone [URL_DEL_REPOSITORIO]
cd copilot-salud-andalucia
```

2. **Crear Entorno Virtual**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate     # Windows
```

3. **Instalar Dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar Variables de Entorno**
```bash
# Crear archivo .env en la raíz del proyecto
echo "GROQ_API_KEY=tu_clave_de_groq_aqui" > .env
echo "JWT_SECRET_KEY=tu_clave_secreta_jwt" >> .env
```

5. **Generar Datos Iniciales (si es necesario)**
```bash
python data_collector_2025.py
```

6. **Ejecutar la Aplicación**
```bash
streamlit run streamlit_app.py
```

### 🌐 **Acceso al Sistema**
- **Streamlit Cloud**: [https://copilot-salud-andalucia.streamlit.app/](https://copilot-salud-andalucia.streamlit.app/)
- **Local**: `http://localhost:8501`

---

## 👥 **Usuarios de Demostración**

| Rol | Usuario | Contraseña | Permisos |
|-----|---------|------------|----------|
| 🔴 **Administrador** | `admin` | `admin123` | Acceso total |
| 🔵 **Gestor Sanitario** | `gestor.malaga` | `gestor123` | Gestión y planificación |
| 🟢 **Analista** | `analista.datos` | `analista123` | Análisis y reportes |
| 🟣 **Invitado** | `demo` | `demo123` | Solo visualización |

---

## 📈 **Casos de Uso Principales**

### 🏥 **Para Directivos Sanitarios**
- Monitoreo de KPIs en tiempo real
- Análisis de equidad territorial
- Planificación estratégica de recursos
- Reportes ejecutivos automatizados

### 👨‍⚕️ **Para Gestores de Centros**
- Optimización de recursos hospitalarios
- Análisis de demanda y capacidad
- Planificación de personal sanitario
- Evaluación de servicios especializados

### 📊 **Para Analistas de Datos**
- Análisis estadístico avanzado
- Visualizaciones interactivas
- Proyecciones demográficas
- Estudios de accesibilidad

### 🎯 **Para Planificadores**
- Identificación de necesidades futuras
- Análisis de ubicaciones óptimas
- Optimización de rutas sanitarias
- Estudios de impacto poblacional

---

## 🧪 **Sistema de Pruebas y Calidad**

### 📋 **Plan de Pruebas Integral**

El proyecto incluye un **sistema completo de pruebas** para garantizar funcionamiento óptimo en todos los dispositivos:

#### **🔧 Herramientas de Testing Incluidas**
- **📄 Plan de Pruebas Completo**: `PLAN_PRUEBAS_COPILOT_SALUD.md` (60+ páginas)
- **✅ Checklist Rápido**: `CHECKLIST_PRUEBAS_RAPIDO.md` (40-60 minutos)
- **🤖 Script Automatizado**: `SCRIPT_PRUEBAS_AUTOMATIZADO.py`
- **📋 Guía Manual**: `GUIA_PRUEBAS_MANUALES.md` (15 tests detallados)

#### **📱 Cobertura Multi-Dispositivo**
- **🖥️ PC Escritorio**: Windows, macOS, Linux (Chrome, Firefox, Safari, Edge)
- **📱 Móviles**: iPhone, Android (375x667, 414x896, 360x640)
- **📟 Tablets**: iPad, Surface, Android (768x1024, 1024x768)

#### **🎯 Tipos de Pruebas**
- ✅ **Funcionales**: Todas las características principales
- ✅ **Responsividad**: Adaptación a diferentes pantallas  
- ✅ **Rendimiento**: Tiempos de carga y fluidez
- ✅ **Seguridad**: Autenticación y control de acceso
- ✅ **Usabilidad**: Experiencia de usuario optimizada
- ✅ **Compatibilidad**: Cross-browser y cross-device

#### **⚡ Ejecución de Pruebas**

**Pruebas Rápidas (1 hora)**:
```bash
# Script automatizado
python SCRIPT_PRUEBAS_AUTOMATIZADO.py

# Seguir checklist rápido
# Ver CHECKLIST_PRUEBAS_RAPIDO.md
```

**Pruebas Completas (1-2 días)**:
```bash
# Plan completo de pruebas
# Ver PLAN_PRUEBAS_COPILOT_SALUD.md
# Ver GUIA_PRUEBAS_MANUALES.md
```

#### **📊 Métricas de Calidad**
- **Cobertura**: >95% casos de prueba
- **Rendimiento**: <5s PC, <8s móviles
- **Compatibilidad**: 100% navegadores principales
- **Accesibilidad**: Cumple WCAG 2.1
- **Botones táctiles**: ≥44px (tablets), ≥48px (móviles)

#### **🔒 Pruebas de Seguridad**
- **Control de Acceso**: RBAC por roles
- **Autenticación**: JWT + bcrypt
- **Sesiones**: Expiración automática
- **Validación**: Sanitización de inputs

---

## 🔮 **Funcionalidades Futuras**

### 🚀 **Roadmap de Desarrollo**

- **🗺️ Mapas Interactivos**: Integración con sistemas GIS
- **📱 Aplicación Móvil**: Versión nativa para dispositivos móviles
- **🔔 Alertas Automáticas**: Notificaciones de eventos críticos
- **📊 Business Intelligence**: Dashboards ejecutivos avanzados
- **🤖 IA Predictiva**: Modelos de machine learning personalizados
- **🔗 APIs REST**: Integración con sistemas externos
- **📧 Reportes Automáticos**: Envío programado de informes
- **🌐 Multi-idioma**: Soporte para múltiples idiomas
- **🧪 Testing Continuo**: Integración CI/CD con pruebas automatizadas

---

## 🔗 **Enlaces Útiles**

### 📚 **Documentación**
- [DEPLOYMENT.md](DEPLOYMENT.md) - Guía completa de despliegue
- [STREAMLIT_CLOUD_SETUP.md](STREAMLIT_CLOUD_SETUP.md) - Configuración rápida
- [Streamlit Cloud](https://share.streamlit.io) - Plataforma de despliegue
- [Groq Console](https://console.groq.com) - API Keys de IA

### 🌐 **Demo en Vivo**
- **URL de Producción**: [https://copilot-salud-andalucia.streamlit.app/](https://copilot-salud-andalucia.streamlit.app/)
- **Estado del Sistema**: [![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://copilot-salud-andalucia.streamlit.app/)

---

## 🤝 **Contribuciones**

### 📋 **Cómo Contribuir**

1. Fork del proyecto
2. Crear rama para nueva funcionalidad (`git checkout -b feature/NuevaFuncionalidad`)
3. Commit de cambios (`git commit -m 'Añadir nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/NuevaFuncionalidad`)
5. Crear Pull Request

### 🐛 **Reporte de Bugs**

Para reportar bugs o solicitar funcionalidades, crear un issue en el repositorio con:
- Descripción detallada del problema
- Pasos para reproducir
- Capturas de pantalla (si aplica)
- Información del entorno

---

## 📜 **Licencia**

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

---

## 📞 **Contacto**

**Autor**: Antonio Jesús Padilla
- 📧 Email: [antoniojesuspadilla.dev@proton.me]
- 💼 LinkedIn: [tu_perfil_linkedin]
- 🐙 GitHub: [https://github.com/antonioJesusPadilla/]

---

## 🙏 **Agradecimientos**

- **Groq AI** por proporcionar acceso a modelos de IA avanzados
- **Streamlit** por el framework de desarrollo web
- **Plotly** por las herramientas de visualización
- **Consejería de Salud de Andalucía** por los datos de referencia
- **Comunidad Open Source** por las librerías utilizadas

---

## 📊 **Estadísticas del Proyecto**

- **Líneas de Código**: ~4,500+
- **Archivos de Configuración**: 3 (config.toml, secrets.example, runtime.txt)
- **Documentación**: 3 archivos especializados
- **Módulos Python**: 6 principales especializados
- **Funciones**: 80+ funciones especializadas
- **Datasets**: 5 datasets integrados + sistema de mapas
- **Roles de Usuario**: 4 niveles con personalización completa
- **Visualizaciones**: 20+ tipos de gráficos y mapas interactivos
- **Permisos**: 18 permisos granulares en español
- **Temas Personalizados**: 4 temas visuales únicos por rol
- **Mapas Épicos**: 8 tipos de mapas con control de acceso
- **🧪 Sistema de Pruebas**: 4 documentos de testing + script automatizado
- **📱 Dispositivos Soportados**: 7 resoluciones diferentes
- **🔧 Casos de Prueba**: 54+ tests automatizados
- **📋 Tests Manuales**: 15 procedimientos detallados
- **✅ Cobertura**: >95% funcionalidades probadas

---

**🏥 Copilot Salud Andalucía - Transformando la gestión sanitaria con inteligencia artificial y personalización total**

*Desarrollado con ❤️ por Antonio Jesús Padilla*
