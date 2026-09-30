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
KPI_DANGER_HOVER = "#DC2626"

# Señal de Advertencia / Por Vencer (Ámbar)
KPI_WARNING_COLOR = "#F59E0B"
KPI_WARNING_HOVER = "#D97706"

# Señal de Éxito / Al Día (Esmeralda Brillante)
KPI_SUCCESS_COLOR = "#10B981"
KPI_SUCCESS_HOVER = "#059669"

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


# ==============================================================================
# TIPOGRAFÍAS ESTANDARIZADAS
# ==============================================================================
FONT_TITLE = ("Segoe UI", 22, "bold")       # Títulos de sección / cabeceras
FONT_SUBTITLE = ("Segoe UI", 16, "bold")    # Subtítulos de tarjetas / formularios
FONT_BODY = ("Segoe UI", 14)                # Texto de navegación / contenido general
FONT_SMALL = ("Segoe UI", 12)               # Labels, campos, Treeview
FONT_SMALL_BOLD = ("Segoe UI", 12, "bold")  # Encabezados de tabla, KPI títulos
FONT_CAPTION = ("Segoe UI", 11)             # Subtexto de KPIs, ayuda

# ==============================================================================
# DIMENSIONES ESTANDARIZADAS
# ==============================================================================
SIDEBAR_WIDTH = 240
FORM_CARD_WIDTH = 330
BTN_NAV_HEIGHT = 42
CORNER_RADIUS = 10
CORNER_RADIUS_NONE = 0
PAD_SECTION_X = 20
PAD_SECTION_Y = 15


def configurar_estilos_treeview():
    """
    Configura el estilo global para todas las tablas ttk.Treeview de la aplicación.
    Asegura tipografía clara a 12pt, altura de fila cómoda y encabezados legibles en negrita.
    """
    style = ttk.Style()
    
    # Filas de datos
    style.configure(
        "Treeview",
        font=FONT_SMALL,
        rowheight=30
    )
    
    # Encabezados de columnas
    style.configure(
        "Treeview.Heading",
        font=FONT_SMALL_BOLD
    )


def configurar_tags_semaforo(tree):
    """
    Aplica los tags de color semáforo (vencido, por_vencer, al_dia) a un Treeview.
    Centraliza la configuración para evitar duplicación en múltiples vistas.
    """
    tree.tag_configure("vencido", background=TAG_VENCIDO_BG, foreground=TAG_VENCIDO_FG)
    tree.tag_configure("por_vencer", background=TAG_POR_VENCER_BG, foreground=TAG_POR_VENCER_FG)
    tree.tag_configure("al_dia", background=TAG_AL_DIA_BG, foreground=TAG_AL_DIA_FG)
