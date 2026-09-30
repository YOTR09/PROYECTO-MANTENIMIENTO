import os
from PIL import Image
import customtkinter as ctk
from src.views.login_view import LoginView
from src.views.dashboard_view import DashboardView
from src.views.vehiculos_view import VehiculosView
from src.views.socios_view import SociosView
from src.views.programacion_mant_view import ProgramacionMantView
from src.views.tipos_mant_view import TiposMantView
from src.views.historial_mant_view import HistorialMantView
from src.views.reportes_view import ReportesView
from src.views.usuarios_view import UsuariosView
from src.controllers.auth_controller import AuthController
from src.models.usuario import Usuario
from src.views.theme import (
    NAV_ACTIVE_COLOR,
    NAV_ACTIVE_COLOR_DARK,
    TEXT_MUTED,
    SIDEBAR_WIDTH,
    BTN_NAV_HEIGHT,
    configurar_estilos_treeview,
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LOGO_DARK_PATH = os.path.join(BASE_DIR, "assets", "logo_empresa_dark.png")
LOGO_LIGHT_PATH = os.path.join(BASE_DIR, "assets", "logo_empresa_light.png")

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Brisas del Palmar - Control de Flota y Mantenimiento Preventivo")
        self.geometry("520x620")
        self.minsize(460, 520)

        # Configuración de tema visual
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")
        configurar_estilos_treeview()

        self.usuario_actual: Usuario = None
        self.vistas = {}
        self.botones_nav = {}
        self.vista_actual_key = None
        self.sidebar = None
        self.container = None

        self._mostrar_pantalla_login()

    def _mostrar_pantalla_login(self):
        # Limpiar componentes previos si viene de logout
        if self.sidebar:
            self.sidebar.destroy()
            self.sidebar = None
        if self.container:
            self.container.destroy()
            self.container = None

        self.vistas.clear()
        self.botones_nav.clear()
        self.vista_actual_key = None
        self.usuario_actual = None
        AuthController.logout()

        self.geometry("520x620")
        self.minsize(460, 520)

        self.login_view = LoginView(self, on_success=self._abrir_aplicacion)
        self.login_view.pack(fill="both", expand=True)

    def _abrir_aplicacion(self, usuario: Usuario = None):
        if usuario is None:
            usuario = AuthController.get_sesion_actual()
            if not usuario:
                usuario = Usuario(id_usuario=1, id_rol=1, username="admin", nombre_completo="Administrador General", rol_nombre="Administrador")

        self.usuario_actual = usuario
        self.login_view.destroy()
        self.geometry("1280x800")
        self.minsize(1080, 700)
        self._setup_layout()
        self._inicializar_vistas()
        self.cambiar_vista("dashboard")

    def _setup_layout(self):
        # Grid 1x2 (Sidebar a la izquierda, Contenido a la derecha)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ---------------- BARRA LATERAL (SIDEBAR) ----------------
        self.sidebar = ctk.CTkFrame(self, width=SIDEBAR_WIDTH, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        # Cargar Logotipo Corporativo con CTkImage
        if os.path.exists(LOGO_DARK_PATH) and os.path.exists(LOGO_LIGHT_PATH):
            try:
                img_dark = Image.open(LOGO_DARK_PATH)
                img_light = Image.open(LOGO_LIGHT_PATH)
                self.logo_sidebar_ctk = ctk.CTkImage(
                    light_image=img_light,
                    dark_image=img_dark,
                    size=(200, 50)
                )
                lbl_logo = ctk.CTkLabel(self.sidebar, text="", image=self.logo_sidebar_ctk)
                lbl_logo.pack(padx=15, pady=(15, 6), anchor="w")
            except Exception:
                lbl_empresa = ctk.CTkLabel(self.sidebar, text="🚍 Brisas del Palmar", font=ctk.CTkFont(size=18, weight="bold"))
                lbl_empresa.pack(padx=20, pady=(20, 2), anchor="w")
        else:
            lbl_empresa = ctk.CTkLabel(self.sidebar, text="🚍 Brisas del Palmar", font=ctk.CTkFont(size=18, weight="bold"))
            lbl_empresa.pack(padx=20, pady=(20, 2), anchor="w")

        # Tarjeta de usuario conectado y rol
        rol_color = "#3B82F6" if self.usuario_actual.es_admin else ("#F59E0B" if self.usuario_actual.es_mecanico else "#10B981")
        card_user = ctk.CTkFrame(self.sidebar, corner_radius=8, fg_color=("gray85", "gray20"))
        card_user.pack(fill="x", padx=15, pady=(0, 10))

        lbl_user = ctk.CTkLabel(
            card_user,
            text=f"👤 {self.usuario_actual.nombre_completo}",
            font=ctk.CTkFont(size=12, weight="bold"),
            anchor="w"
        )
        lbl_user.pack(fill="x", padx=10, pady=(6, 1))

        lbl_rol = ctk.CTkLabel(
            card_user,
            text=f" Nivel: {self.usuario_actual.rol_nombre} ",
            font=ctk.CTkFont(size=10, weight="bold"),
            fg_color=rol_color,
            corner_radius=4,
            text_color="white"
        )
        lbl_rol.pack(anchor="w", padx=10, pady=(0, 6))

        # Contenedor con scroll para los botones de navegación si la pantalla es reducida
        nav_container = ctk.CTkScrollableFrame(self.sidebar, fg_color="transparent")
        nav_container.pack(fill="both", expand=True, padx=5, pady=0)

        # Definición completa de secciones y roles autorizados
        todas_secciones = [
            ("dashboard", "📊 Dashboard y Alertas", ["Administrador", "Mecanico", "Operador"]),
            ("unidades", "🚐 Flota y Unidades", ["Administrador", "Mecanico", "Operador"]),
            ("socios", "👥 Socios y Propietarios", ["Administrador", "Mecanico", "Operador"]),
            ("preventivo", "🛠️ Control Preventivo", ["Administrador", "Mecanico", "Operador"]),
            ("catalogo", "📋 Catálogo Rutinas", ["Administrador", "Mecanico", "Operador"]),
            ("historial", "📜 Bitácora Histórica", ["Administrador", "Mecanico", "Operador"]),
            ("reportes", "📑 Centro de Reportes", ["Administrador", "Mecanico", "Operador"]),
            ("usuarios", "⚙️ Control de Usuarios", ["Administrador"]),
        ]

        rol_nombre = self.usuario_actual.rol_nombre
        for key, label, roles_permitidos in todas_secciones:
            if rol_nombre in roles_permitidos:
                btn = ctk.CTkButton(
                    nav_container,
                    text=label,
                    height=BTN_NAV_HEIGHT,
                    corner_radius=8,
                    fg_color="transparent",
                    text_color=("gray10", "gray90"),
                    hover_color=("gray70", "gray30"),
                    anchor="w",
                    font=ctk.CTkFont(size=13),
                    command=lambda k=key: self.cambiar_vista(k)
                )
                btn.pack(fill="x", padx=8, pady=3)
                self.botones_nav[key] = btn

        # Footer con selector de tema visual y botón Cerrar Sesión
        footer_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        footer_frame.pack(fill="x", padx=15, pady=(5, 15), side="bottom")

        lbl_tema = ctk.CTkLabel(footer_frame, text="Tema de Interfaz:", font=ctk.CTkFont(size=11), text_color=TEXT_MUTED)
        lbl_tema.pack(anchor="w", pady=(0, 2))

        self.combo_tema = ctk.CTkOptionMenu(
            footer_frame,
            values=["Dark", "Light", "System"],
            height=28,
            command=self.cambiar_tema
        )
        self.combo_tema.pack(fill="x", pady=(0, 8))
        self.combo_tema.set("Dark")

        btn_logout = ctk.CTkButton(
            footer_frame,
            text="🚪 Cerrar Sesión",
            height=32,
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#EF4444",
            hover_color="#DC2626",
            command=self._mostrar_pantalla_login
        )
        btn_logout.pack(fill="x")

        # ---------------- CONTENEDOR PRINCIPAL ----------------
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.grid(row=0, column=1, sticky="nsew", padx=15, pady=15)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

    def _inicializar_vistas(self):
        self.vistas["dashboard"] = DashboardView(self.container, on_navigate=self.cambiar_vista)

        for key, view_cls in [
            ("unidades", VehiculosView),
            ("socios", SociosView),
            ("preventivo", ProgramacionMantView),
            ("catalogo", TiposMantView),
        ]:
            try:
                self.vistas[key] = view_cls(self.container, usuario_actual=self.usuario_actual)
            except TypeError:
                self.vistas[key] = view_cls(self.container)
                self.vistas[key].usuario_actual = self.usuario_actual

        self.vistas["historial"] = HistorialMantView(self.container)
        self.vistas["reportes"] = ReportesView(self.container)

        # La vista de administración de usuarios solo se inicializa si el rol es Administrador
        if self.usuario_actual and self.usuario_actual.es_admin:
            try:
                self.vistas["usuarios"] = UsuariosView(self.container, usuario_actual=self.usuario_actual)
            except TypeError:
                self.vistas["usuarios"] = UsuariosView(self.container)

        # Ubicar todas las vistas en el contenedor
        for vista in self.vistas.values():
            vista.grid(row=0, column=0, sticky="nsew")

    def cambiar_vista(self, key):
        if key not in self.vistas:
            return

        self.vista_actual_key = key
        vista = self.vistas[key]
        vista.tkraise()

        # Resaltar botón activo
        for k, btn in self.botones_nav.items():
            if k == key:
                btn.configure(fg_color=(NAV_ACTIVE_COLOR, NAV_ACTIVE_COLOR_DARK), text_color="white")
            else:
                btn.configure(fg_color="transparent", text_color=("gray10", "gray90"))

        # Refrescar datos al navegar
        if hasattr(vista, "actualizar_dashboard"):
            vista.actualizar_dashboard()
        elif hasattr(vista, "cargar_datos"):
            vista.cargar_datos()
        if hasattr(vista, "cargar_socios"):
            vista.cargar_socios()
        if hasattr(vista, "cargar_roles"):
            vista.cargar_roles()

    def cambiar_tema(self, nuevo_tema):
        ctk.set_appearance_mode(nuevo_tema)

