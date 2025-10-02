# 🔧 Problemas Pendientes de Visibilidad - Modo Oscuro

## ✅ Problemas Resueltos
1. **data-theme aplicándose correctamente** - Solucionado usando `parent.document` en componente HTML
2. **Login**: Textos y fondos adaptativos según tema
3. **Chat IA**: Input visible con buen contraste
4. **Alertas Administrativas**: Fondos y textos adaptativos

## ❌ Problemas Pendientes (Reportados por usuario)

### 1. Botones con Fondo Blanco
**Descripción**: Botones blancos sobre fondo blanco - solo visibles al hacer hover
**Ubicación**: Por determinar (esperando capturas)
**Prioridad**: ALTA

### 2. Poca Legibilidad en Botones (Modo Oscuro)
**Descripción**: Botones con bajo contraste en modo oscuro
**Ubicación**: General (esperando capturas específicas)
**Prioridad**: ALTA

### 3. Desplegables en Pestaña "Reportes"
**Descripción**: Problemas de visibilidad en elementos desplegables/expanders
**Ubicación**: Pestaña "Reportes"
**Prioridad**: ALTA

## 🎯 Solución Planificada

Cuando se reciban las capturas:
1. Identificar selectores CSS específicos de los botones afectados
2. Aplicar estilos condicionales según tema:
   ```css
   [data-theme="dark"] .stButton > button {
       background: #334155 !important;
       color: #f8fafc !important;
       border: 1px solid #6b7280 !important;
   }
   ```
3. Verificar expanders/desplegables:
   ```css
   [data-theme="dark"] details[data-testid="stExpander"] {
       background: #1e293b !important;
       color: #f8fafc !important;
   }
   ```

## 📸 Capturas Recibidas
- [x] Botones con fondo blanco - **RECIBIDA** (180131.png)
- [x] Botones en modo oscuro con poca legibilidad - **RECIBIDA** (180113.png)
- [x] Desplegables en pestaña "Reportes" - **RECIBIDA** (180113.png)

## ✅ Correcciones Aplicadas

### 1. Selectbox/Dropdown (Tipo de Reporte)
**Archivos modificados:**
- `assets/extra_styles.css` (líneas 349-390)
- `modules/core/auth_system.py` (líneas 1291-1344)

**Solución:**
```css
[data-theme="dark"] .stSelectbox,
[data-theme="dark"] [data-baseweb="select"] {
    background: #334155 !important;
    color: #f8fafc !important;
}

[data-theme="dark"] [role="option"] {
    background: #1e293b !important;
    color: #f8fafc !important;
}
```

### 2. Botones Generales
**Archivos modificados:**
- `assets/extra_styles.css` (líneas 392-407)
- `modules/core/auth_system.py` (líneas 1346-1367)

**Solución:**
```css
[data-theme="dark"] .stButton > button {
    background: #334155 !important;
    color: #f8fafc !important;
    border: 1px solid #6b7280 !important;
}

[data-theme="dark"] .stButton > button:hover {
    background: #475569 !important;
    color: #ffffff !important;
}
```

## 📅 Fechas
- **Reporte inicial:** 2025-10-01
- **Capturas recibidas:** 2025-10-01 18:01
- **Correcciones aplicadas:** 2025-10-01 18:15

## 🔄 Estado
**✅ CORRECCIONES COMPLETADAS** - Esperando validación del usuario

## 🧪 Para Probar
1. Recargar la página con **Ctrl + Shift + R**
2. Activar modo oscuro
3. Ir a pestaña "Reportes"
4. Verificar que:
   - El dropdown "Tipo de Reporte" tenga fondo oscuro y texto claro
   - Las opciones desplegadas sean visibles con buen contraste
   - Los botones tengan fondo oscuro y texto claro
   - Al hacer hover, los botones cambien de color correctamente
