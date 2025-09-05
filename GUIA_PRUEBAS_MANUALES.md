# 📋 GUÍA DE PRUEBAS MANUALES - COPILOT SALUD ANDALUCÍA

**Guía paso a paso para pruebas manuales en PC, Móviles y Tablets**

---

## 🎯 **OBJETIVO**

Esta guía proporciona instrucciones detalladas para realizar pruebas manuales exhaustivas de la aplicación Copilot Salud Andalucía, asegurando que funcione correctamente en todos los dispositivos objetivo.

---

## 📋 **PREPARACIÓN PREVIA**

### **🔧 Configuración del Entorno**

1. **Verificar Instalación**:
   ```bash
   # Verificar Python
   python --version
   
   # Verificar librerías
   pip list | grep streamlit
   pip list | grep plotly
   pip list | grep folium
   ```

2. **Configurar Variables de Entorno**:
   ```bash
   # Crear archivo .env en la raíz del proyecto
   GROQ_API_KEY=tu_clave_groq_aqui
   JWT_SECRET=tu_clave_secreta_jwt_aqui
   ```

3. **Generar Datos de Prueba**:
   ```bash
   python data_collector_2025.py
   ```

4. **Iniciar Aplicación**:
   ```bash
   streamlit run app.py
   ```

### **👥 Credenciales de Prueba**

| Rol | Usuario | Contraseña | Permisos |
|-----|---------|------------|----------|
| **Administrador** | `admin` | `admin123` | Acceso completo |
| **Gestor** | `gestor.malaga` | `gestor123` | Gestión y planificación |
| **Analista** | `analista.datos` | `analista123` | Análisis y reportes |
| **Invitado** | `demo` | `demo123` | Solo visualización |

---

## 🖥️ **PRUEBAS EN PC (ESCRITORIO)**

### **TEST 1: Carga Inicial y Login**

#### **Objetivo**: Verificar que la aplicación carga y el login funciona
#### **Tiempo Estimado**: 5 minutos

**Pasos**:

1. **Abrir Navegador**:
   - Navegador: Chrome, Firefox, Edge o Safari
   - URL: `http://localhost:8501`
   - Resolución: 1920x1080 o 1366x768

2. **Verificar Carga Inicial**:
   - [ ] La página carga en menos de 5 segundos
   - [ ] No hay errores en la consola del navegador (F12)
   - [ ] Se muestra la pantalla de login
   - [ ] Los estilos CSS se cargan correctamente

