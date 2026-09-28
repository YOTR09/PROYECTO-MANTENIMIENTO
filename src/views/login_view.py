import customtkinter as ctk
from src.services.autenticacion_service import AutenticacionService


class LoginView(ctk.CTkFrame):
    def __init__(self, parent, on_success):
        super().__init__(parent, fg_color="transparent")
        self.on_success = on_success
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        formulario = ctk.CTkFrame(self, width=340, corner_radius=12)
        formulario.grid(row=0, column=0, padx=24, pady=24)
        formulario.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            formulario,
            text="Brisas del Palmar",
            font=ctk.CTkFont(size=24, weight="bold")
        ).grid(row=0, column=0, padx=28, pady=(30, 4))
        ctk.CTkLabel(
            formulario,
            text="Control de flota y mantenimiento",
            text_color="#9CA3AF"
        ).grid(row=1, column=0, padx=28, pady=(0, 24))

        ctk.CTkLabel(formulario, text="Usuario", anchor="w").grid(
            row=2, column=0, padx=28, pady=(0, 5), sticky="ew"
        )
        self.entrada_usuario = ctk.CTkEntry(formulario, placeholder_text="Usuario")
        self.entrada_usuario.grid(row=3, column=0, padx=28, pady=(0, 14), sticky="ew")

        ctk.CTkLabel(formulario, text="Contraseña", anchor="w").grid(
            row=4, column=0, padx=28, pady=(0, 5), sticky="ew"
        )
        self.entrada_contrasena = ctk.CTkEntry(
            formulario, placeholder_text="Contraseña", show="*"
        )
        self.entrada_contrasena.grid(row=5, column=0, padx=28, pady=(0, 8), sticky="ew")
        self.entrada_usuario.bind("<Return>", lambda _event: self._iniciar_sesion())
        self.entrada_contrasena.bind("<Return>", lambda _event: self._iniciar_sesion())

        self.mensaje_error = ctk.CTkLabel(
            formulario, text="", text_color="#EF4444", wraplength=280
        )
        self.mensaje_error.grid(row=6, column=0, padx=28, pady=(0, 8))

        ctk.CTkButton(
            formulario,
            text="Iniciar sesión",
            height=40,
            command=self._iniciar_sesion
        ).grid(row=7, column=0, padx=28, pady=(0, 30), sticky="ew")

        self.entrada_usuario.focus_set()

    def _iniciar_sesion(self):
        usuario = self.entrada_usuario.get()
        contrasena = self.entrada_contrasena.get()
        if AutenticacionService.validar_credenciales(usuario, contrasena):
            self.on_success()
            return

        self.mensaje_error.configure(text="Usuario o contraseña incorrectos.")
        self.entrada_contrasena.delete(0, "end")
        self.entrada_contrasena.focus_set()