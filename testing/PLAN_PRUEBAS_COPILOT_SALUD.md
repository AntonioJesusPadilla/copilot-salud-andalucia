# 🧪 PLAN DE PRUEBAS - COPILOT SALUD ANDALUCÍA

**Sistema Inteligente de Análisis Sanitario con IA para la Provincia de Málaga**

---

## 📋 **INFORMACIÓN DEL DOCUMENTO**

- **Proyecto**: Copilot Salud Andalucía
- **Versión**: 1.0
- **Fecha**: Enero 2025
- **Autor**: Antonio Jesús Padilla
- **Tipo de Aplicación**: Web (Streamlit)
- **Plataformas Objetivo**: PC (Escritorio), Tablets, Móviles

---

## 🎯 **OBJETIVOS DEL PLAN DE PRUEBAS**

### **Objetivos Principales**
1. **Funcionalidad Completa**: Verificar que todas las funcionalidades trabajen correctamente
2. **Compatibilidad Multi-Dispositivo**: Asegurar funcionamiento en PC, tablets y móviles
3. **Experiencia de Usuario**: Garantizar una UX óptima en todos los dispositivos
4. **Rendimiento**: Validar tiempos de respuesta aceptables
5. **Seguridad**: Verificar el sistema de autenticación y autorización
6. **Responsividad**: Confirmar que el diseño se adapte correctamente

### **Criterios de Éxito**
- ✅ **100% de funcionalidades operativas** en todos los dispositivos
- ✅ **Tiempo de carga < 5 segundos** en conexiones normales
- ✅ **UI/UX consistente** en diferentes resoluciones
- ✅ **Seguridad robusta** sin vulnerabilidades críticas
- ✅ **Accesibilidad** según estándares web

---

## 🖥️ **MATRIZ DE COMPATIBILIDAD**

### **Dispositivos y Navegadores**

| Dispositivo | Sistema Operativo | Navegadores | Resoluciones | Prioridad |
|-------------|------------------|-------------|--------------|-----------|
| **PC Escritorio** | Windows 10/11 | Chrome, Firefox, Edge | 1920x1080, 1366x768 | 🔴 Alta |
| **PC Escritorio** | macOS | Chrome, Safari, Firefox | 1920x1080, 2560x1440 | 🟡 Media |
| **PC Escritorio** | Linux Ubuntu | Chrome, Firefox | 1920x1080, 1366x768 | 🟢 Baja |
| **Tablet** | iPad (iOS) | Safari, Chrome | 1024x768, 2048x1536 | 🔴 Alta |
| **Tablet** | Android | Chrome, Firefox | 1280x800, 1920x1200 | 🔴 Alta |
| **Móvil** | iPhone (iOS) | Safari, Chrome | 375x667, 414x896 | 🔴 Alta |
| **Móvil** | Android | Chrome, Firefox | 360x640, 412x915 | 🔴 Alta |

### **Breakpoints de Responsividad**
- **Desktop**: > 1024px
- **Tablet**: 768px - 1024px  
- **Mobile Large**: 480px - 768px
- **Mobile Small**: < 480px

---

## 🧪 **TIPOS DE PRUEBAS**

### **1. PRUEBAS FUNCIONALES**
- Verificación de todas las características principales
- Flujos de usuario completos
- Integración entre módulos
- Validación de datos

### **2. PRUEBAS DE COMPATIBILIDAD**
- Cross-browser testing
- Cross-platform testing  
- Diferentes versiones de navegadores
- Compatibilidad con dispositivos

### **3. PRUEBAS DE RESPONSIVIDAD**
- Adaptación de layouts
- Legibilidad en diferentes tamaños
- Usabilidad en touch screens
- Orientación portrait/landscape

### **4. PRUEBAS DE RENDIMIENTO**
- Tiempos de carga
- Uso de memoria
- Optimización de recursos
- Escalabilidad

### **5. PRUEBAS DE SEGURIDAD**
- Sistema de autenticación
- Control de acceso por roles
- Validación de entrada
- Protección de datos

### **6. PRUEBAS DE USABILIDAD**
- Navegación intuitiva
- Accesibilidad
- Experiencia de usuario
- Feedback visual

---

## 📱 **CASOS DE PRUEBA POR DISPOSITIVO**

## **🖥️ PRUEBAS EN PC (ESCRITORIO)**

