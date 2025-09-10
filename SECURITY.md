# 🔒 Política de Seguridad - Copilot Salud Andalucía

## ⚠️ **IMPORTANTE - LECTURA OBLIGATORIA**

Este proyecto maneja datos sanitarios sensibles. **NUNCA** subas secretos, claves API o credenciales reales al repositorio.

## 🚫 **NUNCA SUBIR A GITHUB:**

- ❌ API Keys reales (GROQ_API_KEY)
- ❌ Claves JWT reales (JWT_SECRET_KEY)
- ❌ Contraseñas de usuarios
- ❌ Tokens de acceso
- ❌ Archivos .env con datos reales
- ❌ Archivos secrets.toml con claves reales

## ✅ **ARCHIVOS SEGUROS PARA SUBIR:**

- ✅ Archivos de código fuente
- ✅ Documentación (sin credenciales reales)
- ✅ Archivos de configuración de ejemplo
- ✅ Requirements.txt
- ✅ Archivos de test

## 🔐 **CONFIGURACIÓN SEGURA:**

### **Variables de Entorno Requeridas:**
```bash
JWT_SECRET_KEY=tu_clave_jwt_super_segura_de_64_caracteres
GROQ_API_KEY=tu_api_key_real_de_groq
SECRET_KEY=tu_clave_secreta_de_32_caracteres
```

### **Archivos de Configuración:**
- Usa `.streamlit/secrets.toml` para desarrollo local
- Configura secrets en Streamlit Cloud para producción
- NUNCA commitees archivos con claves reales

## 🛡️ **MEJORES PRÁCTICAS:**

1. **Usar variables de entorno** para todos los secretos
2. **Validar configuración** al inicio de la aplicación
3. **Encriptar datos sensibles** antes de almacenar
4. **Auditar logs** regularmente
5. **Rotar claves** periódicamente

## 🚨 **EN CASO DE EXPOSICIÓN:**

Si accidentalmente subes un secreto:

1. **Inmediatamente** revoca la clave expuesta
2. **Genera una nueva** clave de reemplazo
3. **Actualiza** todos los entornos
4. **Revisa logs** para detectar uso no autorizado

## 📞 **CONTACTO DE SEGURIDAD:**

Para reportar vulnerabilidades de seguridad:
- Email: [email_protegido]
- No uses issues públicos para reportar problemas de seguridad

---
**Última actualización**: 10/09/2025
**Versión**: 2.1
