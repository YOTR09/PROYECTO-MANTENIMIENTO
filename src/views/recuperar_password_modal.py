import customtkinter as ctk
from tkinter import messagebox
from src.controllers.auth_controller import AuthController
from src.views.theme import (
    BTN_PRIMARY_COLOR,
    BTN_PRIMARY_HOVER,
    BTN_SUCCESS_COLOR,
    BTN_SUCCESS_HOVER,
    TEXT_MUTED
)

class RecuperarPasswordModal(ctk.CTkToplevel):
    def __init__(self, parent, on_success_callback=None):
        super().__init__(parent)
        self.on_success_callback = on_success_callback

        self.title("Recuperación de Contraseña - Brisas del Palmar")
        self.geometry("490x600")
        self.minsize(460, 560)
        self.grab_set()

        self._setup_ui()

    def _setup_ui(self):
        # Cabecera
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=25, pady=(20, 10))

        ctk.CTkLabel(
            header_frame,
            text="🔐 Restablecer Contraseña",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(anchor="w")

        ctk.CTkLabel(
            header_frame,
            text="Recupere el acceso a su cuenta mediante su pregunta secreta o clave maestra.",
            font=ctk.CTkFont(size=11),
            text_color=TEXT_MUTED,
            wraplength=440,
            justify="left"
        ).pack(anchor="w", pady=(2, 0))

        # Selector de Modo (Pestañas)
        self.tabview = ctk.CTkTabview(self, corner_radius=10)
        self.tabview.pack(fill="both", expand=True, padx=25, pady=(5, 15))

        self.tab_pregunta = self.tabview.add("Pregunta Secreta")
        self.tab_maestra = self.tabview.add("Clave Maestra")

        self._setup_tab_pregunta()
        self._setup_tab_maestra()

    # ---------------- PESTAÑA 1: PREGUNTA SECRETA ----------------
    def _setup_tab_pregunta(self):
        f = self.tab_pregunta

        ctk.CTkLabel(f, text="1. Ingrese su Nombre de Usuario:", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=10, pady=(10, 2))
        row_u = ctk.CTkFrame(f, fg_color="transparent")
        row_u.pack(fill="x", padx=10, pady=(0, 10))

        self.entry_u_preg = ctk.CTkEntry(row_u, placeholder_text="Ej: admin, mecanico, auditor", height=34)
        self.entry_u_preg.pack(side="left", fill="x", expand=True, padx=(0, 8))

        btn_buscar = ctk.CTkButton(
            row_u,
            text="Buscar",
            width=85,
            height=34,
            fg_color=BTN_PRIMARY_COLOR,
            hover_color=BTN_PRIMARY_HOVER,
            command=self._buscar_pregunta_usuario
        )
        btn_buscar.pack(side="right")

        # Contenedor dinámico de pregunta y nueva clave (inicialmente oculto o deshabilitado)
        self.card_pregunta = ctk.CTkFrame(f, corner_radius=8, fg_color=("gray90", "gray17"))
        self.card_pregunta.pack(fill="x", padx=10, pady=(0, 10))

        self.lbl_pregunta_tit = ctk.CTkLabel(
            self.card_pregunta,
            text="Pregunta de Seguridad:",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=("gray30", "gray70")
        )
        self.lbl_pregunta_tit.pack(anchor="w", padx=12, pady=(8, 2))

        self.lbl_pregunta_texto = ctk.CTkLabel(
            self.card_pregunta,
            text="Ingrese su usuario y presione 'Buscar' para ver su pregunta.",
            font=ctk.CTkFont(size=12),
            text_color=("#1E3A8A", "#93C5FD"),
            wraplength=380,
            justify="left"
        )
        self.lbl_pregunta_texto.pack(anchor="w", padx=12, pady=(0, 8))

        ctk.CTkLabel(f, text="2. Su Respuesta Secreta:", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=10, pady=(4, 2))
        self.entry_resp = ctk.CTkEntry(f, placeholder_text="Respuesta a su pregunta secreta", height=34)
        self.entry_resp.pack(fill="x", padx=10, pady=(0, 10))

        ctk.CTkLabel(f, text="3. Nueva Contraseña:", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=10, pady=(4, 2))
        self.entry_nueva_preg = ctk.CTkEntry(f, placeholder_text="Mínimo 4 caracteres", show="*", height=34)
        self.entry_nueva_preg.pack(fill="x", padx=10, pady=(0, 8))

        ctk.CTkLabel(f, text="4. Confirmar Nueva Contraseña:", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=10, pady=(4, 2))
        self.entry_conf_preg = ctk.CTkEntry(f, placeholder_text="Repita la nueva contraseña", show="*", height=34)
        self.entry_conf_preg.pack(fill="x", padx=10, pady=(0, 8))

        self.var_show_preg = ctk.BooleanVar(value=False)
        chk_show = ctk.CTkCheckBox(
            f,
            text="Mostrar contraseñas",
            variable=self.var_show_preg,
            font=ctk.CTkFont(size=11),
            command=lambda: self._toggle_show_passwords(self.entry_nueva_preg, self.entry_conf_preg, self.var_show_preg)
        )
        chk_show.pack(anchor="w", padx=12, pady=(0, 15))

        btn_guardar = ctk.CTkButton(
            f,
            text="💾 Restablecer Contraseña",
            height=38,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=BTN_SUCCESS_COLOR,
            hover_color=BTN_SUCCESS_HOVER,
            command=self._ejecutar_restablecer_pregunta
        )
        btn_guardar.pack(fill="x", padx=10, pady=(0, 10))

    # ---------------- PESTAÑA 2: CLAVE MAESTRA ----------------
    def _setup_tab_maestra(self):
        f = self.tab_maestra

        ctk.CTkLabel(
            f,
            text="Uso exclusivo para soporte institucional de Brisas del Palmar.",
            font=ctk.CTkFont(size=11),
            text_color=TEXT_MUTED
        ).pack(anchor="w", padx=10, pady=(10, 8))

        ctk.CTkLabel(f, text="Nombre de Usuario:", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=10, pady=(4, 2))
        self.entry_u_mast = ctk.CTkEntry(f, placeholder_text="Usuario a restablecer", height=34)
        self.entry_u_mast.pack(fill="x", padx=10, pady=(0, 10))

        ctk.CTkLabel(f, text="Código Maestro de Soporte:", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=10, pady=(4, 2))
        self.entry_clave_mast = ctk.CTkEntry(f, placeholder_text="Clave maestra institucional", show="*", height=34)
        self.entry_clave_mast.pack(fill="x", padx=10, pady=(0, 10))

        ctk.CTkLabel(f, text="Nueva Contraseña:", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=10, pady=(4, 2))
        self.entry_nueva_mast = ctk.CTkEntry(f, placeholder_text="Mínimo 4 caracteres", show="*", height=34)
        self.entry_nueva_mast.pack(fill="x", padx=10, pady=(0, 8))

        ctk.CTkLabel(f, text="Confirmar Nueva Contraseña:", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=10, pady=(4, 2))
        self.entry_conf_mast = ctk.CTkEntry(f, placeholder_text="Repita la nueva contraseña", show="*", height=34)
        self.entry_conf_mast.pack(fill="x", padx=10, pady=(0, 8))

        self.var_show_mast = ctk.BooleanVar(value=False)
        chk_show_m = ctk.CTkCheckBox(
            f,
            text="Mostrar contraseñas",
            variable=self.var_show_mast,
            font=ctk.CTkFont(size=11),
            command=lambda: self._toggle_show_passwords(self.entry_nueva_mast, self.entry_conf_mast, self.var_show_mast)
        )
        chk_show_m.pack(anchor="w", padx=12, pady=(0, 15))

        btn_guardar_m = ctk.CTkButton(
            f,
            text="⚡ Restablecer con Clave Maestra",
            height=38,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#F59E0B",
            hover_color="#D97706",
            command=self._ejecutar_restablecer_maestra
        )
        btn_guardar_m.pack(fill="x", padx=10, pady=(0, 10))

    def _toggle_show_passwords(self, entry1, entry2, var):
        char = "" if var.get() else "*"
        entry1.configure(show=char)
        entry2.configure(show=char)

    def _buscar_pregunta_usuario(self):
        usuario = self.entry_u_preg.get().strip()
        ok, pregunta, msg = AuthController.obtener_pregunta_recuperacion(usuario)
        if ok and pregunta:
            texto_p = pregunta if pregunta.startswith("¿") else f"¿{pregunta}?"
            self.lbl_pregunta_texto.configure(text=texto_p)
            self.entry_resp.focus_set()
        else:
            self.lbl_pregunta_texto.configure(text="Usuario no encontrado o inactivo.")
            messagebox.showwarning("Atención", msg)

    def _ejecutar_restablecer_pregunta(self):
        usuario = self.entry_u_preg.get().strip()
        respuesta = self.entry_resp.get().strip()
        nueva = self.entry_nueva_preg.get()
        conf = self.entry_conf_preg.get()

        ok, msg = AuthController.restablecer_por_pregunta(usuario, respuesta, nueva, conf)
        if ok:
            messagebox.showinfo("Éxito", msg)
            if self.on_success_callback:
                self.on_success_callback(usuario)
            self.destroy()
        else:
            messagebox.showerror("Error de Validación", msg)

    def _ejecutar_restablecer_maestra(self):
        usuario = self.entry_u_mast.get().strip()
        clave_maestra = self.entry_clave_mast.get().strip()
        nueva = self.entry_nueva_mast.get()
        conf = self.entry_conf_mast.get()

        ok, msg = AuthController.restablecer_por_clave_maestra(usuario, clave_maestra, nueva, conf)
        if ok:
            messagebox.showinfo("Éxito", msg)
            if self.on_success_callback:
                self.on_success_callback(usuario)
            self.destroy()
        else:
            messagebox.showerror("Error", msg)
