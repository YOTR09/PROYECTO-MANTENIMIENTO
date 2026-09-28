"""
Módulo de Configuración de Tema y Estilos Visuales para la Interfaz Gráfica.
Centraliza la paleta de colores y la configuración estética de los componentes ttk.
"""
from tkinter import ttk

# ==============================================================================
# PALETA DE COLORES DE BOTONES Y ACCIONES (UNIFICADA)
# ==============================================================================
# Botones de Éxito / Guardar / Confirmar (Verde Corporativo)
BTN_SUCCESS_COLOR = "#269225"
BTN_SUCCESS_HOVER = "#059605"

# Botones Principales / Actualizar / Ejecutar (Azul Marino Corporativo)
BTN_PRIMARY_COLOR = "#22447A"
BTN_PRIMARY_HOVER = "#132C63"

# Botones Secundarios / Limpiar / Refrescar (Gris Carbón)
BTN_NEUTRAL_COLOR = "#42464E"
BTN_NEUTRAL_HOVER = "#383F49"

# Botones de Peligro / Eliminar / Quitar (Rojo Borgoña)
BTN_DANGER_COLOR = "#AA3030"
BTN_DANGER_HOVER = "#921919"

# Botones de Advertencia / Odómetro (Ámbar)
BTN_WARNING_COLOR = "#F59E0B"
BTN_WARNING_HOVER = "#D97706"

# Botones de Acento / Navegación Directa (Verde Esmeralda Oscuro)
BTN_ACCENT_COLOR = "#0C8A60"
BTN_ACCENT_HOVER = "#045E41"


def configurar_estilos_treeview():
    """
    Configura el estilo global para todas las tablas ttk.Treeview de la aplicación.
    Asegura tipografía clara a 12pt, altura de fila cómoda y encabezados legibles en negrita.
    """
    style = ttk.Style()
    
    # Filas de datos
    style.configure(
        "Treeview",
        font=("Segoe UI", 12),
        rowheight=30
    )
    
    # Encabezados de columnas
    style.configure(
        "Treeview.Heading",
        font=("Segoe UI", 12, "bold")
    )
