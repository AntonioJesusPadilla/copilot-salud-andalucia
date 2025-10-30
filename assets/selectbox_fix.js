// ================================================================
// SELECTBOX FIX - Corrección JavaScript para espaciado excesivo
// VERSIÓN: 5.0 - SIN MARCOS + HOVER GRIS
// ================================================================
// Este script fuerza la corrección de estilos inline que CSS
// no puede sobrescribir debido a especificidad
// ================================================================

(function() {
    'use strict';

    // Función para corregir el espaciado de los selectbox
    function fixSelectboxSpacing() {
        // Buscar todos los listbox
        const listboxes = document.querySelectorAll('ul[role="listbox"], div[role="listbox"]');

        listboxes.forEach(listbox => {
            // Corregir el contenedor
            listbox.style.padding = '0';
            listbox.style.margin = '0';
            listbox.style.gap = '0';
            listbox.style.rowGap = '0';

            // Buscar todas las opciones
            const options = listbox.querySelectorAll('li, li[role="option"]');

            options.forEach((option, index) => {
                // CRÍTICO: Desactivar posicionamiento absoluto
                option.style.position = 'relative';
                option.style.top = 'auto';
                option.style.left = 'auto';
                option.style.transform = 'none';

                // Forzar estilos compactos
                option.style.padding = '8px 12px';
                option.style.margin = '0';
                option.style.minHeight = 'auto';
                option.style.maxHeight = 'none';
                option.style.height = 'auto';
                option.style.lineHeight = '1.5';
                option.style.display = 'block';
                option.style.boxSizing = 'border-box';

                // ELIMINAR TODOS LOS BORDES
                option.style.border = 'none';
                option.style.borderTop = 'none';
                option.style.borderRight = 'none';
                option.style.borderBottom = 'none';
                option.style.borderLeft = 'none';
                option.style.borderRadius = '0';
                option.style.outline = 'none';
                option.style.boxShadow = 'none';

                // Forzar colores de hover gris
                const isSelected = option.getAttribute('aria-selected') === 'true';
                if (isSelected) {
                    option.style.backgroundColor = '#10b981';
                    option.style.color = '#ffffff';
                } else {
                    option.style.backgroundColor = '#ffffff';
                    option.style.color = '#0f172a';
                }

                // Agregar evento hover para forzar gris - MÁS AGRESIVO
                option.addEventListener('mouseenter', function() {
                    if (this.getAttribute('aria-selected') !== 'true') {
                        // Log para depuración
                        const computedStyle = window.getComputedStyle(this);
                        console.log('🔍 Hover detectado. Color actual:', computedStyle.backgroundColor);

                        this.style.setProperty('background-color', '#f3f4f6', 'important');
                        this.style.setProperty('color', '#0f172a', 'important');
                        this.style.setProperty('border', 'none', 'important');
                        this.style.setProperty('outline', 'none', 'important');
                        this.style.setProperty('box-shadow', 'none', 'important');

                        console.log('✅ Hover forzado a gris. Nuevo color:', window.getComputedStyle(this).backgroundColor);
                    }
                });

                option.addEventListener('mouseleave', function() {
                    if (this.getAttribute('aria-selected') !== 'true') {
                        this.style.setProperty('background-color', '#ffffff', 'important');
                        this.style.setProperty('color', '#0f172a', 'important');
                        this.style.setProperty('border', 'none', 'important');
                        this.style.setProperty('outline', 'none', 'important');
                        this.style.setProperty('box-shadow', 'none', 'important');
                    }
                });

                // Prevenir focus outline
                option.addEventListener('focus', function() {
                    this.style.setProperty('outline', 'none', 'important');
                    this.style.setProperty('box-shadow', 'none', 'important');
                });

                // Corregir elementos hijos
                const children = option.querySelectorAll('*');
                children.forEach(child => {
                    child.style.padding = '0';
                    child.style.margin = '0';
                    child.style.lineHeight = '1.5';
                    child.style.display = 'inline';
                    child.style.verticalAlign = 'middle';
                    child.style.border = 'none';
                    child.style.backgroundColor = 'transparent';
                });
            });
        });
    }

    // Ejecutar al cargar
    fixSelectboxSpacing();

    // Ejecutar cuando se abra un selectbox (usando MutationObserver)
    const observer = new MutationObserver((mutations) => {
        mutations.forEach((mutation) => {
            if (mutation.addedNodes.length) {
                mutation.addedNodes.forEach((node) => {
                    if (node.nodeType === 1) { // Element node
                        // Si es un listbox o contiene un listbox
                        if (node.matches && (node.matches('[role="listbox"]') ||
                            node.querySelector('[role="listbox"]'))) {
                            setTimeout(fixSelectboxSpacing, 10);
                        }
                    }
                });
            }
        });
    });

    // Observar el document body
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });

    // También ejecutar periódicamente como fallback
    setInterval(fixSelectboxSpacing, 500);

    // AGREGAR ESTILO CRÍTICO AL HEAD CON MÁXIMA PRIORIDAD
    // Este estilo se agrega dinámicamente y tiene la última palabra
    const criticalStyle = document.createElement('style');
    criticalStyle.id = 'selectbox-critical-override';
    criticalStyle.textContent = `
        /* OVERRIDE CRÍTICO - MÁXIMA PRIORIDAD */
        [data-theme="light"] li[role="option"]:hover:not([aria-selected="true"]),
        [data-theme="light"] li[role="option"]:hover:not([aria-selected="true"]) *,
        body li[role="option"]:hover:not([aria-selected="true"]),
        html li[role="option"]:hover:not([aria-selected="true"]) {
            background-color: #f3f4f6 !important;
            color: #0f172a !important;
            border: none !important;
            outline: none !important;
            box-shadow: none !important;
        }

        /* Eliminar todos los bordes */
        li[role="option"],
        ul[role="listbox"] li[role="option"] {
            border: none !important;
            border-top: none !important;
            border-right: none !important;
            border-bottom: none !important;
            border-left: none !important;
            outline: none !important;
            box-shadow: none !important;
        }
    `;
    document.head.appendChild(criticalStyle);

    console.log('✅ Selectbox Fix JavaScript cargado - VERSIÓN 5.0 - SIN MARCOS + HOVER GRIS');
})();
