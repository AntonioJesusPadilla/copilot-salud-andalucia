/* ===========================================
   DETECTOR Y CORRECTOR PARA SAFARI iOS 26
   =========================================== */

(function() {
    'use strict';

    // Detectar Safari en iOS 26
    function isSafariIOS26() {
        const userAgent = navigator.userAgent;
        const isIOS = /iPad|iPhone|iPod/.test(userAgent) && !window.MSStream;
        const isSafari = /Safari/.test(userAgent) && !/Chrome|CriOS|FxiOS/.test(userAgent);

        // Detectar iOS 26 específicamente
        const iosVersion = userAgent.match(/OS (\d+)_/);
        const isIOS26 = iosVersion && parseInt(iosVersion[1]) >= 26;

        return isIOS && isSafari && isIOS26;
    }

    // Aplicar fixes específicos para Safari iOS 26
    function applySafariIOS26Fixes() {
        console.log('Aplicando correcciones para Safari iOS 26...');

        // Fix 1: Prevenir zoom en inputs
        const inputs = document.querySelectorAll('input[type="text"], input[type="email"], input[type="password"], textarea, select');
        inputs.forEach(input => {
            input.style.fontSize = '16px';
            input.addEventListener('focus', function() {
                this.style.transform = 'translateZ(0)';
            });
        });

        // Fix 2: Mejorar performance de animaciones
        const animatedElements = document.querySelectorAll('.fade-in, .slide-in-right, .slide-in-left');
        animatedElements.forEach(el => {
            el.style.webkitBackfaceVisibility = 'hidden';
            el.style.webkitTransform = 'translateZ(0)';
        });

        // Fix 3: Corregir touch events
        const touchElements = document.querySelectorAll('button, .stButton > button');
        touchElements.forEach(el => {
            el.style.webkitTapHighlightColor = 'transparent';
            el.style.webkitTouchCallout = 'none';
            el.style.touchAction = 'manipulation';
        });

        // Fix 4: Viewport meta tag dinámico
        let viewport = document.querySelector('meta[name="viewport"]');
        if (!viewport) {
            viewport = document.createElement('meta');
            viewport.name = 'viewport';
            document.head.appendChild(viewport);
        }
        viewport.content = 'width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover';

        // Fix 5: Prevenir bounce scroll
        document.body.style.overscrollBehavior = 'none';
        document.documentElement.style.overscrollBehavior = 'none';

        // Fix 6: CSS de emergencia para backdrop-filter
        const style = document.createElement('style');
        style.textContent = `
            @supports not (backdrop-filter: blur(20px)) {
                .main-header, .sidebar-content, .chat-container {
                    background-color: rgba(255, 255, 255, 0.95) !important;
                }
            }
        `;
        document.head.appendChild(style);
    }

    // Fix específico para Streamlit en iOS 26
    function fixStreamlitIOS26() {
        // Observar cambios en el DOM de Streamlit
        const observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                if (mutation.addedNodes.length > 0) {
                    applySafariIOS26Fixes();
                }
            });
        });

        observer.observe(document.body, {
            childList: true,
            subtree: true
        });

        // Fix inicial
        applySafariIOS26Fixes();
    }

    // Ejecutar cuando el DOM esté listo
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            if (isSafariIOS26()) {
                console.log('Safari iOS 26 detectado - Aplicando correcciones...');
                fixStreamlitIOS26();
            }
        });
    } else {
        if (isSafariIOS26()) {
            console.log('Safari iOS 26 detectado - Aplicando correcciones...');
            fixStreamlitIOS26();
        }
    }

    // Fix para errores de carga específicos de iOS 26
    window.addEventListener('error', function(e) {
        if (isSafariIOS26() && e.message.includes('backdrop-filter')) {
            console.warn('Aplicando fallback para backdrop-filter en iOS 26');
            applySafariIOS26Fixes();
        }
    });

})();