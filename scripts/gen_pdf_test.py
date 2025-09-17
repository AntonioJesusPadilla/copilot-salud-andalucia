import os
import sys
from pathlib import Path

# Asegurar que el directorio raíz del proyecto esté en sys.path para importar src
project_root = os.path.dirname(os.path.dirname(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.app import create_pdf_bytes

Path('tmp').mkdir(exist_ok=True)
text = "Informe Ejecutivo: Gestión Integral del Sistema Sanitario de Málaga\n\nResumen\nEl sistema sanitario de Málaga cuenta con 10 centros hospitalarios...\n\n|Distrito|Población|Tiempo|Hospitales|\n|---|---:|---:|---:|\n|1|200000|60|2|\n|2|250000|65|1|\n"
pdf = create_pdf_bytes('Prueba Informe Málaga', text)
# Generar versión con header simple
pdf_simple = create_pdf_bytes('Prueba Informe Málaga', text, use_simple_header=True)
with open('tmp/informe_simple.pdf','wb') as f:
    f.write(pdf_simple)
print('WROTE tmp/informe_simple.pdf')

# Generar versión con header mejorado
pdf_fancy = create_pdf_bytes('Prueba Informe Málaga', text, use_simple_header=False)
with open('tmp/informe_mejorado.pdf','wb') as f:
    f.write(pdf_fancy)
print('WROTE tmp/informe_mejorado.pdf')
