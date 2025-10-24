#!/usr/bin/env python3
"""
SCRIPT DE RESTAURACIÓN DE SNAPSHOT
===================================
Restaura el sistema a un snapshot anterior.

Uso: python optimization_scripts/restore_snapshot.py [timestamp]
     python optimization_scripts/restore_snapshot.py  (usa el último snapshot)
"""

import os
import sys
import shutil
import json
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
    print(f"{color}[RESTORE]{Colors.END} {message}")

def list_available_snapshots():
    """Listar snapshots disponibles"""
    base_dir = Path(__file__).parent.parent
    backup_dir = base_dir / "optimization_backups"

    if not backup_dir.exists():
        log("No hay snapshots disponibles", Colors.RED)
        return []

    snapshots = []
    for item in backup_dir.iterdir():
        if item.is_dir() and item.name.startswith("snapshot_"):
            manifest_file = item / "manifest.json"
            if manifest_file.exists():
                with open(manifest_file, 'r', encoding='utf-8') as f:
                    manifest = json.load(f)
                    snapshots.append({
                        "timestamp": manifest["timestamp"],
                        "date": manifest["date"],
                        "path": item,
                        "files": len(manifest["files_backed_up"])
                    })

    return sorted(snapshots, key=lambda x: x["timestamp"], reverse=True)

def restore_snapshot(timestamp=None):
    """Restaurar snapshot"""

    base_dir = Path(__file__).parent.parent
    backup_dir = base_dir / "optimization_backups"

    # Si no se especifica timestamp, usar el último
    if not timestamp:
        latest_file = backup_dir / "LATEST_SNAPSHOT.txt"
        if latest_file.exists():
            timestamp = latest_file.read_text().strip()
            log(f"Usando último snapshot: {timestamp}", Colors.BLUE)
        else:
            log("No hay snapshots disponibles", Colors.RED)
            log("\nSnapshots disponibles:", Colors.YELLOW)
            for snap in list_available_snapshots():
                log(f"  - {snap['timestamp']} ({snap['date']}) - {snap['files']} archivos", Colors.YELLOW)
            return False

    snapshot_dir = backup_dir / f"snapshot_{timestamp}"

    if not snapshot_dir.exists():
        log(f"❌ Snapshot no encontrado: {snapshot_dir}", Colors.RED)
        log("\nSnapshots disponibles:", Colors.YELLOW)
        for snap in list_available_snapshots():
            log(f"  - {snap['timestamp']} ({snap['date']}) - {snap['files']} archivos", Colors.YELLOW)
        return False

    # Leer manifest
    manifest_file = snapshot_dir / "manifest.json"
    with open(manifest_file, 'r', encoding='utf-8') as f:
        manifest = json.load(f)

    log(f"Restaurando snapshot: {timestamp}", Colors.BLUE)
    log(f"Fecha: {manifest['date']}", Colors.BLUE)
    log(f"Archivos a restaurar: {len(manifest['files_backed_up'])}", Colors.BLUE)

    # Confirmar
    response = input(f"\n{Colors.YELLOW}¿Continuar con la restauración? (s/N): {Colors.END}")
    if response.lower() not in ['s', 'si', 'yes', 'y']:
        log("Restauración cancelada", Colors.YELLOW)
        return False

    # Restaurar archivos
    restored_count = 0
    for file_path in manifest["files_backed_up"]:
        source = snapshot_dir / file_path
        dest = base_dir / file_path

        if source.exists():
            # Crear directorio de destino si no existe
            dest.parent.mkdir(parents=True, exist_ok=True)

            # Copiar archivo
            shutil.copy2(source, dest)
            restored_count += 1
            log(f"  ✓ Restaurado: {file_path}", Colors.GREEN)
        else:
            log(f"  ⚠ No encontrado en snapshot: {file_path}", Colors.YELLOW)

    log(f"\n{'='*60}", Colors.BLUE)
    log(f"✅ RESTAURACIÓN COMPLETADA", Colors.GREEN)
    log(f"{'='*60}", Colors.BLUE)
    log(f"Archivos restaurados: {restored_count}", Colors.GREEN)

    # Mostrar git diff si existe
    diff_file = snapshot_dir / "git_diff.patch"
    if diff_file.exists():
        log(f"\n📋 Git diff disponible en: {diff_file}", Colors.BLUE)
        log(f"Para aplicar el diff: git apply {diff_file}", Colors.YELLOW)

    return True

if __name__ == "__main__":
    try:
        timestamp = sys.argv[1] if len(sys.argv) > 1 else None

        if timestamp == "--list" or timestamp == "-l":
            log("Snapshots disponibles:", Colors.BLUE)
            for snap in list_available_snapshots():
                log(f"  - {snap['timestamp']} ({snap['date']}) - {snap['files']} archivos", Colors.YELLOW)
        else:
            restore_snapshot(timestamp)
    except Exception as e:
        log(f"❌ ERROR: {e}", Colors.RED)
        raise
