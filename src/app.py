import streamlit as st
import os
import sys
from datetime import datetime

# Añadir directorios al path ANTES de importar módulos locales
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
src_dir = os.path.join(project_root, 'src')

# Asegurar que tanto la raíz como src están en el path
for path in [project_root, src_dir]:
    if path not in sys.path:
        sys.path.insert(0, path)

# Debug info comentado para evitar errores en Windows
# print(f"Project root: {project_root}")
# print(f"Source dir: {src_dir}")
# print(f"Python path: {sys.path}")

# ===== CONFIGURACIÓN DE PÁGINA - DEBE SER LO PRIMERO =====
# CRÍTICO: set_page_config DEBE ir antes de cualquier comando st.*

def is_mobile_device():
    """
    Detecta si el usuario está usando un dispositivo móvil
    OPTIMIZADO: Usa st.context cuando está disponible, fallback rápido
    """
    # Cachear resultado en session_state para evitar detecciones repetidas
    if 'device_type_detected' in st.session_state:
        return st.session_state.get('is_mobile_cached', False)

    try:
        # Método optimizado: Intentar obtener user agent de forma rápida
        user_agent = ""

        # Intentar obtener del contexto de Streamlit (más rápido)
        try:
            # En Streamlit >= 1.28, usar st.context
            if hasattr(st, 'context') and hasattr(st.context, 'headers'):
                user_agent = st.context.headers.get("User-Agent", "").lower()
        except:
            pass

        # Fallback: Intentar websocket headers (solo si el anterior falla)
        if not user_agent:
            try:
                import streamlit.web.server.websocket_headers as wsh
                headers = wsh.get_websocket_headers()
                user_agent = headers.get("User-Agent", "").lower()
            except:
                pass

        # Patrones comunes de dispositivos móviles
        mobile_patterns = [
            'iphone', 'ipad', 'ipod',  # iOS
            'android',                  # Android
            'mobile', 'phone',          # Genéricos
        ]

        is_mobile = any(pattern in user_agent for pattern in mobile_patterns)

        # Cachear resultado
        st.session_state.device_type_detected = True
        st.session_state.is_mobile_cached = is_mobile

        return is_mobile

    except Exception as e:
        # Fallback rápido: Asumir desktop si no podemos detectar
        st.session_state.device_type_detected = True
        st.session_state.is_mobile_cached = False
        return False

def is_ios_device():
    """Detectar si el dispositivo es iOS específicamente - MODO SEGURO"""
    try:
        # Cachear resultado para evitar detecciones repetidas
        if 'is_ios_cached' in st.session_state:
            return st.session_state.is_ios_cached

        user_agent = ""

        # Intentar obtener user agent de forma segura
        try:
            if hasattr(st, 'context') and hasattr(st.context, 'headers'):
                user_agent = st.context.headers.get("User-Agent", "").lower()
        except:
            pass

        if not user_agent:
            try:
                import streamlit.web.server.websocket_headers as wsh
                headers = wsh.get_websocket_headers()
                user_agent = headers.get("User-Agent", "").lower() if headers else ""
            except:
                pass

        # Detectar iOS de forma segura
        is_ios = False
        if user_agent:
            is_ios = any(pattern in user_agent for pattern in ['iphone', 'ipad', 'ipod'])

        # Cachear resultado
        st.session_state.is_ios_cached = is_ios
        return is_ios

    except Exception as e:
        # En caso de cualquier error, asumir que NO es iOS
        # Esto es más seguro que romper la app
        try:
            st.session_state.is_ios_cached = False
        except:
            pass
        return False

# Detectar tipo de dispositivo
IS_MOBILE = is_mobile_device()

# Intentar usar favicon personalizado, fallback a emoji
favicon_path = "assets/favicon.ico"
if os.path.exists(favicon_path):
    page_icon = favicon_path
else:
    page_icon = "⚕️"

# Configuración de página adaptativa: wide para desktop, centered para móvil
try:
    st.set_page_config(
        page_title="Copilot Salud Andalucía - Sistema de Análisis Sociosanitario",
        page_icon=page_icon,
        layout="centered" if IS_MOBILE else "wide",  # Adaptativo según dispositivo
        initial_sidebar_state="collapsed" if IS_MOBILE else "expanded",  # Sidebar colapsado en móvil
        menu_items={
            'Get Help': None,
            'Report a bug': None,
            'About': '# Copilot Salud Andalucía v2.1\nSistema de Análisis Sociosanitario de Málaga'
        }
    )
except Exception:
    # Fallback a configuración básica adaptativa
    st.set_page_config(
        page_title="Copilot Salud Andalucía",
        page_icon="⚕️",
        layout="centered" if IS_MOBILE else "wide",
        initial_sidebar_state="collapsed" if IS_MOBILE else "expanded"
    )
# ===== FIN CONFIGURACIÓN DE PÁGINA =====

# ===== SISTEMA DE DETECCIÓN TEMPRANA DE ERRORES PARA iOS =====
# Este código se ejecuta INMEDIATAMENTE después de set_page_config
# para detectar y mostrar errores visibles en lugar de pantalla negra
st.markdown("""
<script>
(function() {
    'use strict';

    // Detectar iOS
    const isIOS = /iPad|iPhone|iPod/.test(navigator.userAgent) && !window.MSStream;

    if (isIOS) {
        console.log('🍎 iOS detectado - Iniciando sistema de detección de errores...');

        // 1. Capturar TODOS los errores JavaScript
        window.addEventListener('error', function(e) {
            console.error('❌ Error JavaScript capturado:', e.message, e.filename, e.lineno);

            // Mostrar error visible en la página
            const errorDiv = document.createElement('div');
            errorDiv.id = 'ios-error-display';
            errorDiv.style.cssText = `
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                background: #ef4444;
                color: white;
                padding: 1rem;
                z-index: 999999;
                font-family: -apple-system, BlinkMacSystemFont, sans-serif;
                font-size: 14px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.3);
            `;
            errorDiv.innerHTML = `
                <strong>⚠️ Error en iOS:</strong> ${e.message}<br>
                <small>Archivo: ${e.filename} | Línea: ${e.lineno}</small><br>
                <small style="opacity: 0.8;">Recarga la página (swipe down) o contacta soporte</small>
            `;

            // Solo agregar si no existe ya
            if (!document.getElementById('ios-error-display')) {
                document.body.appendChild(errorDiv);
            }
        }, true);

        // 2. Detectar si la app no carga en 15 segundos
        let appLoadedSuccessfully = false;

        setTimeout(function() {
            // Verificar si la app cargó detectando elementos Streamlit
            const streamlitElements = document.querySelectorAll('.stApp, [data-testid="stApp"], .main');
            const hasContent = streamlitElements.length > 0 && streamlitElements[0].children.length > 0;

            if (!hasContent && !appLoadedSuccessfully) {
                console.warn('⚠️ La aplicación no ha cargado después de 15 segundos');

                // Mostrar mensaje de carga lenta
                const loadingDiv = document.createElement('div');
                loadingDiv.style.cssText = `
                    position: fixed;
                    top: 50%;
                    left: 50%;
                    transform: translate(-50%, -50%);
                    background: white;
                    padding: 2rem;
                    border-radius: 12px;
                    box-shadow: 0 10px 40px rgba(0,0,0,0.2);
                    z-index: 999998;
                    text-align: center;
                    max-width: 80%;
                `;
                loadingDiv.innerHTML = `
                    <h2 style="color: #1a202c; margin: 0 0 1rem 0;">⏳ Cargando...</h2>
                    <p style="color: #4a5568; margin: 0;">La aplicación está tardando más de lo esperado.</p>
                    <p style="color: #4a5568; margin: 0.5rem 0;">Por favor espera unos segundos más.</p>
                    <div style="margin-top: 1rem; padding: 0.75rem; background: #fef3c7; border-radius: 8px; color: #92400e; font-size: 14px;">
                        💡 Sugerencia: Si tarda demasiado, prueba recargando la página
                    </div>
                `;

                document.body.appendChild(loadingDiv);

                // Ocultar el mensaje después de 10 segundos más
                setTimeout(function() {
                    if (loadingDiv.parentNode) {
                        loadingDiv.remove();
                    }
                }, 10000);
            }
        }, 15000);

        // 3. Marcar como cargado cuando Streamlit esté listo
        const checkStreamlitLoaded = setInterval(function() {
            const streamlitApp = document.querySelector('.stApp, [data-testid="stApp"]');
            if (streamlitApp && streamlitApp.children.length > 0) {
                appLoadedSuccessfully = true;
                console.log('✅ Streamlit cargado correctamente en iOS');
                clearInterval(checkStreamlitLoaded);
            }
        }, 500);

        // Limpiar el intervalo después de 30 segundos
        setTimeout(function() {
            clearInterval(checkStreamlitLoaded);
        }, 30000);

        // 4. Fix rápido de viewport para evitar pantalla negra
        try {
            let viewport = document.querySelector('meta[name="viewport"]');
            if (!viewport) {
                viewport = document.createElement('meta');
                viewport.name = 'viewport';
                document.head.appendChild(viewport);
            }
            viewport.content = 'width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes, viewport-fit=cover';

            // Fix de altura mínima para evitar colapso visual
            document.documentElement.style.minHeight = '100vh';
            document.body.style.minHeight = '100vh';

            console.log('✅ Viewport y altura mínima configurados para iOS');
        } catch(e) {
            console.error('❌ Error configurando viewport iOS:', e);
        }
    }
})();
</script>
""", unsafe_allow_html=True)
# ===== FIN SISTEMA DE DETECCIÓN DE ERRORES iOS =====

# Imports críticos y ligeros primero
# Debug info (comentado para evitar errores en reruns)
# print(f"Project root: {project_root}")
# print(f"Source dir: {src_dir}")
# print(f"Python path: {repr(sys.path)}")

# OPTIMIZACIÓN MÓVIL: Cargar módulos pesados solo cuando sea necesario
if IS_MOBILE:
    # print("📱 Dispositivo móvil detectado - carga optimizada de módulos")
    # En móvil, importar solo lo esencial
    from modules.ai.streamlit_async_wrapper import get_streamlit_async_wrapper
else:
    # print("💻 Dispositivo desktop detectado - carga completa de módulos")
    pass
    # En desktop, importar todo desde el inicio
    import pandas as pd
    import numpy as np
    import plotly.express as px
    import plotly.graph_objects as go
    import plotly.io as pio
    from io import StringIO
    from modules.ai.streamlit_async_wrapper import get_streamlit_async_wrapper

    # CONFIGURACIÓN GLOBAL DE PLOTLY: Deshabilitar hover por defecto
    pio.templates.default = "plotly"

# Imports comunes (ligeros) - necesarios para todos los dispositivos
import re
# NOTA: option_menu se importa lazy después del login para evitar errores de registro

# Cargar variables de entorno
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Importar sistema de autenticación
try:
    from modules.core.auth_system import (
        check_authentication, render_login_page, logout,
        render_user_management, render_user_profile, HealthAuthenticator
    )
    AUTH_AVAILABLE = True
except ImportError as e:
    print(f"❌ Error importando sistema de autenticación: {str(e)}")
    AUTH_AVAILABLE = False

# ===== LAZY LOADING DE MÓDULOS PESADOS =====
# Cache para módulos cargados dinámicamente
_lazy_modules_cache = {}

def lazy_import_data_modules():
    """Lazy loading de pandas, numpy y plotly - solo cuando se necesiten"""
    if 'data_modules' not in _lazy_modules_cache:
        print("📦 Cargando módulos de datos (pandas, numpy, plotly)...")
        import pandas as pd
        import numpy as np
        import plotly.express as px
        import plotly.graph_objects as go
        import plotly.io as pio
        from io import StringIO

        # Configuración de plotly
        pio.templates.default = "plotly"

        _lazy_modules_cache['data_modules'] = {
            'pd': pd, 'np': np, 'px': px, 'go': go, 'pio': pio, 'StringIO': StringIO
        }
        print("✅ Módulos de datos cargados")
    return _lazy_modules_cache['data_modules']

def lazy_import_ai_modules():
    """Lazy loading de módulos de IA - solo cuando se necesiten"""
    if 'ai_modules' not in _lazy_modules_cache:
        print("🤖 Cargando módulos de IA...")
        try:
            from modules.ai.ai_processor import HealthAnalyticsAI, HealthMetricsCalculator
            from modules.visualization.chart_generator import SmartChartGenerator, DataAnalyzer
            _lazy_modules_cache['ai_modules'] = {
                'HealthAnalyticsAI': HealthAnalyticsAI,
                'HealthMetricsCalculator': HealthMetricsCalculator,
                'SmartChartGenerator': SmartChartGenerator,
                'DataAnalyzer': DataAnalyzer
            }
            print("✅ Módulos de IA cargados")
            return _lazy_modules_cache['ai_modules']
        except ImportError as e:
            print(f"❌ Error importando módulos IA: {str(e)}")
            return None
    return _lazy_modules_cache['ai_modules']

# Importar módulos IA solo si NO es móvil (para desktop sí cargar al inicio)
if not IS_MOBILE:
    try:
        from modules.ai.ai_processor import HealthAnalyticsAI, HealthMetricsCalculator
        from modules.visualization.chart_generator import SmartChartGenerator, DataAnalyzer
        AI_AVAILABLE = True
    except ImportError as e:
        print(f"❌ Error importando módulos IA: {str(e)}")
        AI_AVAILABLE = False
else:
    # En móvil, marcar como disponible pero NO importar aún (usar lazy loading)
    AI_AVAILABLE = True

# Importar módulos de mapas (opcional para Streamlit Cloud y diferido en móvil)
if not IS_MOBILE:
    try:
        import importlib
        import sys

        # Verificar dependencias básicas de mapas
        try:
            import folium
            import streamlit_folium
            # Test adicional: verificar que el módulo local existe
            from modules.visualization.map_interface import MapInterface

            MAPS_DEPENDENCIES_OK = True
            print("✅ GLOBAL INIT: Dependencias de mapas encontradas: folium, streamlit_folium, MapInterface")
        except ImportError as deps_error:
            print(f"❌ GLOBAL INIT: Dependencias de mapas no disponibles: {str(deps_error)}")
            # NO mostrar warning en la UI durante la inicialización global
            MAPS_DEPENDENCIES_OK = False

        # Carga diferida de mapas - solo marcar disponibilidad
        MAPS_AVAILABLE = MAPS_DEPENDENCIES_OK
        print(f"🔧 GLOBAL INIT: MAPS_AVAILABLE establecido en: {MAPS_AVAILABLE}")
        print(f"🔧 GLOBAL INIT: MAPS_DEPENDENCIES_OK es: {MAPS_DEPENDENCIES_OK}")

        # Si las dependencias no están disponibles globalmente, intentar verificación diferida
        if not MAPS_DEPENDENCIES_OK:
            print("⚠️ GLOBAL INIT: Dependencias no disponibles globalmente, se intentará carga diferida")

    except Exception as e:
        print(f"❌ GLOBAL INIT: Excepción en bloque de mapas: {str(e)}")
        # NO mostrar warning en la UI durante la inicialización global
        MAPS_AVAILABLE = False
        MAPS_DEPENDENCIES_OK = False
        print("🔧 GLOBAL INIT: MAPS_AVAILABLE y MAPS_DEPENDENCIES_OK establecidos en False por excepción")
else:
    # En móvil, diferir carga de mapas hasta que se necesite
    print("📱 Móvil: Diferir carga de módulos de mapas")
    MAPS_AVAILABLE = True
    MAPS_DEPENDENCIES_OK = False

# Importar dashboards personalizados por rol
try:
    from modules.core.role_dashboards import RoleDashboards
    ROLE_DASHBOARDS_AVAILABLE = True
except ImportError as e:
    print(f"❌ Error importando dashboards por rol: {str(e)}")
    ROLE_DASHBOARDS_AVAILABLE = False

# Importar sistemas de optimización y seguridad
try:
    from modules.performance.performance_optimizer import get_performance_optimizer, PerformanceOptimizer
    from modules.security.security_auditor import get_security_auditor, SecurityAuditor
    from modules.security.rate_limiter import get_rate_limiter, RateLimiter
    from modules.security.data_encryption import get_data_encryption, DataEncryption
    OPTIMIZATION_AVAILABLE = True
except ImportError as e:
    st.error(f"❌ Error importando sistemas de optimización: {str(e)}")
    OPTIMIZATION_AVAILABLE = False

# Cargar variables de entorno
load_dotenv()

# Comprobar si reportlab está disponible para generación de PDF
try:
    import reportlab
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas as rl_canvas
    REPORTLAB_AVAILABLE = True
    REPORTLAB_IMPORT_ERROR = None
except Exception as e:
    REPORTLAB_AVAILABLE = False
    REPORTLAB_IMPORT_ERROR = str(e)

