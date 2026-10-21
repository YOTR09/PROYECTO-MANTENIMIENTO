@echo off
REM ==============================================================================
REM Script de Compilacion de Ejecutable para Windows (Modo Portable --onefile)
REM Sistema de Control de Mantenimiento Preventivo - Brisas del Palmar
REM ==============================================================================
setlocal

cd /d "%~dp0\.."

echo ============================================================
echo  Compilando BrisasDelPalmar.exe para Windows (64-bit)
echo ============================================================

REM 1. Crear o activar entorno virtual
if not exist "venv\Scripts\activate.bat" (
    echo [1/4] Creando entorno virtual venv...
    python -m venv venv
)

echo [1/4] Activando entorno virtual...
call venv\Scripts\activate.bat

REM 2. Instalar dependencias y PyInstaller
echo [2/4] Instalando dependencias y PyInstaller...
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install "pyinstaller>=6.0.0"

REM 3. Ejecutar pruebas unitarias
echo [3/4] Ejecutando pruebas unitarias...
python -m unittest discover tests -v
if errorlevel 1 (
    echo [ERROR] Las pruebas unitarias fallaron. Abortando compilacion.
    exit /b 1
)

REM 4. Empaquetar ejecutable con PyInstaller
echo [4/4] Generando ejecutable unico en dist\BrisasDelPalmar.exe...
pyinstaller --clean --noconfirm BrisasDelPalmar.spec

echo.
echo ============================================================
echo  Compilacion completada con exito!
echo  Ejecutable generado en: dist\BrisasDelPalmar.exe
echo ============================================================
pause

