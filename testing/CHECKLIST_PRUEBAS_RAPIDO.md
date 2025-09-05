# ✅ CHECKLIST RÁPIDO DE PRUEBAS - COPILOT SALUD

**Guía de verificación rápida para PC, Móviles y Tablets**

---

## 🚀 **PRUEBAS CRÍTICAS (30 MINUTOS)**

### **🖥️ PC - Pruebas Esenciales**
- [ ] **Login funciona** (admin/admin123, gestor.malaga/gestor123)
- [ ] **Dashboard carga** completamente en < 5 segundos
- [ ] **Chat IA responde** en < 10 segundos (requiere GROQ_API_KEY)
- [ ] **Mapas cargan** y son interactivos
- [ ] **Gráficos Plotly** funcionan (hover, zoom)
- [ ] **Temas por rol** se aplican correctamente
- [ ] **Logout** funciona correctamente

### **📱 MÓVIL - Pruebas Esenciales**
- [ ] **Responsive** - No scroll horizontal
- [ ] **Login táctil** funciona correctamente
- [ ] **Sidebar colapsable** en móviles
- [ ] **Botones suficientemente grandes** (>44px)
- [ ] **Gráficos interactivos** con gestos táctiles
- [ ] **Texto legible** sin zoom necesario
- [ ] **Carga rápida** en 4G/WiFi

### **📟 TABLET - Pruebas Esenciales**
- [ ] **Layout intermedio** optimizado
- [ ] **Mapas con gestos** (pinch-zoom, pan)
- [ ] **Orientación portrait/landscape** funciona
- [ ] **Touch + teclado** (si disponible)
- [ ] **Multitarea** no rompe la app
- [ ] **Performance fluida** sin lag

---

## 🔒 **SEGURIDAD BÁSICA (15 MINUTOS)**

### **Autenticación**
- [ ] **Credenciales incorrectas** son rechazadas
- [ ] **Diferentes roles** tienen acceso diferenciado
- [ ] **Sesiones expiran** automáticamente
- [ ] **Logout** invalida la sesión

### **Control de Acceso**
- [ ] **Invitado**: No accede a IA ni planificación
- [ ] **Analista**: No accede a gestión de usuarios
- [ ] **Gestor**: No accede a análisis de equidad
- [ ] **Admin**: Acceso completo a todo

---

## ⚡ **RENDIMIENTO BÁSICO (10 MINUTOS)**

### **Tiempos de Carga**
- [ ] **Página inicial**: < 5 segundos
- [ ] **Dashboard**: < 3 segundos después del login
- [ ] **Chat IA**: < 10 segundos respuesta
- [ ] **Mapas**: < 8 segundos carga completa
- [ ] **Reportes**: < 5 segundos generación

### **Usabilidad**
- [ ] **No hay errores** en consola del navegador
- [ ] **Scroll fluido** en todas las secciones
- [ ] **Botones responden** inmediatamente
- [ ] **Transiciones suaves** sin saltos

---

## 🎨 **UI/UX BÁSICO (10 MINUTOS)**

### **Consistencia Visual**
- [ ] **Colores por rol** aplicados correctamente
- [ ] **Tipografías** consistentes (Inter, Poppins)
- [ ] **Iconos y emojis** visibles y coherentes
- [ ] **Espaciados** uniformes

### **Feedback Visual**
- [ ] **Estados de carga** visibles
- [ ] **Mensajes éxito/error** claros
- [ ] **Hover effects** en botones
- [ ] **Transiciones** funcionan

---

## 🧪 **FUNCIONALIDADES CLAVE (20 MINUTOS)**

### **Dashboard**
- [ ] **Métricas actualizadas** y correctas
- [ ] **Gráficos interactivos** funcionan
- [ ] **Personalización por rol** visible
- [ ] **Sidebar** con navegación correcta

### **Chat IA** (Solo si GROQ_API_KEY configurada)
- [ ] **Consulta básica**: "¿Cuántos hospitales hay?"
- [ ] **Respuesta coherente** y basada en datos
- [ ] **Interface responsive** en móviles
- [ ] **Historial** se mantiene durante sesión