### **TC-PC-001: Carga Inicial de la Aplicación**
- **Objetivo**: Verificar que la aplicación cargue correctamente
- **Pasos**:
  1. Abrir navegador y navegar a la URL
  2. Verificar tiempo de carga < 5 segundos
  3. Confirmar que todos los elementos se rendericen
- **Resultado Esperado**: Página de login visible y funcional
- **Dispositivos**: Todos los PC
- **Navegadores**: Chrome, Firefox, Edge, Safari

### **TC-PC-002: Sistema de Autenticación**
- **Objetivo**: Validar login con diferentes roles
- **Pasos**:
  1. Introducir credenciales de administrador (admin/admin123)
  2. Verificar acceso a todas las funcionalidades
  3. Repetir para gestor, analista e invitado
- **Resultado Esperado**: Acceso según permisos del rol
- **Roles a Probar**: Admin, Gestor, Analista, Invitado

### **TC-PC-003: Dashboard Principal**
- **Objetivo**: Verificar visualización de métricas y KPIs
- **Pasos**:
  1. Acceder al dashboard principal
  2. Verificar carga de todas las métricas
  3. Confirmar interactividad de gráficos
- **Resultado Esperado**: Dashboard completo y funcional
- **Resoluciones**: 1920x1080, 1366x768

### **TC-PC-004: Chat IA (Groq)**
- **Objetivo**: Validar funcionalidad del asistente IA
- **Pasos**:
  1. Acceder a la sección de Chat IA
  2. Realizar consulta: "Analiza la capacidad hospitalaria"
  3. Verificar respuesta coherente y tiempo < 10s
- **Resultado Esperado**: Respuesta IA relevante y rápida
- **Prerequisitos**: GROQ_API_KEY configurada

### **TC-PC-005: Mapas Interactivos**
- **Objetivo**: Verificar funcionalidad de mapas épicos
- **Pasos**:
  1. Acceder a sección de mapas
  2. Probar diferentes tipos de mapas según rol
  3. Verificar interactividad (zoom, click, tooltips)
- **Resultado Esperado**: Mapas cargando y totalmente interactivos
- **Mapas a Probar**: Hospitales, Demografía, Accesibilidad

### **TC-PC-006: Generación de Reportes**
- **Objetivo**: Validar creación de reportes por rol
- **Pasos**:
  1. Seleccionar tipo de reporte según permisos
  2. Generar reporte ejecutivo/operativo/analítico
  3. Verificar contenido y formato
- **Resultado Esperado**: Reporte generado correctamente
- **Tipos**: Ejecutivo, Infraestructura, Demográfico, Equidad

### **TC-PC-007: Planificación Estratégica**
- **Objetivo**: Verificar herramientas de planificación
- **Pasos**:
  1. Acceder a planificación (solo admin/gestor)
  2. Probar análisis de ubicaciones
  3. Verificar proyecciones de demanda
- **Resultado Esperado**: Herramientas funcionando correctamente
- **Roles**: Solo Administrador y Gestor

---

## **📱 PRUEBAS EN MÓVILES**

### **TC-MOV-001: Responsividad General**
- **Objetivo**: Verificar adaptación a pantallas móviles
- **Pasos**:
  1. Acceder desde móvil (portrait y landscape)
  2. Verificar que no haya scroll horizontal
  3. Confirmar legibilidad de texto
- **Resultado Esperado**: UI perfectamente adaptada
- **Resoluciones**: 375x667, 414x896, 360x640

### **TC-MOV-002: Navegación Touch**
- **Objetivo**: Validar interacción táctil
- **Pasos**:
  1. Probar navegación con gestos táctiles
  2. Verificar botones suficientemente grandes (44px mín.)
  3. Confirmar scroll suave en listas/tablas
- **Resultado Esperado**: Navegación táctil fluida
- **Elementos**: Botones, menús, gráficos interactivos

### **TC-MOV-003: Sidebar Responsive**
- **Objetivo**: Verificar comportamiento del sidebar
- **Pasos**:
  1. Acceder desde móvil
  2. Verificar que sidebar se colapse automáticamente
  3. Probar apertura/cierre del menú lateral
- **Resultado Esperado**: Sidebar adaptado para móviles
- **Estados**: Collapsed, Expanded, Auto-hide

### **TC-MOV-004: Gráficos en Móviles**
- **Objetivo**: Validar visualización de gráficos Plotly
- **Pasos**:
  1. Acceder a dashboards con gráficos
  2. Verificar que gráficos se redimensionen
  3. Probar interactividad (zoom, pan, hover)
