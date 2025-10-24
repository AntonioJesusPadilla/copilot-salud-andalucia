# Scripts de Optimización de Rendimiento

Sistema de optimización por fases para mejorar el tiempo de carga de la aplicación en dispositivos móviles (especialmente iPhone con iOS).

## 🎯 Objetivo

Reducir el tiempo de carga de **8-15 segundos** a **2-4 segundos** en iPhone 15 con iOS 18.

## 📊 Ganancia Esperada por Fase

| Fase | Optimización | Ganancia Estimada | Tiempo |
|------|-------------|-------------------|--------|
| **Fase 1** | Extracción y minificación de CSS | 4-6 segundos | 2 horas |
| **Fase 2** | Detección móvil y carga condicional | 1.5-2.5 segundos | 1.5 horas |
| **Fase 3** | Lazy loading y consolidación | 1-2 segundos | 1.5 horas |
| **TOTAL** | **Todas las optimizaciones** | **6.5-10.5 segundos** | **5 horas** |

## 🚀 Uso Rápido

### 1. Crear Snapshot del Sistema Actual

**IMPORTANTE**: Siempre crear un backup antes de optimizar.

```bash
python optimization_scripts/0_create_snapshot.py
```

Esto creará un backup completo en `optimization_backups/snapshot_YYYYMMDD_HHMMSS/`

### 2. Ejecutar Fases en Orden

#### Fase 1: Optimización de CSS
```bash
python optimization_scripts/phase1_css_optimization.py
```

**Qué hace:**
- Extrae CSS inline (1,300+ líneas) de `auth_system.py` a `assets/login.css`
- Minifica todos los archivos CSS (reducción ~40-50%)
- Actualiza referencias para usar CSS externo cacheable

**Después de ejecutar:**
1. Probar en local: `streamlit run src/app.py`
2. Verificar que el login funciona correctamente
3. Verificar que los temas (claro/oscuro) funcionan

#### Fase 2: Optimización Móvil
```bash
python optimization_scripts/phase2_mobile_optimization.py
```

**Qué hace:**
- Optimiza detección de dispositivos móviles (más rápida, con caché)
- Carga `ios_safari_fixes.css` solo en dispositivos iOS
- Evita cargar CSS innecesario en móviles

**Después de ejecutar:**
1. Probar en local: `streamlit run src/app.py`
2. Probar en diferentes dispositivos (si es posible):
   - iPhone/iPad (Safari)
   - Android (Chrome)
   - Desktop (Chrome/Firefox)
3. Verificar que no hay errores en la consola del navegador

#### Fase 3: Lazy Loading
```bash
python optimization_scripts/phase3_lazy_loading.py
```

**Qué hace:**
- Implementa lazy loading de `safari_detector.js` (solo iOS + después de login)
- Agrega preload hints para recursos críticos
- Optimiza orden de carga de CSS
- Genera reporte de CSS duplicados

**Después de ejecutar:**
1. Revisar reporte: `optimization_scripts/css_duplicates_report.txt`
2. Probar en local: `streamlit run src/app.py`
3. Medir tiempo de carga (ver sección Testing)

### 3. Restaurar Snapshot (Si algo falla)

```bash
# Restaurar el último snapshot
python optimization_scripts/restore_snapshot.py

# Restaurar un snapshot específico
python optimization_scripts/restore_snapshot.py 20251022_115252

# Listar snapshots disponibles
python optimization_scripts/restore_snapshot.py --list
```

## 📋 Testing y Validación

### Testing en Local

1. **Iniciar la aplicación:**
   ```bash
   cd C:\Users\Lenovo\Documents\proyectos\copilot-salud-andalucia
   streamlit run src/app.py
   ```

2. **Abrir en navegador:**
   - Local: `http://localhost:8501`

3. **Medir tiempo de carga:**
   - **Chrome DevTools**: F12 → Network → Recargar página
   - Ver "DOMContentLoaded" y "Load" en la línea de tiempo
   - **Antes**: 8-15 segundos
   - **Después**: 2-4 segundos esperados

