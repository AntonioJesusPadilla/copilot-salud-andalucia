# 🔍 Diagnóstico de Problemas de Visibilidad de Temas

## Problema Reportado
"Sigo viendo lo mismo" - Textos poco legibles en modo oscuro

## Cambios Realizados

### 1. ✅ Login (modules/core/auth_system.py)
**Líneas 1259-1276**: Colores condicionales según tema
- **Modo oscuro**: Fondos oscuros (#1e293b, #334155) + textos claros (#f9fafb, #d1d5db)
- **Modo claro**: Fondos claros (#ffffff, #f7fafc) + textos oscuros (#1a202c, #4a5568)

**Líneas 1252-1289**: CSS forzado para:
- Chat input en modo oscuro
- Alertas administrativas en modo oscuro

### 2. ✅ Chat IA (assets/extra_styles.css + auth_system.py)
**Líneas 272-288 (extra_styles.css)**:
```css
[data-theme="dark"] .stChatInput textarea,
[data-theme="dark"] .stChatInput input {
    background: #334155 !important;
    color: #f8fafc !important;
}
```

### 3. ✅ Alertas Administrativas (modules/core/role_dashboards.py + CSS)
**Líneas 295-305 (role_dashboards.py)**: Cambio de estilos inline a clases CSS
**Líneas 290-347 (extra_styles.css)**: Estilos adaptativos

## 🚨 Posibles Causas del Problema

### A. Cache del Navegador ⚠️
**Síntoma**: Los cambios no se ven después de recargar
**Solución**:
1. Presionar **Ctrl + Shift + R** (hard refresh)
2. O abrir DevTools (F12) > Network > ✅ Disable cache
3. Cerrar todas las pestañas y volver a abrir

### B. Streamlit no reiniciado ⚠️
**Síntoma**: Cambios en archivos .py no se aplican
**Solución**:
- El proceso se debe haber reiniciado automáticamente
- Verificar en terminal que aparezca "Rerunning script"

### C. Archivo CSS no cargado ⚠️
**Síntoma**: extra_styles.css no se está inyectando
**Verificación**:
- Abrir DevTools > Elements
- Buscar `<style>` con contenido de "CHAT INPUT FORZADO"
- Buscar `.alert-card` en los estilos

### D. data-theme no se está aplicando ⚠️
**Síntoma**: El atributo `data-theme="dark"` no existe en `<body>`
**Verificación**:
- Abrir DevTools > Elements
- Inspeccionar `<body>` o `<html>`
- Debe tener `data-theme="dark"` cuando está en modo oscuro

## 🔧 Pasos de Diagnóstico

### 1. Verificar que el tema se está aplicando
```javascript
// En la consola del navegador (F12):
document.body.getAttribute('data-theme')
// Debe devolver "dark" o "light"
```

### 2. Verificar estilos CSS cargados
```javascript
// En la consola:
Array.from(document.styleSheets)
  .flatMap(s => Array.from(s.cssRules || []))
  .filter(r => r.cssText?.includes('stChatInput'))
  .map(r => r.cssText)
// Debe mostrar los estilos del chat input
```

### 3. Verificar elemento específico
```javascript
// Verificar color del chat input:
const chatInput = document.querySelector('[data-testid="stChatInput"] textarea');
if (chatInput) {
  const styles = window.getComputedStyle(chatInput);
  console.log('Background:', styles.backgroundColor);
  console.log('Color:', styles.color);
}
```

## 📸 Captura de Pantalla Solicitada

Por favor, proporciona captura mostrando:
1. La página de login en modo oscuro
2. El área problemática marcada/resaltada
3. DevTools abierto mostrando:
   - El atributo `data-theme` en `<body>`
   - Los estilos computados del elemento con problema

## ⏭️ Próximos Pasos

Si después de **Ctrl + Shift + R** el problema persiste:
1. Compartir captura de pantalla
2. Compartir resultados de los scripts de diagnóstico
3. Verificar consola del navegador por errores CSS