- **Resultado Esperado**: Gráficos totalmente funcionales
- **Tipos**: Barras, Líneas, Mapas de calor, Scatter

### **TC-MOV-005: Formularios y Entrada de Datos**
- **Objetivo**: Verificar usabilidad de formularios
- **Pasos**:
  1. Probar login en móvil
  2. Verificar entrada de texto en chat IA
  3. Confirmar selectores y dropdowns
- **Resultado Esperado**: Formularios usables en móvil
- **Elementos**: Inputs, selects, textareas, buttons

### **TC-MOV-006: Performance en Móviles**
- **Objetivo**: Validar rendimiento en dispositivos móviles
- **Pasos**:
  1. Medir tiempo de carga inicial
  2. Verificar fluidez de scrolling
  3. Monitorear uso de memoria
- **Resultado Esperado**: Rendimiento aceptable (< 8s carga)
- **Métricas**: First Paint, Largest Contentful Paint

---

## **📟 PRUEBAS EN TABLETS**

### **TC-TAB-001: Layout Intermedio**
- **Objetivo**: Verificar adaptación a resolución tablet
- **Pasos**:
  1. Acceder desde tablet (1024x768, 1280x800)
  2. Verificar que layout use espacio eficientemente
  3. Confirmar que no se vea "estirado"
- **Resultado Esperado**: Layout optimizado para tablet
- **Orientaciones**: Portrait y Landscape

### **TC-TAB-002: Interacción Híbrida**
- **Objetivo**: Validar uso con touch y teclado/mouse
- **Pasos**:
  1. Probar navegación táctil
  2. Conectar teclado/mouse y verificar funcionalidad
  3. Alternar entre modos de interacción
- **Resultado Esperado**: Soporte completo para ambos modos
- **Dispositivos**: iPad, Surface, Android tablets

### **TC-TAB-003: Mapas en Tablets**
- **Objetivo**: Verificar mapas interactivos en tablet
- **Pasos**:
  1. Acceder a mapas épicos desde tablet
  2. Probar gestos de zoom (pinch-to-zoom)
  3. Verificar tooltips y popups
- **Resultado Esperado**: Mapas completamente funcionales
- **Gestos**: Zoom, Pan, Tap, Long-press

### **TC-TAB-004: Multitarea**
- **Objetivo**: Validar comportamiento en multitarea
- **Pasos**:
  1. Abrir aplicación en modo split-screen
  2. Cambiar entre apps y regresar
  3. Verificar que estado se mantenga
- **Resultado Esperado**: Estado preservado correctamente
- **Escenarios**: Split-screen, App switching

---

## 🔒 **PRUEBAS DE SEGURIDAD**

### **TC-SEC-001: Autenticación Robusta**
- **Objetivo**: Verificar seguridad del login
- **Pasos**:
  1. Intentar login con credenciales incorrectas
  2. Verificar bloqueo tras múltiples intentos fallidos
  3. Confirmar encriptación de contraseñas
- **Resultado Esperado**: Sistema seguro contra ataques
- **Ataques**: Brute force, SQL injection

### **TC-SEC-002: Control de Acceso por Roles**
- **Objetivo**: Validar RBAC (Role-Based Access Control)
- **Pasos**:
  1. Login como diferentes roles
  2. Intentar acceso a funciones restringidas
  3. Verificar mensajes de "acceso denegado"
- **Resultado Esperado**: Acceso estrictamente controlado
- **Roles**: Admin, Gestor, Analista, Invitado

### **TC-SEC-003: Sesiones y Tokens**
- **Objetivo**: Verificar manejo seguro de sesiones
- **Pasos**:
  1. Verificar expiración automática de sesiones
  2. Probar logout correcto
  3. Confirmar invalidación de tokens
- **Resultado Esperado**: Gestión segura de sesiones
- **Elementos**: JWT tokens, Session timeout

### **TC-SEC-004: Validación de Entrada**
- **Objetivo**: Verificar sanitización de inputs
- **Pasos**:
  1. Introducir caracteres especiales en formularios
  2. Probar inyección de código JavaScript
  3. Verificar manejo de archivos maliciosos
- **Resultado Esperado**: Inputs correctamente sanitizados
- **Vectores**: XSS, Code injection, File upload

---

