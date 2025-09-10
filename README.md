# 🏥 Copilot Salud Andalucía

Sistema de análisis sociosanitario inteligente para la provincia de Málaga.

## 📁 Estructura del Proyecto

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
├── docs/                  # Documentación
├── scripts/               # Scripts de utilidad
├── testing/               # Pruebas y verificación
└── assets/                # Recursos estáticos
```

## 🚀 Inicio Rápido

```bash
# Instalar dependencias
python scripts/install_dependencies.py

# Iniciar aplicación
python scripts/start_app.py
```

## 📚 Documentación

- [Guía de Instalación](docs/README.md)
- [Mejoras de Rendimiento](docs/MEJORAS_RENDIMIENTO_SEGURIDAD.md)
- [Guía de Despliegue](docs/DEPLOYMENT.md)
- [Pruebas](testing/README_TESTS.md)

## 🔧 Características

- **IA Avanzada**: Procesamiento inteligente con Groq
- **Seguridad**: Auditoría, rate limiting, encriptación
- **Rendimiento**: Cache inteligente, optimización de datos
- **Visualización**: Mapas interactivos, gráficos dinámicos
- **Roles**: Acceso diferenciado por tipo de usuario

## 📊 Datos

- Hospitales y centros sanitarios
- Demografía de Málaga 2025
- Indicadores de salud
- Accesibilidad sanitaria
- Servicios especializados

## 🛠️ Tecnologías

- **Frontend**: Streamlit
- **IA**: Groq API
- **Datos**: Pandas, NumPy
- **Mapas**: Folium, GeoPandas
- **Seguridad**: Bcrypt, PyJWT
- **Visualización**: Plotly, Seaborn

---

**Versión**: 2.1.0 | **Autor**: Copilot Salud Andalucía Team