def create_pdf_bytes(title: str, text: str, use_simple_header: bool = False) -> bytes:
    """Genera un PDF profesional y elegante usando ReportLab Platypus.

    Características mejoradas:
    - Diseño profesional con cabecera corporativa
    - Estilos tipográficos elegantes y consistentes
    - Detección inteligente de secciones y tablas
    - Formateo automático de contenido markdown
    - Espaciado y disposición optimizada
    - Pie de página con información contextual
    """
    if not REPORTLAB_AVAILABLE:
        raise RuntimeError(f"reportlab no disponible: {REPORTLAB_IMPORT_ERROR}")

    from io import BytesIO
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table as RLTable, TableStyle, PageBreak
    from reportlab.lib.units import mm
    from reportlab.lib import colors
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.utils import ImageReader
    import os
    import re

    buffer = BytesIO()

    left_margin = 18 * mm
    right_margin = 18 * mm
    top_margin = 22 * mm
    bottom_margin = 18 * mm

    doc = SimpleDocTemplate(buffer, pagesize=A4,
                            rightMargin=right_margin, leftMargin=left_margin,
                            topMargin=top_margin, bottomMargin=bottom_margin)
    # Añadir el modo de header como atributo del documento
    doc.simple_header = use_simple_header

    # Registrar fuentes TTF si existen en assets/fonts/
    font_name = 'Helvetica'
    assets_fonts_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'fonts')
    try:
        if os.path.isdir(assets_fonts_dir):
            # Buscar una fuente preferente
            for fname in os.listdir(assets_fonts_dir):
                if fname.lower().endswith('.ttf'):
                    font_path = os.path.join(assets_fonts_dir, fname)
                    try:
                        pdfmetrics.registerFont(TTFont('CustomFont', font_path))
                        font_name = 'CustomFont'
                        break
                    except Exception:
                        continue
    except Exception:
        pass

    styles = getSampleStyleSheet()

    # Estilos profesionales corporativos mejorados
    main_title_style = ParagraphStyle(
        'MainTitle', parent=styles['Heading1'],
        fontName=font_name if font_name else 'Helvetica-Bold',
        fontSize=24, leading=28,
        spaceAfter=16, spaceBefore=8,
        textColor=colors.white,
        backColor=colors.HexColor('#3b82f6'),
        borderWidth=1, borderColor=colors.HexColor('#1e40af'),
        borderRadius=6,
        leftIndent=16, rightIndent=16,
        alignment=1  # Center
    )

    title_style = ParagraphStyle(
        'ProfessionalTitle', parent=styles['Heading1'],
        fontName=font_name if font_name else 'Helvetica-Bold',
        fontSize=20, leading=24,
        spaceAfter=12, spaceBefore=10,
        textColor=colors.HexColor('#1e40af'),
        backColor=colors.HexColor('#dbeafe'),
        borderWidth=1, borderColor=colors.HexColor('#3b82f6'),
        borderRadius=4,
        leftIndent=12, rightIndent=12,
        alignment=0  # Left align
    )

    subtitle_style = ParagraphStyle(
        'ProfessionalSubtitle', parent=styles['Heading2'],
        fontName=font_name if font_name else 'Helvetica-Bold',
        fontSize=16, leading=20,
        spaceBefore=12, spaceAfter=8,
        textColor=colors.HexColor('#1e293b'),
        backColor=colors.HexColor('#f8fafc'),
        borderWidth=0, borderColor=colors.HexColor('#e2e8f0'),
        borderRadius=3,
        leftIndent=10, rightIndent=10,
        alignment=0
    )

    heading_style = ParagraphStyle(
        'ProfessionalHeading', parent=styles['Heading3'],
        fontName=font_name if font_name else 'Helvetica-Bold',
        fontSize=14, leading=17,
        spaceBefore=10, spaceAfter=6,
        textColor=colors.HexColor('#334155'),
        backColor=colors.HexColor('#f1f5f9'),
        leftIndent=8, rightIndent=8
    )

    body_style = ParagraphStyle(
        'ProfessionalBody', parent=styles['BodyText'],
        fontName=font_name if font_name else 'Helvetica',
        fontSize=11, leading=15,
        spaceBefore=4, spaceAfter=6,
        textColor=colors.HexColor('#374151'),
        alignment=4,  # Justify
        leftIndent=0, rightIndent=0
    )

    important_style = ParagraphStyle(
        'ImportantBox', parent=body_style,
        backColor=colors.HexColor('#fef3c7'),
        borderColor=colors.HexColor('#f59e0b'),
        borderWidth=1, borderRadius=4,
        leftIndent=14, rightIndent=14,
        spaceBefore=8, spaceAfter=8,
        textColor=colors.HexColor('#92400e')
    )

    recommendation_style = ParagraphStyle(
        'RecommendationBox', parent=body_style,
        backColor=colors.HexColor('#dcfce7'),
        borderColor=colors.HexColor('#16a34a'),
        borderWidth=1, borderRadius=4,
        leftIndent=14, rightIndent=14,
        spaceBefore=8, spaceAfter=8,
        textColor=colors.HexColor('#166534')
    )

    conclusion_style = ParagraphStyle(
        'ConclusionBox', parent=body_style,
        backColor=colors.HexColor('#eff6ff'),
        borderColor=colors.HexColor('#3b82f6'),
        borderWidth=1, borderRadius=4,
        leftIndent=14, rightIndent=14,
        spaceBefore=8, spaceAfter=8,
        textColor=colors.HexColor('#1e40af')
    )

    highlight_style = ParagraphStyle(
        'HighlightBox', parent=body_style,
        backColor=colors.HexColor('#dbeafe'),
        borderColor=colors.HexColor('#3b82f6'),
        borderWidth=1, borderRadius=4,
        leftIndent=12, rightIndent=12,
        spaceBefore=6, spaceAfter=6,
        textColor=colors.HexColor('#1e40af'),
        fontName=font_name if font_name else 'Helvetica-Bold'
    )

    list_style = ParagraphStyle(
        'ListItem', parent=body_style,
        leftIndent=20, rightIndent=0,
        spaceBefore=2, spaceAfter=2,
        bulletIndent=12,
        bulletFontName=font_name if font_name else 'Helvetica-Bold',
        bulletColor=colors.HexColor('#3b82f6')
    )

    small_style = ParagraphStyle(
        'SmallText', parent=styles['BodyText'],
        fontName=font_name if font_name else 'Helvetica',
        fontSize=9, leading=11,
        textColor=colors.HexColor('#64748b'),
        spaceBefore=2, spaceAfter=2
    )

    story = []

    # Helper: dibujar header/footer
    def _header_footer(canvas, doc):
        # Debug print para verificar el modo de header
        print(f"Generating header with simple_mode: {doc.simple_header}")
        canvas.saveState()
        width, height = A4
        # Logo en la izquierda si existe
        try:
            logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'logo.png')
            if os.path.exists(logo_path):
                img = ImageReader(logo_path)
                img_w = 36
                img_h = 36
                canvas.drawImage(img, left_margin, height - top_margin + 6, width=img_w, height=img_h, preserveAspectRatio=True, mask='auto')
        except Exception:
            pass

            # Elegir entre header simple o mejorado
            try:
                if doc.simple_header:
                    # Header simple minimalista en rojo
                    canvas.setFont(font_name if font_name else 'Helvetica', 12)
                    canvas.setFillColor(colors.HexColor('#FF0000'))  # Rojo
                    canvas.drawString(left_margin, height - top_margin + 12, "VERSIÓN SIMPLE")
                    canvas.setFont(font_name if font_name else 'Helvetica-Bold', 14)
                    canvas.drawString(left_margin, height - top_margin + 30, title)
                    
                    # Línea roja gruesa
                    canvas.setStrokeColor(colors.red)
                    canvas.setLineWidth(2)
                    canvas.line(left_margin, height - top_margin + 4, width - right_margin, height - top_margin + 4)
                else:
                    # Header profesional con diseño médico/sanitario
                    header_h = 75

                    # Fondo degradado azul médico
                    canvas.setFillColor(colors.HexColor('#1e40af'))  # Azul médico principal
                    canvas.rect(0, height - top_margin - header_h + 4, width, header_h, fill=1, stroke=0)

                    # Franja decorativa lateral
                    canvas.setFillColor(colors.HexColor('#0ea5e9'))  # Azul claro
                    canvas.rect(0, height - top_margin - header_h + 4, 8, header_h, fill=1, stroke=0)

                    # Logo/símbolo médico (cruz)
                    canvas.setFillColor(colors.white)
                    cross_x = left_margin + 15
                    cross_y = height - top_margin - 15
                    # Cruz médica estilizada
                    canvas.rect(cross_x - 1, cross_y - 8, 2, 16, fill=1, stroke=0)
                    canvas.rect(cross_x - 6, cross_y - 1, 12, 2, fill=1, stroke=0)

                    # Título principal con tipografía elegante
                    canvas.setFont(font_name if font_name else 'Helvetica-Bold', 18)
                    canvas.setFillColor(colors.white)
                    canvas.drawString(left_margin + 35, height - top_margin - 8, title)

                    # Subtítulo descriptivo
                    canvas.setFont(font_name if font_name else 'Helvetica', 11)
                    canvas.setFillColor(colors.HexColor('#bfdbfe'))
                    canvas.drawString(left_margin + 35, height - top_margin - 25, "Sistema de Análisis Sanitario - Copilot Salud Andalucía")

                    # Información contextual
                    canvas.setFont(font_name if font_name else 'Helvetica', 9)
                    canvas.setFillColor(colors.HexColor('#93c5fd'))
                    fecha = datetime.now().strftime("%d de %B de %Y - %H:%M")
                    canvas.drawString(left_margin + 35, height - top_margin - 40, f"Generado: {fecha}")

                    # Línea decorativa inferior
                    canvas.setStrokeColor(colors.HexColor('#0ea5e9'))
                    canvas.setLineWidth(2)
                    canvas.line(left_margin, height - top_margin - header_h + 2, width - right_margin, height - top_margin - header_h + 2)
            except Exception:
                # Fallback ultra simple
                canvas.setFont(font_name if font_name else 'Helvetica-Bold', 12)
                canvas.setFillColor(colors.black)
                canvas.drawString(left_margin, height - top_margin + 18, title)        # Línea separadora
        canvas.setStrokeColor(colors.grey)
        canvas.setLineWidth(0.5)
        canvas.line(left_margin, height - top_margin + 4, width - right_margin, height - top_margin + 4)

        # Footer con paginado
        canvas.setFont(font_name if font_name else 'Helvetica', 8)
        canvas.setFillColor(colors.grey)
        page_num_text = f"Página {canvas.getPageNumber()}"
        canvas.drawRightString(width - right_margin, bottom_margin - 6, page_num_text)
        canvas.restoreState()

    # Añadir encabezado inicial visual en el story
    story.append(Paragraph(title, title_style))
    story.append(Spacer(1, 6))

    # Detectar bloques de tablas Markdown y procesar el texto en bloques intercalados
    lines = text.split('\n')
    blocks = []
    cur_table = []
    cur_text = []
    def flush_text():
        nonlocal cur_text
        if cur_text:
            blocks.append(('text', '\n'.join(cur_text).strip()))
            cur_text = []
    def flush_table():
        nonlocal cur_table
        if cur_table:
            blocks.append(('table', list(cur_table)))
            cur_table = []

    for line in lines:
        if line.strip().startswith('|') and '|' in line:
            # parte de tabla
            if cur_text:
                flush_text()
            cur_table.append(line)
        else:
            if cur_table:
                flush_table()
            cur_text.append(line)
    flush_table()
    flush_text()

    # Procesar bloques y añadir al story con estilos profesionales
    for btype, content in blocks:
        if btype == 'text':
            # Procesar línea a línea con detección inteligente de contenido
            for line in content.split('\n'):
                ln = line.strip()
                if not ln:
                    # Espacio entre párrafos
                    story.append(Spacer(1, 3))
                    continue

                # Encabezados con estilos específicos
                if ln.startswith('# '):
                    content_text = ln[2:].strip()
                    story.append(Paragraph(content_text, main_title_style))
                    story.append(Spacer(1, 6))
                    continue
                elif ln.startswith('## '):
                    content_text = ln[3:].strip()
                    story.append(Paragraph(content_text, title_style))
                    story.append(Spacer(1, 4))
                    continue
                elif ln.startswith('### '):
                    content_text = ln[4:].strip()
                    story.append(Paragraph(content_text, subtitle_style))
                    story.append(Spacer(1, 3))
                    continue

                # Detección de contenido importante y aplicación de estilos
                ln_lower = ln.lower()

                # Contenido con formato especial para información importante
                if ln.startswith('**') and ln.endswith('**'):
                    content_text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", ln)
                    story.append(Paragraph(content_text, highlight_style))
                    continue

                # Listas con viñetas usando el estilo de lista
                elif ln.startswith('- ') or ln.startswith('* '):
                    item = ln[2:].strip()
                    # Reemplazar markdown en línea
                    item = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", item)
                    item = re.sub(r"\*(.+?)\*", r"<i>\1</i>", item)
                    story.append(Paragraph(f"• {item}", list_style))
                    continue

                # Listas numeradas
                elif re.match(r"^\d+\.\s+", ln):
                    ln_repl = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", ln)
                    ln_repl = re.sub(r"\*(.+?)\*", r"<i>\1</i>", ln_repl)
                    story.append(Paragraph(ln_repl, list_style))
                    continue

                # Contenido importante (alertas)
                elif any(word in ln_lower for word in ['importante', 'clave', 'crítico', 'esencial', 'alerta', 'atención']):
                    # Agregar icono de alerta
                    content_text = f"⚠️ {ln}"
                    content_text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", content_text)
                    story.append(Paragraph(content_text, important_style))
                    continue

                # Recomendaciones
                elif any(word in ln_lower for word in ['recomendación', 'sugerencia', 'mejora', 'optimización', 'propuesta']):
                    content_text = f"💡 {ln}"
                    content_text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", content_text)
                    story.append(Paragraph(content_text, recommendation_style))
                    continue

                # Conclusiones y resultados
                elif any(word in ln_lower for word in ['conclusión', 'resultado', 'hallazgo', 'resumen', 'balance']):
                    content_text = f"📋 {ln}"
                    content_text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", content_text)
                    story.append(Paragraph(content_text, conclusion_style))
                    continue

                # Párrafo normal con procesamiento de markdown
                else:
                    safe = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", ln)
                    safe = re.sub(r"\*(.+?)\*", r"<i>\1</i>", safe)
                    # Mejorar espaciado
                    safe = safe.replace('  ', ' ')
                    if safe:  # Solo agregar si no está vacío
                        story.append(Paragraph(safe, body_style))

            story.append(Spacer(1, 4))
        elif btype == 'table':
            # Parsear tabla Markdown
            try:
                rows = []
                for r in content:
                    # eliminar barras iniciales/finales y split
                    cols = [c.strip() for c in r.strip().strip('|').split('|')]
                    rows.append(cols)
                # Si la segunda fila es separador ---|---, quitarla
                if len(rows) > 1 and all(set(cell) <= set('-: ') for cell in rows[1]):
                    # eliminar fila 1
                    rows.pop(1)
                # Crear tabla profesional con estilo corporativo
                tbl = RLTable(rows, hAlign='CENTER')
                tbl.setStyle(TableStyle([
                    # Cabecera con estilo corporativo
                    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#3b82f6')),
                    ('TEXTCOLOR', (0,0), (-1,0), colors.white),
                    ('FONTNAME', (0,0), (-1,0), font_name if font_name else 'Helvetica-Bold'),
                    ('FONTSIZE', (0,0), (-1,0), 12),

                    # Filas alternadas para mejor legibilidad
                    ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#f8fafc')),
                    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f1f5f9')]),

                    # Estilo de contenido
                    ('FONTNAME', (0,1), (-1,-1), font_name if font_name else 'Helvetica'),
                    ('FONTSIZE', (0,1), (-1,-1), 10),
                    ('TEXTCOLOR', (0,1), (-1,-1), colors.HexColor('#374151')),

                    # Bordes y alineación
                    ('GRID', (0,0), (-1,-1), 1, colors.HexColor('#e5e7eb')),
                    ('LINEBELOW', (0,0), (-1,0), 2, colors.HexColor('#1e40af')),
                    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),

                    # Espaciado interno mejorado
                    ('LEFTPADDING', (0,0), (-1,-1), 8),
                    ('RIGHTPADDING', (0,0), (-1,-1), 8),
                    ('TOPPADDING', (0,0), (-1,-1), 6),
                    ('BOTTOMPADDING', (0,0), (-1,-1), 6),

                    # Sombra sutil para la tabla
                    ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#d1d5db')),
                ]))

                # Agregar título para la tabla
                story.append(Paragraph("📊 Tabla de Datos", subtitle_style))
                story.append(Spacer(1, 4))
                story.append(tbl)
                story.append(Spacer(1, 10))
            except Exception:
                # En caso de error, insertar como texto
                story.append(Paragraph('\n'.join(content), body_style))
                story.append(Spacer(1, 6))

    # Agregar pie de página profesional al documento
    story.append(Spacer(1, 20))

    # Línea separadora elegante
    footer_separator = Paragraph(
        '<para align="center">═══════════════════════════════════════════════════</para>',
        ParagraphStyle('FooterSeparator', parent=small_style, textColor=colors.HexColor('#9ca3af'))
    )
    story.append(footer_separator)
    story.append(Spacer(1, 8))

    # Información del documento
    footer_info = f"""
    <para align="center">
    <b>📋 Documento generado por Copilot Salud Andalucía</b><br/>
    Sistema de Análisis Inteligente para la Gestión Sanitaria<br/>
    <i>Provincia de Málaga - {datetime.now().strftime('%d de %B de %Y')}</i><br/>
    </para>
    """
    story.append(Paragraph(footer_info, small_style))
    story.append(Spacer(1, 6))

    # Información técnica
    technical_info = f"""
    <para align="center">
    <font color="#64748b" size="8">
    Generado con ReportLab • Formato PDF Profesional<br/>
    © 2025 Sistema Sanitario Andaluz - Uso Interno
    </font>
    </para>
    """
    story.append(Paragraph(technical_info, small_style))

    # Construir el documento con header/footer profesional
    doc.build(story, onFirstPage=_header_footer, onLaterPages=_header_footer)
    buffer.seek(0)
    return buffer.read()

def load_health_datasets_optimized(user_role: str = "invitado"):
    """Cargar datasets de salud con optimización avanzada por rol"""
    if not OPTIMIZATION_AVAILABLE:
        st.warning("⚠️ Sistema de optimización no disponible, usando carga estándar")
        return load_health_datasets_legacy()
    
    try:
        # Obtener optimizador de rendimiento
        optimizer = get_performance_optimizer()
        
        # Usar cache inteligente por rol
        @optimizer.cached_data_loader(user_role, "load_datasets")
        def _load_datasets():
            return optimizer.load_health_datasets_optimized(user_role)
        
        return _load_datasets()
        
    except Exception as e:
        st.error(f"❌ Error en carga optimizada: {str(e)}")
        return load_health_datasets_legacy()

@st.cache_data(ttl=3600)
def load_health_datasets_legacy():
    """Cargar datasets de salud con optimización básica (fallback)"""
    try:
        datasets = {}
        file_mapping = {
            'hospitales': 'data/raw/hospitales_malaga_2025.csv',
            'demografia': 'data/raw/demografia_malaga_2025.csv', 
            'servicios': 'data/raw/servicios_sanitarios_2025.csv',
            'accesibilidad': 'data/raw/accesibilidad_sanitaria_2025.csv',
            'indicadores': 'data/raw/indicadores_salud_2025.csv'
        }
        
        # Contador de archivos cargados para progreso
        loaded_files = 0
        total_files = len(file_mapping)
        
        for key, filepath in file_mapping.items():
            if os.path.exists(filepath):
                try:
                    # Optimización: usar dtype específicos para reducir memoria
                    if key == 'demografia':
                        datasets[key] = pd.read_csv(filepath, dtype={
                            'municipio': 'string',
                            'poblacion_2025': 'int32',
                            'poblacion_2024': 'int32',
                            'crecimiento_2024_2025': 'int16',
                            'densidad_hab_km2_2025': 'float32',
                            'renta_per_capita_2024': 'float32',
                            'indice_envejecimiento_2025': 'float32'
                        })
                    elif key == 'hospitales':
                        datasets[key] = pd.read_csv(filepath, dtype={
                            'nombre': 'string',
                            'tipo_centro': 'string',
                            'distrito_sanitario': 'string',
                            'camas_funcionamiento_2025': 'int16',
                            'personal_sanitario_2025': 'int16',
                            'poblacion_referencia_2025': 'int32'
                        })
                    else:
                        # Carga estándar para otros archivos
                        datasets[key] = pd.read_csv(filepath)
                    
                    loaded_files += 1
                    
                except Exception as file_error:
                    st.warning(f"⚠️ Error cargando {filepath}: {str(file_error)}")
            else:
                st.warning(f"⚠️ Archivo no encontrado: {filepath}")
        
        if datasets:
            st.success(f"✅ Cargados {loaded_files}/{total_files} datasets correctamente")
            return datasets
        else:
            st.error("❌ No se pudieron cargar los datasets")
            return None
        
    except Exception as e:
        st.error(f"❌ Error crítico cargando datasets: {str(e)}")
        return None

# NOTA: set_page_config ya se configuró al inicio del archivo (línea ~45)
# para asegurar que se ejecuta ANTES de cualquier otro comando de Streamlit

# ===== ESTILOS CRÍTICOS - APLICAR INMEDIATAMENTE =====
st.markdown("""
<style>
/* CRÍTICO 1: Texto blanco en tarjeta de sidebar - FORZAR */
.sidebar-user-card,
.sidebar-user-card *,
.sidebar-user-card strong,
.sidebar-user-card small,
.sidebar-user-card div,
section[data-testid="stSidebar"] .sidebar-user-card *,
section[data-testid="stSidebar"] .sidebar-user-card strong,
section[data-testid="stSidebar"] .sidebar-user-card small {
    color: #ffffff !important;
    text-shadow: 0 2px 4px rgba(0,0,0,0.7) !important;
}

/* CRÍTICO 2: Tooltips/Help con fondo blanco y texto negro - SIEMPRE */
.stTooltipIcon,
[data-testid="stTooltipHoverTarget"],
[role="tooltip"],
.stTooltipContent,
div[data-baseweb="tooltip"],
[data-theme="light"] [role="tooltip"],
[data-theme="light"] div[data-baseweb="tooltip"],
[data-theme="dark"] [role="tooltip"],
[data-theme="dark"] div[data-baseweb="tooltip"] {
    background: #ffffff !important;
    color: #0f172a !important;
    border: 1px solid #cbd5e1 !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2) !important;
}

[role="tooltip"] *,
.stTooltipContent *,
div[data-baseweb="tooltip"] *,
[data-theme="light"] [role="tooltip"] *,
[data-theme="light"] div[data-baseweb="tooltip"] *,
[data-theme="dark"] [role="tooltip"] *,
[data-theme="dark"] div[data-baseweb="tooltip"] *,
[data-theme="dark"] [role="tooltip"] span,
[data-theme="dark"] div[data-baseweb="tooltip"] span,
[data-theme="dark"] [role="tooltip"] p,
[data-theme="dark"] div[data-baseweb="tooltip"] p,
[data-theme="dark"] [role="tooltip"] div,
[data-theme="dark"] div[data-baseweb="tooltip"] div {
    color: #0f172a !important;
    background: transparent !important;
}

/* CRÍTICO 3: Expansión del sidebar cuando se colapsa - SOLO CSS */
/* Forzar el sidebar a colapsarse completamente */
section[data-testid="stSidebar"][aria-expanded="false"] {
    width: 0 !important;
    min-width: 0 !important;
    max-width: 0 !important;
    overflow: hidden !important;
    padding: 0 !important;
    margin: 0 !important;
}

section[data-testid="stSidebar"][aria-expanded="false"] > div {
    width: 0 !important;
    min-width: 0 !important;
    overflow: hidden !important;
}

/* Cuando aria-expanded="false" el sidebar está COLAPSADO */
section[data-testid="stSidebar"][aria-expanded="false"] ~ section[data-testid="stMain"] {
    margin-left: 0 !important;
    width: 100% !important;
    max-width: 100% !important;
}

section[data-testid="stSidebar"][aria-expanded="false"] ~ section[data-testid="stMain"] .main .block-container {
    max-width: calc(100vw - 4rem) !important;
    width: calc(100vw - 4rem) !important;
    margin-left: 0 !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
}

/* Cuando aria-expanded="true" el sidebar está EXPANDIDO */
section[data-testid="stSidebar"][aria-expanded="true"] {
    width: 21rem !important;
    min-width: 21rem !important;
    max-width: 21rem !important;
}

section[data-testid="stSidebar"][aria-expanded="true"] ~ section[data-testid="stMain"] .main .block-container {
    max-width: calc(100vw - 21rem - 4rem) !important;
    width: calc(100vw - 21rem - 4rem) !important;
}

/* Transiciones suaves */
section[data-testid="stSidebar"],
section[data-testid="stMain"],
.main,
.main .block-container {
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
}

/* CRÍTICO 4: Fix Streamlit toolbar/header buttons in dark mode */
[data-theme="dark"] header[data-testid="stHeader"],
[data-theme="dark"] div[data-testid="stToolbar"],
[data-theme="dark"] header[data-testid="stHeader"] button,
[data-theme="dark"] div[data-testid="stToolbar"] button {
    background: #1e293b !important;
    color: #f8fafc !important;
}

[data-theme="dark"] header[data-testid="stHeader"] button:hover,
[data-theme="dark"] div[data-testid="stToolbar"] button:hover {
    background: #334155 !important;
    color: #ffffff !important;
}

[data-theme="dark"] header[data-testid="stHeader"] svg,
[data-theme="dark"] div[data-testid="stToolbar"] svg {
    fill: #f8fafc !important;
    stroke: #f8fafc !important;
}

/* CRÍTICO 5: Fix selectbox dropdown visibility in dark mode */
[data-theme="dark"] [role="listbox"],
[data-theme="dark"] [data-baseweb="menu"],
[data-theme="dark"] [data-baseweb="popover"],
[data-theme="dark"] ul[role="listbox"] {
    background: #1e293b !important;
    border: 1px solid #6b7280 !important;
}

[data-theme="dark"] [role="option"],
[data-theme="dark"] li[role="option"],
[data-theme="dark"] [data-baseweb="menu"] li,
[data-theme="dark"] [data-baseweb="menu"] > ul > li,
[data-theme="dark"] ul[role="listbox"] li {
    background: #1e293b !important;
    color: #f8fafc !important;
}

[data-theme="dark"] [role="option"] span,
[data-theme="dark"] li[role="option"] span,
[data-theme="dark"] [data-baseweb="menu"] li span,
[data-theme="dark"] ul[role="listbox"] li span,
[data-theme="dark"] [role="option"] div,
[data-theme="dark"] li[role="option"] div,
[data-theme="dark"] [data-baseweb="menu"] li div,
[data-theme="dark"] ul[role="listbox"] li div,
[data-theme="dark"] [role="option"] *,
[data-theme="dark"] li[role="option"] *,
[data-theme="dark"] [data-baseweb="menu"] li *,
[data-theme="dark"] ul[role="listbox"] li * {
    color: #f8fafc !important;
    background: transparent !important;
}

[data-theme="dark"] [role="option"]:hover,
[data-theme="dark"] li[role="option"]:hover,
[data-theme="dark"] [data-baseweb="menu"] li:hover,
[data-theme="dark"] ul[role="listbox"] li:hover {
    background: #3b82f6 !important;
}

[data-theme="dark"] [role="option"]:hover *,
[data-theme="dark"] li[role="option"]:hover *,
[data-theme="dark"] [data-baseweb="menu"] li:hover *,
[data-theme="dark"] ul[role="listbox"] li:hover * {
    color: #ffffff !important;
}
</style>
""", unsafe_allow_html=True)

# Inicializar tema con persistencia en localStorage
if 'theme_mode' not in st.session_state:
    # Intentar leer tema guardado desde localStorage (inyectado via JavaScript)
    st.session_state.theme_mode = 'light'  # CLARO por defecto

    # Inyectar script para leer/escribir tema en localStorage
    st.markdown("""
    <script>
    // Leer tema guardado del localStorage al cargar la página
    (function() {
        const savedTheme = localStorage.getItem('copilot_theme_mode');
        if (savedTheme) {
            // Comunicar al backend via query params (Streamlit limitation)
            const url = new URL(window.location);
            url.searchParams.set('theme', savedTheme);
            if (url.searchParams.get('theme') !== savedTheme) {
                window.history.replaceState({}, '', url);
            }
        }
    })();
    </script>
    """, unsafe_allow_html=True)

# Leer tema desde query params si existe (comunicación JavaScript -> Python)
try:
    from streamlit.web import cli as stcli
    import sys
    query_params = st.query_params
    if 'theme' in query_params:
        saved_theme = query_params['theme']
        if saved_theme in ['light', 'dark']:
            st.session_state.theme_mode = saved_theme
except:
    pass

# Cache para CSS - OPTIMIZADO para móviles
@st.cache_data(ttl=7200, show_spinner=False)  # Cache por 2 horas
def load_css_file(file_path):
    """Cargar archivo CSS CON CACHE para mejor rendimiento en móviles"""
    try:
        # Usar ruta absoluta basada en project_root para compatibilidad con Streamlit Cloud
        if not os.path.isabs(file_path):
            file_path = os.path.join(project_root, file_path)

        # Leer el archivo
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Obtener timestamp de modificación del archivo para cache-busting
        file_mtime = os.path.getmtime(file_path)
        # print(f"📄 CSS cargado: {file_path} (mtime: {file_mtime})")

        return content
    except Exception as e:
        # print(f"⚠️ Error cargando CSS {file_path}: {e}")
        return None

# Cache para datos grandes - Optimización de memoria
@st.cache_data(ttl=3600)  # Cache por 1 hora
def load_large_data():
    """Cache para datos grandes para reducir uso de memoria"""
    return {}

# Limpiar cache automáticamente para evitar acumulación
def clear_cache_if_needed():
    """Limpiar cache si está usando demasiada memoria"""
    try:
        # En Streamlit Cloud, limpiar cache cada 100 interacciones
        if not hasattr(st.session_state, 'cache_counter'):
            st.session_state.cache_counter = 0

        st.session_state.cache_counter += 1

        if st.session_state.cache_counter % 100 == 0:
            st.cache_data.clear()
            st.session_state.cache_counter = 0
    except Exception:
        pass

