import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os
import sys
import re
from io import StringIO
from dotenv import load_dotenv

# Añadir directorios al path ANTES de importar módulos locales
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
src_dir = os.path.join(project_root, 'src')

# Asegurar que tanto la raíz como src están en el path
for path in [project_root, src_dir]:
    if path not in sys.path:
        sys.path.insert(0, path)

# Ahora importar módulos locales
from modules.ai.streamlit_async_wrapper import get_streamlit_async_wrapper

print(f"Project root: {project_root}")
print(f"Source dir: {src_dir}")
print(f"Python path: {sys.path}")

# Importar sistema de autenticación
try:
    from modules.core.auth_system import (
        check_authentication, render_login_page, logout, 
        render_user_management, render_user_profile, HealthAuthenticator
    )
    AUTH_AVAILABLE = True
except ImportError as e:
    st.error(f"❌ Error importando sistema de autenticación: {str(e)}")
    AUTH_AVAILABLE = False

# Importar módulos IA
try:
    from modules.ai.ai_processor import HealthAnalyticsAI, HealthMetricsCalculator
    from modules.visualization.chart_generator import SmartChartGenerator, DataAnalyzer
    AI_AVAILABLE = True
except ImportError as e:
        st.error(f"❌ Error importando módulos IA: {str(e)}")
        AI_AVAILABLE = False

# Importar módulos de mapas (opcional para Streamlit Cloud)
try:
    import importlib
    import sys
    
    # Verificar dependencias básicas de mapas
    try:
        import folium
        import streamlit_folium
        MAPS_DEPENDENCIES_OK = True
    except ImportError as deps_error:
        st.warning(f"⚠️ Dependencias de mapas no disponibles: {str(deps_error)}")
        st.info("💡 Los mapas no estarán disponibles en este despliegue")
        MAPS_DEPENDENCIES_OK = False
    
    if MAPS_DEPENDENCIES_OK:
        try:
            # Forzar recarga de módulos si ya están cargados
            if 'modules.map_interface' in sys.modules:
                importlib.reload(sys.modules['modules.map_interface'])
            if 'modules.interactive_maps' in sys.modules:
                importlib.reload(sys.modules['modules.interactive_maps'])
            
            from modules.visualization.map_interface import MapInterface
            from modules.visualization.interactive_maps import EpicHealthMaps
            MAPS_AVAILABLE = True
        except ImportError as module_error:
            st.warning(f"⚠️ Módulos de mapas no disponibles: {str(module_error)}")
            MAPS_AVAILABLE = False
    else:
        MAPS_AVAILABLE = False
        
except Exception as e:
    st.warning(f"⚠️ Mapas no disponibles: {str(e)}")
    st.info("💡 La aplicación funcionará sin mapas interactivos")
    MAPS_AVAILABLE = False

# Importar dashboards personalizados por rol
try:
    from modules.core.role_dashboards import RoleDashboards
    ROLE_DASHBOARDS_AVAILABLE = True
except ImportError as e:
    st.error(f"❌ Error importando dashboards por rol: {str(e)}")
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

# Configuración de la página
# Intentar usar favicon personalizado, fallback a emoji
favicon_path = "assets/favicon.ico"
if os.path.exists(favicon_path):
    page_icon = favicon_path
else:
    page_icon = "⚕️"  # Símbolo médico más visible

st.set_page_config(
    page_title="Copilot Salud Andalucía",
    page_icon=page_icon,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicializar tema si no existe
if 'theme_mode' not in st.session_state:
    st.session_state.theme_mode = 'light'

# Cargar CSS según el tema seleccionado
try:
    theme_file = f'assets/theme_{st.session_state.theme_mode}.css'
    with open(theme_file, 'r', encoding='utf-8') as f:
        theme_css = f.read()
        st.markdown(f"<style>{theme_css}</style>", unsafe_allow_html=True)
    css_loaded = f"theme_{st.session_state.theme_mode}"
except Exception as e:
    # Fallback al CSS adaptativo
    try:
        with open('assets/adaptive_theme.css', 'r', encoding='utf-8') as f:
            adaptive_css = f.read()
            st.markdown(f"<style>{adaptive_css}</style>", unsafe_allow_html=True)
        css_loaded = "adaptive"
    except Exception as e2:
        # Último fallback al CSS original
        try:
            with open('assets/style.css', 'r', encoding='utf-8') as f:
                css_content = f.read()
            with open('assets/desktop_layout.css', 'r', encoding='utf-8') as f:
                desktop_css = f.read()
            st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)
            st.markdown(f"<style>{desktop_css}</style>", unsafe_allow_html=True)
            css_loaded = "legacy"
        except Exception as e3:
            st.warning(f"⚠️ No se pudieron cargar los estilos CSS: {e3}")
            css_loaded = "none"

