#!/usr/bin/env python3
"""
Generador de favicon profesional para Copilot Salud Andalucía
Crea un favicon ICO de alta calidad con cruz médica
"""

try:
    from PIL import Image, ImageDraw, ImageFont
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

def create_professional_favicon():
    """Crea un favicon ICO profesional"""
    
    if not PIL_AVAILABLE:
        print("❌ Error: PIL (Pillow) no está instalado")
        print("💡 Instalar con: pip install Pillow")
        return
    
    # Tamaños estándar para favicon
    sizes = [16, 32, 48, 64, 128, 256]
    
    # Crear directorio assets si no existe
    from pathlib import Path
    assets_dir = Path(__file__).parent.parent / "assets"
    assets_dir.mkdir(exist_ok=True)
    
    for size in sizes:
        # Crear imagen con fondo transparente
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Fondo azul sanitario con gradiente
        background_color = (0, 64, 128, 255)  # Azul sanitario más oscuro
        draw.rectangle([0, 0, size, size], fill=background_color)
        
        # Cruz médica blanca más gruesa y visible
        cross_width = max(2, size // 6)
        cross_length = size // 2
        
        # Centro de la imagen
        x_center = size // 2
        y_center = size // 2
        
        # Cruz vertical
        draw.rectangle([
            x_center - cross_width // 2,
            y_center - cross_length // 2,
            x_center + cross_width // 2,
            y_center + cross_length // 2
        ], fill=(255, 255, 255, 255))
        
        # Cruz horizontal
        draw.rectangle([
            x_center - cross_length // 2,
            y_center - cross_width // 2,
            x_center + cross_length // 2,
            y_center + cross_width // 2
        ], fill=(255, 255, 255, 255))
        
        # Círculo exterior para mayor visibilidad
        circle_radius = size // 2 - 2
        draw.ellipse([
            x_center - circle_radius,
            y_center - circle_radius,
            x_center + circle_radius,
            y_center + circle_radius
        ], outline=(255, 255, 255, 255), width=2)
        
        # Guardar favicon
        favicon_path = assets_dir / f"favicon_{size}x{size}.png"
        img.save(favicon_path, "PNG")
        print(f"✅ Favicon {size}x{size} creado: {favicon_path}")
    
    # Crear favicon principal (32x32) como ICO
    main_favicon = assets_dir / "favicon.ico"
    img_32 = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
    draw_32 = ImageDraw.Draw(img_32)
    
    # Fondo azul sanitario
    draw_32.rectangle([0, 0, 32, 32], fill=(0, 64, 128, 255))
    
    # Cruz médica blanca
    cross_width = 5
    cross_length = 16
    x_center = 16
    y_center = 16
    
    # Cruz vertical
    draw_32.rectangle([
        x_center - cross_width // 2,
        y_center - cross_length // 2,
        x_center + cross_width // 2,
        y_center + cross_length // 2
    ], fill=(255, 255, 255, 255))
    
    # Cruz horizontal
    draw_32.rectangle([
        x_center - cross_length // 2,
        y_center - cross_width // 2,
        x_center + cross_length // 2,
        y_center + cross_width // 2
    ], fill=(255, 255, 255, 255))
    
    # Círculo exterior
    draw_32.ellipse([2, 2, 30, 30], outline=(255, 255, 255, 255), width=2)
    
    # Guardar como ICO
    img_32.save(main_favicon, "ICO")
    print(f"✅ Favicon principal creado: {main_favicon}")
    
    print("\n🎨 Favicon profesional creado exitosamente!")
    print("📁 Ubicación: assets/favicon.ico")
    print("🔧 Para usar: st.set_page_config(page_icon='assets/favicon.ico')")

if __name__ == "__main__":
    create_professional_favicon()