## ⚡ **PRUEBAS DE RENDIMIENTO**

### **TC-PERF-001: Tiempo de Carga Inicial**
- **Objetivo**: Medir tiempos de carga de la aplicación
- **Métricas**:
  - **PC**: < 3 segundos
  - **Tablet**: < 5 segundos  
  - **Móvil**: < 8 segundos
- **Herramientas**: Chrome DevTools, Lighthouse
- **Condiciones**: WiFi, 4G, 3G

### **TC-PERF-002: Carga de Datasets**
- **Objetivo**: Verificar rendimiento con datos reales
- **Pasos**:
  1. Cargar datasets completos (hospitales, demografía, etc.)
  2. Medir tiempo de procesamiento
  3. Verificar uso de memoria
- **Resultado Esperado**: Carga eficiente sin bloqueos
- **Datasets**: 5 archivos CSV, ~1000 registros total

### **TC-PERF-003: Respuesta del Chat IA**
- **Objetivo**: Validar tiempos de respuesta de Groq
- **Pasos**:
  1. Realizar consultas complejas al chat IA
  2. Medir tiempo de respuesta
  3. Verificar que UI no se bloquee
- **Resultado Esperado**: Respuesta < 10 segundos
- **Consultas**: Análisis demográfico, planificación, reportes

### **TC-PERF-004: Renderizado de Gráficos**
- **Objetivo**: Medir rendimiento de visualizaciones
- **Pasos**:
  1. Generar gráficos complejos con Plotly
  2. Medir tiempo de renderizado
  3. Probar interactividad sin lag
- **Resultado Esperado**: Renderizado fluido < 2 segundos
- **Gráficos**: Scatter plots, mapas de calor, 3D

---

## 🎨 **PRUEBAS DE UI/UX**

### **TC-UI-001: Consistencia Visual**
- **Objetivo**: Verificar coherencia del diseño
- **Elementos a Verificar**:
  - ✅ Colores según tema del rol
  - ✅ Tipografías (Inter, Poppins)
  - ✅ Espaciados y márgenes
  - ✅ Iconos y emojis consistentes
- **Dispositivos**: Todos
- **Resoluciones**: Todas las soportadas