# Cargar CSS extra si existe (mantener compatibilidad)
try:
    with open('assets/extra_styles.css', 'r', encoding='utf-8') as f:
        extra_css = f.read()
    st.markdown(f"<style>{extra_css}</style>", unsafe_allow_html=True)
except Exception:
    extra_css = None

# Cargar detector y correcciones SOLO para iPhone iOS 26 (condicional)
ios_detection_script = """
<script>
function isIPhoneIOS26() {
    const userAgent = navigator.userAgent;
    const isIPhone = /iPhone/.test(userAgent);
    const isSafari = /Safari/.test(userAgent) && !/Chrome|CriOS|FxiOS/.test(userAgent);
    const iosVersion = userAgent.match(/OS (\\d+)_/);
    const isIOS26 = iosVersion && parseInt(iosVersion[1]) >= 26;
    return isIPhone && isSafari && isIOS26;
}

// Solo aplicar correcciones si es iPhone iOS 26
if (isIPhoneIOS26()) {
    console.log('iPhone iOS 26 detectado - Aplicando correcciones específicas...');

    // Inyectar CSS específico para iOS 26
    const iosCSS = `PLACEHOLDER_CSS_CONTENT`;
    const style = document.createElement('style');
    style.textContent = iosCSS;
    document.head.appendChild(style);

    // Inyectar JavaScript específico para iOS 26
    const iosJS = `PLACEHOLDER_JS_CONTENT`;
    eval(iosJS);

    // Meta tags específicos para iOS 26
    const viewport = document.querySelector('meta[name="viewport"]') || document.createElement('meta');
    viewport.setAttribute('name', 'viewport');
    viewport.setAttribute('content', 'width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover');
    if (!document.querySelector('meta[name="viewport"]')) document.head.appendChild(viewport);

    const webAppCapable = document.createElement('meta');
    webAppCapable.setAttribute('name', 'apple-mobile-web-app-capable');
    webAppCapable.setAttribute('content', 'yes');
    document.head.appendChild(webAppCapable);
}
</script>
"""

# Leer CSS y JS para iOS 26 y reemplazar en el script
try:
    with open('assets/ios_safari_fixes.css', 'r', encoding='utf-8') as f:
        ios_fixes_css = f.read().replace('`', '\\`').replace('${', '\\${')
    with open('assets/safari_detector.js', 'r', encoding='utf-8') as f:
        safari_js = f.read().replace('`', '\\`').replace('${', '\\${')

    ios_detection_script = ios_detection_script.replace('PLACEHOLDER_CSS_CONTENT', ios_fixes_css)
    ios_detection_script = ios_detection_script.replace('PLACEHOLDER_JS_CONTENT', safari_js)

    st.markdown(ios_detection_script, unsafe_allow_html=True)
except Exception as e:
    # Si no se pueden cargar los archivos específicos, continuar sin ellos
    pass

