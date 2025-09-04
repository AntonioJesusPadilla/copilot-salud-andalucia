# 🏥 Copilot Salud Andalucía

**Sistema Inteligente de Análisis Sanitario con IA para la Provincia de Málaga**

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
- **Python 3.8+**: Lenguaje principal del proyecto
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

### 📁 **Gestión de Datos**
- **CSV**: Almacenamiento de datasets
- **JSON**: Configuración y datos de usuario
- **OS/Path**: Manipulación de archivos y rutas

### 🔧 **Herramientas de Desarrollo**
- **Git**: Control de versiones
- **Virtual Environment**: Aislamiento de dependencias
- **Requirements.txt**: Gestión de paquetes Python

---

## 📁 **Estructura del Proyecto**

```
copilot-salud-andalucia/
├── 📄 app.py                          # Aplicación principal Streamlit
├── 📄 data_collector_2025.py          # Generador de datasets
├── 📄 requirements.txt               # Dependencias Python
├── 📄 README.md                      # Documentación del proyecto
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
│   └── 🎨 style.css               # Estilos CSS personalizados
└── 📁 venv/                        # Entorno virtual Python
```

---

## 🚀 **Instalación y Configuración**

### 📋 **Prerrequisitos**

- Python 3.8 o superior
- pip (gestor de paquetes Python)
- Cuenta en Groq AI (para funcionalidades de IA)

### ⚙️ **Instalación Paso a Paso**

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
echo "JWT_SECRET=tu_clave_secreta_jwt" >> .env
```

5. **Generar Datos Iniciales**
```bash
python data_collector_2025.py
```

6. **Ejecutar la Aplicación**
```bash
streamlit run app.py
```

### 🌐 **Acceso al Sistema**

Una vez iniciado, accede a: `http://localhost:8501`

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

- **Líneas de Código**: ~4,000+
- **Módulos Python**: 6 principales especializados
- **Funciones**: 80+ funciones especializadas
- **Datasets**: 5 datasets integrados + sistema de mapas
- **Roles de Usuario**: 4 niveles con personalización completa
- **Visualizaciones**: 20+ tipos de gráficos y mapas interactivos
- **Permisos**: 18 permisos granulares en español
- **Temas Personalizados**: 4 temas visuales únicos por rol
- **Mapas Épicos**: 8 tipos de mapas con control de acceso

---

**🏥 Copilot Salud Andalucía - Transformando la gestión sanitaria con inteligencia artificial y personalización total**

*Desarrollado con ❤️ por Antonio Jesús Padilla*
