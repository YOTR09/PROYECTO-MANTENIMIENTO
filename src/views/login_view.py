import os
from PIL import Image
import customtkinter as ctk
from src.controllers.auth_controller import AuthController

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LOGO_DARK_PATH = os.path.join(BASE_DIR, "assets", "logo_empresa_dark.png")
LOGO_LIGHT_PATH = os.path.join(BASE_DIR, "assets", "logo_empresa_light.png")

class LoginView(ctk.CTkFrame):
    def __init__(self, parent, on_success):
        super().__init__(parent, fg_color="transparent")
        self.on_success = on_success
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        formulario = ctk.CTkFrame(self, width=420, corner_radius=14)
        formulario.grid(row=0, column=0, padx=24, pady=24)
        formulario.grid_columnconfigure(0, weight=1)

        # Logotipo Corporativo con CTkImage
        if os.path.exists(LOGO_DARK_PATH) and os.path.exists(LOGO_LIGHT_PATH):
            try:
                img_dark = Image.open(LOGO_DARK_PATH)
                img_light = Image.open(LOGO_LIGHT_PATH)
                self.logo_ctk = ctk.CTkImage(
                    light_image=img_light,
                    dark_image=img_dark,
                    size=(240, 60)
                )
                lbl_logo = ctk.CTkLabel(formulario, text="", image=self.logo_ctk)
                lbl_logo.grid(row=0, column=0, padx=28, pady=(25, 4))
            except Exception:
                ctk.CTkLabel(
                    formulario,
                    text="🚍 Brisas del Palmar",
                    font=ctk.CTkFont(size=24, weight="bold")
                ).grid(row=0, column=0, padx=28, pady=(25, 4))
        else:
            ctk.CTkLabel(
                formulario,
                text="🚍 Brisas del Palmar",
                font=ctk.CTkFont(size=24, weight="bold")
            ).grid(row=0, column=0, padx=28, pady=(25, 4))

        ctk.CTkLabel(
            formulario,
            text="Sistema de Control de Mantenimiento Preventivo",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#3B82F6"
        ).grid(row=1, column=0, padx=28, pady=(0, 16))

        # Campos de entrada
        ctk.CTkLabel(formulario, text="Nombre de Usuario:", anchor="w", font=ctk.CTkFont(size=13, weight="bold")).grid(
            row=2, column=0, padx=28, pady=(0, 4), sticky="ew"
        )
        self.entrada_usuario = ctk.CTkEntry(formulario, placeholder_text="Ej: admin, mecanico, auditor", height=38)
        self.entrada_usuario.grid(row=3, column=0, padx=28, pady=(0, 12), sticky="ew")

        ctk.CTkLabel(formulario, text="Contraseña:", anchor="w", font=ctk.CTkFont(size=13, weight="bold")).grid(
            row=4, column=0, padx=28, pady=(0, 4), sticky="ew"
        )
        self.entrada_contrasena = ctk.CTkEntry(
            formulario, placeholder_text="Contraseña", show="*", height=38
        )
        self.entrada_contrasena.grid(row=5, column=0, padx=28, pady=(0, 6), sticky="ew")

        self.entrada_usuario.bind("<Return>", lambda _event: self._iniciar_sesion())
        self.entrada_contrasena.bind("<Return>", lambda _event: self._iniciar_sesion())

        # Botón Recuperar Contraseña
        btn_olvido = ctk.CTkButton(
            formulario,
            text="¿Olvidaste tu contraseña?",
            font=ctk.CTkFont(size=11, underline=True),
            fg_color="transparent",
            text_color=("#2563EB", "#60A5FA"),
            hover_color=("gray90", "gray20"),
            height=20,
            command=self._abrir_modal_recuperacion
        )
        btn_olvido.grid(row=6, column=0, padx=28, pady=(0, 4), sticky="e")

        self.mensaje_error = ctk.CTkLabel(
            formulario, text="", text_color="#EF4444", wraplength=340, font=ctk.CTkFont(size=12)
        )
        self.mensaje_error.grid(row=7, column=0, padx=28, pady=(0, 6))

        btn_login = ctk.CTkButton(
            formulario,
            text="Iniciar Sesión",
            height=42,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self._iniciar_sesion
        )
        btn_login.grid(row=8, column=0, padx=28, pady=(0, 15), sticky="ew")

        # Tarjeta de ayuda rápida con credenciales de prueba para los 3 roles
        box_roles = ctk.CTkFrame(formulario, corner_radius=8, fg_color=("gray90", "gray17"))
        box_roles.grid(row=9, column=0, padx=28, pady=(0, 20), sticky="ew")

        ctk.CTkLabel(
            box_roles,
            text="🔑 Accesos rápidos para evaluación:",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=("gray30", "gray70")
        ).pack(anchor="w", padx=10, pady=(8, 4))

        f_chips = ctk.CTkFrame(box_roles, fg_color="transparent")
        f_chips.pack(fill="x", padx=8, pady=(0, 8))

        ctk.CTkButton(
            f_chips,
            text="Admin",
            width=80,
            height=26,
            font=ctk.CTkFont(size=11),
            fg_color="#3B82F6",
            hover_color="#2563EB",
            command=lambda: self._autocompletar("admin", "admin123")
        ).pack(side="left", padx=3)

        ctk.CTkButton(
            f_chips,
            text="Mecánico",
            width=85,
            height=26,
            font=ctk.CTkFont(size=11),
            fg_color="#F59E0B",
            hover_color="#D97706",
            command=lambda: self._autocompletar("mecanico", "mecanico123")
        ).pack(side="left", padx=3)

        ctk.CTkButton(
            f_chips,
            text="Operador",
            width=85,
            height=26,
            font=ctk.CTkFont(size=11),
            fg_color="#10B981",
            hover_color="#059669",
            command=lambda: self._autocompletar("auditor", "auditor123")
        ).pack(side="left", padx=3)

        self.entrada_usuario.focus_set()

    def _autocompletar(self, user, pwd):
        self.entrada_usuario.delete(0, "end")
        self.entrada_usuario.insert(0, user)
        self.entrada_contrasena.delete(0, "end")
        self.entrada_contrasena.insert(0, pwd)
        self.mensaje_error.configure(text="")

    def _iniciar_sesion(self):
        usuario = self.entrada_usuario.get()
        contrasena = self.entrada_contrasena.get()

        ok, usuario_obj, msg = AuthController.login(usuario, contrasena)
        if ok and usuario_obj:
            self.on_success(usuario_obj)
            return

        self.mensaje_error.configure(text=msg or "Usuario o contraseña incorrectos.")
        self.entrada_contrasena.delete(0, "end")
        self.entrada_contrasena.focus_set()

    def _abrir_modal_recuperacion(self):
        from src.views.recuperar_password_modal import RecuperarPasswordModal
        RecuperarPasswordModal(self, on_success_callback=self._al_recuperar_exitoso)

    def _al_recuperar_exitoso(self, username):
        self.entrada_usuario.delete(0, "end")
        self.entrada_usuario.insert(0, username)
        self.entrada_contrasena.delete(0, "end")
        self.entrada_contrasena.focus_set()
        self.mensaje_error.configure(
            text="✓ Contraseña actualizada. Ingrese su nueva clave.",
            text_color="#10B981"
        )