4. **Verificaciones funcionales:**
   - [ ] Login funciona correctamente
   - [ ] Toggle tema claro/oscuro funciona
   - [ ] No hay errores en consola del navegador
   - [ ] CSS se aplica correctamente
   - [ ] Inputs son legibles (color de texto correcto)
   - [ ] Botones funcionan

### Testing en Dispositivos Reales

#### iPhone/iPad (iOS)
```bash
# Obtener IP local
ipconfig

# Ejecutar Streamlit con IP accesible
streamlit run src/app.py --server.address 0.0.0.0
```

Luego acceder desde iPhone: `http://192.168.X.X:8501`

**Verificar:**
- [ ] Tiempo de carga (usar Safari devtools remotos)
- [ ] Safe areas (notch/dynamic island) funcionan
- [ ] Touch events funcionan correctamente
- [ ] Scroll suave
- [ ] No hay zoom inesperado en inputs

#### Android
Similar al proceso de iOS, acceder desde navegador Android.

**Verificar:**
- [ ] Tiempo de carga
- [ ] Touch events
- [ ] Scroll suave

### Testing antes de Subir a Cloud

**Checklist final:**

- [ ] Todas las fases ejecutadas sin errores
- [ ] Testing en local completado
- [ ] Testing en dispositivo real (al menos iOS o Android)
- [ ] No hay errores en consola del navegador
- [ ] Funcionalidad completa verificada
- [ ] Git commit creado con los cambios

**Crear commit de optimización:**
```bash
git add .
git commit -m "feat: Optimización de rendimiento móvil - Fases 1-3

- Extracción y minificación de CSS (-4-6 seg)
- Detección móvil optimizada y carga condicional (-1.5-2.5 seg)
- Lazy loading y preload hints (-1-2 seg)

Reducción total: 6.5-10.5 segundos
Tiempo de carga: 8-15 seg → 2-4 seg"
```

## 📈 Medición de Resultados

### Antes de Optimizar

Documentar métricas iniciales:

```bash
# Crear archivo de métricas
echo "MÉTRICAS ANTES DE OPTIMIZACIÓN" > optimization_scripts/metrics_before.txt
echo "=============================" >> optimization_scripts/metrics_before.txt
echo "" >> optimization_scripts/metrics_before.txt
echo "Fecha: $(date)" >> optimization_scripts/metrics_before.txt
echo "Dispositivo: iPhone 15, iOS 18" >> optimization_scripts/metrics_before.txt
echo "Conexión: [4G/5G/WiFi]" >> optimization_scripts/metrics_before.txt
echo "" >> optimization_scripts/metrics_before.txt
echo "Tiempo de carga (DOMContentLoaded): [X] segundos" >> optimization_scripts/metrics_before.txt
echo "Tiempo de carga total (Load): [X] segundos" >> optimization_scripts/metrics_before.txt
echo "Tamaño de CSS transferido: [X] KB" >> optimization_scripts/metrics_before.txt
echo "Tamaño de JS transferido: [X] KB" >> optimization_scripts/metrics_before.txt
```

### Después de Optimizar

```bash
# Crear archivo de métricas después
echo "MÉTRICAS DESPUÉS DE OPTIMIZACIÓN" > optimization_scripts/metrics_after.txt
echo "===============================" >> optimization_scripts/metrics_after.txt
echo "" >> optimization_scripts/metrics_after.txt
echo "Fecha: $(date)" >> optimization_scripts/metrics_after.txt
echo "Dispositivo: iPhone 15, iOS 18" >> optimization_scripts/metrics_after.txt
echo "Conexión: [4G/5G/WiFi]" >> optimization_scripts/metrics_after.txt
echo "" >> optimization_scripts/metrics_after.txt
echo "Tiempo de carga (DOMContentLoaded): [X] segundos" >> optimization_scripts/metrics_after.txt
echo "Tiempo de carga total (Load): [X] segundos" >> optimization_scripts/metrics_after.txt
echo "Tamaño de CSS transferido: [X] KB" >> optimization_scripts/metrics_after.txt
echo "Tamaño de JS transferido: [X] KB" >> optimization_scripts/metrics_after.txt
echo "" >> optimization_scripts/metrics_after.txt
echo "MEJORA: -[X] segundos ([X]% reducción)" >> optimization_scripts/metrics_after.txt
```

