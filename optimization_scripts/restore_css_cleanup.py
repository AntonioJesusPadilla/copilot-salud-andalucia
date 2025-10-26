#!/usr/bin/env python3
"""
Script para restaurar archivos CSS desde el respaldo
Fase 3 - Rollback de limpieza de duplicados

Uso:
    python optimization_scripts/restore_css_cleanup.py
"""
import os
import shutil
from pathlib import Path
from datetime import datetime

# Colores para terminal
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    END = '\033[0m'

def log(message, color=Colors.GREEN):
    """Log con color"""
    print(f"{color}[CSS RESTORE]{Colors.END} {message}")

def main():
    """Función principal de restauración"""
    base_dir = Path(__file__).parent.parent
    backup_dir = base_dir / "optimization_backups" / "css_cleanup_backup_20251026_082702"
    assets_dir = base_dir / "assets"

    log("=" * 70, Colors.BLUE)
    log("RESTAURACIÓN DE CSS - FASE 3", Colors.BLUE)
    log("=" * 70, Colors.BLUE)
    log("")

    # Verificar que existe el respaldo
    if not backup_dir.exists():
        log("❌ ERROR: Carpeta de respaldo no encontrada!", Colors.RED)
        log(f"   Esperado en: {backup_dir}", Colors.RED)
        return False

    # Archivos a restaurar
    files_to_restore = [
        'style.css',
        'adaptive_theme.css',
        'theme_light.css',
        'theme_dark.css',
        'theme_light_cloud.css',
        'theme_dark_cloud.css'
    ]

    log(f"📁 Carpeta de respaldo encontrada: {backup_dir.name}", Colors.GREEN)
    log(f"📋 Archivos a restaurar: {len(files_to_restore)}", Colors.CYAN)
    log("")

    # Confirmar restauración
    log("⚠️  ADVERTENCIA: Esta acción sobrescribirá los archivos CSS actuales", Colors.YELLOW)
    log("   con las versiones respaldadas antes de la limpieza.", Colors.YELLOW)
    log("")

    response = input("¿Desea continuar con la restauración? (s/n): ").lower().strip()

    if response != 's' and response != 'y':
        log("❌ Restauración cancelada por el usuario", Colors.YELLOW)
        return False

    log("")
    log("Iniciando restauración...", Colors.CYAN)
    log("")

    restored_count = 0
    errors = []

    for filename in files_to_restore:
        source_file = backup_dir / filename
        dest_file = assets_dir / filename

        if not source_file.exists():
            log(f"  ⚠️  {filename} - No encontrado en respaldo", Colors.YELLOW)
            continue

        try:
            # Copiar archivo
            shutil.copy2(source_file, dest_file)
            restored_count += 1
            log(f"  ✅ {filename} - Restaurado exitosamente", Colors.GREEN)
        except Exception as e:
            errors.append(f"{filename}: {e}")
            log(f"  ❌ {filename} - Error: {e}", Colors.RED)

    log("")
    log("=" * 70, Colors.BLUE)
    log("RESULTADO DE LA RESTAURACIÓN", Colors.BLUE)
    log("=" * 70, Colors.BLUE)
    log(f"\nArchivos restaurados: {restored_count}/{len(files_to_restore)}", Colors.GREEN if restored_count == len(files_to_restore) else Colors.YELLOW)

    if errors:
        log(f"Errores encontrados: {len(errors)}", Colors.RED)
        for error in errors:
            log(f"  • {error}", Colors.RED)
    else:
        log("Sin errores", Colors.GREEN)

    # Restaurar archivos en app.py
    log("")
    log("=" * 70, Colors.YELLOW)
    log("⚠️  IMPORTANTE: Revertir cambios en app.py manualmente", Colors.YELLOW)
    log("=" * 70, Colors.YELLOW)
    log("\nPara completar la restauración, eliminar la carga de common.css en app.py:", Colors.YELLOW)
    log("\n1. Abrir: src/app.py", Colors.CYAN)
    log("2. Buscar: 'OPTIMIZACIÓN FASE 3: Cargar common.css PRIMERO'", Colors.CYAN)
    log("3. Eliminar las líneas 1291-1303 (bloque de carga de common.css)", Colors.CYAN)
    log("4. Eliminar archivos: assets/common.css y assets/common.min.css", Colors.CYAN)
    log("")

    # Eliminar common.css si existe
    common_files = ['common.css', 'common.min.css']
    log("¿Desea eliminar common.css y common.min.css? (s/n): ", Colors.YELLOW)
    response2 = input().lower().strip()

    if response2 == 's' or response2 == 'y':
        for common_file in common_files:
            common_path = assets_dir / common_file
            if common_path.exists():
                try:
                    os.remove(common_path)
                    log(f"  ✅ {common_file} eliminado", Colors.GREEN)
                except Exception as e:
                    log(f"  ❌ Error eliminando {common_file}: {e}", Colors.RED)

    log("")
    log("✅ RESTAURACIÓN COMPLETADA", Colors.GREEN)
    log("\nPróximos pasos:", Colors.CYAN)
    log("1. Revisar cambios en app.py (eliminar carga de common.css)", Colors.CYAN)
    log("2. Probar aplicación: streamlit run src/app.py", Colors.CYAN)
    log("3. Verificar que todo funciona correctamente", Colors.CYAN)
    log("")

    return True

if __name__ == "__main__":
    try:
        success = main()
        exit(0 if success else 1)
    except Exception as e:
        log(f"\n❌ ERROR CRÍTICO: {e}", Colors.RED)
        log("Por favor, restaurar manualmente desde:", Colors.YELLOW)
        log("  optimization_backups/css_cleanup_backup_20251026_082702/", Colors.CYAN)
        exit(1)
