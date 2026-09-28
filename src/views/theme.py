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

# ==============================================================================
# PALETA DE SEÑALIZACIÓN Y KPI (SEMÁFORO VISUAL)
# ==============================================================================
# Estas constantes se usan en tarjetas de resumen y bordes de KPIs del Dashboard.
# Son intencionalmente más brillantes que los botones para maximizar visibilidad.

# Señal Informativa / Unidades (Azul Brillante)
KPI_INFO_COLOR = "#3B82F6"
KPI_INFO_HOVER = "#2563EB"

# Señal de Peligro / Vencidos (Rojo Brillante)
KPI_DANGER_COLOR = "#EF4444"

# Señal de Advertencia / Por Vencer (Ámbar)
KPI_WARNING_COLOR = "#F59E0B"

# Señal de Éxito / Al Día (Esmeralda Brillante)
KPI_SUCCESS_COLOR = "#10B981"

# ==============================================================================
# COLORES DE FILAS SEMÁFORO EN TABLAS (TREEVIEW TAGS)
# ==============================================================================
# Fila Vencida (fondo rojo suave, texto rojo oscuro)
TAG_VENCIDO_BG = "#FEE2E2"
TAG_VENCIDO_FG = "#991B1B"

# Fila Por Vencer (fondo amarillo suave, texto ámbar oscuro)
TAG_POR_VENCER_BG = "#FEF3C7"
TAG_POR_VENCER_FG = "#92400E"

# Fila Al Día (fondo verde suave, texto verde oscuro)
TAG_AL_DIA_BG = "#D1FAE5"
TAG_AL_DIA_FG = "#065F46"

# ==============================================================================
# COLORES DE NAVEGACIÓN (SIDEBAR)
# ==============================================================================
# Botón de navegación activo (azul brillante sobre fondo oscuro del sidebar)
NAV_ACTIVE_COLOR = "#3B82F6"
NAV_ACTIVE_COLOR_DARK = "#1D4ED8"

# ==============================================================================
# COLORES DE TEXTO SECUNDARIO / AUXILIAR
# ==============================================================================
TEXT_MUTED = "#9CA3AF"       # Texto atenuado (subtítulos, labels KPI)
TEXT_SECONDARY = "#6B7280"   # Texto secundario (subvalores KPI)
TEXT_ACCENT_BLUE = "#3B82F6" # Texto de acento informativo


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
