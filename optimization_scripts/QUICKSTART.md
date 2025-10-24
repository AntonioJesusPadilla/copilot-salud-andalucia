# 🚀 Guía Rápida de Optimización

Esta guía te llevará paso a paso por el proceso de optimización para reducir el tiempo de carga de 8-15 segundos a 2-4 segundos.

## ⏱️ Tiempo Total Estimado: 30-45 minutos

## 📋 Pasos

### Paso 1: Crear Backup (2 min)

```bash
cd C:\Users\Lenovo\Documents\proyectos\copilot-salud-andalucia
python optimization_scripts/0_create_snapshot.py
```

✅ **Verificar:** Debería aparecer un mensaje de éxito con la ubicación del snapshot.

---

### Paso 2: Ejecutar Fase 1 - CSS (5-10 min)

```bash
python optimization_scripts/phase1_css_optimization.py
```

✅ **Verificar:**
1. Se crearon archivos:
   - `assets/login.css`
   - `assets/login.min.css`
   - `assets/style.min.css`
   - `assets/extra_styles.min.css`
   - etc.

2. Probar en local:
   ```bash
   streamlit run src/app.py
   ```

3. Verificar que:
   - [ ] Login se ve correctamente
   - [ ] Toggle tema funciona
   - [ ] No hay errores en consola

**Si algo falla:** `python optimization_scripts/restore_snapshot.py`

---

### Paso 3: Ejecutar Fase 2 - Móvil (5-10 min)

```bash
python optimization_scripts/phase2_mobile_optimization.py
```

✅ **Verificar:**
1. `src/app.py` se actualizó correctamente

2. Probar en local:
   ```bash
   streamlit run src/app.py
   ```

3. Verificar que:
   - [ ] La aplicación carga correctamente
   - [ ] No hay errores en consola

**Si algo falla:** `python optimization_scripts/restore_snapshot.py`

---

### Paso 4: Ejecutar Fase 3 - Lazy Loading (5-10 min)

```bash
python optimization_scripts/phase3_lazy_loading.py
```

✅ **Verificar:**
1. Se generó `optimization_scripts/css_duplicates_report.txt`

2. Probar en local:
   ```bash
   streamlit run src/app.py
   ```

3. Verificar que:
   - [ ] La aplicación carga correctamente
   - [ ] No hay errores en consola

**Si algo falla:** `python optimization_scripts/restore_snapshot.py`

---

### Paso 5: Medir Mejora (5 min)

1. **Abrir Chrome DevTools:**
   - Presionar F12
   - Ir a pestaña "Network"
   - ✅ Marcar "Disable cache"

2. **Recargar la página:**
   - Ctrl + Shift + R (hard reload)

3. **Observar los tiempos:**
   - Buscar la línea azul/roja al final de la carga
   - Ver tiempo de "DOMContentLoaded"

4. **Comparar:**
   - **Antes:** 8-15 segundos
   - **Después:** 2-4 segundos ✅

---

### Paso 6: Testing en iPhone (Opcional, 10 min)

Si tienes un iPhone disponible:

1. **Obtener IP local:**
   ```bash
   ipconfig
   # Buscar "IPv4 Address" en la conexión activa
   ```

2. **Ejecutar Streamlit con IP accesible:**
   ```bash
   streamlit run src/app.py --server.address 0.0.0.0
   ```

3. **Abrir en iPhone:**
   - Safari → `http://192.168.X.X:8501`
   - (Reemplazar X.X con tu IP local)

4. **Verificar:**
   - [ ] Carga rápida (2-4 segundos)
   - [ ] Login funciona
   - [ ] Touch events funcionan
   - [ ] No hay zoom inesperado

---

### Paso 7: Commit y Subir a Cloud (5 min)

Si todo funciona correctamente:

```bash
# Ver cambios
git status

# Agregar archivos
git add .

# Commit
git commit -m "feat: Optimización de rendimiento móvil - Fases 1-3

- Extracción y minificación de CSS (-4-6 seg)
- Detección móvil optimizada y carga condicional (-1.5-2.5 seg)
- Lazy loading y preload hints (-1-2 seg)

Reducción total: 6.5-10.5 segundos
Tiempo de carga: 8-15 seg → 2-4 seg"

# Subir a GitHub
git push origin main
```

**Streamlit Cloud** detectará los cambios automáticamente y desplegará la nueva versión en ~2-3 minutos.

---

## 🆘 Si Algo Sale Mal

### Problema: Script falla con error

**Solución rápida:**
```bash
python optimization_scripts/restore_snapshot.py
```

Esto restaura el sistema al estado anterior a las optimizaciones.

### Problema: La aplicación no carga después de optimizar

**Verificaciones:**
1. ¿Hay errores en la terminal?
2. ¿Se crearon todos los archivos .min.css?
3. ¿El login.css se creó correctamente?

**Solución:**
```bash
# Restaurar snapshot
python optimization_scripts/restore_snapshot.py

# Ejecutar fases una por una y revisar logs
```

### Problema: CSS no se ve correctamente

**Solución:**
```bash
# Hard reload en navegador
Ctrl + Shift + R  (Windows/Linux)
Cmd + Shift + R   (Mac)
```

Si persiste:
```bash
python optimization_scripts/restore_snapshot.py
```

---

## 📊 Checklist Final

Antes de marcar como completado:

- [ ] Snapshot creado exitosamente
- [ ] Fase 1 ejecutada sin errores
- [ ] Fase 2 ejecutada sin errores
- [ ] Fase 3 ejecutada sin errores
- [ ] Testing en local exitoso
- [ ] Tiempo de carga mejorado (medido en Chrome DevTools)
- [ ] Testing en iPhone/móvil (opcional pero recomendado)
- [ ] Commit creado
- [ ] Push a GitHub exitoso
- [ ] Verificación en Streamlit Cloud (después de deploy)

---

## 🎯 Resultados Esperados

| Métrica | Antes | Después | Mejora |
|---------|-------|---------|--------|
| **Tiempo de carga** | 8-15 seg | 2-4 seg | **70-75%** ✅ |
| **CSS transferido** | ~170 KB | ~70 KB | **60%** ✅ |
| **Renders bloqueantes** | Muchos | Pocos | **80%** ✅ |

---

## 📚 Recursos

- **README completo:** `optimization_scripts/README.md`
- **Scripts individuales:** `optimization_scripts/phase*.py`
- **Reporte de duplicados CSS:** `optimization_scripts/css_duplicates_report.txt`

---

**¿Preguntas o problemas?** Revisa el README.md completo para más detalles.

**¡Éxito con la optimización! 🚀**