3. **Probar Login Administrador**:
   - [ ] Introducir usuario: `admin`
   - [ ] Introducir contraseña: `admin123`
   - [ ] Hacer click en "Iniciar Sesión"
   - [ ] Verificar redirección exitosa al dashboard
   - [ ] Confirmar tema azul ejecutivo (#1a365d)

4. **Verificar Elementos del Dashboard**:
   - [ ] Header con título personalizado
   - [ ] Sidebar con navegación completa
   - [ ] Métricas principales visibles
   - [ ] Gráficos se renderizan correctamente

**Criterios de Aprobación**:
- ✅ Login exitoso en menos de 3 segundos
- ✅ Dashboard completo visible
- ✅ Sin errores en consola
- ✅ Tema visual correcto aplicado

---

### **TEST 2: Chat IA (Groq)**

#### **Objetivo**: Validar funcionalidad del asistente IA
#### **Tiempo Estimado**: 10 minutos
#### **Prerequisito**: GROQ_API_KEY configurada

**Pasos**:

1. **Acceder al Chat IA**:
   - [ ] Click en sección "Chat IA" en sidebar
   - [ ] Verificar que la interfaz se carga
   - [ ] Confirmar estado "Activo" si API está configurada

2. **Realizar Consulta Básica**:
   - [ ] Introducir: "¿Cuántos hospitales hay en Málaga?"
   - [ ] Hacer click en "Enviar" o presionar Enter
   - [ ] Verificar tiempo de respuesta < 10 segundos
   - [ ] Confirmar respuesta coherente basada en datos

3. **Probar Consulta Compleja**:
   - [ ] Introducir: "Analiza la capacidad hospitalaria por distrito y sugiere mejoras"
   - [ ] Verificar respuesta estructurada en JSON
   - [ ] Confirmar sugerencias de visualización
   - [ ] Verificar que la respuesta incluye datos reales

4. **Verificar Historial**:
   - [ ] Confirmar que las consultas anteriores se mantienen
   - [ ] Verificar scroll en el área de mensajes
   - [ ] Probar copiar/pegar texto de respuestas

**Criterios de Aprobación**:
- ✅ Respuestas en menos de 10 segundos
- ✅ Contenido basado en datasets reales
- ✅ Formato JSON bien estructurado
- ✅ Historial de conversación funcional

---

### **TEST 3: Mapas Épicos Interactivos**

#### **Objetivo**: Verificar funcionalidad de mapas con Folium
#### **Tiempo Estimado**: 15 minutos

**Pasos**:

1. **Acceder a Mapas Épicos**:
   - [ ] Click en "Mapas Épicos" en sidebar
   - [ ] Verificar carga del dashboard de mapas
   - [ ] Confirmar header con gradiente épico

2. **Probar Mapa Completo Épico (Solo Admin)**:
   - [ ] Seleccionar "🌟 Mapa Completo Épico"
   - [ ] Verificar tiempo de carga < 8 segundos
   - [ ] Confirmar todas las capas visibles:
     - Hospitales (marcadores rojos)
     - Municipios (áreas coloreadas)
     - Rutas de acceso (líneas)
   - [ ] Verificar leyenda en esquina inferior izquierda

3. **Probar Interactividad**:
   - [ ] Hacer zoom in/out con rueda del mouse
   - [ ] Arrastrar mapa (pan) con mouse
   - [ ] Click en marcadores de hospitales
   - [ ] Verificar tooltips informativos
   - [ ] Confirmar popup con datos detallados

4. **Probar Otros Mapas**:
   - [ ] Mapa de Hospitales y Centros
   - [ ] Mapa de Demografía
   - [ ] Heatmap de Accesibilidad
   - [ ] Verificar que cada uno tiene datos únicos

**Criterios de Aprobación**:
- ✅ Todos los mapas cargan correctamente
- ✅ Interactividad completa (zoom, pan, click)
- ✅ Datos precisos en tooltips y popups
- ✅ Leyendas informativas y legibles

---

### **TEST 4: Dashboards Personalizados por Rol**

#### **Objetivo**: Verificar personalización según rol de usuario
#### **Tiempo Estimado**: 20 minutos

**Pasos**:

1. **Dashboard Administrador**:
   - [ ] Login como `admin`
   - [ ] Verificar tema azul ejecutivo (#1a365d)
   - [ ] Confirmar header "Panel de Control Ejecutivo"
   - [ ] Verificar métricas estratégicas:
     - Total de hospitales
     - Capacidad total de camas
     - Población total atendida
     - Índice de equidad promedio
   - [ ] Confirmar acceso a todas las secciones

2. **Dashboard Gestor**:
   - [ ] Logout y login como `gestor.malaga`
   - [ ] Verificar tema azul gestión (#2b6cb0)
   - [ ] Confirmar header "Centro de Gestión Sanitaria"
   - [ ] Verificar métricas operativas:
     - Capacidad hospitalaria
     - Personal sanitario
     - Ocupación promedio
     - Eficiencia operativa
   - [ ] Confirmar acceso restringido (no gestión de usuarios)

3. **Dashboard Analista**:
   - [ ] Logout y login como `analista.datos`
   - [ ] Verificar tema verde analítico (#059669)
   - [ ] Confirmar header "Laboratorio de Análisis de Datos"
   - [ ] Verificar métricas analíticas:
     - Correlaciones demográficas
     - Tendencias poblacionales
     - Análisis estadísticos
     - Proyecciones de demanda
   - [ ] Confirmar acceso a análisis pero no planificación

4. **Dashboard Invitado**:
   - [ ] Logout y login como `demo`
   - [ ] Verificar tema gris público (#6b7280)
   - [ ] Confirmar header "Portal de Información Pública"
   - [ ] Verificar información básica únicamente
   - [ ] Confirmar acceso muy limitado (sin IA, sin planificación)

**Criterios de Aprobación**:
- ✅ Cada rol ve su interfaz personalizada
- ✅ Colores y temas específicos aplicados
- ✅ Métricas relevantes según permisos
- ✅ Control de acceso funcionando correctamente

---

### **TEST 5: Generación de Reportes**

#### **Objetivo**: Verificar creación de reportes por rol
#### **Tiempo Estimado**: 15 minutos

**Pasos**:

1. **Reporte Ejecutivo (Admin/Gestor)**:
   - [ ] Login como admin o gestor
   - [ ] Acceder a sección "Reportes"
   - [ ] Seleccionar "Reporte Ejecutivo"
   - [ ] Verificar generación < 5 segundos
   - [ ] Confirmar contenido:
     - Resumen de KPIs
     - Gráficos de tendencias
     - Conclusiones y recomendaciones
   - [ ] Verificar formato profesional

2. **Reporte de Infraestructura**:
   - [ ] Seleccionar "Análisis de Infraestructura"
   - [ ] Verificar datos de hospitales y centros
   - [ ] Confirmar análisis de capacidad
   - [ ] Verificar recomendaciones de mejora

3. **Reporte de Equidad (Solo Admin)**:
   - [ ] Login como admin
   - [ ] Seleccionar "Evaluación de Equidad"
   - [ ] Verificar acceso permitido
   - [ ] Confirmar análisis territorial detallado
   - [ ] Logout y login como gestor
   - [ ] Verificar acceso denegado con mensaje claro

4. **Análisis Completo (Solo Admin)**:
   - [ ] Login como admin
   - [ ] Seleccionar "Análisis Completo"
   - [ ] Verificar reporte integral del sistema
   - [ ] Confirmar todas las métricas incluidas

**Criterios de Aprobación**:
- ✅ Reportes se generan rápidamente
- ✅ Contenido relevante y actualizado
- ✅ Control de acceso por rol funciona
- ✅ Formato profesional y legible

---

## 📱 **PRUEBAS EN MÓVILES**

### **TEST 6: Responsividad General**

#### **Objetivo**: Verificar adaptación a pantallas móviles
#### **Tiempo Estimado**: 15 minutos

**Pasos de Configuración**:
1. **Usar Emulador de Móvil**:
   - Abrir Chrome DevTools (F12)
   - Click en icono de dispositivo móvil
   - Seleccionar resolución: iPhone 12 Pro (390x844)
   - Refrescar página

2. **Usar Dispositivo Real**:
   - Acceder desde smartphone
   - URL: `http://[IP_LOCAL]:8501`
   - Ejemplo: `http://192.168.1.100:8501`

**Pruebas**:

1. **Verificar Layout Responsivo**:
   - [ ] No hay scroll horizontal
   - [ ] Sidebar se colapsa automáticamente
   - [ ] Header se adapta al ancho de pantalla
   - [ ] Métricas se apilan verticalmente
   - [ ] Texto es legible sin zoom

2. **Probar Navegación Táctil**:
   - [ ] Tap en botones funciona correctamente
   - [ ] Botones tienen tamaño mínimo 44px
   - [ ] Menú hamburguesa abre/cierra sidebar
   - [ ] Scroll vertical es suave
   - [ ] No hay elementos superpuestos

3. **Verificar Formularios**:
   - [ ] Login funciona con teclado táctil
   - [ ] Campos de texto se enfocan correctamente
   - [ ] Teclado no oculta campos importantes
   - [ ] Botones de envío son accesibles

4. **Probar en Orientaciones**:
   - [ ] Portrait (vertical): Layout se adapta
   - [ ] Landscape (horizontal): Aprovecha ancho extra
   - [ ] Rotación no rompe la interfaz
   - [ ] Estado se mantiene al rotar

**Criterios de Aprobación**:
- ✅ UI perfectamente adaptada a móvil
- ✅ Navegación táctil fluida
- ✅ Sin elementos cortados o superpuestos
- ✅ Texto legible sin zoom necesario

---

### **TEST 7: Gráficos en Móviles**

#### **Objetivo**: Validar visualizaciones Plotly en móviles
#### **Tiempo Estimado**: 10 minutos

**Pasos**:

1. **Acceder a Dashboard desde Móvil**:
   - [ ] Login desde dispositivo móvil
   - [ ] Navegar a dashboard principal
   - [ ] Verificar que gráficos se cargan

2. **Probar Gráficos de Barras**:
   - [ ] Gráfico se redimensiona al ancho de pantalla
   - [ ] Barras son visibles y diferenciables
   - [ ] Tap en barras muestra tooltip
   - [ ] Leyenda es legible

3. **Probar Gráficos de Líneas**:
   - [ ] Líneas se ven claramente
   - [ ] Puntos de datos son tocables
   - [ ] Zoom con gestos funciona
   - [ ] Pan horizontal funciona

4. **Probar Interactividad Táctil**:
   - [ ] Pinch-to-zoom funciona
   - [ ] Pan con un dedo funciona
   - [ ] Double-tap para reset zoom
   - [ ] Controles de Plotly accesibles

5. **Verificar Performance**:
   - [ ] Gráficos cargan en < 3 segundos
   - [ ] Interacciones son fluidas
   - [ ] No hay lag al tocar/arrastrar
   - [ ] Batería no se drena excesivamente

**Criterios de Aprobación**:
- ✅ Gráficos totalmente funcionales en móvil
- ✅ Gestos táctiles responden correctamente
- ✅ Performance aceptable
- ✅ Controles accesibles con dedos

---

### **TEST 8: Chat IA en Móviles**

#### **Objetivo**: Verificar usabilidad del chat en móviles
#### **Tiempo Estimado**: 10 minutos

**Pasos**:

1. **Acceder al Chat desde Móvil**:
   - [ ] Navegar a sección Chat IA
   - [ ] Verificar que interface se adapta
   - [ ] Confirmar área de chat visible

2. **Probar Entrada de Texto**:
   - [ ] Tap en campo de texto abre teclado
   - [ ] Teclado no oculta área de chat
   - [ ] Texto se puede escribir normalmente
   - [ ] Botón enviar es accesible

3. **Realizar Consulta**:
   - [ ] Escribir consulta: "Hospitales en Málaga"
   - [ ] Enviar consulta
   - [ ] Verificar que chat se desplaza automáticamente
   - [ ] Respuesta es legible sin zoom

4. **Probar Funciones Avanzadas**:
   - [ ] Scroll en historial de chat funciona
   - [ ] Copiar texto de respuesta funciona
   - [ ] Seleccionar texto es preciso
   - [ ] Compartir respuesta (si disponible)

**Criterios de Aprobación**:
- ✅ Chat completamente usable en móvil
- ✅ Teclado no interfiere con funcionalidad
- ✅ Texto legible y seleccionable
- ✅ Scroll y navegación fluidos

---

## 📟 **PRUEBAS EN TABLETS**

### **TEST 9: Layout Intermedio en Tablets**

#### **Objetivo**: Verificar adaptación a resolución tablet
#### **Tiempo Estimado**: 15 minutos

**Configuración**:
- **Emulador**: iPad (1024x768) en Chrome DevTools
- **Dispositivo Real**: iPad, Surface, Android tablet
- **Orientaciones**: Portrait y Landscape

**Pasos**:

1. **Verificar Layout Portrait (768x1024)**:
   - [ ] Sidebar se mantiene visible pero compacto
   - [ ] Métricas usan 2 columnas
   - [ ] Gráficos ocupan ancho completo
   - [ ] Header se adapta correctamente
   - [ ] Footer no se solapa con contenido

2. **Verificar Layout Landscape (1024x768)**:
   - [ ] Sidebar expandido es usable
   - [ ] Métricas usan 3-4 columnas
   - [ ] Gráficos aprovechan ancho extra
   - [ ] Navegación horizontal cómoda
   - [ ] Aprovecha espacio disponible

3. **Probar Transición entre Orientaciones**:
   - [ ] Rotación no rompe layout
   - [ ] Estado de la aplicación se mantiene
   - [ ] Animaciones de transición suaves
   - [ ] Scroll position se preserva
   - [ ] Modales/popups se reposicionan

4. **Verificar Usabilidad**:
   - [ ] Elementos no se ven "estirados"
   - [ ] Espaciado apropiado entre elementos
   - [ ] **Botones de tamaño adecuado** (mínimo 44px de altura)
   - [ ] Texto con tamaño óptimo de lectura
   - [ ] **Verificar botones táctiles**: Probar con dedo que todos los botones son fáciles de presionar
   - [ ] **Área de toque suficiente**: No hay botones demasiado pequeños o juntos

**Criterios de Aprobación**:
- ✅ Layout optimizado para ambas orientaciones
- ✅ Transiciones suaves entre orientaciones
- ✅ Aprovechamiento eficiente del espacio
- ✅ Usabilidad excelente en tablet

---

### **TEST 10: Mapas en Tablets**

#### **Objetivo**: Verificar mapas interactivos en tablet
#### **Tiempo Estimado**: 15 minutos

**Pasos**:

1. **Cargar Mapas en Tablet**:
   - [ ] Acceder a Mapas Épicos desde tablet
   - [ ] Seleccionar mapa completo
   - [ ] Verificar carga < 8 segundos
   - [ ] Confirmar todas las capas visibles

2. **Probar Gestos Táctiles**:
   - [ ] **Pinch-to-zoom**: Pellizcar para zoom in/out
   - [ ] **Pan**: Arrastrar con un dedo para mover
   - [ ] **Tap**: Tocar marcadores para info
   - [ ] **Long-press**: Mantener presionado para opciones
   - [ ] **Double-tap**: Doble toque para zoom rápido

3. **Verificar Precisión**:
   - [ ] Zoom es suave y preciso
   - [ ] Pan responde inmediatamente
   - [ ] Tap en marcadores es preciso
   - [ ] No hay "fantasma touches"
   - [ ] Multitouch funciona correctamente

4. **Probar en Ambas Orientaciones**:
   - [ ] Portrait: Mapa ocupa pantalla completa
   - [ ] Landscape: Aprovecha ancho extra
   - [ ] Leyenda se reposiciona correctamente
   - [ ] Controles siguen siendo accesibles

5. **Verificar Performance**:
   - [ ] Gestos responden sin lag
   - [ ] Zoom es fluido a cualquier nivel
   - [ ] Rendering de capas es rápido
   - [ ] Memoria no se agota con uso prolongado

**Criterios de Aprobación**:
- ✅ Todos los gestos táctiles funcionan perfectamente
- ✅ Precisión excelente en interacciones
- ✅ Performance fluida sin lag
- ✅ Funciona bien en ambas orientaciones

---

### **TEST 11: Multitarea en Tablets**

#### **Objetivo**: Validar comportamiento en multitarea
#### **Tiempo Estimado**: 10 minutos

**Pasos**:

1. **Probar Split-Screen (iPad/Surface)**:
   - [ ] Abrir aplicación en pantalla completa
   - [ ] Activar split-screen con otra app
   - [ ] Verificar que layout se adapta
   - [ ] Confirmar funcionalidad completa
   - [ ] Cambiar tamaño de ventanas

2. **Probar App Switching**:
   - [ ] Cambiar a otra aplicación
   - [ ] Regresar a Copilot Salud
   - [ ] Verificar que estado se mantiene
   - [ ] Confirmar que login sigue activo
   - [ ] Verificar que datos no se perdieron

3. **Probar Suspensión/Reactivación**:
   - [ ] Poner tablet en standby
   - [ ] Reactivar después de 5 minutos
   - [ ] Verificar que app sigue funcionando
   - [ ] Confirmar que sesión no expiró
   - [ ] Verificar que datos están actualizados

4. **Probar Notificaciones**:
   - [ ] Recibir notificación mientras usa app
   - [ ] Verificar que app no se interrumpe
   - [ ] Confirmar que puede volver fácilmente
   - [ ] Verificar que no hay pérdida de datos

**Criterios de Aprobación**:
- ✅ Funciona correctamente en split-screen
- ✅ Estado se preserva al cambiar apps
- ✅ Sesión se mantiene activa apropiadamente
- ✅ No hay pérdida de datos o estado

---

## 🔒 **PRUEBAS DE SEGURIDAD**

### **TEST 12: Control de Acceso por Roles**

#### **Objetivo**: Verificar RBAC (Role-Based Access Control)
#### **Tiempo Estimado**: 20 minutos

**Pasos**:

1. **Probar Acceso de Administrador**:
   - [ ] Login como `admin`
   - [ ] Verificar acceso a "Gestión de Usuarios"
   - [ ] Confirmar acceso a "Análisis de Equidad"
   - [ ] Verificar acceso a "Planificación Estratégica"
   - [ ] Confirmar acceso a todos los mapas
   - [ ] Verificar acceso a Chat IA completo

2. **Probar Restricciones de Gestor**:
   - [ ] Login como `gestor.malaga`
   - [ ] Intentar acceder a "Gestión de Usuarios"
   - [ ] Verificar acceso denegado con mensaje claro
   - [ ] Confirmar acceso a "Planificación Estratégica"
   - [ ] Verificar acceso a Chat IA
   - [ ] Confirmar acceso a mapas operativos

3. **Probar Restricciones de Analista**:
   - [ ] Login como `analista.datos`
   - [ ] Intentar acceder a "Planificación Estratégica"
   - [ ] Verificar acceso denegado
   - [ ] Confirmar acceso a Chat IA para análisis
   - [ ] Verificar acceso a mapas analíticos
   - [ ] Confirmar acceso a reportes técnicos

4. **Probar Restricciones de Invitado**:
   - [ ] Login como `demo`
   - [ ] Intentar acceder a Chat IA
   - [ ] Verificar acceso denegado
   - [ ] Confirmar acceso solo a dashboard básico
   - [ ] Verificar acceso solo a mapas públicos
   - [ ] Confirmar restricciones en reportes

**Criterios de Aprobación**:
- ✅ Cada rol tiene acceso exactamente a lo permitido
- ✅ Accesos denegados muestran mensajes claros
- ✅ No hay bypass de seguridad posible
- ✅ Mensajes de error no revelan información sensible

---

### **TEST 13: Seguridad de Sesiones**

#### **Objetivo**: Verificar manejo seguro de sesiones
#### **Tiempo Estimado**: 15 minutos

**Pasos**:

1. **Probar Login Seguro**:
   - [ ] Intentar login con credenciales incorrectas
   - [ ] Verificar que se muestra error genérico
   - [ ] Confirmar que no revela si usuario existe
   - [ ] Probar múltiples intentos fallidos
   - [ ] Verificar que no hay bloqueo permanente

2. **Probar Expiración de Sesión**:
   - [ ] Login exitoso
   - [ ] Esperar tiempo de inactividad (si configurado)
   - [ ] Verificar redirección automática a login
   - [ ] Confirmar que sesión se invalida
   - [ ] Intentar acceder directamente a páginas protegidas

3. **Probar Logout Seguro**:
   - [ ] Login exitoso
   - [ ] Click en "Cerrar Sesión"
   - [ ] Verificar redirección a login
   - [ ] Confirmar que botón "Atrás" no permite acceso
   - [ ] Verificar que nueva pestaña requiere login

4. **Probar Seguridad de Tokens**:
   - [ ] Inspeccionar cookies/localStorage (F12)
   - [ ] Verificar que tokens no son legibles en texto plano
   - [ ] Confirmar que tokens tienen expiración
   - [ ] Verificar que tokens se invalidan al logout

**Criterios de Aprobación**:
- ✅ Login seguro sin revelación de información
- ✅ Sesiones expiran apropiadamente
- ✅ Logout invalida completamente la sesión
- ✅ Tokens están protegidos adecuadamente

---

## ⚡ **PRUEBAS DE RENDIMIENTO**

### **TEST 14: Tiempos de Carga**

#### **Objetivo**: Medir tiempos de carga en diferentes dispositivos
#### **Tiempo Estimado**: 20 minutos

**Herramientas**:
- Chrome DevTools (Network tab)
- Lighthouse (Auditoría)
- Stopwatch para medición manual

**Pasos**:

1. **Medir Carga Inicial (PC)**:
   - [ ] Abrir Chrome DevTools > Network
   - [ ] Refrescar página (Ctrl+F5)
   - [ ] Medir tiempo hasta "DOMContentLoaded"
   - [ ] **Objetivo**: < 3 segundos
   - [ ] Verificar tamaño total de recursos
   - [ ] **Objetivo**: < 5MB

2. **Medir Carga Inicial (Móvil)**:
   - [ ] Simular conexión 4G en DevTools
   - [ ] Refrescar página
   - [ ] Medir tiempo de carga completa
   - [ ] **Objetivo**: < 8 segundos
   - [ ] Verificar que no hay recursos innecesarios

3. **Medir Carga de Dashboard**:
   - [ ] Login exitoso
   - [ ] Medir tiempo hasta dashboard completo
   - [ ] **Objetivo**: < 3 segundos después de login
   - [ ] Verificar carga de gráficos
   - [ ] **Objetivo**: Gráficos en < 2 segundos

4. **Medir Respuesta de Chat IA**:
   - [ ] Realizar consulta simple
   - [ ] Medir tiempo de respuesta
   - [ ] **Objetivo**: < 10 segundos
   - [ ] Realizar consulta compleja
   - [ ] **Objetivo**: < 15 segundos

5. **Medir Carga de Mapas**:
   - [ ] Acceder a mapa épico completo
   - [ ] Medir tiempo hasta interactividad
   - [ ] **Objetivo**: < 8 segundos
   - [ ] Verificar fluidez de interacciones

**Criterios de Aprobación**:
- ✅ PC: Carga inicial < 3s, dashboard < 3s
- ✅ Móvil: Carga inicial < 8s, usabilidad fluida
- ✅ Chat IA: Respuestas < 10s (simples), < 15s (complejas)
- ✅ Mapas: Carga < 8s, interactividad fluida

---

### **TEST 15: Prueba de Estrés**

#### **Objetivo**: Verificar comportamiento bajo carga
#### **Tiempo Estimado**: 15 minutos

**Pasos**:

1. **Abrir Múltiples Pestañas**:
   - [ ] Abrir 5-10 pestañas de la aplicación
   - [ ] Login en cada una con diferentes usuarios
   - [ ] Verificar que todas funcionan correctamente
   - [ ] Confirmar que no hay interferencia entre sesiones

2. **Usar Múltiples Funciones Simultáneamente**:
   - [ ] Tener chat IA activo
   - [ ] Abrir mapas en otra pestaña
   - [ ] Generar reporte en tercera pestaña
   - [ ] Verificar que todo funciona sin conflictos

3. **Probar con Datos Grandes**:
   - [ ] Generar consulta IA que requiera todos los datasets
   - [ ] Abrir mapa con todas las capas
   - [ ] Verificar que memoria no se agota
   - [ ] Confirmar que browser no se congela

4. **Monitorear Recursos**:
   - [ ] Abrir Task Manager/Activity Monitor
   - [ ] Verificar uso de CPU < 80%
   - [ ] Confirmar uso de RAM razonable
   - [ ] Verificar que no hay memory leaks

**Criterios de Aprobación**:
- ✅ Múltiples sesiones funcionan independientemente
- ✅ Uso de recursos dentro de límites aceptables
- ✅ No hay memory leaks detectables
- ✅ Performance se mantiene estable

---

## 📊 **DOCUMENTACIÓN DE RESULTADOS**

### **Plantilla de Reporte por Prueba**

```markdown
## TEST [NÚMERO]: [NOMBRE DE LA PRUEBA]

**Fecha**: [DD/MM/YYYY]
**Tester**: [Nombre]
**Dispositivo**: [PC/Móvil/Tablet]
**Navegador**: [Chrome/Firefox/Safari/Edge]
**Resolución**: [WxH]

### Resultados:
- [ ] ✅ PASS: [Descripción del éxito]
- [ ] ❌ FAIL: [Descripción del fallo]
- [ ] ⚠️ WARNING: [Descripción de la advertencia]

### Observaciones:
[Notas adicionales, capturas de pantalla, logs de error]

### Tiempo de Ejecución:
[X minutos]

### Recomendaciones:
[Mejoras sugeridas]
```

### **Criterios de Aprobación Global**

| Categoría | Criterio | Peso | Estado |
|-----------|----------|------|--------|
| **Funcionalidad** | 95%+ casos pasan | 40% | [ ] |
| **Rendimiento** | Tiempos dentro de límites | 25% | [ ] |
| **Compatibilidad** | Funciona en todos los dispositivos | 20% | [ ] |
| **Seguridad** | Sin vulnerabilidades críticas | 10% | [ ] |
| **Usabilidad** | UX consistente y fluida | 5% | [ ] |

### **Decisión Final**

- [ ] ✅ **APROBADO**: Listo para producción
- [ ] ⚠️ **APROBADO CON OBSERVACIONES**: Listo con mejoras menores
- [ ] ❌ **RECHAZADO**: Requiere correcciones antes de desplegar

---

## 🛠️ **HERRAMIENTAS RECOMENDADAS**

### **Para Pruebas Manuales**:
- **Chrome DevTools**: F12 para inspección y emulación
- **Firefox Developer Tools**: Herramientas de desarrollo
- **Lighthouse**: Auditoría de performance y accesibilidad
- **WAVE**: Testing de accesibilidad web
- **Postman**: Testing de APIs (si aplica)

### **Para Documentación**:
- **Markdown**: Para reportes de prueba
- **Screenshots**: Capturar evidencia visual
- **Screen Recording**: Para bugs complejos
- **JSON**: Para reportes estructurados

### **Para Análisis de Performance**:
- **Chrome DevTools Performance**: Profiling detallado
- **Network Tab**: Análisis de carga de recursos
- **Memory Tab**: Detección de memory leaks
- **Lighthouse CI**: Auditorías automatizadas

---

## 📞 **SOPORTE Y ESCALACIÓN**

### **En caso de problemas críticos**:

1. **Documentar completamente**:
   - Pasos exactos para reproducir
   - Capturas de pantalla/video
   - Logs de error de consola
   - Información del entorno

2. **Clasificar severidad**:
   - **🔴 Crítico**: Bloquea funcionalidad principal
   - **🟡 Alto**: Funcionalidad importante afectada  
   - **🟢 Medio**: Problema menor
   - **⚪ Bajo**: Cosmético

3. **Contactar**:
   - **Desarrollador**: Antonio Jesús Padilla
   - **Email**: antoniojesuspadilla.dev@proton.me
   - **GitHub**: Issues en el repositorio del proyecto

---

**🧪 Guía de Pruebas Manuales - Copilot Salud Andalucía**

*Asegurando calidad y funcionalidad en todos los dispositivos*

**Versión 1.0 - Enero 2025**
