import customtkinter as ctk
from src.views.dashboard_view import DashboardView
from src.views.vehiculos_view import VehiculosView
from src.views.socios_view import SociosView
from src.views.programacion_mant_view import ProgramacionMantView
from src.views.tipos_mant_view import TiposMantView
from src.views.historial_mant_view import HistorialMantView

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Brisas del Palmar - Control de Flota y Mantenimiento Preventivo")
        self.geometry("1240x760")
        self.minsize(1050, 680)

        # Configuración de tema visual
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        self.vistas = {}
        self.botones_nav = {}
        self.vista_actual_key = None

        self._setup_layout()
        self._inicializar_vistas()
        self.cambiar_vista("dashboard")

    def _setup_layout(self):
        # Configurar grid 1x2 (Sidebar a la izquierda, Contenido a la derecha)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ---------------- BARRA LATERAL (SIDEBAR) ----------------
        self.sidebar = ctk.CTkFrame(self, width=240, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(8, weight=1) # Empuja selector de tema al fondo

        # Logo y Título
        lbl_empresa = ctk.CTkLabel(
            self.sidebar,
            text="🚍 Brisas del Palmar",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        lbl_empresa.grid(row=0, column=0, padx=20, pady=(25, 2), sticky="w")

        lbl_sub = ctk.CTkLabel(
            self.sidebar,
            text="Transporte y Mantenimiento",
            font=ctk.CTkFont(size=12),
            text_color="#9CA3AF"
        )
        lbl_sub.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="w")

        # Botones de Navegación
        secciones = [
            ("dashboard", "📊 Dashboard y Alertas"),
            ("unidades", "🚐 Flota y Unidades"),
            ("socios", "👥 Socios y Propietarios"),
            ("preventivo", "🛠️ Control Preventivo"),
            ("catalogo", "📋 Catálogo Rutinas"),
            ("historial", "📜 Bitácora Histórica"),
        ]

        for i, (key, label) in enumerate(secciones, start=2):
            btn = ctk.CTkButton(
                self.sidebar,
                text=label,
                height=42,
                corner_radius=8,
                fg_color="transparent",
                text_color=("gray10", "gray90"),
                hover_color=("gray70", "gray30"),
                anchor="w",
                font=ctk.CTkFont(size=14),
                command=lambda k=key: self.cambiar_vista(k)
            )
            btn.grid(row=i, column=0, padx=15, pady=4, sticky="ew")
            self.botones_nav[key] = btn

        # Selector de Tema al fondo de la barra
        lbl_tema = ctk.CTkLabel(self.sidebar, text="Modo de Interfaz:", font=ctk.CTkFont(size=12))
        lbl_tema.grid(row=9, column=0, padx=20, pady=(10, 0), sticky="w")

        self.combo_tema = ctk.CTkOptionMenu(
            self.sidebar,
            values=["Dark", "Light", "System"],
            command=self.cambiar_tema
        )
        self.combo_tema.grid(row=10, column=0, padx=15, pady=(5, 20), sticky="ew")
        self.combo_tema.set("Dark")

        # ---------------- CONTENEDOR PRINCIPAL ----------------
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.grid(row=0, column=1, sticky="nsew", padx=15, pady=15)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

    def _inicializar_vistas(self):
        self.vistas["dashboard"] = DashboardView(self.container, on_navigate=self.cambiar_vista)
        self.vistas["unidades"] = VehiculosView(self.container)
        self.vistas["socios"] = SociosView(self.container)
        self.vistas["preventivo"] = ProgramacionMantView(self.container)
        self.vistas["catalogo"] = TiposMantView(self.container)
        self.vistas["historial"] = HistorialMantView(self.container)

        # Ubicar todas las vistas en el contenedor (ocultas inicialmente)
        for vista in self.vistas.values():
            vista.grid(row=0, column=0, sticky="nsew")

    def cambiar_vista(self, key):
        if key not in self.vistas:
            return

        self.vista_actual_key = key
        vista = self.vistas[key]
        vista.tkraise()

        # Estilo del botón activo
        for k, btn in self.botones_nav.items():
            if k == key:
                btn.configure(fg_color=("#3B82F6", "#1D4ED8"), text_color="white")
            else:
                btn.configure(fg_color="transparent", text_color=("gray10", "gray90"))

        # Refrescar datos al navegar
        if hasattr(vista, "actualizar_dashboard"):
            vista.actualizar_dashboard()
        elif hasattr(vista, "cargar_datos"):
            vista.cargar_datos()
        if hasattr(vista, "cargar_socios"):
            vista.cargar_socios()

    def cambiar_tema(self, nuevo_tema):
        ctk.set_appearance_mode(nuevo_tema)

