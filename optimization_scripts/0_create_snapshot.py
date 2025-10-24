#!/usr/bin/env python3
"""
SCRIPT DE SNAPSHOT/BACKUP DEL SISTEMA
======================================
Crea un backup completo del estado actual antes de aplicar optimizaciones.

Uso: python optimization_scripts/0_create_snapshot.py
"""

import os
import shutil
import json
from datetime import datetime
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
    print(f"{color}[SNAPSHOT]{Colors.END} {message}")

def create_snapshot():
    """Crear snapshot del sistema"""

    # Directorio base
    base_dir = Path(__file__).parent.parent
    backup_dir = base_dir / "optimization_backups"

    # Timestamp para el backup
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    snapshot_dir = backup_dir / f"snapshot_{timestamp}"

    log(f"Creando snapshot en: {snapshot_dir}", Colors.BLUE)

    # Crear directorio de snapshot
    snapshot_dir.mkdir(parents=True, exist_ok=True)

    # Archivos y directorios a respaldar
    items_to_backup = [
        # Archivos críticos
        "src/app.py",
        "modules/core/auth_system.py",

        # Assets CSS
        "assets/style.css",
        "assets/extra_styles.css",
        "assets/extra_styles_cloud.css",
        "assets/theme_light.css",
        "assets/theme_dark.css",
        "assets/theme_light_cloud.css",
        "assets/theme_dark_cloud.css",
        "assets/ios_safari_fixes.css",
        "assets/adaptive_theme.css",
        "assets/desktop_layout.css",

        # JavaScript
        "assets/safari_detector.js",

        # Config
        ".streamlit/config.toml",

        # Data
        "data/users.json",
    ]

    # Manifest del backup
    manifest = {
        "timestamp": timestamp,
        "date": datetime.now().isoformat(),
        "files_backed_up": [],
        "git_status": None
    }

    # Copiar archivos
    backed_up_count = 0
    for item in items_to_backup:
        source = base_dir / item
        if source.exists():
            # Crear estructura de directorios en backup
            relative_path = Path(item)
            dest = snapshot_dir / relative_path
            dest.parent.mkdir(parents=True, exist_ok=True)

            # Copiar archivo
            shutil.copy2(source, dest)
            manifest["files_backed_up"].append(item)
            backed_up_count += 1
            log(f"  ✓ {item}", Colors.GREEN)
        else:
            log(f"  ⚠ No encontrado: {item}", Colors.YELLOW)

    # Guardar estado de git
    try:
        import subprocess
        git_status = subprocess.check_output(
            ["git", "status", "--porcelain"],
            cwd=base_dir,
            text=True
        )
        manifest["git_status"] = git_status

        # También guardar el diff
        git_diff = subprocess.check_output(
            ["git", "diff"],
            cwd=base_dir,
            text=True
        )

        # Guardar diff en archivo
        diff_file = snapshot_dir / "git_diff.patch"
        diff_file.write_text(git_diff, encoding='utf-8')
        log(f"  ✓ Git diff guardado", Colors.GREEN)

    except Exception as e:
        log(f"  ⚠ No se pudo obtener estado de git: {e}", Colors.YELLOW)

    # Guardar manifest
    manifest_file = snapshot_dir / "manifest.json"
    with open(manifest_file, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    log(f"\n{'='*60}", Colors.BLUE)
    log(f"✅ SNAPSHOT COMPLETADO", Colors.GREEN)
    log(f"{'='*60}", Colors.BLUE)
    log(f"Archivos respaldados: {backed_up_count}", Colors.GREEN)
    log(f"Ubicación: {snapshot_dir}", Colors.BLUE)
    log(f"\nPara restaurar este snapshot, ejecuta:", Colors.YELLOW)
    log(f"  python optimization_scripts/restore_snapshot.py {timestamp}", Colors.YELLOW)

    # Crear archivo con el timestamp del último snapshot
    latest_file = backup_dir / "LATEST_SNAPSHOT.txt"
    latest_file.write_text(timestamp)

    return snapshot_dir

if __name__ == "__main__":
    try:
        create_snapshot()
    except Exception as e:
        log(f"❌ ERROR: {e}", Colors.RED)
        raise
