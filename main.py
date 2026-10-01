#!/usr/bin/env python3
"""
=========================================================
SISTEMA DE CONTROL DE MANTENIMIENTO PREVENTIVO
Empresa de Transporte Público: Brisas del Palmar
=========================================================
Punto de entrada principal de la aplicación de escritorio.
"""

import sys
import os

# Asegurar que la raíz del proyecto esté en el PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config.database import init_db
from src.views.main_window import MainWindow

def main():
    # 1. Inicializar base de datos SQLite y semillas si no existen
    try:
        init_db()
    except Exception as e:
        print(f"Error crítico al inicializar la base de datos: {e}", file=sys.stderr)
        try:
            from tkinter import messagebox
            import tkinter as tk
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Error Crítico de Base de Datos", f"No se pudo inicializar la base de datos:\n{e}\n\nEl sistema se cerrará.")
            root.destroy()
        except Exception:
            pass
        sys.exit(1)

    # 2. Iniciar interfaz gráfica de escritorio
    app = MainWindow()
    app.mainloop()

if __name__ == "__main__":
    main()

