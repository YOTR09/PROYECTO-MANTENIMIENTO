#!/usr/bin/env bash
# ==============================================================================
# Script de Compilación de Ejecutable para Linux (Modo Portable --onefile)
# Sistema de Control de Mantenimiento Preventivo - Brisas del Palmar
# ==============================================================================
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

echo "============================================================"
echo " Compilando BrisasDelPalmar para Linux (x86_64)             "
echo "============================================================"

# 1. Crear o activar entorno virtual
if [ ! -d "venv" ]; then
    echo "[1/4] Creando entorno virtual venv..."
    python3 -m venv venv
fi

echo "[1/4] Activando entorno virtual..."
source venv/bin/activate

# 2. Instalar dependencias y PyInstaller si no están presentes
echo "[2/4] Verificando dependencias y PyInstaller..."
if ! python3 -c "import customtkinter, reportlab, openpyxl, PIL, PyInstaller" >/dev/null 2>&1; then
    pip install --upgrade pip
    pip install -r requirements.txt
    pip install "pyinstaller>=6.0.0"
fi

# 3. Ejecutar suite de pruebas unitarias antes de empaquetar
echo "[3/4] Ejecutando pruebas unitarias..."
python3 -m unittest discover tests -v

# 4. Empaquetar ejecutable con PyInstaller
echo "[4/4] Generando ejecutable único en dist/BrisasDelPalmar..."
pyinstaller --clean --noconfirm BrisasDelPalmar.spec

chmod +x dist/BrisasDelPalmar

echo ""
echo "============================================================"
echo " ¡Compilación completada con éxito!"
echo " Ejecutable generado en: dist/BrisasDelPalmar"
echo " Para ejecutarlo: ./dist/BrisasDelPalmar"
echo "============================================================"