# Cargar CSS optimizado para el dispositivo
def load_optimized_css():
    """Cargar CSS optimizado según el dispositivo con cache"""
    try:
        # Detectar si es móvil usando la variable global IS_MOBILE
        is_mobile = IS_MOBILE

        # CSS básico y MINIFICADO para móviles (más liviano y optimizado)
        if is_mobile:
            mobile_css = """
            <style>
            /* CSS Minificado para Móviles - Optimizado para carga rápida */
            .main .block-container{padding:1rem;max-width:100%}
            .stSidebar{background:#f8f9fa}
            .stSelectbox label{font-size:14px}
            .stButton button{width:100%;margin-bottom:0.5rem;padding:0.5rem}
            .metric-card{margin-bottom:1rem;padding:1rem}
            .stProgress .st-bo{height:4px}
            .js-plotly-plot,.plotly{width:100%!important}
            /* Optimizaciones adicionales para rendimiento */
            *{-webkit-tap-highlight-color:transparent}
            img{max-width:100%;height:auto}
            .stSpinner>div{border-width:2px}
            /* Reducir animaciones para mejor rendimiento */
            *{animation-duration:0.2s!important;transition-duration:0.2s!important}
            </style>
            """
            st.markdown(mobile_css, unsafe_allow_html=True)
            print("📱 CSS móvil minificado aplicado")
            return "mobile_basic"

        # CSS completo para desktop - CON CACHE
        # Detectar si estamos en Streamlit Cloud (método correcto según comunidad)
        is_cloud = any([
            os.getenv('USER') == 'appuser',  # Usuario en Streamlit Cloud
            os.path.exists('/home/appuser/.streamlit/'),  # Directorio de Streamlit Cloud
            'HOSTNAME' in os.environ and 'streamlit' in os.environ.get('HOSTNAME', '').lower(),
            os.getenv('STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION') is not None  # Variable específica de Cloud
        ])

        # Usar versión optimizada para Cloud (sin variables CSS, con !important)
        if is_cloud:
            theme_file = f'assets/theme_{st.session_state.theme_mode}_cloud.min.css'
        else:
            theme_file = f'assets/theme_{st.session_state.theme_mode}.min.css'

        # print(f"🔍 Intentando cargar: {theme_file} (Cloud: {is_cloud})")
        # print(f"📁 Project root: {project_root}")
        # print(f"📂 Ruta absoluta: {os.path.join(project_root, theme_file)}")
        # print(f"✅ Existe archivo: {os.path.exists(os.path.join(project_root, theme_file))}")

        # Guardar info de debug en session_state para mostrarla después
        st.session_state['css_debug_info'] = {
            'tema': st.session_state.theme_mode,
            'is_cloud': is_cloud,
            'theme_file': theme_file,
            'user_env': os.getenv("USER", "N/A"),
            'hostname_env': os.getenv("HOSTNAME", "N/A"),
            'appuser_path_exists': os.path.exists('/home/appuser/.streamlit/')
        }

        theme_css = load_css_file(theme_file)
        if theme_css:
            # print(f"✅ CSS cargado exitosamente: {len(theme_css)} caracteres")

            # Agregar hash del contenido + timestamp para cache-busting AGRESIVO
            import hashlib
            import time
            css_hash = hashlib.md5(theme_css.encode()).hexdigest()[:8]
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            cache_buster = int(time.time())  # Unix timestamp para forzar recarga

            # Comentario con timestamp Y hash para romper caché del navegador
            css_with_version = f"/* CSS Version: {timestamp} | Hash: {css_hash} | CB: {cache_buster} */\n{theme_css}"

            # print(f"🎨 CSS aplicado - Tema: {st.session_state.theme_mode} | Hash: {css_hash} | CB: {cache_buster}")
            # Usar ID único en el style tag para forzar re-render
            st.markdown(f"<style id='theme-css-{cache_buster}'>{css_with_version}</style>", unsafe_allow_html=True)
            return f"theme_{st.session_state.theme_mode}_{'cloud' if is_cloud else 'local'}"
        else:
            # Fallback inmediato si no se puede cargar el tema
            # print(f"❌ No se pudo cargar {theme_file}")
            raise Exception(f"No se pudo cargar el tema principal: {theme_file}")

    except Exception as e:
        # Fallback con cache
        try:
            adaptive_css = load_css_file('assets/adaptive_theme.css')
            if adaptive_css:
                st.markdown(f"<style>{adaptive_css}</style>", unsafe_allow_html=True)
                return "adaptive"
            else:
                raise Exception("No se pudo cargar CSS adaptativo")
        except Exception as e2:
            # Último fallback con cache
            try:
                css_content = load_css_file('assets/style.min.css')
                if css_content:
                    # Solo cargar desktop_layout.css si no es móvil
                    is_mobile_fallback = False
                    try:
                        if hasattr(st, 'context') and hasattr(st.context, 'user_agent'):
                            user_agent = str(st.context.user_agent or "").lower()
                            is_mobile_fallback = any(mobile in user_agent for mobile in ['mobile', 'android', 'iphone', 'ipad'])
                    except:
                        pass

                    if not is_mobile_fallback:
                        desktop_css = load_css_file('assets/desktop_layout.css')
                        if desktop_css:
                            st.markdown(f"<style>{desktop_css}</style>", unsafe_allow_html=True)
                    st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)
                    return "legacy"
                else:
                    raise Exception("No se pudo cargar CSS legacy")
            except Exception as e3:
                # FALLBACK CRÍTICO: CSS Embebido para Streamlit Cloud
                current_theme = st.session_state.get('theme_mode', 'light')

                if current_theme == 'light':
                    fallback_css = """
                    <style>
                    /* === FALLBACK CSS EMBEBIDO PARA STREAMLIT CLOUD === */

                    /* Sidebar buttons - TEMA CLARO */
                    .stSidebar .stButton > button {
                        background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
                        color: white !important;
                        border: none !important;
                        border-radius: 12px !important;
                        padding: 0.75rem 1rem !important;
                        font-weight: 500 !important;
                        width: 100% !important;
                        margin-bottom: 0.5rem !important;
                        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1) !important;
                        transition: all 0.2s ease !important;
                    }

                    .stSidebar .stButton > button:hover {
                        background: linear-gradient(135deg, #059669 0%, #047857 100%) !important;
                        transform: translateY(-1px) !important;
                        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15) !important;
                    }

                    /* Texto general - FORZAR VISIBLE */
                    .stMarkdown, .stMarkdown *, .element-container *,
                    .stChatMessage, .stChatMessage *,
                    div[data-testid="stMarkdownContainer"] * {
                        color: #111827 !important;
                    }

                    /* Mantener blanco en fondos verdes */
                    [style*="background: linear-gradient(135deg, #22c55e"] *,
                    [style*="background: linear-gradient(135deg, #4CAF50"] *,
                    .access-granted * {
                        color: white !important;
                    }

                    /* Chat AI específico */
                    .stChatMessage {
                        background: #ffffff !important;
                        border: 1px solid #e5e7eb !important;
                        border-radius: 8px !important;
                    }
                    </style>
                    """
                else:
                    fallback_css = """
                    <style>
                    /* === FALLBACK CSS EMBEBIDO PARA STREAMLIT CLOUD - TEMA OSCURO === */

                    .stSidebar .stButton > button {
                        background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
                        color: white !important;
                        border: none !important;
                        border-radius: 12px !important;
                        padding: 0.75rem 1rem !important;
                        font-weight: 500 !important;
                        width: 100% !important;
                        margin-bottom: 0.5rem !important;
                        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1) !important;
                        transition: all 0.2s ease !important;
                    }

                    /* Texto para tema oscuro */
                    .stMarkdown, .stMarkdown *, .element-container *,
                    .stChatMessage, .stChatMessage * {
                        color: #ffffff !important;
                    }
                    </style>
                    """

                st.markdown(fallback_css, unsafe_allow_html=True)
                return "embedded_fallback"

# Limpiar cache automáticamente
clear_cache_if_needed()

# NOTA: CSS se carga DESPUÉS de verificar autenticación (ver main())
# Esto evita que el CSS de la app principal contamine la pantalla de login

# Cargar detector y correcciones para iOS Safari (compatible con todas las versiones)
def load_ios_fixes():
    """Cargar fixes de iOS solo cuando sea necesario - VERSIÓN SEGURA"""
    try:
        # Leer archivos CSS y JS primero
        ios_fixes_css = load_css_file('assets/ios_safari_fixes.css')
        safari_js = load_css_file('assets/safari_detector.js')

        # Si no se cargan los archivos, usar un fix mínimo y seguro
        if not ios_fixes_css or not safari_js:
            print("⚠️ Archivos iOS no disponibles - usando fixes mínimos")
            minimal_ios_fix = """
            <script>
            (function() {
                'use strict';
                try {
                    const isIOS = /iPad|iPhone|iPod/.test(navigator.userAgent) && !window.MSStream;
                    if (isIOS) {
                        console.log('iOS detectado - Aplicando fixes mínimos...');
                        // Fix básico de viewport
                        let viewport = document.querySelector('meta[name="viewport"]');
                        if (!viewport) {
                            viewport = document.createElement('meta');
                            viewport.name = 'viewport';
                            document.head.appendChild(viewport);
                        }
                        viewport.content = 'width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes, viewport-fit=cover';

                        // Fix básico de altura
                        document.documentElement.style.height = '100vh';
                        document.body.style.minHeight = '100vh';
                    }
                } catch (error) {
                    console.error('Error en fixes iOS mínimos:', error);
                }
            })();
            </script>
            """
            st.markdown(minimal_ios_fix, unsafe_allow_html=True)
            return

        # Procesar archivos cargados de forma segura
        # 1. Escapar CSS para template literals
        ios_fixes_css_escaped = ios_fixes_css.replace('\\', '\\\\').replace('`', '\\`').replace('${', '\\${')

        # 2. NO intentar extraer el IIFE de safari_js, usarlo directamente en el HTML
        # El safari_js ya viene con su propia estructura IIFE completa

        # Crear script seguro con CSS inline y JS separado
        safe_ios_script = f"""
        <script>
        (function() {{
            'use strict';
            try {{
                // Detectar iOS Safari
                const userAgent = navigator.userAgent;
                const isIOS = /iPad|iPhone|iPod/.test(userAgent) && !window.MSStream;
                const isSafari = /Safari/.test(userAgent) && !/Chrome|CriOS|FxiOS/.test(userAgent);

                if (isIOS && isSafari) {{
                    console.log('iOS Safari detectado - Cargando fixes específicos...');

                    // Inyectar CSS de forma segura
                    const style = document.createElement('style');
                    style.id = 'ios-safari-fixes';
                    style.textContent = `{ios_fixes_css_escaped}`;
                    document.head.appendChild(style);

                    // Meta tags específicos
                    let viewport = document.querySelector('meta[name="viewport"]');
                    if (!viewport) {{
                        viewport = document.createElement('meta');
                        viewport.name = 'viewport';
                        document.head.appendChild(viewport);
                    }}
                    viewport.content = 'width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes, viewport-fit=cover';

                    const webAppCapable = document.createElement('meta');
                    webAppCapable.name = 'apple-mobile-web-app-capable';
                    webAppCapable.content = 'yes';
                    if (!document.querySelector('meta[name="apple-mobile-web-app-capable"]')) {{
                        document.head.appendChild(webAppCapable);
                    }}

                    console.log('✅ Fixes iOS aplicados correctamente');
                }}
            }} catch (error) {{
                console.error('Error aplicando fixes de iOS:', error);
                // Aplicar fix mínimo de emergencia
                try {{
                    let viewport = document.querySelector('meta[name="viewport"]');
                    if (!viewport) {{
                        viewport = document.createElement('meta');
                        viewport.name = 'viewport';
                        document.head.appendChild(viewport);
                    }}
                    viewport.content = 'width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes';
                }} catch(e) {{
                    console.error('Error en fix de emergencia:', e);
                }}
            }}
        }})();
        </script>
        """

        # Cargar el script seguro
        st.markdown(safe_ios_script, unsafe_allow_html=True)

        # Cargar el safari_detector.js por separado (ya tiene su propia protección)
        st.markdown(f"<script>{safari_js}</script>", unsafe_allow_html=True)

    except Exception as e:
        # Si hay cualquier error, usar fix ultra mínimo de emergencia
        print(f"❌ Error cargando iOS fixes: {e}")
        emergency_fix = """
        <script>
        (function() {
            try {
                if (/iPad|iPhone|iPod/.test(navigator.userAgent)) {
                    console.log('iOS detectado - Fix de emergencia');
                    let viewport = document.querySelector('meta[name="viewport"]');
                    if (viewport) {
                        viewport.content = 'width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes';
                    }
                    document.body.style.minHeight = '100vh';
                }
            } catch(e) { console.error('Error en fix iOS de emergencia:', e); }
        })();
        </script>
        """
        st.markdown(emergency_fix, unsafe_allow_html=True)

# NOTA: Los fixes de iOS se cargan ahora de forma diferida en la aplicación principal
# para evitar que aparezcan como texto durante el login

# NOTA: Estilos adicionales se cargan DESPUÉS de verificar autenticación en main()