### **Mapas Épicos**
- [ ] **Mapa básico** carga correctamente
- [ ] **Marcadores** visibles y clickeables
- [ ] **Zoom y pan** funcionan
- [ ] **Leyenda** visible y legible
- [ ] **Gestos táctiles** en móvil/tablet

### **Reportes**
- [ ] **Reporte básico** se genera
- [ ] **Formato correcto** y legible
- [ ] **Gráficos integrados** correctamente
- [ ] **Acceso por rol** respetado

---

## 🔧 **CONFIGURACIÓN PREVIA**

### **Variables de Entorno Necesarias**
```bash
# Crear archivo .env
GROQ_API_KEY=tu_clave_groq_aqui
JWT_SECRET=tu_clave_secreta_jwt
```

### **Datos de Prueba**
```bash
# Ejecutar antes de las pruebas
python data_collector_2025.py
```

### **Usuarios de Prueba**
| Rol | Usuario | Contraseña | Acceso |
|-----|---------|------------|--------|
| Admin | admin | admin123 | Completo |
| Gestor | gestor.malaga | gestor123 | Gestión |
| Analista | analista.datos | analista123 | Análisis |
| Invitado | demo | demo123 | Básico |

---

## 📱 **DISPOSITIVOS RECOMENDADOS PARA PRUEBAS**

### **PC/Escritorio**
- **Windows**: Chrome, Firefox, Edge
- **macOS**: Chrome, Safari, Firefox
- **Resoluciones**: 1920x1080, 1366x768

### **Móviles**
- **iPhone**: Safari, Chrome (375x667, 414x896)
- **Android**: Chrome, Firefox (360x640, 412x915)

### **Tablets**
- **iPad**: Safari, Chrome (1024x768, 2048x1536)
- **Android**: Chrome (1280x800, 1920x1200)

---

## 🐛 **PROBLEMAS COMUNES Y SOLUCIONES**

### **Chat IA no responde**
- ✅ Verificar GROQ_API_KEY en .env
- ✅ Comprobar conexión a internet
- ✅ Revisar logs de error en consola

### **Mapas no cargan**
- ✅ Verificar librerías Folium instaladas
- ✅ Comprobar datos de geolocalización
- ✅ Revisar permisos de acceso por rol

### **Gráficos no aparecen**
- ✅ Verificar Plotly instalado correctamente
- ✅ Comprobar datasets cargados
- ✅ Revisar JavaScript habilitado

### **Login no funciona**
- ✅ Verificar archivo data/users.json existe
- ✅ Comprobar credenciales correctas
- ✅ Revisar JWT_SECRET configurado

### **Responsive no funciona**
- ✅ Verificar CSS cargado correctamente
- ✅ Comprobar viewport meta tag
- ✅ Revisar breakpoints en CSS

---

## 📊 **CRITERIOS DE APROBACIÓN**

### **✅ Pruebas APROBADAS si:**
- **Funcionalidad**: 95%+ de casos pasan
- **Rendimiento**: Cargas < 5s en PC, < 8s en móvil
- **Compatibilidad**: Funciona en navegadores principales
- **Seguridad**: Control de acceso funciona correctamente
- **Responsividad**: UI adaptada en todos los dispositivos

### **❌ Pruebas FALLAN si:**
- Login no funciona en cualquier dispositivo
- Chat IA no responde (con API configurada)
- Mapas no cargan o no son interactivos
- UI rota en móviles/tablets
- Errores críticos en consola

---

## 🚀 **EJECUCIÓN RÁPIDA**

### **Orden Recomendado:**
1. **🖥️ PC Desktop** (15 min) - Funcionalidad base
2. **📱 Móvil** (10 min) - Responsive crítico  
3. **📟 Tablet** (5 min) - Layout intermedio
4. **🔒 Seguridad** (5 min) - Roles y permisos
5. **⚡ Performance** (5 min) - Tiempos de carga

### **Comando de Inicio:**
```bash
# Terminal/PowerShell
cd copilot-salud-andalucia
streamlit run app.py
```

### **URL de Acceso:**
```
http://localhost:8501
```

---

**⏱️ Tiempo Total Estimado: 40-60 minutos**

**🎯 Objetivo: Verificación rápida de funcionalidad en todos los dispositivos**

---

*Checklist creado para Copilot Salud Andalucía - Testing Rápido*