## 🔧 Estructura de Archivos

```
optimization_scripts/
├── README.md                          # Esta documentación
├── 0_create_snapshot.py               # Script de backup
├── restore_snapshot.py                # Script de restauración
├── phase1_css_optimization.py         # Fase 1: CSS
├── phase2_mobile_optimization.py      # Fase 2: Móvil
├── phase3_lazy_loading.py             # Fase 3: Lazy loading
├── css_duplicates_report.txt          # Reporte de duplicados (generado)
├── metrics_before.txt                 # Métricas antes (manual)
└── metrics_after.txt                  # Métricas después (manual)

optimization_backups/
└── snapshot_YYYYMMDD_HHMMSS/
    ├── manifest.json                  # Manifiesto del backup
    ├── git_diff.patch                 # Diff de git
    ├── src/
    │   └── app.py
    ├── modules/
    │   └── core/
    │       └── auth_system.py
    └── assets/
        ├── *.css
        └── *.js
```

## ⚠️ Troubleshooting

### Problema: Script falla con error de encoding

**Solución:**
```bash
# Asegurarse de que el terminal usa UTF-8
chcp 65001  # En Windows
```

### Problema: CSS no se aplica después de optimización

**Posibles causas:**
1. Caché del navegador → Ctrl+Shift+R (hard reload)
2. Ruta de archivo incorrecta → Verificar que `assets/login.min.css` existe
3. Error en minificación → Revisar `assets/login.min.css` manualmente

**Solución rápida:**
```bash
# Restaurar snapshot
python optimization_scripts/restore_snapshot.py
```

### Problema: La aplicación no carga en Cloud después de subir

**Verificaciones:**
1. ¿Se subieron todos los archivos nuevos?
   ```bash
   git status
   git add assets/*.min.css
   git add optimization_scripts/
   ```

2. ¿Hay errores en los logs de Cloud?
   - Ver logs en Streamlit Cloud dashboard

3. ¿Las rutas de archivos son correctas?
   - En Cloud, usar rutas relativas desde project_root

**Rollback en Cloud:**
```bash
# Revertir commit
git revert HEAD
git push
```

### Problema: El tiempo de carga no mejora significativamente

**Verificaciones:**
1. ¿Se ejecutaron TODAS las fases? (1, 2 y 3)
2. ¿Se está probando con caché limpia? (Ctrl+Shift+R)
3. ¿La conexión es estable? (Probar con WiFi rápido)
4. ¿Streamlit Cloud está lento? (A veces el problema es del servidor)

**Medición correcta:**
- Usar Chrome DevTools → Network tab
- Deshabilitar caché (checkbox "Disable cache")
- Recargar 3 veces y promediar

## 📞 Soporte

Si encuentras problemas:

1. **Revisar logs:** Los scripts imprimen información detallada
2. **Verificar snapshot:** Siempre puedes revertir con `restore_snapshot.py`
3. **Revisar git diff:** `git diff` para ver cambios exactos
4. **Documentar el error:** Capturar mensaje de error completo

## 📝 Notas Adicionales

### Compatibilidad

- **Python**: 3.8+
- **Streamlit**: 1.28+
- **Navegadores**: Chrome 90+, Safari 14+, Firefox 88+

### Mantenimiento Futuro

Si se agregan nuevos archivos CSS:
1. Agregar a `0_create_snapshot.py` en `items_to_backup`
2. Agregar a `phase1_css_optimization.py` en `css_files_to_minify`

### Consideraciones de Cloud

En Streamlit Cloud:
- Los cambios en `assets/` se aplican inmediatamente
- Los cambios en código Python requieren restart
- El caché de navegador puede persistir → instruir a usuarios hacer hard reload

---

**¡Éxito con las optimizaciones! 🚀**