# Aplicar estilos adicionales básicos
st.markdown(f"""
<style>
/* Importar fuentes modernas */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Poppins:wght@300;400;500;600;700&display=swap');

/* Estilos adicionales solo si no se cargó el CSS temático */
{'' if css_loaded.startswith('theme_') else 'body { font-family: Inter, sans-serif; }'}
</style>

<script>
// Forzar viewport de escritorio
(function() {{
    var viewport = document.querySelector("meta[name=viewport]");
    if (viewport) {{
        viewport.setAttribute('content', 'width=1200, initial-scale=1.0, maximum-scale=1.0, user-scalable=no');
    }} else {{
        var meta = document.createElement('meta');
        meta.name = "viewport";
        meta.content = "width=1200, initial-scale=1.0, maximum-scale=1.0, user-scalable=no";
        document.getElementsByTagName('head')[0].appendChild(meta);
    }}

    // Forzar layout desktop
    if (window.innerWidth < 1200 && !document.body.classList.contains('desktop-forced')) {{
        document.body.classList.add('desktop-forced');
        document.body.style.minWidth = '1200px';
        document.body.style.overflowX = 'auto';
    }}

    // Funciones básicas de la aplicación pueden ir aquí si es necesario
}})();
</script>
""", unsafe_allow_html=True)

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
                
                # Inicializar mapas si está disponible
                if MAPS_AVAILABLE:
                    try:
                        self.map_interface = MapInterface()
                        # Verificar que el método tenga la signatura correcta
                        import inspect
                        sig = inspect.signature(self.map_interface.render_epic_maps_dashboard)
                        params = list(sig.parameters.keys())
                        print(f"🔧 MapInterface parámetros: {params}")
                    except Exception as e:
                        print(f"❌ Error inicializando MapInterface: {str(e)}")
                        self.map_interface = None
                else:
                    self.map_interface = None
                
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
            st.markdown(f"""
            <div style="background: {theme.get('primary_gradient', 'linear-gradient(135deg, #6b7280 0%, #9ca3af 100%)')}; 
                        padding: 1.5rem; border-radius: 12px; text-align: center; margin-bottom: 1rem; color: white;">
                <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">{self.role_info['icon']}</div>
                <strong style="font-size: 1.1rem;">{self.user['name']}</strong><br>
                <small style="color: rgba(255,255,255,0.8); font-size: 0.9rem;">{self.role_info['name']}</small>
                <div style="margin-top: 0.5rem; padding: 0.5rem; background: rgba(255,255,255,0.1); border-radius: 8px;">
                    <small style="color: rgba(255,255,255,0.9);">{self.user['organization']}</small>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Botón de logout
            if st.button("🚪 Cerrar Sesión", key="logout_sidebar"):
                logout()
            
            # Enlaces rápidos personalizados por rol
            if sidebar_style == 'expanded':
                st.markdown("### 🚀 Panel de Control")
                
                if st.button("🏛️ Vista Ejecutiva", width="stretch"):
                    st.session_state.page = "main"
                    st.session_state.selected_tab = "dashboard"
                    st.rerun()
                    
                if self.has_permission('gestion_usuarios'):
                    if st.button("👥 Gestión de Usuarios", width="stretch"):
                        st.session_state.page = "gestion_usuarios"
                        st.rerun()
                        
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
    """Aplicar correcciones a gráficos de Plotly para evitar errores de hover"""
    try:
        # Correcciones para evitar errores de hoversubplots
        fig.update_layout(
            hovermode="closest",  # Modo hover simple
            hoverdistance=100,    # Distancia de hover
            spikedistance=100,    # Distancia de spike
            # Protecciones anti-rangeslider
            showrangeslider=False,
            rangeslider=dict(visible=False),
            # Configuración segura de ejes
            xaxis=dict(
                rangeslider=dict(visible=False),
                showrangeslider=False
            ),
            # Configuración segura de hover para subplots
            hoversubplots="axis"  # Configuración segura para subplots
        )

        # Protección adicional para subplots múltiples
        for i in range(10):  # Hasta 10 subplots
            if i == 0:
                continue
            try:
                fig.update_layout(**{f'xaxis{i+1}': dict(rangeslider=dict(visible=False), showrangeslider=False)})
            except:
                pass

    except Exception as e:
        # Si hay error, al menos intentar las protecciones básicas
        try:
            fig.update_layout(hovermode="closest", showrangeslider=False)
        except:
            pass

    return fig

def main():
    """Función principal con autenticación completa"""

    # Importar re localmente para evitar problemas de ámbito en funciones anidadas
    import re

    # TOGGLE DE TEMA GLOBAL (siempre visible)
    with st.sidebar:
        st.markdown("---")

        # Inicializar tema en session_state si no existe
        if 'theme_mode' not in st.session_state:
            st.session_state.theme_mode = 'light'

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            # Toggle visual con iconos
            if st.button(
                "🌙 Oscuro" if st.session_state.theme_mode == 'light' else "☀️ Claro",
                key="global_theme_toggle",
                help="Cambiar entre tema claro y oscuro",
                use_container_width=True
            ):
                # Cambiar tema
                st.session_state.theme_mode = 'dark' if st.session_state.theme_mode == 'light' else 'light'
                st.rerun()  # Recargar para aplicar el nuevo tema

        st.markdown("---")

    if not AUTH_AVAILABLE:
        st.error("❌ Sistema de autenticación no disponible. Instala: pip install bcrypt PyJWT")
        return

    # Verificar autenticación
    if not check_authentication():
        render_login_page()
        return
    
    # Usuario autenticado - inicializar aplicación segura
    app = SecureHealthAnalyticsApp()
    
    if not app.authenticated:
        st.error("❌ Error en la autenticación. Intenta iniciar sesión nuevamente.")
        logout()
        return
    
    # Verificar que los datos se cargaron correctamente
    if app.data is None:
        st.error("❌ Error cargando los datos. Por favor, recarga la página o contacta al administrador.")
        st.stop()
    
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
        <p><em>🏥 Sistema de Análisis Sociosanitario de Málaga v2.1 - Acceso Autorizado</em></p>
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
            tabs_available.append("📊 Dashboard")
            tab_functions.append(lambda: render_secure_dashboard(app))
        
        if app.has_permission('analisis_ia'):
            tabs_available.append("🤖 Chat IA")
            tab_functions.append(lambda: render_secure_chat(app))
        
        if app.has_permission('reportes'):
            tabs_available.append("📋 Reportes")
            tab_functions.append(lambda: render_secure_reportes(app))
        
        if app.has_permission('planificacion'):
            tabs_available.append("🗺️ Planificación")
            tab_functions.append(lambda: render_secure_planificacion(app))
        
        # Tab de mapas épicos disponible para usuarios con permisos de ver_datos o superior
        if app.has_permission('ver_datos') and MAPS_AVAILABLE:
            tabs_available.append("🗺️ Mapas Épicos")
            tab_functions.append(lambda: render_epic_maps_tab(app))
        
        # Si solo tiene un tab, mostrarlo directamente
        if len(tabs_available) == 1:
            tab_functions[0]()
        elif len(tabs_available) > 1:
            # Verificar si hay un tab específico seleccionado desde el sidebar
            selected_tab = st.session_state.get('selected_tab', None)
            
            # Crear tabs siempre
            tabs = st.tabs(tabs_available)
            
            # Mostrar todos los tabs normalmente
            for i, tab_function in enumerate(tab_functions):
                with tabs[i]:
                    tab_function()
            
            # Si hay un tab específico seleccionado, mostrar un mensaje informativo
            if selected_tab:
                if selected_tab == "dashboard":
                    st.info("💡 **Vista Ejecutiva**: Haz clic en el tab 'Dashboard' para acceder a la vista ejecutiva")
                elif selected_tab == "chat_ia":
                    st.info("💡 **Análisis Estratégico**: Haz clic en el tab 'Chat IA' para realizar análisis con IA")
                elif selected_tab == "reportes":
                    st.info("💡 **Reportes**: Haz clic en el tab 'Reportes' para acceder a los reportes")
                elif selected_tab == "planificacion":
                    st.info("💡 **Planificación**: Haz clic en el tab 'Planificación' para acceder a las herramientas de planificación")
                elif selected_tab == "mapas":
                    st.info("💡 **Mapas**: Haz clic en el tab 'Mapas Épicos' para acceder a los mapas interactivos")
                
                # Limpiar la selección
                st.session_state.selected_tab = None
        else:
            if app.user['role'] == 'invitado':
                st.info("ℹ️ **Usuario Invitado**: Solo tienes acceso al Dashboard básico. Para más funcionalidades, contacta al administrador.")
            else:
                st.error("❌ No tienes permisos para acceder a ninguna funcionalidad")

def render_assistant_message_with_css(content):
    """Renderizar mensaje del asistente con formato CSS adaptado para modo oscuro"""

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
                    color: var(--text-color, #ffffff) !important;
                    padding: 8px 12px !important;
                    border-left: 4px solid #3b82f6 !important;
                    margin: 6px 0 !important;
                    border-radius: 0 4px 4px 0 !important;
                ">
                    <span style="color: var(--text-color, #ffffff) !important; font-size: 14px !important;">• {list_text}</span>
                </div>
                """, unsafe_allow_html=True)

            # Texto con iconos al inicio
            elif any(line.startswith(icon) for icon in ['📋', '✅', '📊', '💡', '❌', '⚠️', '🔒']):
                st.markdown(f"""
                <div style="
                    background: rgba(99, 102, 241, 0.1) !important;
                    color: var(--text-color, #ffffff) !important;
                    padding: 10px 14px !important;
                    border-radius: 6px !important;
                    margin: 8px 0 !important;
                    border: 1px solid rgba(99, 102, 241, 0.3) !important;
                ">
                    <span style="color: var(--text-color, #ffffff) !important; font-size: 14px !important;">{clean_line}</span>
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
                    color: var(--text-color, #ffffff) !important;
                    padding: 6px 0 !important;
                    line-height: 1.5 !important;
                ">
                    <span style="color: var(--text-color, #ffffff) !important; font-size: 14px !important;">{processed_text}</span>
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
    
    # Estado de IA mejorado
    st.markdown(f"""
    <div class="access-granted">
        <h4>✅ Acceso Autorizado al Análisis con IA</h4>
        <p><strong>Usuario:</strong> {app.user['name']} | <strong>Rol:</strong> {app.role_info['name']}</p>
        <p><strong>Organización:</strong> {app.user['organization']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Inicializar mensajes personalizados por usuario
    user_messages_key = f'secure_messages_{app.user["username"]}'
    if user_messages_key not in st.session_state:
        # Crear saludo personalizado según el rol
        role_specific_content = {
            'admin': {
                'greeting': 'Soy tu asistente de análisis sociosanitario con **acceso administrativo completo**.',
                'analyses': [
                    '• Gestión integral del sistema sanitario',
                    '• Configuración y supervisión de usuarios',
                    '• Análisis de equidad territorial completo',
                    '• Planificación estratégica avanzada',
                    '• Reportes ejecutivos y auditoría',
                    '• Evaluación de recursos a nivel provincial'
                ],
                'suggestion': 'Como administrador, puedes consultar sobre cualquier aspecto del sistema sanitario de Málaga.'
            },
            'gestor': {
                'greeting': 'Soy tu asistente especializado en **gestión sanitaria operacional**.',
                'analyses': [
                    '• Optimización de recursos hospitalarios',
                    '• Análisis de capacidad asistencial',
                    '• Evaluación de accesibilidad por distrito',
                    '• Planificación de servicios sanitarios',
                    '• Reportes operacionales y de gestión',
                    '• Identificación de déficits asistenciales'
                ],
                'suggestion': 'Como gestor sanitario, puedes consultar sobre eficiencia operacional y planificación de recursos.'
            },
            'analista': {
                'greeting': 'Soy tu asistente especializado en **análisis estadístico y de datos sanitarios**.',
                'analyses': [
                    '• Análisis estadísticos avanzados',
                    '• Visualizaciones de datos epidemiológicos',
                    '• Estudios de correlación demográfica',
                    '• Análisis de tendencias poblacionales',
                    '• Reportes técnicos especializados',
                    '• Evaluación de indicadores de salud'
                ],
                'suggestion': 'Como analista, puedes solicitar análisis estadísticos detallados y visualizaciones específicas.'
            },
            'invitado': {
                'greeting': 'Soy tu asistente de consulta para **información básica del sistema sanitario**.',
                'analyses': [
                    '• Información general de hospitales',
                    '• Datos demográficos básicos',
                    '• Consultas sobre servicios disponibles',
                    '• Indicadores generales de salud',
                    '• Información de accesibilidad básica'
                ],
                'suggestion': 'Como usuario invitado, puedes consultar información general del sistema sanitario.'
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

**💡 {current_role_content['suggestion']}**"""}
        ]
    
    # Mostrar historial específico del usuario
    for message in st.session_state[user_messages_key]:
        with st.chat_message(message["role"]):
            if message["role"] == "assistant":
                # Convertir resumen de asistente a formato CSS para modo oscuro
                render_assistant_message_with_css(message["content"])
            else:
                st.markdown(message["content"])
    
    # Input del usuario
    if prompt := st.chat_input(f"Consulta como {app.role_info['name']}..."):
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
                            def render_professional_analysis(text):
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
                                            st.markdown(f"""
                                            <div style="
                                                background: #dbeafe;
                                                border: 1px solid #3b82f6;
                                                padding: 12px;
                                                margin: 8px 0;
                                                border-radius: 6px;
                                                font-weight: 600;
                                                color: #1e40af;
                                            ">
                                                <strong>{bold_text}</strong>
                                            </div>
                                            """, unsafe_allow_html=True)

                                    # Listas con viñetas
                                    elif clean_line.startswith('- '):
                                        list_text = clean_line[2:].strip()
                                        if list_text:  # Solo mostrar si hay contenido
                                            st.markdown(f"""
                                            <div style="
                                                margin: 4px 0 !important;
                                                padding: 8px 20px !important;
                                                color: var(--text-color, #ffffff) !important;
                                                background: rgba(59, 130, 246, 0.1) !important;
                                                border-radius: 4px !important;
                                                border-left: 3px solid #3b82f6 !important;
                                            ">
                                                <span style="color: #3b82f6 !important; font-weight: bold !important;">•</span> {list_text}
                                            </div>
                                            """, unsafe_allow_html=True)

                                    # Listas numeradas
                                    elif any(clean_line.startswith(f'{i}. ') for i in range(1, 10)):
                                        st.markdown(f"""
                                        <div style="margin: 4px 0 !important; padding: 8px 12px !important; background: rgba(100, 116, 139, 0.1) !important; border-radius: 4px !important; color: var(--text-color, #ffffff) !important; border-left: 3px solid #64748b !important;">
                                            {clean_line}
                                        </div>
                                        """, unsafe_allow_html=True)

                                    # Resaltado de contenido importante
                                    elif any(word in clean_line.lower() for word in ['importante', 'clave', 'crítico', 'esencial', 'alerta']):
                                        st.markdown(f"""
                                        <div style="
                                            background: #fef3c7;
                                            border: 1px solid #f59e0b;
                                            padding: 12px;
                                            border-radius: 6px;
                                            margin: 8px 0;
                                            color: #92400e;
                                        ">
                                            ⚠️ {clean_line}
                                        </div>
                                        """, unsafe_allow_html=True)

                                    elif any(word in clean_line.lower() for word in ['recomendación', 'sugerencia', 'mejora', 'optimización']):
                                        st.markdown(f"""
                                        <div style="
                                            background: #dcfce7;
                                            border: 1px solid #16a34a;
                                            padding: 12px;
                                            border-radius: 6px;
                                            margin: 8px 0;
                                            color: #166534;
                                        ">
                                            💡 {clean_line}
                                        </div>
                                        """, unsafe_allow_html=True)

                                    elif any(word in clean_line.lower() for word in ['conclusión', 'resultado', 'hallazgo', 'resumen']):
                                        st.markdown(f"""
                                        <div style="
                                            background: #eff6ff;
                                            border: 1px solid #3b82f6;
                                            padding: 12px;
                                            border-radius: 6px;
                                            margin: 8px 0;
                                            color: #1e40af;
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
                                            st.markdown(f"""
                                            <div style="
                                                margin: 6px 0 !important;
                                                line-height: 1.6 !important;
                                                color: var(--text-color, #ffffff) !important;
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
                            render_professional_analysis(processed_text)

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
            st.plotly_chart(fig_tipos, width='stretch')
            
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
            st.plotly_chart(fig_hospitales, width='stretch')
        
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
            st.plotly_chart(fig_demo, width='stretch')
            
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
            st.plotly_chart(fig_scatter, width='stretch')
        
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
                st.plotly_chart(fig_coverage, width='stretch')
                
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
                st.plotly_chart(fig_heatmap, width='stretch')
                    
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
    st.dataframe(tipo_analysis, width='stretch')

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
                st.dataframe(equity_summary, width='stretch')
                
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
    st.markdown("### 🗺️ Planificación Estratégica Segura")
    
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
    st.plotly_chart(fig_planificacion, width='stretch')
    
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
    st.plotly_chart(fig_projection, width='stretch')
    
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
                st.plotly_chart(fig_redistrib, width='stretch')
                
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
        st.plotly_chart(fig_routes, width='stretch')
        
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
        st.plotly_chart(fig_tipos, width='stretch')
    
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
        st.plotly_chart(fig_growth, width='stretch')
    
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
                    st.plotly_chart(fig_equity, width='stretch')
                    
                    # Tabla detallada de equidad
                    st.markdown("##### 📋 Detalle por Distrito")
                    st.dataframe(equity_data, width='stretch')
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
            st.plotly_chart(fig_access, width='stretch')
    
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

def render_epic_maps_tab(app):
    """Tab de mapas épicos con verificación de permisos"""
    st.markdown("### 🗺️ Mapas Interactivos Épicos")
    
    if not app.require_permission('ver_datos'):
        return
    
    # Verificar disponibilidad de mapas
    if not MAPS_AVAILABLE:
        st.error("❌ Sistema de mapas no disponible. Instala: pip install folium streamlit-folium")
        return
    
    if not app.map_interface:
        st.error("❌ Interface de mapas no inicializada")
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
    
    # Renderizar dashboard de mapas épicos con permisos del usuario
    try:
        user_permissions = app.role_info['permissions']
        
        # Verificar si el método acepta user_permissions
        try:
            app.map_interface.render_epic_maps_dashboard(app.data, user_permissions)
        except TypeError as te:
            if "takes 2 positional arguments but 3 were given" in str(te):
                st.warning("⚠️ Usando versión de mapas sin permisos diferenciados")
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