class SecureHealthAnalyticsApp:
    def __init__(self):
        # Inicializar propiedades por defecto
        self.authenticated = False
        self.user = None
        self.auth = None
        self.role_info = None
        self.data = None
        self.ai_processor = None
        self.chart_generator = None
        self.metrics_calculator = None
        self.map_interface = None
        self.map_interface_loaded = False  # IMPORTANTE: Inicializar siempre

        # Inicializar sistemas de optimización y seguridad
        self.performance_optimizer = None
        self.security_auditor = None
        self.rate_limiter = None
        self.data_encryption = None
        
        if not AUTH_AVAILABLE:
            st.error("❌ Sistema de autenticación no disponible")
            return
            
        # Verificar autenticación
        self.authenticated = check_authentication()
        
        if self.authenticated:
            try:
                self.user = st.session_state.user
                self.auth = HealthAuthenticator()
                self.role_info = self.auth.get_role_info(self.user['role'])
                
                # Inicializar sistemas de optimización y seguridad
                if OPTIMIZATION_AVAILABLE:
                    self.performance_optimizer = get_performance_optimizer()
                    self.security_auditor = get_security_auditor()
                    self.rate_limiter = get_rate_limiter()
                    self.data_encryption = get_data_encryption()
                    
                    # Registrar inicio de sesión
                    self.security_auditor.log_user_action(
                        user=self.user['username'],
                        action="login",
                        resource="application",
                        success=True,
                        details={"role": self.user['role']}
                    )
                
                # Cargar datasets con optimización
                self.load_datasets()
                
                # Inicializar IA si está disponible y el usuario tiene permisos
                if AI_AVAILABLE and os.getenv('GROQ_API_KEY') and self.has_permission('analisis_ia'):
                    self.ai_processor = HealthAnalyticsAI()
                    self.chart_generator = SmartChartGenerator()
                    self.metrics_calculator = HealthMetricsCalculator()
                
                # Carga diferida de mapas - no cargar hasta que se necesiten
                # (map_interface y map_interface_loaded ya inicializados arriba)
                
                # Inicializar dashboards personalizados
                if ROLE_DASHBOARDS_AVAILABLE:
                    self.role_dashboards = RoleDashboards()
                else:
                    self.role_dashboards = None
                    
            except Exception as e:
                st.error(f"❌ Error inicializando aplicación: {str(e)}")
                self.authenticated = False
    
    def has_permission(self, permission: str) -> bool:
        """Verificar si el usuario tiene un permiso específico"""
        try:
            if not self.authenticated or not self.auth or not self.user:
                return False
            
            user_role = self.user.get('role')
            if not user_role:
                return False
                
            return self.auth.has_permission(user_role, permission)
            
        except Exception as e:
            print(f"❌ Error verificando permisos: {str(e)}")
            return False

    def apply_viewport_optimization(self):
        """Aplicar optimización de viewport solo cuando la app esté cargada"""
        viewport_script = """
        <script>
        // Script optimizado por dispositivo (cargado post-login)
        (function() {
            // Detectar si es móvil
            var isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);

            if (isMobile) {
                // Configuración móvil - viewport responsive
                var viewport = document.querySelector("meta[name=viewport]");
                if (viewport) {
                    viewport.setAttribute('content', 'width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes');
                } else {
                    var meta = document.createElement('meta');
                    meta.name = "viewport";
                    meta.content = "width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes";
                    document.getElementsByTagName('head')[0].appendChild(meta);
                }
            } else {
                // Configuración desktop - forzar ancho mínimo
                var viewport = document.querySelector("meta[name=viewport]");
                if (viewport) {
                    viewport.setAttribute('content', 'width=1200, initial-scale=1.0, maximum-scale=1.0, user-scalable=no');
                } else {
                    var meta = document.createElement('meta');
                    meta.name = "viewport";
                    meta.content = "width=1200, initial-scale=1.0, maximum-scale=1.0, user-scalable=no";
                    document.getElementsByTagName('head')[0].appendChild(meta);
                }

                // Forzar layout desktop
                if (window.innerWidth < 1200 && !document.body.classList.contains('desktop-forced')) {
                    document.body.classList.add('desktop-forced');
                    document.body.style.minWidth = '1200px';
                    document.body.style.overflowX = 'auto';
                }
            }
        })();
        </script>
        """
        st.markdown(viewport_script, unsafe_allow_html=True)

    def ensure_map_variables_initialized(self):
        """Asegurar que las variables de mapas estén inicializadas"""
        if not hasattr(self, 'map_interface_loaded'):
            self.map_interface_loaded = False
            print("🔧 Inicializando map_interface_loaded = False")

        if not hasattr(self, 'map_interface'):
            self.map_interface = None
            print("🔧 Inicializando map_interface = None")

    def load_map_interface(self):
        """Cargar interfaz de mapas de forma diferida solo cuando se necesite"""
        # Debug info
        print(f"🔧 load_map_interface llamado. MAPS_AVAILABLE: {MAPS_AVAILABLE}")

        # Mostrar debug en la UI también
        st.write(f"🔧 **Debug:** MAPS_AVAILABLE = {MAPS_AVAILABLE}")

        # Asegurar que las variables estén inicializadas
        self.ensure_map_variables_initialized()

        st.write(f"🔧 **Debug:** Variables inicializadas. map_interface_loaded = {self.map_interface_loaded}")

        if not MAPS_AVAILABLE:
            st.error("❌ Los mapas no están disponibles. Dependencias no instaladas.")
            st.write("💡 **Diagnóstico:** Las dependencias folium/streamlit-folium no están disponibles")
            return False

        if self.map_interface_loaded and self.map_interface is not None:
            print("✅ MapInterface ya está cargado")
            st.success("✅ MapInterface ya está cargado previamente")
            return True

        st.write("🚀 **Debug:** Iniciando carga de MapInterface...")

        try:
            # Mostrar spinner solo en carga inicial
            with st.spinner("🗺️ Cargando sistema de mapas..."):
                print("📦 Importando módulos de mapas...")
                st.write("📦 **Debug:** Importando módulos...")

                # Importar módulos de mapas dinámicamente
                from modules.visualization.map_interface import MapInterface

                print("🏗️ Creando instancia de MapInterface...")
                st.write("🏗️ **Debug:** Creando instancia...")

                self.map_interface = MapInterface()
                self.map_interface_loaded = True

                # Verificar signatura del método
                import inspect
                sig = inspect.signature(self.map_interface.render_epic_maps_dashboard)
                params = list(sig.parameters.keys())
                print(f"🔧 MapInterface cargado con parámetros: {params}")

                st.success("✅ Sistema de mapas cargado correctamente")
                st.write(f"🔧 **Debug:** Método encontrado con parámetros: {params}")
                return True

        except Exception as e:
            error_msg = f"❌ Error cargando mapas: {str(e)}"
            print(error_msg)
            st.error(error_msg)

            # Mostrar detalles adicionales para debugging
            with st.expander("🔧 Detalles del error (ABIERTO para debugging)", expanded=True):
                st.write(f"**Tipo de error:** {type(e).__name__}")
                st.write(f"**Mensaje:** {str(e)}")
                import traceback
                error_trace = traceback.format_exc()
                st.code(error_trace)
                print(f"Traceback completo: {error_trace}")

            self.map_interface = None
            self.map_interface_loaded = False
            return False
    
    def require_permission(self, permission: str) -> bool:
        """Decorador para requerir permisos específicos"""
        if not self.has_permission(permission):
            # Obtener información del rol de forma segura
            role_display = "Usuario desconocido"
            if self.role_info:
                role_display = f"{self.role_info['icon']} {self.role_info['name']}"
            elif self.user and self.user.get('role'):
                role_display = f"👤 {self.user['role']}"
            
            st.markdown(f"""
            <div class="permission-required">
                <h3>🚫 Acceso Restringido</h3>
                <p><strong>Permiso requerido:</strong> {permission}</p>
                <p><strong>Tu rol:</strong> {role_display}</p>
                <p>Contacta al administrador para obtener acceso.</p>
            </div>
            """, unsafe_allow_html=True)
            return False
        return True
        
    def _load_datasets_static(self):
        """Cargar datasets con verificación de permisos y optimización"""
        if OPTIMIZATION_AVAILABLE and self.performance_optimizer:
            return load_health_datasets_optimized(self.user['role'])
        else:
            return load_health_datasets_legacy()
    
    def load_datasets(self):
        """Inicializar datasets con optimización y auditoría"""
        try:
            if self.has_permission('ver_datos'):
                # Verificar rate limiting
                if self.rate_limiter:
                    allowed, message, details = self.rate_limiter.is_allowed(
                        self.user['username'], 
                        'data_access'
                    )
                    if not allowed:
                        st.error(f"🚫 {message}")
                        self.data = None
                        return
                
                # Cargar datos
                self.data = self._load_datasets_static()
                
                # Registrar acceso a datos
                if self.security_auditor:
                    self.security_auditor.log_user_action(
                        user=self.user['username'],
                        action="data_access",
                        resource="health_datasets",
                        success=self.data is not None,
                        details={"role": self.user['role'], "datasets_loaded": len(self.data) if self.data else 0}
                    )
            else:
                self.data = None
        except Exception as e:
            print(f"❌ Error inicializando datasets: {str(e)}")
            self.data = None
            
            # Registrar error
            if self.security_auditor:
                self.security_auditor.log_user_action(
                    user=self.user['username'],
                    action="data_access",
                    resource="health_datasets",
                    success=False,
                    details={"error": str(e)}
                )
        
    def render_secure_header(self):
        """Cabecera personalizada según el rol del usuario"""
        if not self.authenticated or not self.user or not self.role_info:
            st.error("❌ Error: Información de usuario no disponible")
            return
            
        try:
            user_name = self.user.get('name', 'Usuario')
            user_username = self.user.get('username', 'N/A')
            role_icon = self.role_info.get('icon', '👤')
            role_name = self.role_info.get('name', 'Usuario')
            theme = self.role_info.get('theme', {})
            
            # Personalización por rol
            welcome_message = theme.get('welcome_message', 'Sistema de Análisis Sociosanitario')
            gradient = theme.get('primary_gradient', 'linear-gradient(135deg, #ffffff 0%, #f8fafc 100%)')
            header_style = theme.get('header_style', 'simple')
            
            # Estilos específicos por tipo de header
            if header_style == 'executive':
                header_content = f"""
                <div class="main-header-secure" style="background: {gradient}; color: white;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <h1 style="color: white;">🏛️ {welcome_message}</h1>
                            <h2 style="color: rgba(255,255,255,0.9); font-size: 1.2rem;">Sistema Integrado de Gestión Sanitaria</h2>
                        </div>
                        <div style="text-align: right;">
                            <div class="executive-badge" style="background: rgba(255,255,255,0.2); padding: 1rem; border-radius: 12px;">
                                <div style="font-size: 2rem;">{role_icon}</div>
                                <strong style="color: white;">{user_name}</strong><br>
                                <small style="color: rgba(255,255,255,0.8);">{role_name}</small>
                            </div>
                        </div>
                    </div>
                    <p style="color: rgba(255,255,255,0.8); margin-top: 1rem;">🔐 Acceso Ejecutivo Autorizado | Provincia de Málaga</p>
                </div>
                """
            elif header_style == 'operational':
                header_content = f"""
                <div class="main-header-secure" style="background: {gradient}; color: white;">
                    <h1 style="color: white;">⚙️ {welcome_message}</h1>
                    <h2 style="color: rgba(255,255,255,0.9);">Panel Operativo - Gestión Sanitaria</h2>
                    <div class="user-badge" style="background: rgba(255,255,255,0.2); color: white; border: 1px solid rgba(255,255,255,0.3);">
                        {role_icon} <strong>{user_name}</strong> | {role_name}
                    </div>
                    <p style="color: rgba(255,255,255,0.8);">📊 Sistema Operativo Activo | Málaga</p>
                </div>
                """
            elif header_style == 'analytical':
                header_content = f"""
                <div class="main-header-secure" style="background: {gradient}; color: white;">
                    <h1 style="color: white;">📊 {welcome_message}</h1>
                    <h2 style="color: rgba(255,255,255,0.9);">Plataforma de Análisis Avanzado</h2>
                    <div class="user-badge" style="background: rgba(255,255,255,0.2); color: white; border: 1px solid rgba(255,255,255,0.3);">
                        {role_icon} <strong>{user_name}</strong> | {role_name}
                    </div>
                    <p style="color: rgba(255,255,255,0.8);">📈 Análisis de Datos Activo | Málaga</p>
                </div>
                """
            else:  # simple
                header_content = f"""
                <div class="main-header-secure" style="background: {gradient}; color: white;">
                    <h1 style="color: white;">👁️ {welcome_message}</h1>
                    <h2 style="color: rgba(255,255,255,0.9);">Información Pública Sanitaria</h2>
                    <div class="user-badge" style="background: rgba(255,255,255,0.2); color: white; border: 1px solid rgba(255,255,255,0.3);">
                        {role_icon} <strong>{user_name}</strong>
                    </div>
                    <p style="color: rgba(255,255,255,0.8);">📋 Acceso Público | Málaga</p>
                </div>
                """
            
            st.markdown(header_content, unsafe_allow_html=True)
    
            # Indicador de rol fijo
            st.markdown(f"""
            <div class="role-indicator">
                {role_icon} {user_username} ({role_name})
            </div>
            """, unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"❌ Error renderizando header: {str(e)}")
    
    def render_secure_sidebar(self):
        """Sidebar personalizado según el rol del usuario"""
        with st.sidebar:
            theme = self.role_info.get('theme', {})
            sidebar_style = theme.get('sidebar_style', 'minimal')
            focus_areas = theme.get('focus_areas', ['Información General'])
            
            # Información del usuario personalizada por rol
            current_theme = st.session_state.get('theme_mode', 'light')
            # Eliminar border en modo oscuro para evitar filo verde
            border_style = 'border: none;' if current_theme == 'dark' else 'border: 1px solid rgba(255,255,255,0.2);'
            org_border = 'border: none;' if current_theme == 'dark' else 'border: 1px solid rgba(255,255,255,0.2);'

            st.markdown(f"""
            <div class="sidebar-user-card" style="background: {theme.get('primary_gradient', 'linear-gradient(135deg, #6b7280 0%, #9ca3af 100%)')};
                        padding: 1.5rem; border-radius: 12px; text-align: center; margin-bottom: 1rem; {border_style}">
                <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">{self.role_info['icon']}</div>
                <strong class="sidebar-user-name" style="font-size: 1.1rem; color: #ffffff !important; font-weight: 700; text-shadow: 0 2px 4px rgba(0,0,0,0.6); display: block;">{self.user['name']}</strong><br>
                <small class="sidebar-user-role" style="color: #ffffff !important; font-size: 0.9rem; font-weight: 600; text-shadow: 0 2px 4px rgba(0,0,0,0.6); display: block;">{self.role_info['name']}</small>
                <div class="sidebar-user-org" style="margin-top: 0.5rem; padding: 0.5rem; background: rgba(255,255,255,0.3); border-radius: 8px; {org_border}">
                    <small style="color: #ffffff !important; font-weight: 700; text-shadow: 0 2px 4px rgba(0,0,0,0.6);">{self.user['organization']}</small>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Botones de tema y salir
            st.markdown("---")

            col1, col2 = st.columns(2)
            with col1:
                current_theme = st.session_state.get('theme_mode', 'light')
                theme_icon = "🌙" if current_theme == 'light' else "☀️"
                theme_text = "Oscuro" if current_theme == 'light' else "Claro"

                if st.button(f"{theme_icon} {theme_text}", key="sidebar_theme_toggle", use_container_width=True):
                    new_theme = 'dark' if current_theme == 'light' else 'light'
                    st.session_state.theme_mode = new_theme

                    # Guardar tema en localStorage para persistencia
                    st.markdown(f"""
                    <script>
                    localStorage.setItem('copilot_theme_mode', '{new_theme}');
                    </script>
                    """, unsafe_allow_html=True)

                    st.rerun()

            with col2:
                if st.button("🚪 Salir", key="sidebar_logout", use_container_width=True, type="secondary"):
                    logout()
                    st.rerun()

            st.markdown("---")

            # Enlaces rápidos personalizados por rol
            if sidebar_style == 'expanded':
                st.markdown("### 🚀 Panel de Control")
                
                if st.button("🏛️ Vista Ejecutiva", width="stretch"):
                    st.session_state.page = "main"
                    st.session_state.selected_tab = "dashboard"
                    
                if self.has_permission('gestion_usuarios'):
                    if st.button("👥 Gestión de Usuarios", width="stretch"):
                        st.session_state.page = "gestion_usuarios"
                        
                if st.button("📊 Análisis Estratégico", width="stretch"):
                    st.session_state.page = "main"
                    st.session_state.selected_tab = "chat_ia"
                    
            elif sidebar_style == 'compact':
                st.markdown("### ⚙️ Gestión")
                
                if st.button("📊 Dashboard", width="stretch"):
                    st.session_state.page = "main"
                    st.session_state.selected_tab = "dashboard"
                    
                if st.button("🗺️ Mapas", width="stretch"):
                    st.session_state.page = "main"
                    st.session_state.selected_tab = "mapas"
                    
            elif sidebar_style == 'detailed':
                st.markdown("### 📈 Análisis")
                
                if st.button("📊 Dashboard Analítico", width="stretch"):
                    st.session_state.page = "main"
                    st.session_state.selected_tab = "dashboard"
                    
                if st.button("🔍 Exploración de Datos", width="stretch"):
                    st.session_state.page = "main"
                    st.session_state.selected_tab = "mapas"
                    
            else:  # minimal
                st.markdown("### 📋 Navegación")
                
                if st.button("🏠 Inicio", width="stretch"):
                    st.session_state.page = "main"
            
            # Perfil siempre disponible
            if st.button("👤 Mi Perfil", width="stretch"):
                st.session_state.page = "profile"
                
            st.markdown("---")
                
            # Áreas de enfoque personalizadas por rol
            st.markdown(f"### 🎯 Áreas de Enfoque")
            for i, area in enumerate(focus_areas):
                st.markdown(f"**{i+1}.** {area}")
            
            st.markdown("---")
            
            # Información del sistema personalizada por rol
            if self.data and self.has_permission('ver_datos'):
                if sidebar_style == 'expanded':
                    st.markdown("### 📊 KPIs Ejecutivos")
                    total_hospitales = len(self.data['hospitales'])
                    total_poblacion = self.data['demografia']['poblacion_2025'].sum()
                    
                    st.metric("🏥 Centros", total_hospitales)
                    st.metric("👥 Población", f"{total_poblacion/1000:.0f}K")
                    st.metric("🎯 Cobertura", f"{(total_hospitales/total_poblacion*100000):.1f}/100K")
                    
                elif sidebar_style == 'compact':
                    st.markdown("### ⚙️ Métricas Operativas")
                    if 'accesibilidad' in self.data:
                        avg_time = self.data['accesibilidad']['tiempo_coche_minutos'].mean()
                        st.metric("⏱️ Tiempo Medio", f"{avg_time:.0f} min")
                    
                elif sidebar_style == 'detailed':
                    st.markdown("### 📈 Indicadores Analíticos")
                    if 'indicadores' in self.data:
                        avg_ratio = self.data['indicadores']['ratio_medico_1000_hab'].mean()
                        st.metric("👨‍⚕️ Ratio Médicos", f"{avg_ratio:.1f}/1K")
                
                else:  # minimal
                    st.markdown("### 📋 Info Básica")
                    st.info(f"🏥 {len(self.data['hospitales'])} centros disponibles")
                
                # Indicador de acceso a IA
                if self.ai_processor:
                    st.success("🤖 IA Activa")
                else:
                    st.info("🔧 IA Limitada")
            
            st.markdown("---")
            
            # Información del sistema
            st.markdown("### ℹ️ Información del Sistema")
            st.info(f"🎭 Rol: {self.role_info['name']}")
            st.info(f"🏢 Organización: {self.user['organization']}")
            
            # Indicador de estado de la aplicación
            if self.data:
                st.success("✅ Datos cargados")
            else:
                st.warning("⚠️ Cargando datos...")
                
            if self.ai_processor:
                st.success("🤖 IA Asíncrona activa")
            else:
                st.info("🔧 IA limitada")

def fix_plotly_hover_issues(fig):
    """Aplicar correcciones EXTREMAS a gráficos de Plotly para eliminar TODOS los errores de hover"""
    try:
        # PASO 1: Deshabilitar COMPLETAMENTE hover en todas las trazas
        for trace in fig.data:
            try:
                trace.update(hoverinfo='none', hovertemplate=None)
                # Eliminar atributos problemáticos si existen
                if hasattr(trace, 'hoversubplots'):
                    delattr(trace, 'hoversubplots')
            except:
                pass

        # PASO 2: RECREAR COMPLETAMENTE la figura sin hover
        try:
            # Obtener datos y layout limpios
            data = fig.data
            layout_dict = dict(fig.layout)

            # Debug: verificar estructura de data
            print(f"🔍 Debug - Tipo de data: {type(data)}")
            print(f"🔍 Debug - Longitud de data: {len(data) if hasattr(data, '__len__') else 'N/A'}")
            if hasattr(data, '__iter__'):
                for i, trace in enumerate(data):
                    print(f"🔍 Debug - Trace {i}: tipo={type(trace)}")
                    if hasattr(trace, 'keys'):
                        print(f"🔍 Debug - Trace {i} keys: {list(trace.keys())[:5]}...")  # Primeras 5 keys
                    break  # Solo mostrar el primero

            # Eliminar TODAS las configuraciones de hover del layout
            hover_keys = [
                'hovermode', 'hoversubplots', 'hoverdistance', 'spikedistance',
                'hoverlabel', 'hovertemplate', 'hoverformat'
            ]

            clean_layout = {}
            for k, v in layout_dict.items():
                if k not in hover_keys:
                    if isinstance(v, dict):
                        # Limpiar diccionarios anidados
                        clean_v = {sk: sv for sk, sv in v.items() if sk not in hover_keys}
                        clean_layout[k] = clean_v
                    else:
                        clean_layout[k] = v

            # Forzar configuración segura
            clean_layout.update({
                'hovermode': False
            })

            # Si hay ejes, limpiarlos también
            for axis in ['xaxis', 'yaxis']:
                if axis in clean_layout:
                    if isinstance(clean_layout[axis], dict):
                        clean_layout[axis].update({
                            'rangeslider': dict(visible=False)
                        })
                        # Eliminar hover de ejes
                        hover_axis_keys = ['hoverformat']
                        for hk in hover_axis_keys:
                            if hk in clean_layout[axis]:
                                del clean_layout[axis][hk]

            # Crear nueva figura completamente limpia
            # Simplificar: usar add_trace en lugar de pasar data directamente
            new_fig = go.Figure(layout=clean_layout)

            # Agregar traces uno por uno para evitar problemas de estructura
            for trace in data:
                try:
                    new_fig.add_trace(trace)
                except Exception as trace_error:
                    print(f"Error agregando trace: {trace_error}")
                    continue

            fig = new_fig

        except Exception as recreation_error:
            print(f"Error recreando figura: {recreation_error}")
            print(f"Tipo de error: {type(recreation_error).__name__}")
            if hasattr(recreation_error, 'args'):
                print(f"Argumentos del error: {recreation_error.args}")

            # Fallback a método original
            try:
                fig.update_layout(hovermode=False)
            except Exception as fallback_error:
                print(f"Error en fallback: {fallback_error}")
                # Crear figura básica nueva si todo falla
                fig = go.Figure()

        # PASO 3: Protección para subplots múltiples
        for i in range(1, 11):  # xaxis1 hasta xaxis10
            try:
                axis_updates = {
                    f'xaxis{i}': dict(
                        rangeslider=dict(visible=False)
                    )
                }
                fig.update_layout(**axis_updates)
            except:
                pass

    except Exception as e:
        print(f"Error CRÍTICO en fix_plotly_hover_issues: {e}")
        # ÚLTIMO RECURSO: Crear figura básica sin hover
        try:
            fig.update_layout(hovermode=False)
            for trace in fig.data:
                trace.update(hoverinfo='none')
        except:
            print("No se pudo aplicar ni las correcciones básicas")

    return fig

def main():
    """Función principal con autenticación completa"""

    # Importar re localmente para evitar problemas de ámbito en funciones anidadas
    import re

    if not AUTH_AVAILABLE:
        st.error("❌ Sistema de autenticación no disponible. Instala: pip install bcrypt PyJWT")
        return

    # Verificar autenticación PRIMERO
    if not check_authentication():
        render_login_page()
        return

    # === A PARTIR DE AQUÍ: USUARIO AUTENTICADO ===

    # Mostrar indicador de carga para dispositivos móviles
    if IS_MOBILE:
        with st.spinner('⚡ Cargando aplicación...'):
            import time
            time.sleep(0.1)  # Breve pausa para que se vea el spinner

    # Marcar el body como "authenticated" para que el CSS de tema se aplique
    st.markdown("""
    <script>
    (function() {
        document.body.setAttribute('data-authenticated', 'true');
        document.body.setAttribute('data-page', 'app');
        document.documentElement.setAttribute('data-authenticated', 'true');
        document.documentElement.setAttribute('data-page', 'app');
        console.log('🔐 Usuario AUTENTICADO - Body marcado');
    })();
    </script>
    """, unsafe_allow_html=True)

    # FORZAR LAYOUT WIDE CON CSS (set_page_config no siempre funciona en Cloud)
    st.markdown("""
    <style>
    /* FORZAR WIDE MODE */
    .main .block-container {
        max-width: 100% !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }
    section[data-testid="stMain"] {
        max-width: 100% !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # CARGAR CSS DE LA APLICACIÓN (Solo para usuarios autenticados)
    css_loaded = load_optimized_css()

    # CSS GUARDIÁN: Asegurar que SIEMPRE se puede resetear en login
    # Este CSS se carga DESPUÉS del tema y tiene timestamp único
    guardian_css_timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    st.markdown(f"""
    <style id="guardian-reset-{guardian_css_timestamp}">
    /* CSS GUARDIÁN - Se carga DESPUÉS del tema para permitir reset en login */
    /* Este CSS NO hace nada cuando estás autenticado */
    /* Pero en login, render_login_page() puede sobrescribirlo fácilmente */
    </style>
    """, unsafe_allow_html=True)

    # Cargar CSS extra solo en desktop (Optimización Fase 2: evitar carga en móvil)
    if css_loaded != "mobile_basic" and not IS_MOBILE:
        # Detectar si estamos en Cloud
        is_cloud = any([
            os.getenv('USER') == 'appuser',
            os.path.exists('/home/appuser/.streamlit/'),
            'HOSTNAME' in os.environ and 'streamlit' in os.environ.get('HOSTNAME', '').lower(),
            os.getenv('STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION') is not None
        ])

        # Usar versión Cloud si está en Cloud
        extra_css_file = 'assets/extra_styles_cloud.min.css' if is_cloud else 'assets/extra_styles.min.css'
        extra_css = load_css_file(extra_css_file)
        if extra_css:
            # Agregar timestamp para romper caché del navegador
            extra_css_with_version = f"/* Extra CSS Version: {datetime.now().strftime('%Y%m%d_%H%M%S')} */\n{extra_css}"
            st.markdown(f"<style>{extra_css_with_version}</style>", unsafe_allow_html=True)

            # Guardar info de extra CSS en debug
            if 'css_debug_info' in st.session_state:
                st.session_state['css_debug_info']['extra_css_file'] = extra_css_file
                st.session_state['css_debug_info']['extra_css_size'] = len(extra_css)

        # CSS crítico inline para tarjeta de sidebar
        critical_css = """
        <style>
        /* CRÍTICO: Texto blanco en tarjeta de sidebar */
        .sidebar-user-card,
        .sidebar-user-card *,
        .sidebar-user-card strong,
        .sidebar-user-card small,
        section[data-testid="stSidebar"] .sidebar-user-card *,
        section[data-testid="stSidebar"] strong,
        section[data-testid="stSidebar"] small {
            color: #ffffff !important;
            text-shadow: 0 2px 4px rgba(0,0,0,0.6) !important;
        }

        /* CRÍTICO: Expansión del sidebar */
        section[data-testid="stSidebar"][aria-expanded="false"] ~ section[data-testid="stMain"] .main .block-container {
            max-width: 100% !important;
            width: 100% !important;
            margin-left: 0 !important;
            padding-left: 3rem !important;
            padding-right: 3rem !important;
        }
        </style>
        """
        st.markdown(critical_css, unsafe_allow_html=True)

        # NOTA: JavaScript no funciona en Cloud (filtrado por Streamlit)
        # Toda la solución de estilos se hace via CSS puro en theme_dark_cloud.css
        # con selectores específicos para Emotion CSS y máxima especificidad

    # Aplicar estilos adicionales según dispositivo
    if css_loaded == "mobile_basic":
        # Estilos básicos para móviles - no cargar fuentes pesadas
        st.markdown("""
        <style>
        /* Usar fuente del sistema en móviles para mejor performance */
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
            font-size: 16px; /* Prevenir zoom en iOS */
        }
        </style>
        """, unsafe_allow_html=True)
    else:
        # Estilos completos para desktop
        st.markdown("""
        <style>
        /* Importar fuentes modernas */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Poppins:wght@300;400;500;600;700&display=swap');
        </style>
        """, unsafe_allow_html=True)

    # DEBUG INFO deshabilitado (descomentar solo para debugging)
    # with st.sidebar:
    #     if 'css_debug_info' in st.session_state:
    #         with st.expander("🔧 Info Debug CSS", expanded=False):
    #             info = st.session_state['css_debug_info']
    #             st.write(f"**Tema:** `{info.get('tema', 'N/A')}`")
    #             st.write(f"**Cloud detectado:** `{info.get('is_cloud', 'N/A')}`")
    #             st.write(f"**Archivo tema:** `{info.get('theme_file', 'N/A')}`")
    #             st.write(f"**Archivo extra:** `{info.get('extra_css_file', 'N/A')}`")
    #             st.write(f"**USER env:** `{info.get('user_env', 'N/A')}`")
    #             st.write(f"**HOSTNAME:** `{info.get('hostname_env', 'N/A')}`")
    #             st.write(f"**Path /home/appuser:** `{info.get('appuser_path_exists', 'N/A')}`")

    # Inicializar tema
    if 'theme_mode' not in st.session_state:
        st.session_state.theme_mode = 'light'

    # CSS para reducir padding superior y mejorar visibilidad de iconos sidebar
    collapse_icon_css = """
    <style>
    /* Reducir padding superior del contenedor principal */
    .main .block-container {
        padding-top: 1rem !important;
    }

    /* Reducir espacio del primer elemento */
    .main .block-container > div:first-child {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }

    /* Icono << dentro del sidebar (para colapsar) - modo oscuro */
    [data-testid="stSidebar"] button[kind="header"],
    [data-testid="stSidebar"] button[kind="headerNoPadding"],
    [data-testid="collapsedControl"] {
        background-color: rgba(255, 255, 255, 0.15) !important;
        border-radius: 6px !important;
        transition: all 0.2s ease !important;
    }

    [data-testid="stSidebar"] button[kind="header"]:hover,
    [data-testid="stSidebar"] button[kind="headerNoPadding"]:hover,
    [data-testid="collapsedControl"]:hover {
        background-color: rgba(255, 255, 255, 0.25) !important;
    }

    [data-testid="stSidebar"] button[kind="header"] svg,
    [data-testid="stSidebar"] button[kind="headerNoPadding"] svg,
    [data-testid="collapsedControl"] svg {
        fill: #ffffff !important;
        color: #ffffff !important;
    }

    /* Icono >> en la barra superior blanca (para expandir) - modo oscuro */
    .stApp > header button[kind="header"],
    .stApp > header button[kind="headerNoPadding"],
    section[data-testid="stHeader"] button[kind="header"],
    section[data-testid="stHeader"] button[kind="headerNoPadding"] {
        background-color: rgba(0, 0, 0, 0.1) !important;
        border-radius: 6px !important;
        transition: all 0.2s ease !important;
    }

    .stApp > header button[kind="header"]:hover,
    .stApp > header button[kind="headerNoPadding"]:hover,
    section[data-testid="stHeader"] button[kind="header"]:hover,
    section[data-testid="stHeader"] button[kind="headerNoPadding"]:hover {
        background-color: rgba(0, 0, 0, 0.2) !important;
    }

    .stApp > header button[kind="header"] svg,
    .stApp > header button[kind="headerNoPadding"] svg,
    section[data-testid="stHeader"] button[kind="header"] svg,
    section[data-testid="stHeader"] button[kind="headerNoPadding"] svg {
        fill: #0f172a !important;
        color: #0f172a !important;
    }
    </style>
    """

    st.markdown(collapse_icon_css, unsafe_allow_html=True)

    # === OPCIÓN 1: Botones en Sidebar (Implementación Simple) ===
    # Los botones se agregarán en render_secure_sidebar() más abajo

    # === NOTA: components.html() DESHABILITADO ===
    # Causa errores MutationObserver irresolubles en Cloud
    # Reemplazado con CSS puro que se carga condicionalmente

    current_theme = st.session_state.get('theme_mode', 'light')

    # TODO el manejo de tema se hace vía CSS puro cargado en load_optimized_css()
    # No se usa JavaScript para evitar problemas con iframes en Cloud

    # === CSS EMBEBIDO CRÍTICO PARA STREAMLIT CLOUD ===
    # Aplicar inmediatamente para garantizar visibilidad

    # Colores de texto principales según tema
    if current_theme == 'light':
        text_color = '#0f172a'  # Texto muy oscuro para modo claro
        secondary_text = '#334155'  # Texto secundario
        muted_text = '#64748b'  # Texto tenue
    else:
        text_color = '#f8fafc'  # Texto muy claro para modo oscuro
        secondary_text = '#cbd5e1'  # Texto secundario
        muted_text = '#94a3b8'  # Texto tenue

    # FORZAR sidebar text color - SIEMPRE NEGRO
    sidebar_text_color = '#0f172a'

    # ========== ESTILOS ESPECÍFICOS PARA BADGES SEGÚN TEMA ==========
    if current_theme == 'dark':
        badge_css = """
        /* MODO OSCURO: Badges con fondos BRILLANTES y texto oscuro */

        /* Success badges - Verde esmeralda brillante */
        div[data-testid="stAlert"],
        div[data-baseweb="notification"],
        .stAlert {
            background-color: #10b981 !important;
            background: #10b981 !important;
            border-left: 4px solid #059669 !important;
        }

        /* FORZAR texto oscuro en todos los badges */
        div[data-testid="stAlert"],
        div[data-testid="stAlert"] *,
        div[data-testid="stAlert"] p,
        div[data-testid="stAlert"] div,
        div[data-testid="stAlert"] span,
        div[data-baseweb="notification"],
        div[data-baseweb="notification"] *,
        div[data-baseweb="notification"] p,
        div[data-baseweb="notification"] div,
        div[data-baseweb="notification"] span,
        .stAlert,
        .stAlert * {
            color: #0f172a !important;
            background-color: transparent !important;
        }

        /* Restaurar fondo de contenedores principales */
        div[data-testid="stAlert"],
        div[data-baseweb="notification"],
        .stAlert {
            background-color: #10b981 !important;
        }

        /* Warning badges - Amarillo oro brillante */
        div[data-baseweb="notification"][kind="warning"],
        div[data-testid="stAlert"][kind="warning"] {
            background-color: #fbbf24 !important;
            background: #fbbf24 !important;
            border-left: 4px solid #f59e0b !important;
        }

        /* Error badges - Rojo coral brillante */
        div[data-baseweb="notification"][kind="error"],
        div[data-testid="stAlert"][kind="error"] {
            background-color: #fca5a5 !important;
            background: #fca5a5 !important;
            border-left: 4px solid #f87171 !important;
        }

        /* Info badges - Azul cielo brillante */
        div[data-baseweb="notification"][kind="info"],
        div[data-testid="stAlert"][kind="info"] {
            background-color: #7dd3fc !important;
            background: #7dd3fc !important;
            border-left: 4px solid #38bdf8 !important;
        }
        """
    else:
        badge_css = """
        /* MODO CLARO: Texto oscuro en badges para contraste */
        div[data-testid="stAlert"],
        div[data-testid="stAlert"] *,
        div[data-baseweb="notification"],
        div[data-baseweb="notification"] *,
        .stAlert,
        .stAlert * {
            color: #0f172a !important;
        }
        """

    # Generar timestamp único para forzar recarga de CSS
    import time
    css_timestamp = int(time.time())

    # Aplicar colores de fondo según tema
    if current_theme == 'dark':
        bg_color = '#0f172a'
        bg_secondary = '#1e293b'
    else:
        bg_color = '#ffffff'
        bg_secondary = '#f8f9fa'

    st.markdown(f"""
    <style data-timestamp="{css_timestamp}">
    /* CRITICAL CSS v10-BACKGROUND - TIMESTAMP: {css_timestamp} */
    /* TEMA: {current_theme} - TEXT: {text_color} - BG: {bg_color} */

    /* ========== CAMBIAR FONDO DE LA APLICACIÓN ========== */
    .stApp {{
        background-color: {bg_color} !important;
    }}

    .main, .main > div, [data-testid="stAppViewContainer"] {{
        background-color: {bg_color} !important;
    }}

    /* ========== REDIMENSIONAMIENTO DINÁMICO DEL SIDEBAR ========== */
    /* Transición suave para todos los cambios */
    .main,
    .main .block-container,
    section[data-testid="stMain"],
    div[data-testid="stMainBlockContainer"],
    [data-testid="stAppViewContainer"] > section.main {{
        transition: margin-left 0.3s ease, max-width 0.3s ease, width 0.3s ease !important;
    }}

    /* Estado por defecto del contenedor principal */
    .main .block-container {{
        transition: all 0.3s ease !important;
    }}

    /* ========== FORZAR COLOR DE TEXTO GLOBAL (EXCEPTO LOGIN Y SIDEBAR) ========== */
    /* NO aplicar a elementos dentro de login-container */
    .main:not(:has(.login-container)) {{
        color: {text_color} !important;
    }}

    .main > div:not(.login-container) *:not(.stButton *):not([data-testid="stAlert"] *):not([data-baseweb="notification"] *):not(.main-header-secure *) {{
        color: {text_color} !important;
    }}

    /* ========== LOGIN: FORZAR TEXTO CLARO EN MODO OSCURO ========== */
    /* Aplicar después de todas las reglas con máxima prioridad */

    /* Sidebar buttons styling */
    .stSidebar .stButton > button {{
        background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 1rem !important;
        font-weight: 500 !important;
        width: 100% !important;
        margin-bottom: 0.5rem !important;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1) !important;
    }}

    /* SIDEBAR TEXT VISIBILITY - SIEMPRE NEGRO */
    .stSidebar h1, .stSidebar h2, .stSidebar h3, .stSidebar h4, .stSidebar h5, .stSidebar h6,
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] h4, [data-testid="stSidebar"] h5, [data-testid="stSidebar"] h6,
    .stSidebar p:not(.stButton p), .stSidebar span:not(.stButton span),
    [data-testid="stSidebar"] p:not(.stButton p), [data-testid="stSidebar"] span:not(.stButton span),
    .stSidebar .stMarkdown p, .stSidebar .stMarkdown h1, .stSidebar .stMarkdown h2, .stSidebar .stMarkdown h3,
    .stSidebar .stMarkdown h4, .stSidebar .stMarkdown h5, .stSidebar .stMarkdown h6,
    .stSidebar .stMarkdown strong, .stSidebar .stMarkdown em,
    [data-testid="stSidebar"] .stMarkdown p, [data-testid="stSidebar"] .stMarkdown h1,
    [data-testid="stSidebar"] .stMarkdown h2, [data-testid="stSidebar"] .stMarkdown h3,
    [data-testid="stSidebar"] .stMarkdown h4, [data-testid="stSidebar"] .stMarkdown h5,
    [data-testid="stSidebar"] .stMarkdown h6,
    [data-testid="stSidebar"] .stMarkdown strong, [data-testid="stSidebar"] .stMarkdown em,
    .stSidebar .stMetric label, .stSidebar .stMetric div,
    [data-testid="stSidebar"] .stMetric label, [data-testid="stSidebar"] .stMetric div,
    .stSidebar label:not(.stButton label),
    [data-testid="stSidebar"] label:not(.stButton label) {{
        color: {sidebar_text_color} !important;
    }}

    /* SIDEBAR BUTTONS - Keep green background with white text */
    .stSidebar .stButton > button,
    [data-testid="stSidebar"] .stButton > button {{
        background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
        color: white !important;
    }}

    /* SIDEBAR ALERTS - SIEMPRE NEGRO */
    .stSidebar .stAlert p, .stSidebar .stAlert span, .stSidebar .stAlert div:not([role="alert"]),
    [data-testid="stSidebar"] .stAlert p, [data-testid="stSidebar"] .stAlert span,
    [data-testid="stSidebar"] .stAlert div:not([role="alert"]),
    .stSidebar [data-testid="stAlertContentInfo"] p,
    .stSidebar [data-testid="stAlertContentSuccess"] p,
    [data-testid="stSidebar"] [data-testid="stAlertContentInfo"] p,
    [data-testid="stSidebar"] [data-testid="stAlertContentSuccess"] p {{
        color: {sidebar_text_color} !important;
    }}

    /* ========== CONTRASTE DASHBOARD (NO TOCAR LOGIN) ========== */

    /* Texto principal de la app */
    .main .block-container div[data-testid="stVerticalBlock"] > div,
    .stMarkdown:not(.login-container .stMarkdown),
    .element-container:not(.login-container .element-container),
    [data-testid="stMarkdownContainer"]:not(.login-container [data-testid="stMarkdownContainer"]) {{
        color: {text_color} !important;
    }}

    /* Métricas - FORZAR contraste fuerte con máxima especificidad */
    div[data-testid="stMetric"],
    div[data-testid="stMetric"] div,
    div[data-testid="stMetric"] label,
    div[data-testid="stMetric"] span,
    div[data-testid="stMetric"] p,
    div[data-testid="stMetric"] *,
    [data-testid="stMetricLabel"],
    [data-testid="stMetricLabel"] *,
    [data-testid="stMetricValue"],
    [data-testid="stMetricValue"] *,
    [data-testid="stMetricDelta"],
    [data-testid="stMetricDelta"] *,
    .stMetric,
    .stMetric * {{
        color: {text_color} !important;
    }}

    /* Labels y texto general */
    label:not(.stButton label) {{
        color: {text_color} !important;
    }}

    /* ========== Texto blanco en fondos oscuros/verdes ========== */
    .stButton > button,
    .stButton > button *,
    .main-header-secure,
    .main-header-secure *,
    [style*="background: linear-gradient(135deg, #22c55e"] *,
    [style*="background: linear-gradient(135deg, #4CAF50"] *,
    [style*="background: linear-gradient(135deg, #10b981"] *,
    [style*="background: linear-gradient(135deg, #1e3a8a"] *,
    [style*="background: linear-gradient(135deg, #1e40af"] * {{
        color: white !important;
    }}

    /* ========== EXPANDERS - CONTRASTE FORZADO CON MÁXIMA PRIORIDAD ========== */
    /* Expanders: texto visible en modo oscuro */
    div[data-testid="stExpander"],
    div[data-testid="stExpander"] *,
    div[data-testid="stExpander"] summary,
    div[data-testid="stExpander"] summary *,
    div[data-testid="stExpander"] details,
    div[data-testid="stExpander"] details *,
    div[data-testid="stExpander"] p,
    div[data-testid="stExpander"] span,
    div[data-testid="stExpander"] div,
    div[data-testid="stExpander"] label,
    .streamlit-expanderHeader,
    .streamlit-expanderHeader *,
    details[data-testid="stExpander"],
    details[data-testid="stExpander"] * {{
        color: {text_color} !important;
        background-color: transparent !important;
    }}

    /* Asegurar fondo del expander */
    div[data-testid="stExpander"] {{
        background-color: var(--bg-surface, transparent) !important;
    }}

    /* ========== BADGES DINÁMICOS SEGÚN TEMA ACTIVO ========== */
    {badge_css}

    /* ========== DEBUG INFO ========== */
    /* TEMA ACTUAL: {current_theme} */
    /* TEXT COLOR: {text_color} */
    /* SIDEBAR COLOR: {sidebar_text_color} */

    /* ========== LOGIN FINAL OVERRIDE - MÁXIMA ESPECIFICIDAD ========== */
    html body .stApp .main .login-container,
    html body .stApp .main .login-header,
    html body .stApp .main .login-container h1,
    html body .stApp .main .login-container h2,
    html body .stApp .main .login-container h3,
    html body .stApp .main .login-container p,
    html body .stApp .main .login-header h1,
    html body .stApp .main .login-header h2,
    html body .stApp .main .login-header h3,
    html body .stApp .main .login-header p {{
        color: {'#f9fafb' if current_theme == 'dark' else '#1a202c'} !important;
    }}

    </style>

    <script>
    // APLICAR data-theme INMEDIATAMENTE - SIN DELAYS
    (function() {{
        const theme = '{current_theme}';
        const textColor = '{text_color}';

        // Aplicar atributo data-theme a TODOS los elementos principales
        document.documentElement.setAttribute('data-theme', theme);
        document.body.setAttribute('data-theme', theme);

        // Intentar aplicar a stApp también
        const stApp = document.querySelector('.stApp');
        if (stApp) {{
            stApp.setAttribute('data-theme', theme);
        }}

        const main = document.querySelector('.main');
        if (main) {{
            main.setAttribute('data-theme', theme);
        }}

        console.log('✅ Theme aplicado a HTML/BODY/stApp/main:', theme);
        console.log('✅ Text color:', textColor);

        // FORZAR estilos con JavaScript después de que Streamlit cargue
        setTimeout(function() {{
            const isLoginPage = document.querySelector('.login-container') !== null;

            if (!isLoginPage) {{
                // Aplicar color de texto a elementos del dashboard
                const mainElements = document.querySelectorAll('.main *, [data-testid="stMetric"] *, [data-testid="stExpander"] *');
                mainElements.forEach(function(el) {{
                    if (!el.closest('.stButton') &&
                        !el.closest('[data-testid="stAlert"]') &&
                        !el.closest('[data-baseweb="notification"]') &&
                        !el.closest('.main-header-secure')) {{
                        el.style.color = textColor;
                    }}
                }});
                console.log('✅ Estilos dashboard aplicados:', mainElements.length, 'elementos');
            }} else {{
                // FORZAR texto claro en login con inline styles
                console.log('✅ Login detectado - aplicando estilos de login');

                // Forzar texto claro en login-header
                const loginHeaderElements = document.querySelectorAll('.login-header, .login-header *, .login-header h1, .login-header h2, .login-header h3, .login-header p');
                loginHeaderElements.forEach(function(el) {{
                    el.style.setProperty('color', '#f9fafb', 'important');
                }});

                // Forzar texto claro en login-container (excepto inputs)
                const loginElements = document.querySelectorAll('.login-container h4, .login-container p:not(input *), .login-container span:not(input *)');
                loginElements.forEach(function(el) {{
                    if (!el.closest('input') && !el.closest('.stTextInput')) {{
                        el.style.setProperty('color', '#f9fafb', 'important');
                    }}
                }});

                console.log('✅ Login text forced to white:', loginHeaderElements.length + loginElements.length, 'elementos');
            }}
        }}, 1000);  // Aumentar delay a 1 segundo

        // Repetir después de 2 segundos por si acaso
        setTimeout(function() {{
            const isLoginPage = document.querySelector('.login-container') !== null;
            if (isLoginPage && theme === 'dark') {{
                const loginAllText = document.querySelectorAll('.login-header *, .login-container *:not(input):not(.stTextInput *)');
                loginAllText.forEach(function(el) {{
                    if (!el.closest('input') && !el.closest('.stTextInput') && !el.closest('button')) {{
                        el.style.setProperty('color', '#f9fafb', 'important');
                    }}
                }});
                console.log('✅ Login reapplied (2s):', loginAllText.length, 'elementos');
            }}
        }}, 2000);

        // Observar cambios del DOM para aplicar estilos a nuevos elementos
        try {{
            const observer = new MutationObserver(function(mutations) {{
                const isLoginPage = document.querySelector('.login-container') !== null;
                if (isLoginPage) return; // No aplicar estilos en login

                mutations.forEach(function(mutation) {{
                    mutation.addedNodes.forEach(function(node) {{
                        if (node.nodeType === 1) {{ // Element node
                            const elements = node.querySelectorAll('.main *, [data-testid="stMetric"] *');
                            elements.forEach(function(el) {{
                                if (!el.closest('.stButton') &&
                                    !el.closest('[data-testid="stAlert"]') &&
                                    !el.closest('[data-baseweb="notification"]') &&
                                    !el.closest('.main-header-secure') &&
                                    !el.closest('.login-container')) {{
                                    el.style.color = textColor;
                                }}
                            }});
                        }}
                    }});
                }});
            }});

            // Verificar que document.body existe antes de observar
            if (document.body && document.body.nodeType === 1) {{
                observer.observe(document.body, {{ childList: true, subtree: true }});
            }} else {{
                // Esperar a que document.body esté disponible
                if (document.readyState === 'loading') {{
                    document.addEventListener('DOMContentLoaded', function() {{
                        if (document.body && document.body.nodeType === 1) {{
                            observer.observe(document.body, {{ childList: true, subtree: true }});
                        }}
                    }});
                }}
            }}
        }} catch(e) {{
            console.warn('⚠️ No se pudo inicializar MutationObserver para tema:', e);
        }}
    }})();
    </script>
    """, unsafe_allow_html=True)

    # Usuario autenticado - inicializar aplicación segura (ya validado arriba)
    app = SecureHealthAnalyticsApp()
    
    if not app.authenticated:
        st.error("❌ Error en la autenticación. Intenta iniciar sesión nuevamente.")
        logout()
        return
    
    # Verificar que los datos se cargaron correctamente
    if app.data is None:
        st.error("❌ Error cargando los datos. Por favor, recarga la página o contacta al administrador.")
        st.stop()

    # Aplicar optimización de viewport ahora que la app está cargada
    try:
        app.apply_viewport_optimization()
    except Exception as e:
        print(f"⚠️ Error aplicando optimización de viewport: {e}")

    # Aplicar fixes de iOS si es necesario (Optimización Fase 2: carga condicional)
    try:
        # Usar función optimizada con caché para detectar iOS
        if is_ios_device():
            app.load_ios_fixes()
    except Exception as e:
        print(f"⚠️ Error aplicando fixes de iOS: {e}")

    # Renderizar aplicación segura
    app.render_secure_header()
    app.render_secure_sidebar()
    
    # Navegación principal
    render_page_navigation(app)

    # Footer con información de seguridad y auditoría
    st.markdown("---")
    st.markdown(f"""
    <div style="text-align: center; color: #666; padding: 1rem; background: linear-gradient(135deg, rgba(0,168,107,0.05), rgba(33,150,243,0.05)); border-radius: 10px; border: 1px solid rgba(0,168,107,0.2);">
        <p><strong>🔐 Sistema Seguro v2.0</strong> |
        <strong>👤 Usuario:</strong> {app.user['name']} ({app.user['username']}) |
        <strong>🎭 Rol:</strong> {app.role_info['name']} |
        <strong>🏢 Org:</strong> {app.user['organization']}</p>
        <p><strong>⏰ Sesión:</strong> {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} |
        <strong>🔑 Permisos:</strong> {len(app.role_info['permissions'])} activos |
        <strong>🤖 IA:</strong> {'🟢 Disponible' if app.ai_processor else '🔒 Restringida'}</p>
    </div>
    """, unsafe_allow_html=True)

def render_page_navigation(app):
    """Navegación entre páginas según permisos"""
    
    current_page = st.session_state.get('page', 'main')
    
    if current_page == 'gestion_usuarios' and app.has_permission('gestion_usuarios'):
        render_user_management()
    elif current_page == 'profile':
        render_user_profile()
    else:
        # Página principal con tabs dinámicos
        tabs_available = []
        tab_functions = []

        # Dashboard siempre disponible para usuarios con ver_datos
        if app.has_permission('ver_datos'):
            tabs_available.append("Dashboard")
            tab_functions.append(lambda: render_secure_dashboard(app))

        if app.has_permission('analisis_ia'):
            tabs_available.append("Chat IA")
            tab_functions.append(lambda: render_secure_chat(app))

        if app.has_permission('reportes'):
            tabs_available.append("Reportes")
            tab_functions.append(lambda: render_secure_reportes(app))

        if app.has_permission('planificacion'):
            tabs_available.append("Planificación")
            tab_functions.append(lambda: render_secure_planificacion(app))

        # Tab de mapas épicos disponible para usuarios con permisos de ver_datos o superior
        if app.has_permission('ver_datos') and MAPS_AVAILABLE:
            tabs_available.append("Mapas Épicos")
            tab_functions.append(lambda: render_epic_maps_tab(app))
        
        # Si solo tiene un tab, mostrarlo directamente
        if len(tabs_available) == 1:
            tab_functions[0]()
        elif len(tabs_available) > 1:
            # Detectar tema actual para estilos
            current_theme = st.session_state.get('theme_mode', 'light')

            # CSS personalizado para tabs nativos de Streamlit con hover
            hover_bg = "#e9ecef" if current_theme == 'light' else "#64748b"
            hover_shadow = "0.15" if current_theme == 'light' else "0.3"

            st.markdown(f"""
            <style>
            /* ===== ESTILOS PARA TABS NATIVOS DE STREAMLIT ===== */

            /* Contenedor de tabs */
            .stTabs [data-baseweb="tab-list"] {{
                gap: 4px;
                background-color: transparent;
                padding: 0;
            }}

            /* Cada tab individual */
            .stTabs [data-baseweb="tab"] {{
                height: auto;
                padding: 12px 20px;
                background-color: {'#f8f9fa' if current_theme == 'light' else '#475569'};
                color: {'#495057' if current_theme == 'light' else '#cbd5e1'};
                border-radius: 8px 8px 0 0;
                border: none;
                font-size: 16px;
                font-weight: 500;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                cursor: pointer;
            }}

            /* HOVER: Tab no activo */
            .stTabs [data-baseweb="tab"]:not([aria-selected="true"]):hover {{
                background-color: {hover_bg} !important;
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(0, 0, 0, {hover_shadow}) !important;
            }}

            /* ACTIVO: Tab seleccionado */
            .stTabs [data-baseweb="tab"][aria-selected="true"] {{
                background: linear-gradient(135deg, #3b82f6, #2563eb) !important;
                color: white !important;
                font-weight: 600 !important;
                border-bottom: 3px solid #3b82f6 !important;
                box-shadow: 0 2px 8px rgba(59, 130, 246, 0.4) !important;
            }}

            /* Hover sobre tab activo - realce sutil */
            .stTabs [data-baseweb="tab"][aria-selected="true"]:hover {{
                background: linear-gradient(135deg, #2563eb, #1d4ed8) !important;
                transform: none !important;
                box-shadow: 0 3px 10px rgba(59, 130, 246, 0.6) !important;
            }}

            /* Ocultar barra inferior predeterminada */
            .stTabs [data-baseweb="tab-highlight"] {{
                display: none;
            }}

            /* Panel de contenido del tab */
            .stTabs [data-baseweb="tab-panel"] {{
                padding-top: 1rem;
            }}
            </style>
            """, unsafe_allow_html=True)

            # Usar tabs nativos de Streamlit - PERSISTENCIA AUTOMÁTICA
            tabs_components = st.tabs(tabs_available)

            # Renderizar contenido en cada tab
            for i, tab in enumerate(tabs_components):
                with tab:
                    tab_functions[i]()

        else:
            if app.user['role'] == 'invitado':
                st.info("ℹ️ **Usuario Invitado**: Solo tienes acceso al Dashboard básico. Para más funcionalidades, contacta al administrador.")
            else:
                st.error("❌ No tienes permisos para acceder a ninguna funcionalidad")

def render_assistant_message_with_css(content):
    """Renderizar mensaje del asistente con formato CSS adaptado según el tema"""

    # Detectar el tema actual
    current_theme = st.session_state.get('theme_mode', 'light')

    # Definir colores según el tema
    if current_theme == 'dark':
        text_color = '#ffffff'
        text_var = 'var(--text-color, #ffffff)'
    else:
        text_color = '#111827'  # Color oscuro para tema claro
        text_var = 'var(--text-primary, #111827)'

    # CSS EMBEBIDO para garantizar que funcione en Streamlit Cloud
    st.markdown(f"""
    <style>
    /* FORZAR VISIBILIDAD DE TEXTO EN CHAT AI - STREAMLIT CLOUD */
    .stChatMessage, .stChatMessage * {{
        color: {text_color} !important;
    }}

    .stMarkdown, .stMarkdown *, .element-container * {{
        color: {text_color} !important;
    }}

    /* Mantener texto blanco SOLO en fondos verdes */
    [style*="background: linear-gradient(135deg, #22c55e"] * {{
        color: white !important;
    }}

    [style*="background: linear-gradient(135deg, #4CAF50"] * {{
        color: white !important;
    }}
    </style>
    """, unsafe_allow_html=True)

    # Dividir contenido por párrafos
    paragraphs = content.split('\n\n')

    for paragraph in paragraphs:
        paragraph = paragraph.strip()
        if not paragraph:
            continue

        lines = paragraph.split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Limpiar contenido para evitar problemas de renderizado
            clean_line = line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

            # Títulos con ** ** (texto en negrita)
            if line.startswith('**') and line.endswith('**') and len(line) > 4:
                title_text = clean_line[2:-2].strip()
                st.markdown(f"""
                <div style="
                    background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%) !important;
                    color: white !important;
                    padding: 12px 16px !important;
                    border-radius: 6px !important;
                    margin: 12px 0 !important;
                    border: 1px solid #16a34a !important;
                    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2) !important;
                ">
                    <h4 style="margin: 0 !important; font-size: 16px !important; font-weight: 600 !important; color: white !important;">{title_text}</h4>
                </div>
                """, unsafe_allow_html=True)

            # Elementos de lista que empiezan con -
            elif line.startswith('- '):
                list_text = clean_line[2:].strip()
                # Procesar texto en negrita dentro de la lista
                list_text = list_text.replace('**', '')
                st.markdown(f"""
                <div style="
                    background: rgba(59, 130, 246, 0.1) !important;
                    color: {text_color} !important;
                    padding: 8px 12px !important;
                    border-left: 4px solid #3b82f6 !important;
                    margin: 6px 0 !important;
                    border-radius: 0 4px 4px 0 !important;
                ">
                    <span style="color: {text_color} !important; font-size: 14px !important;">• {list_text}</span>
                </div>
                """, unsafe_allow_html=True)

            # Texto con iconos al inicio
            elif any(line.startswith(icon) for icon in ['📋', '✅', '📊', '💡', '❌', '⚠️', '🔒']):
                st.markdown(f"""
                <div style="
                    background: rgba(99, 102, 241, 0.1) !important;
                    color: {text_color} !important;
                    padding: 10px 14px !important;
                    border-radius: 6px !important;
                    margin: 8px 0 !important;
                    border: 1px solid rgba(99, 102, 241, 0.3) !important;
                ">
                    <span style="color: {text_color} !important; font-size: 14px !important;">{clean_line}</span>
                </div>
                """, unsafe_allow_html=True)

            # Texto regular con formato mejorado
            else:
                # Procesar texto en negrita
                processed_text = clean_line
                if '**' in processed_text:
                    processed_text = processed_text.replace('**', '<strong style="color: #3b82f6 !important;">', 1)
                    processed_text = processed_text.replace('**', '</strong>', 1)

                st.markdown(f"""
                <div style="
                    color: {text_color} !important;
                    padding: 6px 0 !important;
                    line-height: 1.5 !important;
                ">
                    <span style="color: {text_color} !important; font-size: 14px !important;">{processed_text}</span>
                </div>
                """, unsafe_allow_html=True)

def render_secure_chat(app):
    """Chat con verificación de permisos, rate limiting y auditoría"""
    st.markdown("### 🤖 Asistente IA Seguro")
    
    if not app.require_permission('analisis_ia'):
        # Mensaje específico para cada rol sin permisos
        if app.user['role'] == 'invitado':
            st.warning("🔒 **Chat IA no disponible**: Los usuarios invitados no tienen acceso al asistente de IA.")
            st.info("💡 **Sugerencia**: Solicita una cuenta con permisos de 'Analista' o superior para acceder al Chat IA.")
        return
    
    # Verificar rate limiting para consultas IA
    if app.rate_limiter:
        allowed, message, details = app.rate_limiter.is_allowed(
            app.user['username'], 
            'ai_query'
        )
        if not allowed:
            st.error(f"🚫 {message}")
            if 'retry_after' in details:
                st.info(f"⏰ Intenta de nuevo en {details['retry_after']} segundos")
            return
        elif details.get('warning'):
            st.warning(f"⚠️ {details['warning']}")
    
    # Mostrar requests restantes y estado de procesamiento asíncrono
    col1, col2 = st.columns(2)
    
    with col1:
        if app.rate_limiter:
            remaining = app.rate_limiter.get_remaining_requests(app.user['username'], 'ai_query')
            st.info(f"📊 Consultas IA restantes: {remaining}")
    
    with col2:
        if app.ai_processor:
            # Mostrar métricas de procesamiento asíncrono
            try:
                metrics = app.ai_processor.get_async_processing_metrics()
                if 'error' not in metrics:
                    success_rate = (metrics.get('successful_requests', 0) / max(1, metrics.get('total_requests', 1))) * 100
                    st.success(f"🤖 IA Asíncrona: {success_rate:.1f}% éxito")
                else:
                    st.info("🤖 IA Asíncrona: Disponible")
            except:
                st.info("🤖 IA Asíncrona: Disponible")
    
    # Inicializar mensajes personalizados por usuario
    user_messages_key = f'secure_messages_{app.user["username"]}'
    if user_messages_key not in st.session_state:
        # Crear saludo personalizado según el rol
        role_specific_content = {
            'admin': {
                'greeting': 'Soy tu asistente de análisis sociosanitario con **acceso administrativo completo**.',
                'analyses': [
                    '• **Análisis Estratégico**: ROI hospitales, eficiencia gasto sanitario, sostenibilidad',
                    '• **Planificación**: ¿Dónde abrir próximo hospital? Optimización red hospitalaria',
                    '• **Gestión Integral**: Comparar rendimiento distritos, análisis equidad territorial',
                    '• **Reportes Ejecutivos**: Informes para Consejería, auditoría sistema',
                    '• **Inversiones**: ¿Qué centros necesitan más inversión? Planificación 5 años',
                    '• **Recursos**: Evaluación especialidades, distribución personal sanitario'
                ],
                'examples': [
                    '"Genera un informe ejecutivo del sistema sanitario"',
                    '"¿Cuál es el ROI de los hospitales por distrito?"',
                    '"Analiza eficiencia de gasto sanitario per cápita"',
                    '"¿Qué centros necesitan más inversión?"',
                    '"Compara rendimiento entre distritos sanitarios"',
                    '"¿Dónde abrir el próximo hospital?"',
                    '"Análisis de sostenibilidad financiera"',
                    '"¿Qué especialidades faltan más?"'
                ],
                'suggestion': 'Como administrador, tienes acceso completo a análisis estratégicos, financieros y de planificación.'
            },
            'gestor': {
                'greeting': 'Soy tu asistente especializado en **gestión sanitaria operacional**.',
                'analyses': [
                    '• **Optimización Camas**: Ocupación, turnos, redistribución de recursos',
                    '• **Gestión Flujos**: Tiempos espera, saturación, rutas ambulancias',
                    '• **Personal**: Distribución plantilla, planificación turnos según demanda',
                    '• **Servicios**: Infrautilización, refuerzo urgencias, coordinación centros',
                    '• **Planificación**: Recursos invierno/verano, capacidad asistencial',
                    '• **Eficiencia**: Análisis productividad, indicadores operacionales'
                ],
                'examples': [
                    '"¿Cómo optimizar la ocupación de camas?"',
                    '"Analiza tiempos de espera por especialidad"',
                    '"¿Qué hospitales están saturados?"',
                    '"¿Cómo redistribuir personal sanitario?"',
                    '"Analiza flujos de pacientes entre centros"',
                    '"¿Qué servicios están infrautilizados?"',
                    '"Optimiza rutas de ambulancias"',
                    '"¿Dónde reforzar urgencias?"',
                    '"Planifica recursos para invierno"'
                ],
                'suggestion': 'Como gestor, puedes optimizar recursos, flujos de pacientes y eficiencia operativa.'
            },
            'analista': {
                'greeting': 'Soy tu asistente especializado en **análisis estadístico y de datos sanitarios**.',
                'analyses': [
                    '• **Correlaciones**: Renta vs esperanza vida, factores sociales de salud',
                    '• **Visualizaciones**: Heatmaps mortalidad, clustering municipios, mapas inequidad',
                    '• **Predictivo**: Modelos demanda, tendencias envejecimiento, supervivencia',
                    '• **Equidad**: Acceso especialidades, inequidades territoriales',
                    '• **Epidemiología**: Análisis preventivo, factores riesgo poblacional',
                    '• **Estadística**: Análisis multivariante, regresiones, tests significancia'
                ],
                'examples': [
                    '"Correlación entre renta y esperanza de vida"',
                    '"Heatmap de mortalidad infantil por zona"',
                    '"¿Hay inequidades en acceso a cardiología?"',
                    '"Análisis demográfico predictivo"',
                    '"¿Qué factores afectan más la salud?"',
                    '"Clustering de municipios similares"',
                    '"Tendencias de envejecimiento poblacional"',
                    '"¿Dónde concentrar prevención?"',
                    '"Modelos predictivos de demanda"',
                    '"Análisis de supervivencia por distrito"'
                ],
                'suggestion': 'Como analista, puedes realizar estudios estadísticos avanzados y modelos predictivos.'
            },
            'invitado': {
                'greeting': 'Soy tu asistente de consulta para **información básica del sistema sanitario**.',
                'analyses': [
                    '• **Ubicaciones**: Hospitales cercanos, centros de salud, especialidades',
                    '• **Servicios**: ¿Qué especialidades están disponibles? Horarios, contactos',
                    '• **Acceso**: ¿Cómo llegar? Transporte público, tiempos de viaje',
                    '• **Información Básica**: Datos generales municipios, población, servicios',
                    '• **Orientación**: Primeros auxilios, consejos salud general'
                ],
                'examples': [
                    '"¿Dónde está el hospital más cercano?"',
                    '"¿Qué servicios tiene mi centro de salud?"',
                    '"Información básica de mi municipio"',
                    '"¿Cómo llegar al hospital de Málaga?"',
                    '"¿Qué especialidades hay disponibles?"',
                    '"¿Cuál es el teléfono de urgencias?"'
                ],
                'suggestion': 'Como invitado, puedes consultar información general y de orientación sanitaria.'
            }
        }
        
        current_role_content = role_specific_content.get(app.user['role'], role_specific_content['invitado'])
        
        st.session_state[user_messages_key] = [
            {"role": "assistant", "content": f"""¡Hola **{app.user['name']}**! 👋

{current_role_content['greeting']}

**🔐 Sesión Autenticada:**
- **Usuario:** {app.user['username']}
- **Rol:** {app.role_info['icon']} {app.role_info['name']}
- **Organización:** {app.user['organization']}

**🎯 Análisis Disponibles para tu rol:**

{'  \n'.join(current_role_content['analyses'])}

**💡 {current_role_content['suggestion']}**

**📝 Ejemplos de Consultas que puedes hacer:**

{'  \n'.join(current_role_content['examples'])}

**🚀 ¡Prueba cualquiera de estos ejemplos o haz tu propia consulta!**"""}
        ]
    
    # Mostrar mensaje de bienvenida inicial (solo si no hay interacción previa)
    if len(st.session_state[user_messages_key]) == 1:
        # Mostrar mensaje de bienvenida directamente, no como chat
        welcome_msg = st.session_state[user_messages_key][0]["content"]
        with st.chat_message("assistant"):
            render_assistant_message_with_css(welcome_msg)

        # Separador antes del input
        st.markdown("---")

        # Input del usuario - JUSTO DESPUÉS del mensaje de bienvenida
        prompt = st.chat_input(f"💬 Consulta como {app.role_info['name']}...")

    else:
        # Ya hay interacciones, mostrar historial completo
        st.markdown("---")
        st.markdown("### 💬 Historial de Conversación")

        for message in st.session_state[user_messages_key]:
            with st.chat_message(message["role"]):
                if message["role"] == "assistant":
                    render_assistant_message_with_css(message["content"])
                else:
                    st.markdown(message["content"])

        # Separador antes del input
        st.markdown("---")

        # Input del usuario - DESPUÉS del historial
        prompt = st.chat_input(f"💬 Consulta como {app.role_info['name']}...")

    # Procesar nuevo prompt si existe
    if prompt:
        # Registrar intento de consulta IA
        if app.security_auditor:
            app.security_auditor.log_user_action(
                user=app.user['username'],
                action="ai_query",
                resource="chat_interface",
                success=True,
                details={"prompt_length": len(prompt), "role": app.user['role']}
            )
        
        # Añadir contexto de usuario a la consulta
        enhanced_prompt = f"[Usuario: {app.user['name']}, Rol: {app.role_info['name']}, Org: {app.user['organization']}] {prompt}"
        
        st.session_state[user_messages_key].append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Procesar con IA si está disponible
        with st.chat_message("assistant"):
            if app.ai_processor and app.chart_generator:
                with st.spinner("🔒 Procesando consulta segura con IA asíncrona..."):
                    try:
                        # Procesar consulta con contexto de rol usando procesamiento asíncrono
                        #analysis = app.ai_processor.process_health_query_async(
                        #    enhanced_prompt, 
                        #    app.data, 
                        #    app.user['role']
                        #)
                        
                        
                        async_wrapper = get_streamlit_async_wrapper()
                        analysis = async_wrapper.process_query_sync(
                            enhanced_prompt, 
                            app.data, 
                            app.user['role']
                        )

                        if analysis.get('analysis_type') != 'error':
                            # Mostrar análisis completo con información de auditoría
                            # Usar full_response si está disponible, sino usar main_insight
                            full_response = analysis.get('full_response', '')
                            main_insight = analysis.get('main_insight', 'Análisis completado')
                            detailed_analysis = analysis.get('detailed_analysis', '')
                            summary = analysis.get('summary', '')
                            content = analysis.get('content', '')
                            
                            # Usar full_response como prioridad, sino combinar otros campos
                            if full_response:
                                full_analysis = full_response
                            else:
                                full_analysis = f"""
# {main_insight}

{detailed_analysis if detailed_analysis else ''}

{summary if summary else ''}
"""
                                if detailed_analysis:
                                    full_analysis += f"\n\n{detailed_analysis}"
                                if summary:
                                    full_analysis += f"\n\n{summary}"
                                if content:
                                    full_analysis += f"\n\n{content}"
                            
                            # Definir función de procesamiento de texto para evitar problemas de alcance
                            def process_analysis_text(text):
                                import re  # Importar re localmente para evitar problemas de ámbito
                                # Eliminar divs y spans HTML
                                text = text.strip()
                                text = re.sub(r'<div[^>]*>|</div>|<span[^>]*>|</span>', '', text)
                                
                                # Convertir tablas mal formateadas a formato markdown
                                table_pattern = r'\|\s*([^|\n]+)\s*\|\s*(\d[\d.,]*)\s*\|\s*(\d[\d.,]*)\s*\|\s*([^|\n]+)\s*\|'
                                text = re.sub(table_pattern, 
                                           lambda m: f"\n| {m.group(1).strip()} | {m.group(2)} | {m.group(3)} | {m.group(4).strip()} |", 
                                           text)
                                return text
                            
                            # Procesar el texto del análisis
                            cleaned_analysis = process_analysis_text(full_analysis)
                            
                                                        # Procesar las tablas en el análisis
                            lines = cleaned_analysis.split('\n')
                            processed_lines = []
                            current_table = []
                            in_table = False
                            
                            # Si encontramos una línea que es parte de una tabla
                            for line in lines:
                                if '|' in line:
                                    if not in_table:
                                        in_table = True
                                    current_table.append(line.strip())
                                elif in_table:
                                    # Termina la tabla actual
                                    if current_table:
                                        # Si no hay separador, crear uno
                                        if not any('---' in row for row in current_table):
                                            header = current_table[0]
                                            separator = '|' + '|'.join('-' * len(part.strip()) for part in header.split('|')[1:-1]) + '|'
                                            current_table.insert(1, separator)
                                        processed_lines.extend(current_table)
                                        processed_lines.append('')
                                    current_table = []
                                    in_table = False
                                    if line.strip():
                                        processed_lines.append(line)
                                else:
                                    if line.strip():
                                        processed_lines.append(line)
                            
                            # Procesar la última tabla si existe
                            if current_table:
                                if not any('---' in row for row in current_table):
                                    header = current_table[0]
                                    separator = '|' + '|'.join('-' * len(part.strip()) for part in header.split('|')[1:-1]) + '|'
                                    current_table.insert(1, separator)
                                processed_lines.extend(current_table)
                            
                            cleaned_analysis = '\n'.join(processed_lines)
                            
                            # Importar re localmente para evitar problemas de ámbito
                            import re
                            
                            # Formatear encabezados markdown
                            cleaned_analysis = re.sub(r'^(?!#)([A-Z][^\n:]+:)', r'### \1', cleaned_analysis, flags=re.MULTILINE)
                            
                            # Formatear secciones y subsecciones
                            sections = {
                                'Resumen Ejecutivo': '## ',
                                'Análisis de Indicadores': '## ',
                                'Métricas de Rendimiento': '## ',
                                'Recomendaciones Estratégicas': '## ',
                                'Conclusión': '## '
                            }
                            
                            for section, prefix in sections.items():
                                cleaned_analysis = re.sub(f'^{section}:', f'{prefix}{section}', 
                                                       cleaned_analysis, flags=re.MULTILINE)
                            
                            # Formatear listas
                            cleaned_analysis = re.sub(r'^[-*]\s+', '- ', cleaned_analysis, flags=re.MULTILINE)
                            
                            # Formatear negritas
                            cleaned_analysis = re.sub(r'\*\*([^*]+)\*\*-', r'**\1**:', cleaned_analysis)
                            
                            # Eliminar líneas vacías excesivas
                            cleaned_analysis = re.sub(r'\n{3,}', '\n\n', cleaned_analysis)
                            
                            # Asegurar espaciado consistente alrededor de secciones
                            cleaned_analysis = re.sub(r'(#{1,3}[^\n]+)\n(?!\n)', r'\1\n\n', cleaned_analysis)
                            
                            # Procesar el texto para el formato profesional
                            processed_text = cleaned_analysis

                            # Mostrar análisis con cabecera profesional
                            st.markdown("---")

                            # Cabecera del análisis
                            st.markdown(f"""
                            <div style="
                                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                                color: white;
                                padding: 20px;
                                border-radius: 10px;
                                margin: 20px 0;
                                text-align: center;
                            ">
                                <h2 style="margin: 0; font-size: 24px;">🔍 Análisis del Sistema Sanitario</h2>
                                <p style="margin: 8px 0 0 0; opacity: 0.9;">Copilot Salud Andalucía - {app.role_info['name']}</p>
                            </div>
                            """, unsafe_allow_html=True)

                            # Información del usuario
                            col1, col2 = st.columns(2)
                            with col1:
                                st.info(f"👤 **Usuario:** {app.user['name']}")
                            with col2:
                                st.info(f"📅 **Generado:** {datetime.now().strftime('%d/%m/%Y %H:%M')}")

                            st.markdown("---")

                            # Función para procesar y mostrar contenido con formato profesional
                            def render_professional_analysis(text, theme):
                                lines = text.split('\n')

                                for line in lines:
                                    line = line.strip()
                                    # Filtrar líneas vacías, con solo espacios o caracteres especiales
                                    if not line or len(line) < 3 or line in ['---', '___', '***']:
                                        continue

                                    # Limpiar contenido para evitar problemas de renderizado
                                    clean_line = line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

                                    # Títulos principales
                                    if clean_line.startswith('# '):
                                        st.markdown(f"""
                                        <div style="
                                            background: linear-gradient(135deg, #3b82f6 0%, #1e40af 100%) !important;
                                            color: white !important;
                                            padding: 18px !important;
                                            border-radius: 8px !important;
                                            margin: 16px 0 !important;
                                            text-align: center !important;
                                            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3) !important;
                                            border: 2px solid #1e40af !important;
                                        ">
                                            <h2 style="margin: 0 !important; font-size: 20px !important; font-weight: 600 !important; color: white !important; text-shadow: 1px 1px 2px rgba(0,0,0,0.5) !important;">{clean_line[2:].strip()}</h2>
                                        </div>
                                        """, unsafe_allow_html=True)

                                    # Títulos secundarios
                                    elif clean_line.startswith('## '):
                                        subtitle_text = clean_line[3:].strip()
                                        if subtitle_text:  # Solo mostrar si hay contenido
                                            st.markdown(f"""
                                            <div style="
                                                background: rgba(59, 130, 246, 0.1) !important;
                                                border-left: 4px solid #3b82f6 !important;
                                                padding: 15px !important;
                                                margin: 15px 0 !important;
                                                border-radius: 5px !important;
                                                box-shadow: 0 2px 4px rgba(59, 130, 246, 0.2) !important;
                                                border: 1px solid rgba(59, 130, 246, 0.3) !important;
                                            ">
                                                <h3 style="margin: 0 !important; color: #3b82f6 !important; font-size: 18px !important; font-weight: 600 !important; text-shadow: none !important;">{subtitle_text}</h3>
                                            </div>
                                            """, unsafe_allow_html=True)

                                    # Subtítulos
                                    elif clean_line.startswith('### '):
                                        subheading_text = clean_line[4:].strip()
                                        if subheading_text:  # Solo mostrar si hay contenido
                                            st.markdown(f"""
                                            <div style="
                                                background: rgba(100, 116, 139, 0.1) !important;
                                                border-left: 3px solid #64748b !important;
                                                padding: 12px !important;
                                                margin: 12px 0 !important;
                                                border-radius: 4px !important;
                                                border: 1px solid rgba(100, 116, 139, 0.3) !important;
                                            ">
                                                <h4 style="margin: 0 !important; color: #64748b !important; font-size: 16px !important; font-weight: 500 !important;">{subheading_text}</h4>
                                            </div>
                                            """, unsafe_allow_html=True)

                                    # Contenido con formato especial para información importante
                                    elif clean_line.startswith('**') and clean_line.endswith('**'):
                                        bold_text = clean_line[2:-2].strip()
                                        if bold_text:  # Solo mostrar si hay contenido
                                            # Colores según tema
                                            bg_color = '#dbeafe' if theme == 'light' else '#1e40af'
                                            text_color = '#1e40af' if theme == 'light' else '#ffffff'
                                            border_color = '#3b82f6' if theme == 'light' else '#60a5fa'
                                            st.markdown(f"""
                                            <div style="
                                                background: {bg_color};
                                                border: 1px solid {border_color};
                                                padding: 12px;
                                                margin: 8px 0;
                                                border-radius: 6px;
                                                font-weight: 600;
                                                color: {text_color};
                                            ">
                                                <strong>{bold_text}</strong>
                                            </div>
                                            """, unsafe_allow_html=True)

                                    # Listas con viñetas
                                    elif clean_line.startswith('- '):
                                        list_text = clean_line[2:].strip()
                                        if list_text:  # Solo mostrar si hay contenido
                                            # Determinar color según tema actual
                                            bullet_text_color = '#0f172a' if theme == 'light' else '#f8fafc'
                                            st.markdown(f"""
                                            <div style="
                                                margin: 4px 0 !important;
                                                padding: 8px 20px !important;
                                                color: {bullet_text_color} !important;
                                                background: rgba(59, 130, 246, 0.1) !important;
                                                border-radius: 4px !important;
                                                border-left: 3px solid #3b82f6 !important;
                                            ">
                                                <span style="color: #3b82f6 !important; font-weight: bold !important;">•</span> {list_text}
                                            </div>
                                            """, unsafe_allow_html=True)

                                    # Listas numeradas
                                    elif any(clean_line.startswith(f'{i}. ') for i in range(1, 10)):
                                        numbered_text_color = '#0f172a' if theme == 'light' else '#f8fafc'
                                        st.markdown(f"""
                                        <div style="margin: 4px 0 !important; padding: 8px 12px !important; background: rgba(100, 116, 139, 0.1) !important; border-radius: 4px !important; color: {numbered_text_color} !important; border-left: 3px solid #64748b !important;">
                                            {clean_line}
                                        </div>
                                        """, unsafe_allow_html=True)

                                    # Resaltado de contenido importante
                                    elif any(word in clean_line.lower() for word in ['importante', 'clave', 'crítico', 'esencial', 'alerta']):
                                        # Colores según tema
                                        bg_color = '#fef3c7' if theme == 'light' else '#92400e'
                                        text_color = '#92400e' if theme == 'light' else '#ffffff'
                                        border_color = '#f59e0b' if theme == 'light' else '#fbbf24'
                                        st.markdown(f"""
                                        <div style="
                                            background: {bg_color};
                                            border: 1px solid {border_color};
                                            padding: 12px;
                                            border-radius: 6px;
                                            margin: 8px 0;
                                            color: {text_color};
                                        ">
                                            ⚠️ {clean_line}
                                        </div>
                                        """, unsafe_allow_html=True)

                                    elif any(word in clean_line.lower() for word in ['recomendación', 'sugerencia', 'mejora', 'optimización']):
                                        # Colores según tema
                                        bg_color = '#dcfce7' if theme == 'light' else '#065f46'
                                        text_color = '#166534' if theme == 'light' else '#ffffff'
                                        border_color = '#16a34a' if theme == 'light' else '#34d399'
                                        st.markdown(f"""
                                        <div style="
                                            background: {bg_color};
                                            border: 1px solid {border_color};
                                            padding: 12px;
                                            border-radius: 6px;
                                            margin: 8px 0;
                                            color: {text_color};
                                        ">
                                            💡 {clean_line}
                                        </div>
                                        """, unsafe_allow_html=True)

                                    elif any(word in clean_line.lower() for word in ['conclusión', 'resultado', 'hallazgo', 'resumen']):
                                        # Colores según tema
                                        bg_color = '#eff6ff' if theme == 'light' else '#1e3a8a'
                                        text_color = '#1e40af' if theme == 'light' else '#ffffff'
                                        border_color = '#3b82f6' if theme == 'light' else '#60a5fa'
                                        st.markdown(f"""
                                        <div style="
                                            background: {bg_color};
                                            border: 1px solid {border_color};
                                            padding: 12px;
                                            border-radius: 6px;
                                            margin: 8px 0;
                                            color: {text_color};
                                        ">
                                            📋 {clean_line}
                                        </div>
                                        """, unsafe_allow_html=True)

                                    # Líneas con tablas (saltar, se procesan después)
                                    elif '|' in clean_line and clean_line.startswith('|'):
                                        continue

                                    # Contenido normal
                                    else:
                                        # Solo mostrar si tiene contenido significativo
                                        if clean_line and len(clean_line.strip()) > 2:
                                            default_text_color = '#0f172a' if theme == 'light' else '#f8fafc'
                                            st.markdown(f"""
                                            <div style="
                                                margin: 6px 0 !important;
                                                line-height: 1.6 !important;
                                                color: {default_text_color} !important;
                                                padding: 8px 12px !important;
                                                background: rgba(255, 255, 255, 0.05) !important;
                                                border-radius: 4px !important;
                                                border-left: 2px solid #3b82f6 !important;
                                                font-size: 14px !important;
                                            ">
                                                {clean_line}
                                            </div>
                                            """, unsafe_allow_html=True)

                            # Renderizar el análisis con formato profesional
                            # Obtener tema actual desde session_state
                            chat_theme = st.session_state.get('theme_mode', 'light')
                            render_professional_analysis(processed_text, chat_theme)

                            # Información sobre la exportación PDF
                            st.info("📋 **Exportación PDF**: Se genera un documento profesional con cabecera corporativa, estilos mejorados y formato optimizado para presentaciones.")
                            
                            # Botón para exportar a PDF (usa función global create_pdf_bytes)
                            try:
                                # Detectar bloques de tablas Markdown para intentar renderizarlas en el PDF
                                def extract_markdown_tables(text: str):
                                    tables = []
                                    lines = [l for l in text.split('\n')]
                                    cur = []
                                    for line in lines:
                                        if line.strip().startswith('|') and '|' in line:
                                            cur.append(line)
                                        else:
                                            if cur:
                                                tables.append(cur)
                                                cur = []
                                    if cur:
                                        tables.append(cur)
                                    return tables

                                tables = extract_markdown_tables(processed_text)

                                # Usar siempre la función create_pdf_bytes profesional
                                if False:  # Deshabilitado: usar siempre create_pdf_bytes
                                    # Construir un texto base y adjuntar tablas en el PDF
                                    from reportlab.platypus import Table as RLTable, TableStyle
                                    from reportlab.lib import colors
                                    from io import BytesIO

                                    # Intentaremos componer un Story similar al create_pdf_bytes
                                    from reportlab.lib.styles import getSampleStyleSheet
                                    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
                                    from reportlab.lib.units import mm

                                    buffer = BytesIO()
                                    doc = SimpleDocTemplate(buffer, pagesize=A4,
                                                            rightMargin=20*mm, leftMargin=20*mm,
                                                            topMargin=20*mm, bottomMargin=20*mm)
                                    styles = getSampleStyleSheet()
                                    story = []
                                    story.append(Paragraph(f"Análisis generado por {app.user['name']}", styles['Heading2']))
                                    story.append(Spacer(1, 4))
                                    # En lugar de texto simple, usar la función profesional
                                    # Desactivar esta generación manual y usar solo create_pdf_bytes
                                    pass  # Se elimina para usar solo create_pdf_bytes
                                    story.append(Spacer(1, 6))

                                    # Añadir la primera tabla detectada (si existe)
                                    if tables:
                                        try:
                                            md_table = tables[0]
                                            # Parsear cabecera y filas
                                            rows = []
                                            for r in md_table:
                                                # Quitar barras laterales y separar por |
                                                cols = [c.strip() for c in r.strip().strip('|').split('|')]
                                                rows.append(cols)
                                            rl_table = RLTable(rows, hAlign='LEFT')
                                            rl_table.setStyle(TableStyle([
                                                ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f2f7fb')),
                                                ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
                                                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                                                ('ALIGN', (0,0), (-1,-1), 'LEFT'),
                                            ]))
                                            story.append(rl_table)
                                            story.append(Spacer(1,6))
                                        except Exception:
                                            # Si falla la conversión, continuar sin tabla
                                            pass

                                    doc.build(story)
                                    buffer.seek(0)
                                    report_bytes = buffer.read()

                                # Usar siempre la función profesional create_pdf_bytes
                                if REPORTLAB_AVAILABLE:
                                    # Usar el header mejorado por defecto con título más descriptivo
                                    report_title = f"Análisis del Sistema Sanitario - {app.user['name']}"
                                    report_bytes = create_pdf_bytes(report_title, processed_text, use_simple_header=False)
                                else:
                                    report_bytes = None

                                # Ofrecer descarga del PDF profesional
                                if report_bytes:
                                    st.download_button(
                                    "📋 Exportar Reporte PDF Profesional",
                                    data=report_bytes,
                                    file_name=f"reporte_sanitario_{app.user['username']}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                                    mime='application/pdf',
                                    help="Documento PDF con diseño profesional, cabecera corporativa y formato optimizado"
                                )
                                else:
                                    st.error("❌ No se pudo generar el PDF del análisis con reportlab.")
                                    # Siempre ofrecer exportación HTML que preserva CSS para imprimir a PDF desde el navegador
                                    try:
                                        css_inline = extra_css if extra_css else ''
                                    except Exception:
                                        css_inline = ''

                                    html_export = f"""
                                    <!doctype html>
                                    <html lang=\"es\"> 
                                    <head>
                                    <meta charset=\"utf-8\" />
                                    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
                                    <style>
                                    {css_inline}
                                    body {{ font-family: Inter, Poppins, Arial, sans-serif; padding:20px; background:#fff; color:#111 }}
                                    .analysis-card {{ 
                                        margin-bottom: 12px; 
                                        padding: 16px; 
                                        border: 1px solid #e2e8f0; 
                                        border-radius: 8px; 
                                        background: #f8fafc;
                                    }}
                                    .analysis-title {{ 
                                        font-size: 18px; 
                                        font-weight: 600; 
                                        color: #1e293b; 
                                        margin-bottom: 8px;
                                    }}
                                    .analysis-subtitle {{ 
                                        font-size: 14px; 
                                        color: #64748b; 
                                        margin-bottom: 12px;
                                    }}
                                    .analysis-highlight {{ 
                                        background: #dbeafe; 
                                        color: #1e40af; 
                                        padding: 4px 8px; 
                                        border-radius: 4px; 
                                        font-size: 12px; 
                                        font-weight: 500;
                                    }}
                                    </style>
                                    <title>Análisis - {app.user['name']}</title>
                                    </head>
                                    <body>
                                    <div class=\"analysis-card\">{processed_text.split('\n')[0][:1000].replace('\n','<br/>')}</div>
                                    <div>{processed_text.replace('\n','<br/>')}</div>
                                    </body>
                                    </html>
                                    """

                                    st.download_button(
                                        "🌐 Exportar Reporte HTML Profesional",
                                        data=html_export,
                                        file_name=f"reporte_sanitario_{app.user['username']}_{datetime.now().strftime('%Y%m%d_%H%M')}.html",
                                        mime='text/html',
                                        help="Documento HTML profesional optimizado para impresión y presentaciones"
                                    )

                                    # Ofrecer también TXT como última opción
                                    st.download_button("📄 Exportar análisis (TXT)", data=cleaned_analysis, file_name=f"analisis_{app.user['username']}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt", mime='text/plain')

                            except Exception as e:
                                # Si reportlab no está instalado, dar una instrucción clara para instalarlo
                                if 'reportlab' in str(e).lower():
                                    st.error("❌ reportlab no disponible: instala con `pip install reportlab` e intenta de nuevo.")
                                else:
                                    st.error(f"❌ Error exportando análisis: {e}")
                                # Fallback claro a TXT
                                st.download_button("📄 Exportar análisis (TXT)", data=cleaned_analysis, file_name=f"analisis_{app.user['username']}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt", mime='text/plain')

                            # Verificar si necesita visualización y generar gráficos
                            if analysis.get('needs_visualization', False) and analysis.get('chart_config'):
                                chart_config = analysis.get('chart_config', {})
                                st.markdown("---")
                                st.markdown("### 📊 Visualizaciones Generadas Automáticamente")

                                try:
                                    # Generar gráfico basado en la configuración
                                    if app.chart_generator:
                                        # Determinar qué dataset usar basado en data_query
                                        data_query = analysis.get('data_query', 'data')

                                        if data_query and data_query != 'data':
                                            # Usar dataset específico (ej: data['hospitales'])
                                            try:
                                                dataset_name = data_query.replace("data['", "").replace("']", "")
                                                chart_data_input = app.data.get(dataset_name, app.data['hospitales'])
                                            except Exception:
                                                chart_data_input = app.data['hospitales']
                                        else:
                                            chart_data_input = app.data['hospitales']

                                        # Mejorar configuración del gráfico con datos específicos
                                        enhanced_config = chart_config.copy()
                                        if enhanced_config.get('x_axis') is None and len(chart_data_input.columns) > 0:
                                            # Seleccionar automáticamente columnas apropiadas
                                            if 'nombre' in chart_data_input.columns:
                                                enhanced_config['x_axis'] = 'nombre'
                                            elif 'municipio' in chart_data_input.columns:
                                                enhanced_config['x_axis'] = 'municipio'
                                            elif 'distrito' in chart_data_input.columns:
                                                enhanced_config['x_axis'] = 'distrito'
                                            else:
                                                enhanced_config['x_axis'] = chart_data_input.columns[0]

                                        if enhanced_config.get('y_axis') is None and len(chart_data_input.columns) > 1:
                                            # Buscar columnas numéricas relevantes
                                            numeric_cols = chart_data_input.select_dtypes(include=['number']).columns
                                            if 'camas_funcionamiento_2025' in numeric_cols:
                                                enhanced_config['y_axis'] = 'camas_funcionamiento_2025'
                                            elif 'personal_total' in numeric_cols:
                                                enhanced_config['y_axis'] = 'personal_total'
                                            elif len(numeric_cols) > 0:
                                                enhanced_config['y_axis'] = numeric_cols[0]

                                        chart_data = app.chart_generator.generate_chart(
                                            enhanced_config,
                                            chart_data_input,
                                            st.session_state.get('theme_mode', 'light')
                                        )

                                        if chart_data:
                                            # Aplicar correcciones de hover antes de mostrar
                                            chart_data = fix_plotly_hover_issues(chart_data)
                                            st.plotly_chart(chart_data, use_container_width=True)
                                            st.success("📊 Visualización generada automáticamente")
                                        else:
                                            st.info("📈 Visualización sugerida: " + chart_config.get('title', 'Gráfico recomendado'))
                                    else:
                                        st.info("📈 Visualización sugerida: " + chart_config.get('title', 'Gráfico recomendado'))
                                except Exception as e:
                                    st.warning(f"⚠️ No se pudo generar la visualización: {str(e)}")
                                    st.info("📈 Visualización sugerida: " + chart_config.get('title', 'Gráfico recomendado'))

                            # Agregar respuesta completa al historial (usar respuesta de IA)
                            response = full_response

                        else:
                            response = f"❌ **Error en análisis**: {analysis.get('main_insight', 'No se pudo procesar')}"

                    except Exception as e:
                        response = f"⚠️ **Error de sistema**: {str(e)}"
                        st.error(response)
            else:
                response = "🔒 **IA requiere configuración** o permisos insuficientes."
                st.warning(response)
            
            st.session_state[user_messages_key].append({"role": "assistant", "content": response})

def render_secure_dashboard(app):
    """Dashboard personalizado según el rol del usuario"""
    
    if not app.require_permission('ver_datos'):
        return
    
    if not app.data:
        st.error("❌ No hay datos disponibles. Ejecuta data_collector_2025.py")
        return
    
    # Usar dashboard personalizado si está disponible
    if app.role_dashboards and ROLE_DASHBOARDS_AVAILABLE:
        try:
            app.role_dashboards.render_personalized_dashboard(
                app.user['role'], 
                app.data, 
                app.role_info
            )
            return
        except Exception as e:
            st.error(f"❌ Error en dashboard personalizado: {str(e)}")
            st.info("🔄 Usando dashboard por defecto...")
    
    # Dashboard por defecto si no hay personalización
    st.markdown("### 📊 Dashboard Seguro")
    
    # Información de acceso
    st.markdown(f"""
    <div class="access-granted">
        ✅ <strong>Acceso Autorizado a Dashboard</strong> | Usuario: {app.user['name']} | Rol: {app.role_info['name']}
        </div>
        """, unsafe_allow_html=True)
    
    # Métricas básicas (todos los roles con ver_datos)
    col1, col2, col3, col4 = st.columns(4)
    
    total_pop = app.data['demografia']['poblacion_2025'].sum()
    total_hospitals = len(app.data['hospitales'])
    total_beds = app.data['hospitales']['camas_funcionamiento_2025'].sum()
    
    with col1:
        st.metric("👥 Población", f"{total_pop/1000:.0f}K")
    with col2:
        st.metric("🏥 Centros", total_hospitals)
    with col3:
        st.metric("🛏️ Camas", f"{total_beds:,}")
    with col4:
        bed_ratio = (total_beds / total_pop) * 1000
        st.metric("Camas/1000 hab", f"{bed_ratio:.1f}")
    
    # Contenido adicional basado en permisos
    if app.has_permission('analisis_ia'):
        st.markdown("---")
        st.markdown("#### 📈 Análisis Avanzado (Autorizado)")
    elif app.user['role'] == 'invitado':
        st.markdown("---")
        st.markdown("#### 📊 Dashboard Básico")
        st.info("🔒 **Usuario Invitado**: Acceso limitado a métricas generales. Para análisis avanzados, contacta al administrador.")
        
        tab1, tab2, tab3 = st.tabs(["🏥 Infraestructura", "👥 Demografía", "🔬 Servicios"])
        
        with tab1:
            # Gráfico de hospitales por tipo
            tipo_counts = app.data['hospitales']['tipo_centro'].value_counts()
            fig_tipos = px.pie(
                values=tipo_counts.values,
                names=tipo_counts.index,
                title="🏥 Distribución de Centros por Tipo",
                hole=0.4
            )
            fig_tipos.update_traces(textposition='inside', textinfo='percent+label')
            fig_tipos = fix_plotly_hover_issues(fig_tipos)  # Aplicar correcciones
            st.plotly_chart(fig_tipos, use_container_width=True)
            
            # Capacidad hospitalaria
            fig_hospitales = px.bar(
                app.data['hospitales'],
                x='nombre',
                y='camas_funcionamiento_2025',
                title="🛏️ Capacidad Hospitalaria",
                color='tipo_centro',
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig_hospitales.update_xaxes(tickangle=45)
            fig_hospitales = fix_plotly_hover_issues(fig_hospitales)
            st.plotly_chart(fig_hospitales, use_container_width=True)
        
        with tab2:
            # Top municipios por población
            top_pop = app.data['demografia'].nlargest(12, 'poblacion_2025')
            fig_demo = px.bar(
                top_pop,
                x='municipio',
                y='poblacion_2025',
                title="👥 Top 12 Municipios por Población",
                color='crecimiento_2024_2025',
                color_continuous_scale='Viridis'
            )
            fig_demo.update_xaxes(tickangle=45)
            fig_demo = fix_plotly_hover_issues(fig_demo)
            st.plotly_chart(fig_demo, use_container_width=True)
            
            # Análisis de densidad vs renta
            fig_scatter = px.scatter(
                app.data['demografia'],
                x='densidad_hab_km2_2025',
                y='renta_per_capita_2024',
                size='poblacion_2025',
                color='indice_envejecimiento_2025',
                hover_data=['municipio'],
                title="🏘️ Densidad vs Renta per Cápita",
                color_continuous_scale='Spectral_r'
            )
            fig_scatter = fix_plotly_hover_issues(fig_scatter)
            st.plotly_chart(fig_scatter, use_container_width=True)
        
        with tab3:
            # Análisis de servicios
            servicios_bool = app.data['servicios'].select_dtypes(include=['bool'])
            if not servicios_bool.empty:
                # Estadísticas de cobertura
                coverage_stats = (servicios_bool.mean() * 100).round(1).sort_values(ascending=False)
                
                fig_coverage = px.bar(
                    x=coverage_stats.index,
                    y=coverage_stats.values,
                    title="📊 Cobertura de Servicios (%)",
                    color=coverage_stats.values,
                    color_continuous_scale='RdYlGn'
                )
                fig_coverage.update_xaxes(tickangle=45)
                fig_coverage.add_hline(y=75, line_dash="dash", line_color="red", 
                                     annotation_text="Objetivo mínimo 75%")
                fig_coverage = fix_plotly_hover_issues(fig_coverage)
                st.plotly_chart(fig_coverage, use_container_width=True)
                
                # Matriz de servicios
                services_matrix = servicios_bool.astype(int)
                services_matrix.index = app.data['servicios']['centro_sanitario']
                
                fig_heatmap = px.imshow(
                    services_matrix.T,
                    title="🔬 Matriz de Servicios Disponibles",
                    color_continuous_scale='RdYlGn',
                    aspect='auto'
                )
                fig_heatmap.update_layout(height=400)
                fig_heatmap = fix_plotly_hover_issues(fig_heatmap)
                st.plotly_chart(fig_heatmap, use_container_width=True)
                    
            else:
                st.info("📊 Análisis avanzado disponible con permisos de 'analisis_ia'")

def render_secure_reportes(app):
    """Sistema de reportes con control de acceso"""
    st.markdown("### 📋 Reportes Seguros")
    
    if not app.require_permission('reportes'):
        # Mensaje específico para cada rol sin permisos
        if app.user['role'] == 'invitado':
            st.warning("🔒 **Reportes no disponibles**: Los usuarios invitados no tienen acceso a reportes avanzados.")
            st.info("💡 **Sugerencia**: Solicita una cuenta con permisos de 'Analista' o superior para acceder a los reportes.")
        return
    
    st.markdown(f"""
    <div class="access-granted">
        ✅ <strong>Acceso Autorizado a Reportes</strong> | Usuario: {app.user['name']}
    </div>
    """, unsafe_allow_html=True)
    
    # Selector de tipo de reporte
    report_types = ["📈 Reporte Ejecutivo", "🏥 Análisis de Infraestructura", "👥 Reporte Demográfico"]
    
    # Solo administradores pueden acceder al análisis de equidad
    if app.has_permission('analisis_equidad'):
        report_types.append("⚖️ Evaluación de Equidad")
    
    # Análisis completo solo para administradores
    if app.has_permission('acceso_completo'):
        report_types.append("🔍 Análisis Completo")
    
    selected_report = st.selectbox("Tipo de Reporte:", report_types)
    
    if "Ejecutivo" in selected_report:
        render_executive_report_secure(app)
    elif "Infraestructura" in selected_report:
        render_infrastructure_report_secure(app)
    elif "Demográfico" in selected_report:
        render_demographic_report_secure(app)
    elif "Equidad" in selected_report:
        render_equity_report_secure(app)
    elif "Análisis Completo" in selected_report:
        render_complete_analysis_secure(app)
    # Nota: la opción de Planificación Málaga se ha eliminado temporalmente mientras se estabiliza la aplicación.

def render_executive_report_secure(app):
    """Reporte ejecutivo con auditoría"""
    st.markdown("#### 📈 Reporte Ejecutivo Seguro")
    
    report_date = datetime.now().strftime("%d de %B de %Y")
    user_info = f"Generado por: {app.user['name']} ({app.role_info['name']}) - {app.user['organization']}"
    
    if not app.data:
        st.error("❌ Datos no disponibles")
        return
    
    executive_summary = f"""
    # 🏥 REPORTE EJECUTIVO - SISTEMA SANITARIO MÁLAGA
    **Fecha de análisis:** {report_date}  
    **{user_info}**
    
    ---
    
    ## 📊 INDICADORES PRINCIPALES
    - **Población total atendida:** {app.data['demografia']['poblacion_2025'].sum():,} habitantes
    - **Red asistencial:** {len(app.data['hospitales'])} centros sanitarios  
    - **Capacidad hospitalaria:** {app.data['hospitales']['camas_funcionamiento_2025'].sum():,} camas
    - **Personal sanitario:** {app.data['hospitales']['personal_sanitario_2025'].sum():,} profesionales
    - **Ratio camas/1000 hab:** {(app.data['hospitales']['camas_funcionamiento_2025'].sum() / app.data['demografia']['poblacion_2025'].sum() * 1000):.1f}
    
    ## 🗺️ DISTRIBUCIÓN TERRITORIAL
    - **Distritos sanitarios:** {len(app.data['hospitales']['distrito_sanitario'].unique())}
    - **Municipios cubiertos:** {len(app.data['demografia'])}
    - **Tiempo medio acceso:** {app.data['accesibilidad']['tiempo_coche_minutos'].mean():.1f} minutos
    
    ## 🎯 RECOMENDACIONES ESTRATÉGICAS
    1. **Prioridad Alta:** Evaluar equidad en distritos con menor ratio de recursos
    2. **Accesibilidad:** Mejorar conexiones en municipios con >60 min de acceso
    3. **Capacidad:** Monitorear ocupación en hospitales regionales
    4. **Personal:** Reforzar plantillas en áreas de alta demanda
    
    ---
    **Clasificación:** Uso Interno | **Acceso:** {app.role_info['name']} | **Timestamp:** {datetime.now().isoformat()}
    """
    
    st.markdown(executive_summary)
    
    # Botón de descarga con auditoría
    st.download_button(
        f"📥 Descargar Reporte Ejecutivo ({app.user['username']})",
        executive_summary,
        file_name=f"reporte_ejecutivo_{app.user['username']}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
        mime="text/plain"
    )

def render_infrastructure_report_secure(app):
    """Reporte de infraestructura con permisos"""
    st.markdown("#### 🏥 Reporte de Infraestructura")
    
    if not app.data:
        return
    
    # Análisis básico
    total_beds = app.data['hospitales']['camas_funcionamiento_2025'].sum()
    total_population = app.data['demografia']['poblacion_2025'].sum()
    bed_ratio = (total_beds / total_population) * 1000
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🛏️ Total Camas", f"{total_beds:,}")
    with col2:
        st.metric("📊 Ratio Camas/1K hab", f"{bed_ratio:.1f}")
    with col3:
        status = "✅ Adecuado" if bed_ratio >= 3 else "⚠️ Por debajo OMS"
        st.metric("🎯 Estado vs OMS", status)
    
    # Gráfico de distribución
    tipo_analysis = app.data['hospitales'].groupby('tipo_centro', observed=False).agg({
        'camas_funcionamiento_2025': ['sum', 'mean'],
        'personal_sanitario_2025': 'sum',
        'poblacion_referencia_2025': 'sum'
    }).round(1)
    
    st.markdown("##### 📊 Análisis por Tipo de Centro")
    st.dataframe(tipo_analysis, use_container_width=True)

def render_demographic_report_secure(app):
    """Reporte demográfico seguro"""
    st.markdown("#### 👥 Reporte Demográfico")
    
    if not app.data:
        return
    
    # Estadísticas de crecimiento
    total_growth = app.data['demografia']['crecimiento_2024_2025'].sum()
    total_pop_2024 = app.data['demografia']['poblacion_2024'].sum()
    growth_rate = (total_growth / total_pop_2024) * 100
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📈 Crecimiento 2024-2025", f"+{total_growth:,}")
    with col2:
        st.metric("📊 Tasa Crecimiento", f"{growth_rate:.2f}%")
    with col3:
        growing_munic = len(app.data['demografia'][app.data['demografia']['crecimiento_2024_2025'] > 0])
        st.metric("🏘️ Municipios en Crecimiento", growing_munic)
    
    # Top municipios
    st.markdown("##### 🏆 Top 5 Municipios en Crecimiento")
    top_growth = app.data['demografia'].nlargest(5, 'crecimiento_2024_2025')
    
    for _, row in top_growth.iterrows():
        growth_pct = (row['crecimiento_2024_2025'] / row['poblacion_2024']) * 100
        st.write(f"• **{row['municipio']}**: +{row['crecimiento_2024_2025']:,} hab ({growth_pct:.1f}%)")

def render_equity_report_secure(app):
    """Reporte de equidad (solo usuarios autorizados)"""
    st.markdown("#### ⚖️ Reporte de Equidad")
    
    if not app.has_permission('analisis_equidad'):
        st.warning("🔒 Reporte de equidad requiere permisos de administrador")
        return
    
    if app.metrics_calculator and app.data:
        try:
            equity_data = app.metrics_calculator.calculate_equity_index(app.data)
            if not equity_data.empty:
                st.markdown("##### 📊 Índices de Equidad por Distrito")
                
                equity_summary = equity_data[['distrito', 'score_equidad', 'ratio_camas_1000hab', 'ratio_personal_1000hab']].round(2)
                st.dataframe(equity_summary, use_container_width=True)
                
                # Alertas automáticas
                low_equity = equity_data[equity_data['score_equidad'] < 50]
                if not low_equity.empty:
                    st.error(f"🚨 **ALERTA**: {len(low_equity)} distritos con equidad crítica (<50 puntos)")
                    for _, district in low_equity.iterrows():
                        st.write(f"• **{district['distrito']}**: {district['score_equidad']:.0f}/100")
        except Exception as e:
            st.error(f"Error calculando equidad: {str(e)}")

def render_secure_planificacion(app):
    """Módulo de planificación con permisos"""
    st.markdown("### 📍 Planificación Estratégica Segura")
    
    if not app.require_permission('planificacion'):
        # Mensaje específico para cada rol sin permisos
        if app.user['role'] == 'invitado':
            st.warning("🔒 **Planificación no disponible**: Los usuarios invitados no tienen acceso a herramientas de planificación.")
            st.info("💡 **Sugerencia**: Solicita una cuenta con permisos de 'Gestor' o superior para acceder a la planificación.")
        elif app.user['role'] == 'analista':
            st.warning("🔒 **Planificación restringida**: Los analistas no tienen acceso a herramientas de planificación estratégica.")
            st.info("💡 **Sugerencia**: Contacta a un Gestor Sanitario o Administrador para funciones de planificación.")
        return
    
    st.markdown(f"""
    <div class="access-granted">
        ✅ <strong>Acceso Autorizado a Planificación</strong> | {app.user['name']} ({app.role_info['name']})
    </div>
    """, unsafe_allow_html=True)
    
    if not app.data:
        st.error("❌ Datos no disponibles")
        return
    
    # Análisis de planificación
    planificacion_options = st.selectbox(
        "🎯 Tipo de Análisis de Planificación:",
        [
            "🏥 Ubicación Óptima de Nuevos Centros",
            "📈 Proyección de Demanda Sanitaria", 
            "⚖️ Redistribución de Recursos",
            "🚗 Optimización de Rutas de Acceso"
        ]
    )
    
    if "Ubicación" in planificacion_options:
        render_location_planificacion(app)
    elif "Proyección" in planificacion_options:
        render_demand_projection(app)
    elif "Redistribución" in planificacion_options:
        render_resource_redistribution(app)
    elif "Optimización" in planificacion_options:
        render_route_optimization(app)

def render_location_planificacion(app):
    """Análisis de ubicación óptima"""
    st.markdown("#### 🏥 Análisis de Ubicación Óptima")
    
    # Simular análisis de planificación
    planificacion_metrics = []
    
    for _, municipio_data in app.data['demografia'].iterrows():
        municipio = municipio_data['municipio']
        pop_growth = municipio_data['crecimiento_2024_2025']
        population = municipio_data['poblacion_2025']
        
        # Tiempo de acceso promedio
        access_data = app.data['accesibilidad'][app.data['accesibilidad']['municipio_origen'] == municipio]
        avg_access_time = access_data['tiempo_coche_minutos'].mean() if not access_data.empty else 60
        
        # Score de necesidad
        need_score = (
            (pop_growth / 1000) * 0.3 +
            (population / 10000) * 0.4 +
            (avg_access_time / 10) * 0.3
        )
        
        planificacion_metrics.append({
            'municipio': municipio,
            'poblacion': population,
            'crecimiento': pop_growth,
            'tiempo_acceso_promedio': avg_access_time,
            'score_necesidad': need_score,
            'prioridad': 'Alta' if need_score > 15 else 'Media' if need_score > 8 else 'Baja'
        })
    
    planificacion_df = pd.DataFrame(planificacion_metrics).sort_values('score_necesidad', ascending=False)
    
    # Visualización
    fig_planificacion = px.scatter(
        planificacion_df,
        x='tiempo_acceso_promedio',
        y='poblacion',
        size='crecimiento',
        color='score_necesidad',
        hover_data=['municipio', 'prioridad'],
        title="🎯 Análisis de Ubicaciones Prioritarias",
        color_continuous_scale='Reds'
    )
    fig_planificacion = fix_plotly_hover_issues(fig_planificacion)
    st.plotly_chart(fig_planificacion, use_container_width=True)
    
    # Top 5 recomendaciones
    st.markdown("##### 🏆 Top 5 Ubicaciones Recomendadas")
    top_5 = planificacion_df.head(5)
    
    for i, (_, row) in enumerate(top_5.iterrows()):
        priority_emoji = "🔴" if row['prioridad'] == 'Alta' else "🟡" if row['prioridad'] == 'Media' else "🟢"
        
        with st.expander(f"{i+1}. {priority_emoji} {row['municipio']} - Prioridad {row['prioridad']}"):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Población actual:** {row['poblacion']:,}")
                st.write(f"**Crecimiento esperado:** +{row['crecimiento']:,}")
            with col2:
                st.write(f"**Tiempo acceso actual:** {row['tiempo_acceso_promedio']:.1f} min")
                st.write(f"**Score de necesidad:** {row['score_necesidad']:.1f}")

def render_demand_projection(app):
    """Proyección de demanda"""
    st.markdown("#### 📈 Proyección de Demanda Sanitaria")
    
    # Proyección basada en crecimiento poblacional
    current_pop = app.data['demografia']['poblacion_2025'].sum()
    growth_rate = (app.data['demografia']['crecimiento_2024_2025'].sum() / app.data['demografia']['poblacion_2024'].sum()) * 100
    
    years = [2025, 2026, 2027, 2028, 2029, 2030]
    projected_pop = []
    projected_demand = []
    
    for year in years:
        years_ahead = year - 2025
        pop_projection = current_pop * ((1 + growth_rate/100) ** years_ahead)
        demand_projection = pop_projection * 0.15  # Estimación 15% necesita atención sanitaria anual
        
        projected_pop.append(pop_projection)
        projected_demand.append(demand_projection)
    
    projection_df = pd.DataFrame({
        'año': years,
        'poblacion_proyectada': projected_pop,
        'demanda_sanitaria': projected_demand
    })
    
    fig_projection = px.line(
        projection_df,
        x='año',
        y=['poblacion_proyectada', 'demanda_sanitaria'],
        title="📈 Proyección de Población y Demanda Sanitaria 2025-2030"
    )
    fig_projection = fix_plotly_hover_issues(fig_projection)
    st.plotly_chart(fig_projection, use_container_width=True)
    
    # Métricas de proyección
    col1, col2, col3 = st.columns(3)
    with col1:
        pop_2030 = projected_pop[-1]
        st.metric("👥 Población 2030", f"{pop_2030/1000:.0f}K")
    with col2:
        demand_2030 = projected_demand[-1]
        st.metric("🏥 Demanda 2030", f"{demand_2030/1000:.0f}K")
    with col3:
        growth_total = ((pop_2030 - current_pop) / current_pop) * 100
        st.metric("📊 Crecimiento Total", f"{growth_total:.1f}%")

def render_resource_redistribution(app):
    """Análisis de redistribución de recursos"""
    st.markdown("#### ⚖️ Redistribución Óptima de Recursos")
    
    if app.metrics_calculator:
        try:
            equity_data = app.metrics_calculator.calculate_equity_index(app.data)
            if not equity_data.empty:
                # Identificar distritos con desequilibrios
                avg_ratio_camas = equity_data['ratio_camas_1000hab'].mean()
                avg_ratio_personal = equity_data['ratio_personal_1000hab'].mean()
                
                redistribution_needs = []
                for _, district in equity_data.iterrows():
                    camas_deficit = avg_ratio_camas - district['ratio_camas_1000hab']
                    personal_deficit = avg_ratio_personal - district['ratio_personal_1000hab']
                    
                    redistribution_needs.append({
                        'distrito': district['distrito'],
                        'deficit_camas': camas_deficit,
                        'deficit_personal': personal_deficit,
                        'prioridad_redistribucion': abs(camas_deficit) + abs(personal_deficit)
                    })
                
                redistrib_df = pd.DataFrame(redistribution_needs).sort_values('prioridad_redistribucion', ascending=False)
                
                # Visualizar necesidades de redistribución
                fig_redistrib = px.bar(
                    redistrib_df,
                    x='distrito',
                    y=['deficit_camas', 'deficit_personal'],
                    title="⚖️ Déficits por Distrito (valores negativos = exceso)",
                    barmode='group'
                )
                fig_redistrib = fix_plotly_hover_issues(fig_redistrib)
                st.plotly_chart(fig_redistrib, use_container_width=True)
                
                # Recomendaciones de redistribución
                st.markdown("##### 🎯 Recomendaciones de Redistribución")
                top_needs = redistrib_df.head(3)
                
                for _, row in top_needs.iterrows():
                    if row['deficit_camas'] > 0:
                        st.warning(f"**{row['distrito']}**: Necesita +{row['deficit_camas']:.1f} camas/1000 hab")
                    if row['deficit_personal'] > 0:
                        st.info(f"**{row['distrito']}**: Necesita +{row['deficit_personal']:.1f} personal/1000 hab")
        
        except Exception as e:
            st.error(f"Error en análisis de redistribución: {str(e)}")

def render_route_optimization(app):
    """Optimización de rutas de acceso"""
    st.markdown("#### 🚗 Optimización de Rutas de Acceso")
    
    # Análisis de tiempos de acceso
    access_analysis = app.data['accesibilidad'].groupby('municipio_origen', observed=False).agg({
        'tiempo_coche_minutos': ['mean', 'min', 'max'],
        'coste_transporte_euros': 'mean'
    }).round(1)
    
    access_analysis.columns = ['tiempo_promedio', 'tiempo_minimo', 'tiempo_maximo', 'coste_promedio']
    access_analysis = access_analysis.reset_index()
    
    # Identificar rutas problemáticas
    problematic_routes = access_analysis[access_analysis['tiempo_promedio'] > 60]
    
    if not problematic_routes.empty:
        st.error(f"🚨 **{len(problematic_routes)} municipios** con tiempo de acceso >60 minutos")
        
        fig_routes = px.bar(
            problematic_routes,
            x='municipio_origen',
            y='tiempo_promedio',
            title="⚠️ Municipios con Acceso Deficiente (>60 min)",
            color='tiempo_promedio',
            color_continuous_scale='Reds'
        )
        fig_routes = fix_plotly_hover_issues(fig_routes)
        st.plotly_chart(fig_routes, use_container_width=True)
        
        # Recomendaciones de mejora
        st.markdown("##### 🛣️ Recomendaciones de Mejora")
        for _, route in problematic_routes.iterrows():
            st.write(f"• **{route['municipio_origen']}**: Mejorar conexión (actual: {route['tiempo_promedio']:.0f} min)")
    else:
        st.success("✅ Todos los municipios tienen acceso adecuado (<60 min)")





def render_complete_analysis_secure(app):
    """Análisis completo del sistema (solo administradores)"""
    st.markdown("#### 🔍 Análisis Completo del Sistema")
    
    if not app.has_permission('acceso_completo'):
        st.error("🔒 Este análisis requiere permisos de administrador")
        return
    
    st.markdown(f"""
    <div class="access-granted">
        ✅ <strong>Análisis Completo Autorizado</strong> | Administrador: {app.user['name']}
    </div>
    """, unsafe_allow_html=True)
    
    if not app.data:
        st.error("❌ No hay datos disponibles para el análisis")
        return
    
    # Análisis integral de todos los componentes
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🏥 Infraestructura", "👥 Demografía", "⚖️ Equidad", 
        "🗺️ Accesibilidad", "📊 Resumen Ejecutivo"
    ])
    
    with tab1:
        st.markdown("##### 🏥 Análisis de Infraestructura Hospitalaria")
        
        # Métricas clave
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            total_hospitals = len(app.data['hospitales'])
            st.metric("🏥 Total Hospitales", total_hospitals)
        with col2:
            total_beds = app.data['hospitales']['camas_funcionamiento_2025'].sum()
            st.metric("🛏️ Camas Totales", f"{total_beds:,}")
        with col3:
            total_staff = app.data['hospitales']['personal_sanitario_2025'].sum()
            st.metric("👨‍⚕️ Personal Sanitario", f"{total_staff:,}")
        with col4:
            total_population = app.data['demografia']['poblacion_2025'].sum()
            bed_ratio = (total_beds / total_population) * 1000
            st.metric("Camas/1000 hab", f"{bed_ratio:.1f}")
        
        # Distribución por tipo de centro
        tipo_dist = app.data['hospitales']['tipo_centro'].value_counts()
        fig_tipos = px.pie(values=tipo_dist.values, names=tipo_dist.index,
                          title="Distribución de Centros por Tipo")
        fig_tipos = fix_plotly_hover_issues(fig_tipos)
        st.plotly_chart(fig_tipos, use_container_width=True)
    
    with tab2:
        st.markdown("##### 👥 Análisis Demográfico Detallado")
        
        # Proyecciones demográficas
        total_pop_2025 = app.data['demografia']['poblacion_2025'].sum()
        total_growth = app.data['demografia']['crecimiento_2024_2025'].sum()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("👥 Población 2025", f"{total_pop_2025:,}")
        with col2:
            st.metric("📈 Crecimiento 2024-25", f"+{total_growth:,}")
        with col3:
            growth_rate = (total_growth / total_pop_2025) * 100
            st.metric("📊 Tasa Crecimiento", f"{growth_rate:.2f}%")
        
        # Top municipios por crecimiento
        top_growth = app.data['demografia'].nlargest(10, 'crecimiento_2024_2025')
        fig_growth = px.bar(top_growth, x='municipio', y='crecimiento_2024_2025',
                           title="Top 10 Municipios por Crecimiento Poblacional")
        fig_growth.update_xaxes(tickangle=45)
        fig_growth = fix_plotly_hover_issues(fig_growth)
        st.plotly_chart(fig_growth, use_container_width=True)
    
    with tab3:
        st.markdown("##### ⚖️ Análisis de Equidad Territorial")
        
        if app.metrics_calculator:
            try:
                equity_data = app.metrics_calculator.calculate_equity_index(app.data)
                if not equity_data.empty:
                    # Métricas de equidad
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        avg_score = equity_data['score_equidad'].mean()
                        st.metric("📊 Score Promedio", f"{avg_score:.1f}/100")
                    with col2:
                        max_score = equity_data['score_equidad'].max()
                        best_district = equity_data[equity_data['score_equidad'] == max_score]['distrito'].iloc[0]
                        st.metric("🏆 Mejor Distrito", f"{best_district} ({max_score:.1f})")
                    with col3:
                        min_score = equity_data['score_equidad'].min()
                        worst_district = equity_data[equity_data['score_equidad'] == min_score]['distrito'].iloc[0]
                        st.metric("⚠️ Distrito con Menor Score", f"{worst_district} ({min_score:.1f})")
                    
                    # Gráfico de equidad
                    fig_equity = px.bar(equity_data, x='distrito', y='score_equidad',
                                       title="Score de Equidad por Distrito Sanitario",
                                       color='score_equidad', color_continuous_scale='RdYlGn',
                                       labels={'score_equidad': 'Score de Equidad (0-100)', 'distrito': 'Distrito Sanitario'})
                    fig_equity.update_xaxes(tickangle=45)
                    fig_equity = fix_plotly_hover_issues(fig_equity)
                    st.plotly_chart(fig_equity, use_container_width=True)
                    
                    # Tabla detallada de equidad
                    st.markdown("##### 📋 Detalle por Distrito")
                    st.dataframe(equity_data, use_container_width=True)
                else:
                    st.info("No se pudieron calcular los índices de equidad")
            except Exception as e:
                st.error(f"Error calculando equidad: {str(e)}")
        else:
            st.warning("Calculadora de métricas no disponible")
    
    with tab4:
        st.markdown("##### 🗺️ Análisis de Accesibilidad")
        
        if 'accesibilidad' in app.data:
            # Tiempos de acceso promedio
            avg_time = app.data['accesibilidad']['tiempo_coche_minutos'].mean()
            max_time = app.data['accesibilidad']['tiempo_coche_minutos'].max()
            min_time = app.data['accesibilidad']['tiempo_coche_minutos'].min()
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("⏱️ Tiempo Promedio", f"{avg_time:.1f} min")
            with col2:
                st.metric("⏱️ Tiempo Máximo", f"{max_time:.1f} min")
            with col3:
                st.metric("⏱️ Tiempo Mínimo", f"{min_time:.1f} min")
            
            # Distribución de tiempos de acceso
            fig_access = px.histogram(app.data['accesibilidad'], x='tiempo_coche_minutos',
                                     title="Distribución de Tiempos de Acceso",
                                     nbins=20)
            fig_access = fix_plotly_hover_issues(fig_access)
            st.plotly_chart(fig_access, use_container_width=True)
    
    with tab5:
        st.markdown("##### 📊 Resumen Ejecutivo Completo")
        
        # Alertas y recomendaciones críticas
        st.markdown("**🚨 Alertas del Sistema:**")
        
        # Verificar ratios críticos
        alerts = []
        total_population = app.data['demografia']['poblacion_2025'].sum()
        total_beds = app.data['hospitales']['camas_funcionamiento_2025'].sum()
        bed_ratio = (total_beds / total_population) * 1000
        avg_time = app.data['accesibilidad']['tiempo_coche_minutos'].mean()
        
        if bed_ratio < 3.0:
            alerts.append("⚠️ Ratio de camas por habitante por debajo del estándar (3.0/1000)")
        
        if avg_time > 45:
            alerts.append("⚠️ Tiempo de acceso promedio superior a 45 minutos")
        
        long_access = app.data['accesibilidad'][app.data['accesibilidad']['tiempo_coche_minutos'] > 60]
        if not long_access.empty:
            alerts.append(f"⚠️ {len(long_access)} rutas con tiempo de acceso superior a 60 minutos")
        
        if alerts:
            for alert in alerts:
                st.warning(alert)
        else:
            st.success("✅ Todos los indicadores dentro de parámetros normales")
        
        # Recomendaciones estratégicas
        st.markdown("**💡 Recomendaciones Estratégicas:**")
        
        recommendations = [
            "🏥 Evaluar la creación de nuevos centros de salud en zonas de alto crecimiento poblacional",
            "🚑 Optimizar rutas de transporte sanitario para reducir tiempos de acceso",
            "👨‍⚕️ Planificar contratación de personal sanitario según proyecciones demográficas",
            "⚖️ Implementar medidas de equidad territorial en distritos con menores recursos",
            "📊 Establecer sistema de monitoreo continuo de indicadores clave"
        ]
        
        for rec in recommendations:
            st.info(rec)

def debug_maps_step_by_step():
    """Test exhaustivo paso a paso para diagnosticar problemas de mapas"""
    st.markdown("## 🔬 DEBUG EXHAUSTIVO DE MAPAS ÉPICOS")

    debug_results = {}

    # TEST 1: Variables globales
    st.subheader("1️⃣ Test de Variables Globales")
    try:
        debug_results["globals"] = {
            "MAPS_AVAILABLE": MAPS_AVAILABLE,
            "MAPS_DEPENDENCIES_OK": globals().get('MAPS_DEPENDENCIES_OK', 'NO DEFINIDA')
        }
        st.json(debug_results["globals"])
        if MAPS_AVAILABLE:
            st.success("✅ Variables globales OK")
        else:
            st.error("❌ MAPS_AVAILABLE es False")
    except Exception as e:
        st.error(f"❌ Error en variables globales: {e}")
        debug_results["globals"] = {"error": str(e)}

    # TEST 2: Imports básicos
    st.subheader("2️⃣ Test de Imports Básicos")
    imports_status = {}

    # Test folium
    try:
        import folium
        imports_status["folium"] = {"status": "OK", "version": getattr(folium, '__version__', 'desconocida')}
        st.success(f"✅ folium v{imports_status['folium']['version']}")
    except Exception as e:
        imports_status["folium"] = {"status": "ERROR", "error": str(e)}
        st.error(f"❌ folium: {e}")

    # Test streamlit_folium
    try:
        import streamlit_folium
        imports_status["streamlit_folium"] = {"status": "OK"}
        st.success("✅ streamlit_folium")
    except Exception as e:
        imports_status["streamlit_folium"] = {"status": "ERROR", "error": str(e)}
        st.error(f"❌ streamlit_folium: {e}")

    debug_results["imports_basic"] = imports_status

    # TEST 3: Sistema de archivos
    st.subheader("3️⃣ Test de Sistema de Archivos")
    import os
    import sys

    filesystem_status = {}

    # Verificar directorio actual
    current_dir = os.getcwd()
    filesystem_status["current_dir"] = current_dir
    st.write(f"📁 Directorio actual: {current_dir}")

    # Verificar path de Python
    filesystem_status["python_path"] = sys.path
    st.write("🐍 Python path:")
    for i, path in enumerate(sys.path[:5]):  # Solo primeros 5
        st.write(f"  {i}: {path}")

    # Verificar estructura de módulos
    modules_to_check = [
        "modules",
        "modules/visualization",
        "modules/visualization/map_interface.py"
    ]

    for module_path in modules_to_check:
        exists = os.path.exists(module_path)
        filesystem_status[module_path] = exists
        if exists:
            st.success(f"✅ {module_path}")
            if os.path.isdir(module_path):
                try:
                    contents = os.listdir(module_path)
                    st.write(f"   Contenido: {contents[:5]}...")  # Primeros 5
                except:
                    st.write("   (No se pudo listar contenido)")
        else:
            st.error(f"❌ {module_path}")

    debug_results["filesystem"] = filesystem_status

    # TEST 4: Import del módulo local
    st.subheader("4️⃣ Test de Import de MapInterface")
    try:
        # Primero verificar si el módulo está en sys.modules
        if 'modules.visualization.map_interface' in sys.modules:
            st.info("ℹ️ MapInterface ya está en sys.modules")

        # Intentar import
        from modules.visualization.map_interface import MapInterface

        # Verificar la clase
        map_interface_info = {
            "class_type": str(type(MapInterface)),
            "methods": [method for method in dir(MapInterface) if not method.startswith('_')],
            "module_file": getattr(MapInterface, '__module__', 'desconocido')
        }
        debug_results["map_interface_import"] = map_interface_info

        st.success("✅ MapInterface importado correctamente")
        st.json(map_interface_info)

        # TEST 5: Instanciación
        st.subheader("5️⃣ Test de Instanciación")
        try:
            instance = MapInterface()
            instance_info = {
                "instance_type": str(type(instance)),
                "attributes": [attr for attr in dir(instance) if not attr.startswith('_')][:10]  # Primeros 10
            }
            debug_results["map_interface_instance"] = instance_info
            st.success("✅ MapInterface instanciado correctamente")
            st.json(instance_info)

        except Exception as inst_e:
            debug_results["map_interface_instance"] = {"error": str(inst_e)}
            st.error(f"❌ Error instanciando MapInterface: {inst_e}")
            import traceback
            st.code(traceback.format_exc())

    except Exception as import_e:
        debug_results["map_interface_import"] = {"error": str(import_e)}
        st.error(f"❌ Error importando MapInterface: {import_e}")
        import traceback
        st.code(traceback.format_exc())

    # RESUMEN FINAL
    st.subheader("📋 Resumen del Diagnóstico")
    st.json(debug_results)

    # Determinar la causa más probable
    if not debug_results["globals"]["MAPS_AVAILABLE"]:
        st.error("🎯 **CAUSA PRINCIPAL:** MAPS_AVAILABLE es False desde el inicio")
        st.write("💡 **Solución:** Revisar el bloque de inicialización global al inicio de app.py")
    elif "error" in debug_results.get("map_interface_import", {}):
        st.error("🎯 **CAUSA PRINCIPAL:** Error importando MapInterface")
        st.write("💡 **Solución:** Revisar dependencias dentro del archivo map_interface.py")
    elif "error" in debug_results.get("map_interface_instance", {}):
        st.error("🎯 **CAUSA PRINCIPAL:** Error instanciando MapInterface")
        st.write("💡 **Solución:** Revisar constructor de la clase MapInterface")
    else:
        st.success("🎯 **DIAGNÓSTICO:** Los tests básicos pasaron, el problema debe estar en el flujo de la aplicación")

def render_epic_maps_tab(app):
    """Tab de mapas épicos con verificación de permisos"""
    st.markdown("### 🗺️ Mapas Interactivos Épicos")


    if not app.require_permission('ver_datos'):
        return
    
    # CARGA AUTOMÁTICA DE MAPAS - Sin verificar MAPS_AVAILABLE
    if not app.map_interface:
        with st.spinner("🗺️ Cargando sistema de mapas automáticamente..."):
            try:
                # Intentar cargar directamente
                from modules.visualization.map_interface import MapInterface
                app.map_interface = MapInterface()
                app.map_interface_loaded = True
                st.success("✅ Sistema de mapas cargado correctamente")

            except Exception as load_error:
                st.error(f"❌ Error cargando mapas automáticamente: {str(load_error)}")

                # Mostrar opción de bypass manual como fallback
                with st.expander("🛠️ Bypass Manual", expanded=True):
                    st.warning("⚠️ Carga automática falló, intenta cargar manualmente:")
                    if st.button("🚀 Cargar mapas manualmente", key="force_maps_bypass"):
                        try:
                            from modules.visualization.map_interface import MapInterface
                            app.map_interface = MapInterface()
                            app.map_interface_loaded = True
                            st.success("✅ Mapas cargados manualmente")
                        except Exception as manual_error:
                            st.error(f"❌ Error en carga manual: {str(manual_error)}")
                            import traceback
                            st.code(traceback.format_exc())
                return
    
    # Información de acceso
    st.markdown(f"""
    <div class="access-granted">
        ✅ <strong>Acceso Autorizado a Mapas Épicos</strong> | Usuario: {app.user['name']} | Rol: {app.role_info['name']}
    </div>
    """, unsafe_allow_html=True)
    
    if not app.data:
        st.error("❌ No hay datos disponibles para generar mapas. Ejecuta data_collector_2025.py")
        return

    # Renderizar mapas directamente
    try:
        user_permissions = app.role_info['permissions'] if app.role_info else []

        # Verificar si el método acepta user_permissions
        try:
            app.map_interface.render_epic_maps_dashboard(app.data, user_permissions)
        except TypeError as te:
            if "takes 2 positional arguments but 3 were given" in str(te):
                # Versión sin permisos diferenciados
                app.map_interface.render_epic_maps_dashboard(app.data)
            else:
                raise te
    except Exception as e:
        st.error(f"❌ Error renderizando mapas épicos: {str(e)}")
        
        # Información de depuración para administradores
        if app.has_permission('acceso_completo'):
            with st.expander("🔧 Información de Depuración (Solo Administradores)"):
                st.code(f"Error: {str(e)}")
                st.write("**Datos disponibles:**")
                st.write(f"- Hospitales: {len(app.data.get('hospitales', []))}")
                st.write(f"- Demografia: {len(app.data.get('demografia', []))}")
                st.write(f"- Servicios: {len(app.data.get('servicios', []))}")
                st.write(f"- Accesibilidad: {len(app.data.get('accesibilidad', []))}")

if __name__ == "__main__":
    main()