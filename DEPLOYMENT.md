# 🚀 Guía de Despliegue - Copilot Salud Andalucía

## 📋 Requisitos Previos

### Sistema
- Python 3.9 o superior
- Git instalado
- Cuenta de GitHub
- Cuenta de Streamlit Cloud (gratuita)

### Dependencias
Todas las dependencias están listadas en `requirements.txt` optimizado para cloud.

## 🌐 Despliegue en Streamlit Cloud (Recomendado)

### 1. Preparación del Repositorio en GitHub
```bash
# Asegúrate de que todos los cambios estén en GitHub
git add .
git commit -m "Preparar para despliegue en Streamlit Cloud"
git push origin main
```

### 2. Despliegue en Streamlit Cloud

#### Paso 1: Acceder a Streamlit Cloud
1. Ve a [share.streamlit.io](https://share.streamlit.io)
2. Inicia sesión con tu cuenta de GitHub
3. Haz clic en "New app"

#### Paso 2: Configurar la Aplicación
1. **Repository**: Selecciona tu repositorio `copilot-salud-andalucia`
2. **Branch**: `main` (o la rama principal)
3. **Main file path**: `streamlit_app.py`
4. **App URL** (opcional): Personaliza la URL de tu app

#### Paso 3: Configurar Variables de Entorno (Secrets)
En la sección "Advanced settings" → "Secrets", añade:

```toml
# Copia el contenido de .streamlit/secrets.toml.example y personaliza:

GROQ_API_KEY = "tu_groq_api_key_real"
JWT_SECRET_KEY = "tu_jwt_secret_super_segura_de_32_caracteres_minimo"
APP_ENVIRONMENT = "production"
ENABLE_DEBUG_MODE = false
SYSTEM_NAME = "Copilot Salud Andalucía"
SYSTEM_VERSION = "2.0"
ADMIN_EMAIL = "tu-email@dominio.com"
```

#### Paso 4: Deploy
1. Haz clic en "Deploy!"
2. La aplicación se construirá automáticamente
3. En 2-5 minutos estará disponible en tu URL personalizada

### 3. Configuración Post-Despliegue

#### Verificar el Estado
- ✅ La app debe cargar sin errores
- ✅ Los datos deben cargarse correctamente
- ✅ La autenticación debe funcionar
- ✅ Los mapas deben renderizarse

#### Usuarios por Defecto (Cambiar en Producción)
- **Admin**: admin / admin123
- **Gestor**: gestor / gestor123  
- **Analista**: analista / analista123
- **Invitado**: invitado / invitado123

⚠️ **IMPORTANTE**: Cambiar estas credenciales en producción editando `data/users.json`

## 🔧 Configuración Avanzada

### Monitoreo y Logs
Streamlit Cloud proporciona:
- Logs en tiempo real
- Métricas de uso
- Estado de la aplicación
- Reinicio automático en caso de errores

### Actualizaciones Automáticas
- Cada push a la rama principal activa un redespliegue automático
- Los cambios se reflejan en 1-2 minutos

### Gestión de Recursos
- **Memoria**: 1GB disponible (optimizada con dtypes específicos)
- **CPU**: Compartida, optimizada para análisis de datos
- **Almacenamiento**: 200MB para archivos

## 🔐 Configuración de Seguridad en Producción

### 1. Variables de Entorno Críticas
```toml
# En Streamlit Cloud Secrets:
GROQ_API_KEY = "gsk-..." # Tu API key real de Groq
JWT_SECRET_KEY = "clave-super-segura-de-al-menos-32-caracteres"
```

### 2. Cambiar Credenciales por Defecto
Edita `data/users.json` con credenciales seguras:
```json
{
  "admin": {
    "password": "nueva_password_segura_hasheada",
    "name": "Administrador del Sistema",
    "role": "admin",
    "organization": "Junta de Andalucía - Salud"
  }
}
```

### 3. Configurar HTTPS
Streamlit Cloud proporciona HTTPS automáticamente.

## 📊 Gestión de Datos

### Datos Incluidos
Los datasets están en `data/raw/` y se cargan automáticamente:
- Hospitales de Málaga 2025
- Demografía municipal
- Servicios sanitarios
- Accesibilidad territorial
- Indicadores de salud

### Actualización de Datos
Para actualizar datos:
1. Modifica los archivos CSV en `data/raw/`
2. Haz commit y push a GitHub
3. La app se actualizará automáticamente

## 🛠️ Alternativas de Despliegue

### Docker (Para Despliegues Personalizados)
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Heroku
```bash
# Crear Procfile
echo "web: streamlit run streamlit_app.py --server.port=\$PORT --server.address=0.0.0.0" > Procfile

# Deploy a Heroku
heroku create tu-app-salud-andalucia
git push heroku main
```

## 🐛 Resolución de Problemas

### Error: "ModuleNotFoundError"
- Verifica que `requirements.txt` esté actualizado
- En Streamlit Cloud: "Reboot app" desde el dashboard

### Error: "File not found" 
- Verifica que los archivos CSV estén en `data/raw/`
- Ejecuta localmente `python data_collector_2025.py` si faltan datos

### Error de Autenticación
- Verifica que `data/users.json` existe y es válido
- Comprueba la configuración de `JWT_SECRET_KEY`

### Error de Memoria
- Los dtypes están optimizados para reducir uso de memoria
- Si persiste, considera filtrar datos por fechas/regiones

### Mapas no Cargan
- Verifica que folium y streamlit-folium estén instalados
- Revisa los logs para errores específicos de mapas

## 📞 Soporte

### Logs y Debugging
- **Streamlit Cloud**: Accede a logs desde el dashboard
- **Local**: Los logs aparecen en la terminal

### Contacto
- **Desarrollador**: [Tu información de contacto]
- **Documentación**: [Link a documentación adicional]
- **Issues**: [Link al repositorio de GitHub]

---

## ✅ Checklist de Despliegue

- [ ] Repositorio subido a GitHub
- [ ] `requirements.txt` actualizado
- [ ] Configuración de Streamlit Cloud completada
- [ ] Secrets configurados correctamente
- [ ] Aplicación desplegada y funcionando
- [ ] Datos cargándose correctamente
- [ ] Autenticación funcionando
- [ ] Mapas renderizándose
- [ ] Credenciales por defecto cambiadas (producción)
- [ ] URL personalizada configurada
- [ ] Monitoreo activado

🎉 **¡Tu aplicación está lista para producción!**