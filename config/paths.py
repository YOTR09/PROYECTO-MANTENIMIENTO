"""
Módulo de resolución centralizada de rutas de archivos.
Soporta ejecución tanto desde el código fuente (desarrollo) como desde un
ejecutable autónomo empaquetado con PyInstaller (--onefile / --onedir).
"""
import os
import sys


def is_frozen() -> bool:
    """Indica si la aplicación se está ejecutando desde un binario empaquetado (PyInstaller)."""
    return getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS")


def get_resource_dir() -> str:
    """
    Directorio base para recursos empaquetados de solo lectura (assets/, database/*.sql).
    En PyInstaller (--onefile) apunta a sys._MEIPASS; en desarrollo a la raíz del proyecto.
    """
    if is_frozen():
        return sys._MEIPASS
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_app_dir() -> str:
    """
    Directorio base para archivos persistentes de lectura/escritura (data/mantenimiento.db).
    En PyInstaller apunta a la carpeta donde reside el ejecutable; en desarrollo a la raíz del proyecto.
    """
    if is_frozen():
        return os.path.dirname(os.path.abspath(sys.executable))
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_asset_path(filename: str) -> str:
    """Retorna la ruta absoluta a un archivo dentro de assets/."""
    return os.path.join(get_resource_dir(), "assets", filename)