### **TC-UI-002: Temas por Rol**
- **Objetivo**: Validar personalización visual por rol
- **Temas a Probar**:
  - 🔴 **Admin**: Azul ejecutivo (#1a365d)
  - 🔵 **Gestor**: Azul gestión (#2b6cb0)  
  - 🟢 **Analista**: Verde analítico (#059669)
  - 🟣 **Invitado**: Gris público (#6b7280)
- **Elementos**: Headers, sidebar, botones, métricas

### **TC-UI-003: Feedback Visual**
- **Objetivo**: Verificar retroalimentación al usuario
- **Elementos**:
  - ✅ Estados de carga (spinners)
  - ✅ Mensajes de éxito/error
  - ✅ Hover effects en botones
  - ✅ Transiciones suaves
- **Interacciones**: Clicks, hovers, loading states

### **TC-UI-004: Accesibilidad**
- **Objetivo**: Validar cumplimiento de estándares WCAG
- **Criterios**:
  - ✅ Contraste de colores suficiente
  - ✅ Navegación con teclado
  - ✅ Textos alternativos en imágenes
  - ✅ Etiquetas en formularios
- **Herramientas**: axe-core, WAVE, Lighthouse

---

## 📊 **PLAN DE EJECUCIÓN**

### **Fase 1: Preparación (Día 1)**
- ✅ Configurar entornos de prueba
- ✅ Preparar dispositivos y navegadores
- ✅ Configurar herramientas de testing
- ✅ Validar datos de prueba

### **Fase 2: Pruebas Funcionales (Días 2-3)**
- ✅ Ejecutar casos de prueba PC
- ✅ Validar todas las funcionalidades principales
- ✅ Probar integración entre módulos
- ✅ Verificar flujos de usuario completos

### **Fase 3: Pruebas de Compatibilidad (Días 4-5)**
- ✅ Testing en múltiples navegadores
- ✅ Pruebas en diferentes dispositivos
- ✅ Validación de responsividad
- ✅ Testing de rendimiento

### **Fase 4: Pruebas Móviles y Tablets (Días 6-7)**
- ✅ Casos de prueba específicos para móviles
- ✅ Validación en tablets
- ✅ Pruebas de usabilidad táctil
- ✅ Verificación de layouts responsivos

### **Fase 5: Pruebas de Seguridad (Día 8)**
- ✅ Testing de autenticación
- ✅ Validación de control de acceso
- ✅ Pruebas de penetración básicas
- ✅ Verificación de manejo de sesiones

### **Fase 6: Documentación y Cierre (Día 9)**
- ✅ Documentar resultados
- ✅ Crear reporte de bugs encontrados
- ✅ Definir criterios de aceptación
- ✅ Entrega final del reporte

---

## 🐛 **GESTIÓN DE DEFECTOS**

### **Clasificación de Severidad**

| Nivel | Descripción | Tiempo Resolución | Ejemplo |
|-------|-------------|-------------------|---------|
| **🔴 Crítico** | Bloquea funcionalidad principal | 24 horas | Login no funciona |
| **🟡 Alto** | Funcionalidad importante afectada | 48 horas | Chat IA sin respuesta |
| **🟢 Medio** | Problema menor de funcionalidad | 1 semana | Gráfico no se actualiza |
| **⚪ Bajo** | Problema cosmético o menor | 2 semanas | Color incorrecto |

### **Proceso de Reporte**
1. **Detección**: Identificar y reproducir el bug
2. **Documentación**: Crear reporte detallado con pasos
3. **Clasificación**: Asignar severidad y prioridad
4. **Asignación**: Enviar al equipo de desarrollo
5. **Seguimiento**: Monitorear resolución
6. **Verificación**: Confirmar corrección
7. **Cierre**: Marcar como resuelto

---

## 📈 **MÉTRICAS DE CALIDAD**

### **KPIs de Testing**
- **Cobertura de Pruebas**: > 95%
- **Tasa de Éxito**: > 90%
- **Bugs Críticos**: 0
- **Tiempo Promedio de Carga**: < 5s
- **Compatibilidad**: 100% en navegadores principales

### **Criterios de Aceptación**
- ✅ **Funcionalidad**: Todas las características operativas
- ✅ **Rendimiento**: Tiempos dentro de límites establecidos
- ✅ **Compatibilidad**: Funciona en todos los dispositivos objetivo
- ✅ **Seguridad**: Sin vulnerabilidades críticas o altas
- ✅ **Usabilidad**: UX consistente y intuitiva

---

## 🛠️ **HERRAMIENTAS DE TESTING**

### **Testing Manual**
- **Navegadores**: Chrome, Firefox, Safari, Edge
- **Dispositivos**: PC, tablets, smartphones reales
- **Emuladores**: Chrome DevTools, Firefox Responsive Mode

### **Testing Automatizado**
- **Selenium**: Automatización de navegador
- **Pytest**: Testing de backend Python
- **Lighthouse**: Auditoría de rendimiento y accesibilidad
- **axe-core**: Testing de accesibilidad

### **Herramientas de Rendimiento**
- **Chrome DevTools**: Profiling y network analysis
- **GTmetrix**: Análisis de velocidad web
- **WebPageTest**: Testing de rendimiento detallado

### **Testing de Seguridad**
- **OWASP ZAP**: Scanner de vulnerabilidades
- **Burp Suite**: Testing de seguridad web
- **JWT.io**: Validación de tokens JWT

---

## 📋 **ENTREGABLES**

### **Documentos de Salida**
1. **📊 Reporte Ejecutivo de Pruebas**
   - Resumen de resultados
   - Métricas de calidad
   - Recomendaciones

2. **🐛 Reporte Detallado de Bugs**
   - Lista completa de defectos encontrados
   - Clasificación por severidad
   - Pasos de reproducción

3. **📱 Matriz de Compatibilidad**
   - Resultados por dispositivo/navegador
   - Capturas de pantalla
   - Notas específicas

4. **⚡ Reporte de Rendimiento**
   - Métricas de velocidad
   - Análisis de carga
   - Recomendaciones de optimización

5. **🔒 Reporte de Seguridad**
   - Vulnerabilidades encontradas
   - Nivel de riesgo
   - Medidas correctivas

---

## 🎯 **CASOS DE PRUEBA ESPECÍFICOS POR FUNCIONALIDAD**

### **AUTENTICACIÓN Y ROLES**

#### **TC-AUTH-001: Login Administrador**
```
Prerrequisitos: Aplicación desplegada y accesible
Pasos:
1. Navegar a la URL de la aplicación
2. Introducir usuario: admin
3. Introducir contraseña: admin123
4. Hacer click en "Iniciar Sesión"
5. Verificar redirección al dashboard de administrador

Resultado Esperado:
- Login exitoso
- Dashboard con tema azul ejecutivo (#1a365d)
- Acceso a todas las funcionalidades
- Mensaje de bienvenida personalizado

Dispositivos: PC, Tablet, Móvil
Navegadores: Chrome, Firefox, Safari, Edge
```

#### **TC-AUTH-002: Control de Acceso por Roles**
```
Prerrequisitos: Usuario logueado como "invitado"
Pasos:
1. Intentar acceder a "Gestión de Usuarios"
2. Intentar acceder a "Chat IA"
3. Intentar acceder a "Planificación Estratégica"
4. Verificar mensajes de acceso denegado

Resultado Esperado:
- Acceso bloqueado a funciones restringidas
- Mensajes claros de "Permisos insuficientes"
- Redirección a funciones permitidas

Roles a Probar: Invitado, Analista, Gestor
```

### **CHAT IA Y PROCESAMIENTO**

#### **TC-AI-001: Consulta Básica al Chat IA**
```
Prerrequisitos: Usuario con permisos de IA (admin/gestor/analista)
Pasos:
1. Acceder a la sección "Chat IA"
2. Introducir consulta: "¿Cuál es la capacidad total de camas en Málaga?"
3. Enviar consulta
4. Esperar respuesta (máximo 10 segundos)
5. Verificar que la respuesta sea coherente y basada en datos

Resultado Esperado:
- Respuesta en < 10 segundos
- Información basada en datasets reales
- Formato JSON bien estructurado
- Posible sugerencia de visualización

Dispositivos: Todos
API: Requiere GROQ_API_KEY configurada
```

#### **TC-AI-002: Chat IA en Móviles**
```
Prerrequisitos: Acceso desde dispositivo móvil
Pasos:
1. Acceder al chat desde móvil
2. Verificar que el teclado virtual no oculte el chat
3. Introducir consulta larga (>100 caracteres)
4. Verificar scroll automático
5. Probar copiar/pegar respuesta

Resultado Esperado:
- Interface adaptada para móvil
- Teclado no interfiere con la visualización
- Scroll fluido en conversación
- Texto seleccionable y copiable

Resoluciones: 375x667, 414x896, 360x640
```

### **MAPAS INTERACTIVOS**

#### **TC-MAPS-001: Carga de Mapa Épico Completo**
```
Prerrequisitos: Usuario administrador
Pasos:
1. Acceder a "Mapas Épicos"
2. Seleccionar "🌟 Mapa Completo Épico"
3. Esperar carga completa (máximo 8 segundos)
4. Verificar todas las capas visibles:
   - Hospitales (marcadores rojos)
   - Municipios (áreas coloreadas)
   - Rutas de acceso (líneas)
5. Probar interactividad (zoom, click en marcadores)

Resultado Esperado:
- Mapa carga completamente
- Todas las capas visibles y diferenciadas
- Leyenda visible en esquina inferior izquierda
- Tooltips informativos al hacer hover
- Zoom y pan funcionando correctamente

Solo para: Administrador
Librerías: Folium, Streamlit-Folium
```

#### **TC-MAPS-002: Mapas en Dispositivos Táctiles**
```
Prerrequisitos: Acceso desde tablet o móvil
Pasos:
1. Acceder a mapas desde dispositivo táctil
2. Probar gestos de zoom (pinch-to-zoom)
3. Probar arrastre del mapa (pan)
4. Tocar marcadores para ver popups
5. Verificar que leyenda sea legible

Resultado Esperado:
- Gestos táctiles responden correctamente
- Zoom suave y preciso
- Popups se abren con tap único
- Leyenda adaptada al tamaño de pantalla
- No hay interferencia con scroll de página

Dispositivos: iPad, Android tablets, smartphones
Gestos: Tap, pinch-zoom, pan, long-press
```

### **DASHBOARDS Y VISUALIZACIONES**

#### **TC-DASH-001: Dashboard Personalizado por Rol**
```
Prerrequisitos: Usuarios de diferentes roles
Pasos:
1. Login como Administrador
   - Verificar tema azul ejecutivo
   - Confirmar métricas estratégicas visibles
2. Login como Gestor
   - Verificar tema azul gestión
   - Confirmar métricas operativas
3. Login como Analista
   - Verificar tema verde analítico
   - Confirmar correlaciones estadísticas
4. Login como Invitado
   - Verificar tema gris público
   - Confirmar solo información básica

Resultado Esperado:
- Cada rol ve su dashboard personalizado
- Colores y temas específicos aplicados
- Métricas relevantes según permisos
- Headers personalizados por rol

Roles: Admin, Gestor, Analista, Invitado
```

#### **TC-DASH-002: Gráficos Interactivos Plotly**
```
Prerrequisitos: Dashboard cargado con datos
Pasos:
1. Localizar gráfico de barras (capacidad hospitalaria)
2. Hacer hover sobre barras individuales
3. Verificar tooltip con información detallada
4. Probar zoom en gráfico
5. Verificar botones de control (reset, pan, zoom)
6. Cambiar filtros si están disponibles

Resultado Esperado:
- Tooltips informativos y precisos
- Zoom funciona correctamente
- Controles de Plotly visibles y funcionales
- Gráficos se actualizan con filtros
- Rendimiento fluido sin lag

Gráficos: Barras, líneas, scatter, mapas de calor
Controles: Zoom, pan, reset, download
```

### **REPORTES Y ANÁLISIS**

#### **TC-REP-001: Generación de Reporte Ejecutivo**
```
Prerrequisitos: Usuario administrador o gestor
Pasos:
1. Acceder a sección "Reportes"
2. Seleccionar "Reporte Ejecutivo"
3. Verificar tiempo de generación < 5 segundos
4. Revisar contenido del reporte:
   - Resumen de KPIs principales
   - Gráficos de tendencias
   - Conclusiones y recomendaciones
5. Verificar formato y legibilidad

Resultado Esperado:
- Reporte se genera rápidamente
- Contenido relevante y actualizado
- Formato profesional y legible
- Gráficos integrados correctamente
- Posibilidad de scroll fluido

Roles Permitidos: Admin, Gestor
Secciones: KPIs, Tendencias, Recomendaciones
```

#### **TC-REP-002: Reporte de Equidad (Solo Admin)**
```
Prerrequisitos: Usuario administrador
Pasos:
1. Acceder como administrador
2. Ir a "Reportes" > "Análisis de Equidad"
3. Verificar acceso permitido
4. Generar reporte completo
5. Logout y login como gestor
6. Intentar acceder al mismo reporte
7. Verificar acceso denegado

Resultado Esperado:
- Admin: Acceso completo al reporte
- Contenido sensible sobre equidad territorial
- Análisis detallado de disparidades
- Otros roles: Acceso denegado con mensaje claro

Restricción: Solo Administrador
Contenido: Datos sensibles de equidad
```

### **PLANIFICACIÓN ESTRATÉGICA**

#### **TC-PLAN-001: Planificación de Ubicaciones**
```
Prerrequisitos: Usuario administrador o gestor
Pasos:
1. Acceder a "Planificación Estratégica"
2. Seleccionar "Planificación de Ubicaciones"
3. Introducir parámetros:
   - Tipo de centro: Hospital
   - Población objetivo: 50,000
   - Radio de cobertura: 15 km
4. Ejecutar análisis
5. Verificar recomendaciones generadas

Resultado Esperado:
- Análisis se ejecuta sin errores
- Recomendaciones basadas en datos reales
- Visualización de ubicaciones sugeridas
- Justificación de cada recomendación
- Tiempo de procesamiento < 8 segundos

Algoritmos: Análisis geoespacial, optimización
Datos: Demografía, accesibilidad, capacidad actual
```

---

## 🔍 **ESCENARIOS DE PRUEBA AVANZADOS**

### **Escenario 1: Flujo Completo de Usuario Administrador**
```
Narrativa: Un administrador del sistema sanitario necesita realizar 
un análisis completo de la situación actual y planificar mejoras.

Pasos del Flujo:
1. Login como administrador
2. Revisar dashboard ejecutivo
3. Consultar al chat IA sobre capacidad actual
4. Generar mapa épico completo
5. Crear reporte de equidad territorial
6. Usar planificación estratégica para nuevas ubicaciones
7. Gestionar usuarios del sistema
8. Logout seguro

Validaciones:
- Cada paso se ejecuta sin errores
- Datos consistentes entre secciones
- Tiempo total < 5 minutos
- Experiencia fluida sin interrupciones
```

### **Escenario 2: Uso en Dispositivo Móvil Durante Reunión**
```
Narrativa: Un gestor sanitario necesita acceder a datos específicos 
durante una reunión usando su smartphone.

Pasos del Flujo:
1. Login desde móvil en 4G
2. Acceder rápidamente a métricas clave
3. Mostrar gráfico específico a colegas
4. Realizar consulta al chat IA
5. Compartir información relevante

Validaciones:
- Login rápido en conexión móvil
- Información legible en pantalla pequeña
- Gráficos interactivos funcionan con touch
- Respuesta IA en tiempo razonable
- Batería no se drena excesivamente
```

### **Escenario 3: Análisis Colaborativo en Tablet**
```
Narrativa: Un equipo de analistas usa una tablet durante una 
sesión de trabajo colaborativo para revisar datos demográficos.

Pasos del Flujo:
1. Login como analista en tablet
2. Abrir dashboard analítico
3. Explorar correlaciones demográficas
4. Generar reportes específicos
5. Usar mapas para identificar patrones
6. Alternar entre modo portrait y landscape

Validaciones:
- Interface adaptada para trabajo colaborativo
- Rotación de pantalla no afecta funcionalidad
- Múltiples usuarios pueden ver claramente
- Interacciones táctiles precisas
- Datos actualizados y consistentes
```

---

## 📊 **MATRIZ DE TRAZABILIDAD**

| Funcionalidad | TC-PC | TC-MOV | TC-TAB | TC-SEC | TC-PERF | Prioridad |
|---------------|--------|---------|---------|---------|----------|-----------|
| **Autenticación** | ✅ | ✅ | ✅ | ✅ | ✅ | 🔴 Alta |
| **Dashboard Principal** | ✅ | ✅ | ✅ | ❌ | ✅ | 🔴 Alta |
| **Chat IA** | ✅ | ✅ | ✅ | ✅ | ✅ | 🔴 Alta |
| **Mapas Épicos** | ✅ | ✅ | ✅ | ✅ | ✅ | 🔴 Alta |
| **Reportes** | ✅ | ✅ | ✅ | ✅ | ✅ | 🟡 Media |
| **Planificación** | ✅ | ✅ | ✅ | ✅ | ✅ | 🟡 Media |
| **Gestión Usuarios** | ✅ | ❌ | ✅ | ✅ | ❌ | 🟢 Baja |

---

## 🎯 **CONCLUSIONES Y RECOMENDACIONES**

### **Fortalezas del Sistema**
- ✅ **Arquitectura Robusta**: Streamlit + Python proporciona base sólida
- ✅ **Diseño Responsivo**: CSS avanzado con breakpoints bien definidos
- ✅ **Seguridad Implementada**: Sistema RBAC completo
- ✅ **IA Integrada**: Chat inteligente con Groq/Llama
- ✅ **Visualizaciones Ricas**: Plotly + Folium para gráficos y mapas

### **Áreas de Atención**
- 🟡 **Rendimiento en Móviles**: Optimizar carga de datasets grandes
- 🟡 **Compatibilidad Safari**: Probar extensivamente en iOS
- 🟡 **Offline Functionality**: Considerar capacidades sin conexión
- 🟡 **Accesibilidad**: Mejorar contraste y navegación por teclado

### **Recomendaciones de Mejora**
1. **Implementar Service Workers** para mejor rendimiento offline
2. **Optimizar imágenes y assets** para carga más rápida en móviles
3. **Añadir tests automatizados** para regresiones futuras
4. **Mejorar feedback visual** durante operaciones largas
5. **Implementar lazy loading** para gráficos complejos

---

## 📞 **CONTACTO Y SOPORTE**

**Equipo de Testing**: 
- **Lead Tester**: Antonio Jesús Padilla
- **Email**: antoniojesuspadilla.dev@proton.me
- **Proyecto**: Copilot Salud Andalucía

**Recursos Adicionales**:
- 📚 **Documentación Técnica**: README.md
- 🚀 **Guía de Despliegue**: DEPLOYMENT.md
- ☁️ **Setup Cloud**: STREAMLIT_CLOUD_SETUP.md

---

**🏥 Copilot Salud Andalucía - Plan de Pruebas Integral**

*Garantizando calidad y funcionamiento óptimo en todos los dispositivos*

**Versión 1.0 - Enero 2025**
