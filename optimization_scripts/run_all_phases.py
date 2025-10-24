#!/usr/bin/env python3
"""
EJECUTAR TODAS LAS FASES DE OPTIMIZACIÓN
========================================
Script auxiliar para ejecutar todas las fases en secuencia.

⚠️  ADVERTENCIA: Este script ejecuta todas las fases automáticamente.
    Se recomienda ejecutar fase por fase y probar entre cada una.

Uso: python optimization_scripts/run_all_phases.py
"""

import os
import sys
from pathlib import Path

# Colores para terminal
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    END = '\033[0m'

def log(message, color=Colors.GREEN):
    """Log con color"""
    print(f"{color}[RUN ALL]{Colors.END} {message}")

def run_all_phases():
    """Ejecutar todas las fases de optimización"""

    log("="*60, Colors.BLUE)
    log("EJECUTAR TODAS LAS FASES DE OPTIMIZACIÓN", Colors.BLUE)
    log("="*60, Colors.BLUE)

    # Advertencia
    log("\n⚠️  ADVERTENCIA:", Colors.YELLOW)
    log("Este script ejecutará TODAS las fases automáticamente.", Colors.YELLOW)
    log("Se recomienda ejecutar fase por fase para poder probar entre cada una.", Colors.YELLOW)
    log("\nEsto incluye:", Colors.YELLOW)
    log("  1. Crear snapshot del sistema actual", Colors.YELLOW)
    log("  2. Fase 1: Optimización de CSS", Colors.YELLOW)
    log("  3. Fase 2: Optimización móvil", Colors.YELLOW)
    log("  4. Fase 3: Lazy loading", Colors.YELLOW)

    # Confirmar
    response = input(f"\n{Colors.YELLOW}¿Continuar? (s/N): {Colors.END}")
    if response.lower() not in ['s', 'si', 'yes', 'y']:
        log("Operación cancelada", Colors.YELLOW)
        return False

    base_dir = Path(__file__).parent.parent
    scripts_dir = Path(__file__).parent

    # Lista de scripts a ejecutar en orden
    scripts = [
        ("0_create_snapshot.py", "Creando snapshot del sistema"),
        ("phase1_css_optimization.py", "Ejecutando Fase 1: Optimización CSS"),
        ("phase2_mobile_optimization.py", "Ejecutando Fase 2: Optimización Móvil"),
        ("phase3_lazy_loading.py", "Ejecutando Fase 3: Lazy Loading"),
    ]

    success_count = 0
    failed_count = 0

    for script_name, description in scripts:
        script_path = scripts_dir / script_name

        log(f"\n{'='*60}", Colors.BLUE)
        log(description, Colors.BLUE)
        log(f"{'='*60}", Colors.BLUE)

        if not script_path.exists():
            log(f"❌ Script no encontrado: {script_path}", Colors.RED)
            failed_count += 1
            continue

        # Ejecutar script
        try:
            import subprocess
            result = subprocess.run(
                [sys.executable, str(script_path)],
                cwd=base_dir,
                capture_output=False,
                text=True
            )

            if result.returncode == 0:
                log(f"✅ {script_name} completado exitosamente", Colors.GREEN)
                success_count += 1
            else:
                log(f"❌ {script_name} falló con código {result.returncode}", Colors.RED)
                failed_count += 1

                # Preguntar si continuar
                response = input(f"\n{Colors.YELLOW}¿Continuar con las siguientes fases? (s/N): {Colors.END}")
                if response.lower() not in ['s', 'si', 'yes', 'y']:
                    log("Operación cancelada por el usuario", Colors.YELLOW)
                    break

        except Exception as e:
            log(f"❌ Error ejecutando {script_name}: {e}", Colors.RED)
            failed_count += 1

            # Preguntar si continuar
            response = input(f"\n{Colors.YELLOW}¿Continuar con las siguientes fases? (s/N): {Colors.END}")
            if response.lower() not in ['s', 'si', 'yes', 'y']:
                log("Operación cancelada por el usuario", Colors.YELLOW)
                break

    # Resumen final
    log(f"\n{'='*60}", Colors.BLUE)
    log("RESUMEN DE EJECUCIÓN", Colors.BLUE)
    log(f"{'='*60}", Colors.BLUE)
    log(f"Scripts ejecutados con éxito: {success_count}/{len(scripts)}", Colors.GREEN)

    if failed_count > 0:
        log(f"Scripts fallidos: {failed_count}/{len(scripts)}", Colors.RED)

    if success_count == len(scripts):
        log("\n🎉 ¡TODAS LAS FASES COMPLETADAS CON ÉXITO!", Colors.GREEN)
        log("\nPróximos pasos:", Colors.YELLOW)
        log("1. Probar en local: streamlit run src/app.py", Colors.YELLOW)
        log("2. Verificar que todo funciona correctamente", Colors.YELLOW)
        log("3. Medir tiempo de carga (ver README.md)", Colors.YELLOW)
        log("4. Si todo está bien, hacer commit y subir a Cloud", Colors.YELLOW)
    else:
        log("\n⚠️  Algunas fases fallaron", Colors.YELLOW)
        log("Revisar los logs arriba para ver detalles", Colors.YELLOW)

    log("\nPara revertir todos los cambios:", Colors.RED)
    log("  python optimization_scripts/restore_snapshot.py", Colors.RED)

    return success_count == len(scripts)

if __name__ == "__main__":
    try:
        run_all_phases()
    except KeyboardInterrupt:
        log("\n\n❌ Operación cancelada por el usuario", Colors.YELLOW)
        log("Para revertir cambios:", Colors.RED)
        log("  python optimization_scripts/restore_snapshot.py", Colors.RED)
    except Exception as e:
        log(f"\n\n❌ ERROR: {e}", Colors.RED)
        log("Para revertir cambios:", Colors.RED)
        log("  python optimization_scripts/restore_snapshot.py", Colors.RED)
        raise
