# 🔧 TAREA PENDIENTE - Visibilidad de Textos en Temas

## Problema Identificado

### ✅ Modo Claro (FUNCIONA BIEN)
- Cartel de aplicación: fondo claro con texto negro
- Resto de elementos tienen buena visibilidad

### ❌ Modo Oscuro (PROBLEMA CRÍTICO)
- **Texto oscuro sobre fondo oscuro** → NO SE LEE
- Falta de contraste hace el texto invisible

## Solución Requerida

### En Modo Oscuro necesitamos:
1. **Textos principales**: `#f8fafc` (casi blanco)
2. **Textos secundarios**: `#cbd5e1` (gris claro)
3. **Textos destacados**: `#ffffff` (blanco puro)
4. **Fondos oscuros**: `#0f172a` (base), `#1e293b` (superficie), `#334155` (elevado)

### Archivos a Revisar:
- `modules/core/auth_system.py` (página de login)
  - Header del login
  - Labels de inputs (Usuario, Contraseña)
  - Credenciales de demostración
  - Sección de roles
  - Botones de acción

### Elementos Críticos:
```css
/* MODO OSCURO - Todos los textos deben ser claros */
[data-theme="dark"] .login-header h1,
[data-theme="dark"] .login-header h3,
[data-theme="dark"] .login-header p {
    color: #f8fafc !important; /* Texto claro */
}

[data-theme="dark"] label,
[data-theme="dark"] .stMarkdown,
[data-theme="dark"] p,
[data-theme="dark"] h1,
[data-theme="dark"] h2,
[data-theme="dark"] h3 {
    color: #f8fafc !important; /* Texto claro */
}

[data-theme="dark"] input,
[data-theme="dark"] input::placeholder {
    color: #cbd5e1 !important; /* Placeholder visible */
    background: #334155 !important;
}
```

## Capturas de Referencia
Ver archivos en `.claude/`:
- `Captura de pantalla 2025-09-30 161319.png` (Modo Claro - OK)
- `Captura de pantalla 2025-09-30 161329.png` (Modo Oscuro - PROBLEMA)

## Prioridad
🔴 **ALTA** - Afecta usabilidad en modo oscuro
