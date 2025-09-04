# 🚀 Guía de Despliegue - Copilot Salud Andalucía

## 🌐 Despliegue en Vercel

### 📋 Pasos para Desplegar:

1. **Crear cuenta en Vercel**: Ve a [vercel.com](https://vercel.com) y regístrate
2. **Conectar con GitHub**: Autoriza Vercel para acceder a tus repositorios
3. **Importar proyecto**: Selecciona el repositorio `copilot-salud-andalucia`
4. **Configurar variables de entorno** (CRÍTICO):

### 🔑 Variables de Entorno Requeridas:

```bash
GROQ_API_KEY=tu_clave_de_groq_aqui
JWT_SECRET=tu_clave_secreta_jwt_muy_segura
STREAMLIT_SERVER_HEADLESS=true
STREAMLIT_SERVER_PORT=8501
STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
```

### ⚙️ Configuración de Build:

- **Framework Preset**: Streamlit
- **Build Command**: `pip install -r requirements.txt`
- **Output Directory**: Dejar vacío
- **Install Command**: `pip install -r requirements.txt`

### 🔧 Configuración Avanzada:

- **Runtime**: Python 3.9
- **Region**: Washington, D.C. (iad1) - recomendado
- **Function Timeout**: 30 segundos

### 🚨 Notas Importantes:

1. **Clave de Groq**: Obtén tu clave API gratuita en [console.groq.com](https://console.groq.com)
2. **JWT Secret**: Genera una clave segura de al menos 32 caracteres
3. **Primer despliegue**: Puede tomar 5-10 minutos
4. **Límites gratuitos**: Vercel permite 100GB de ancho de banda mensual

### 🌍 URL de Acceso:

Una vez desplegado, tu aplicación estará disponible en:
`https://tu-proyecto.vercel.app`

### 👥 Usuarios de Demostración:

| Rol | Usuario | Contraseña |
|-----|---------|------------|
| Admin | `admin` | `admin123` |
| Gestor | `gestor.malaga` | `gestor123` |
| Analista | `analista.datos` | `analista123` |
| Invitado | `demo` | `demo123` |

### 🔧 Solución de Problemas:

- **Error de build**: Verifica que requirements.txt esté completo
- **Error de IA**: Confirma que GROQ_API_KEY esté configurada
- **Error de autenticación**: Verifica que JWT_SECRET esté configurada
- **Timeout**: La primera carga puede ser lenta, espera hasta 30 segundos

### 📞 Soporte:

Si encuentras problemas, revisa los logs en el dashboard de Vercel o contacta al desarrollador.
