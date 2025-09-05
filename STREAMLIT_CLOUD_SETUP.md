# 🌐 Configuración Rápida para Streamlit Cloud

## 🚀 Pasos Inmediatos para Desplegar

### 1. Verificar Archivos Clave ✅
- `streamlit_app.py` - ✅ Punto de entrada configurado
- `requirements.txt` - ✅ Optimizado para cloud
- `.streamlit/config.toml` - ✅ Configuración de producción
- `data/raw/*.csv` - ✅ Datos incluidos

### 2. Variables de Entorno (Secrets) 🔑

Copia esto en Streamlit Cloud → Advanced Settings → Secrets:

```toml
GROQ_API_KEY = "tu_groq_api_key_aqui"
JWT_SECRET_KEY = "una_clave_super_segura_de_32_caracteres_o_mas"
APP_ENVIRONMENT = "production"
ENABLE_DEBUG_MODE = false
SYSTEM_NAME = "Copilot Salud Andalucía"
SYSTEM_VERSION = "2.0"
ADMIN_EMAIL = "tu-email@dominio.com"
```

### 3. Configuración de la App 📱

**En Streamlit Cloud:**
- **Repository**: `tu-usuario/copilot-salud-andalucia`
- **Branch**: `main`
- **Main file path**: `streamlit_app.py`
- **Python version**: 3.9

### 4. Obtener API Key de Groq 🤖

1. Ve a [console.groq.com](https://console.groq.com)
2. Crea cuenta gratuita
3. Ve a "API Keys"
4. Crea nueva key
5. Copia la key (empieza con `gsk-`)

### 5. Generar JWT Secret 🔒

```python
import secrets
jwt_secret = secrets.token_urlsafe(32)
print(f"JWT_SECRET_KEY = \"{jwt_secret}\"")
```

### 6. Primera Prueba 🧪

Después del despliegue, prueba:
1. **Login**: admin / admin123
2. **Dashboard**: Verificar que cargan los datos
3. **Chat IA**: Hacer una pregunta simple
4. **Mapas**: Verificar que se renderizan

### 7. URLs de Ejemplo 🌍

Tu app estará en:
- `https://copilot-salud-andalucia-tu-usuario.streamlit.app`
- O la URL personalizada que elijas

## ⚡ Solución Rápida de Problemas

### Si no carga:
```bash
# Verificar que requirements.txt está completo
pip install -r requirements.txt

# Probar localmente
streamlit run streamlit_app.py
```

### Si falta IA:
- Verificar que `GROQ_API_KEY` está en secrets
- Probar la key en [console.groq.com](https://console.groq.com)

### Si faltan datos:
```bash
# Ejecutar recolector de datos
python data_collector_2025.py
```

## 📱 Acceso Móvil

La app es responsive y funciona en móviles. Los mapas se adaptan automáticamente.

## 🔄 Actualizaciones

Cada `git push` a main despliega automáticamente. Cambios visibles en 1-2 minutos.

---

## 🎯 Checklist Mínimo

- [ ] Repo en GitHub
- [ ] App creada en Streamlit Cloud
- [ ] Secrets configurados
- [ ] App desplegada
- [ ] Login funciona
- [ ] Datos cargan

**¡Listo para producción en 10 minutos!** 🚀
