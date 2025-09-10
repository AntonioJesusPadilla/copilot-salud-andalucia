#!/usr/bin/env python3
"""
Generador de favicon personalizado para Copilot Salud Andalucía
Crea un favicon basado en el emoji de hospital 🏥
"""

from PIL import Image, ImageDraw, ImageFont
import os
from pathlib import Path

def create_favicon():
    """Crea un favicon personalizado para la aplicación"""
    
    # Tamaños estándar para favicon
    sizes = [16, 32, 48, 64, 128, 256]
    
    # Crear directorio assets si no existe
    assets_dir = Path(__file__).parent.parent / "assets"
    assets_dir.mkdir(exist_ok=True)
    
    for size in sizes:
        # Crear imagen con fondo transparente
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Color de fondo azul sanitario
        background_color = (0, 102, 204, 255)  # Azul sanitario
        draw.rectangle([0, 0, size, size], fill=background_color)
        
        # Dibujar cruz médica blanca
        cross_width = size // 8
        cross_length = size // 2
        
        # Cruz vertical
        x_center = size // 2
        y_center = size // 2
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
        
        # Guardar favicon
        favicon_path = assets_dir / f"favicon_{size}x{size}.png"
        img.save(favicon_path, "PNG")
        print(f"✅ Favicon {size}x{size} creado: {favicon_path}")
    
    # Crear favicon principal (32x32)
    main_favicon = assets_dir / "favicon.ico"
    img_32 = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
    draw_32 = ImageDraw.Draw(img_32)
    
    # Fondo azul sanitario
    draw_32.rectangle([0, 0, 32, 32], fill=(0, 102, 204, 255))
    
    # Cruz médica blanca
    cross_width = 4
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
    
    # Guardar como ICO
    img_32.save(main_favicon, "ICO")
    print(f"✅ Favicon principal creado: {main_favicon}")
    
    print("\n🎨 Favicon personalizado creado exitosamente!")
    print("📁 Ubicación: assets/favicon.ico")
    print("🔧 Para usar: st.set_page_config(page_icon='assets/favicon.ico')")

if __name__ == "__main__":
    try:
        create_favicon()
    except ImportError:
        print("❌ Error: PIL (Pillow) no está instalado")
        print("💡 Instalar con: pip install Pillow")
    except Exception as e:
        print(f"❌ Error creando favicon: {e}")
