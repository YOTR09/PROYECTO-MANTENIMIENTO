import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import customtkinter as ctk
from src.controllers.usuario_controller import UsuarioController
from src.models.usuario import Usuario
from src.views.theme import (
    BTN_PRIMARY_COLOR,
    BTN_PRIMARY_HOVER,
    BTN_DANGER_COLOR,
    BTN_DANGER_HOVER,
    TEXT_MUTED
)

class UsuariosView(ctk.CTkFrame):
    def __init__(self, parent, usuario_actual: Usuario):
        super().__init__(parent, corner_radius=10)
        self.usuario_actual = usuario_actual
        self.usuario_seleccionado_id = None
        self.roles_map = {}
        self._setup_ui()
        self.cargar_roles()
        self.cargar_datos()

    def _setup_ui(self):
        # Configuración grid: 2 columnas (Izquierda: Formulario | Derecha: Tabla de usuarios)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ---------------- PANEL IZQUIERDO: FORMULARIO ----------------
        self.form_card = ctk.CTkFrame(self, width=320, corner_radius=10)
        self.form_card.grid(row=0, column=0, padx=(15, 10), pady=15, sticky="nsew")

        lbl_form = ctk.CTkLabel(
            self.form_card,
            text="👤 Gestión de Usuarios",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        lbl_form.pack(padx=20, pady=(20, 15), anchor="w")

        # Username
        ctk.CTkLabel(self.form_card, text="Nombre de Usuario:", font=ctk.CTkFont(size=12, weight="bold")).pack(padx=20, pady=(4, 2), anchor="w")
        self.entry_username = ctk.CTkEntry(self.form_card, placeholder_text="ej: jmecanico")
        self.entry_username.pack(fill="x", padx=20, pady=(0, 8))

        # Nombre completo
        ctk.CTkLabel(self.form_card, text="Nombre Completo:", font=ctk.CTkFont(size=12, weight="bold")).pack(padx=20, pady=(4, 2), anchor="w")
        self.entry_nombre = ctk.CTkEntry(self.form_card, placeholder_text="ej: Juan Pérez")
        self.entry_nombre.pack(fill="x", padx=20, pady=(0, 8))

        # Rol
        ctk.CTkLabel(self.form_card, text="Nivel de Acceso / Rol:", font=ctk.CTkFont(size=12, weight="bold")).pack(padx=20, pady=(4, 2), anchor="w")
        self.combo_rol = ctk.CTkOptionMenu(self.form_card, values=["Cargando..."])
        self.combo_rol.pack(fill="x", padx=20, pady=(0, 8))

        # Contraseña
        ctk.CTkLabel(self.form_card, text="Contraseña (mínimo 4 caracteres):", font=ctk.CTkFont(size=12, weight="bold")).pack(padx=20, pady=(4, 2), anchor="w")
        self.entry_password = ctk.CTkEntry(self.form_card, placeholder_text="Contraseña inicial", show="*")
        self.entry_password.pack(fill="x", padx=20, pady=(0, 15))

        # Botones de Acción
        self.btn_guardar = ctk.CTkButton(
            self.form_card,
            text="💾 Registrar Usuario",
            fg_color=BTN_PRIMARY_COLOR,
            hover_color=BTN_PRIMARY_HOVER,
            command=self.guardar_usuario
        )
        self.btn_guardar.pack(fill="x", padx=20, pady=4)

        self.btn_reset_pwd = ctk.CTkButton(
            self.form_card,
            text="🔑 Restablecer Contraseña",
            fg_color="#D97706",
            hover_color="#B45309",
            command=self.restablecer_pwd
        )
        self.btn_reset_pwd.pack(fill="x", padx=20, pady=4)

        self.btn_eliminar = ctk.CTkButton(
            self.form_card,
            text="🗑️ Desactivar (Baja Lógica)",
            fg_color=BTN_DANGER_COLOR,
            hover_color=BTN_DANGER_HOVER,
            command=self.eliminar_usuario
        )
        self.btn_eliminar.pack(fill="x", padx=20, pady=4)

        self.btn_limpiar = ctk.CTkButton(
            self.form_card,
            text="🔄 Limpiar Selección",
            fg_color="transparent",
            border_width=1,
            command=self.limpiar_formulario
        )
        self.btn_limpiar.pack(fill="x", padx=20, pady=(4, 20))

        # ---------------- PANEL DERECHO: TABLA DE USUARIOS ----------------
        right_frame = ctk.CTkFrame(self, corner_radius=10)
        right_frame.grid(row=0, column=1, padx=(5, 15), pady=15, sticky="nsew")
        right_frame.grid_rowconfigure(1, weight=1)
        right_frame.grid_columnconfigure(0, weight=1)

        # Barra superior de búsqueda
        top_bar = ctk.CTkFrame(right_frame, fg_color="transparent")
        top_bar.grid(row=0, column=0, padx=15, pady=(15, 10), sticky="ew")

        ctk.CTkLabel(
            top_bar,
            text="📋 Cuentas y Accesos Registrados",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(side="left")

        self.entry_buscar = ctk.CTkEntry(top_bar, placeholder_text="Buscar usuario o nombre...", width=240)
        self.entry_buscar.pack(side="right")
        self.entry_buscar.bind("<KeyRelease>", lambda e: self.cargar_datos())

        # Tabla Treeview
        table_container = ctk.CTkFrame(right_frame, corner_radius=8)
        table_container.grid(row=1, column=0, padx=15, pady=(0, 15), sticky="nsew")

        cols = ("id", "username", "nombre", "rol", "estado", "creado")
        self.tree = ttk.Treeview(table_container, columns=cols, show="headings", selectmode="browse")

        self.tree.heading("id", text="ID")
        self.tree.heading("username", text="Usuario")
        self.tree.heading("nombre", text="Nombre Completo")
        self.tree.heading("rol", text="Nivel de Acceso (Rol)")
        self.tree.heading("estado", text="Estado")
        self.tree.heading("creado", text="Fecha Creación")

        self.tree.column("id", width=45, anchor="center")
        self.tree.column("username", width=120, anchor="w")
        self.tree.column("nombre", width=180, anchor="w")
        self.tree.column("rol", width=140, anchor="center")
        self.tree.column("estado", width=90, anchor="center")
        self.tree.column("creado", width=130, anchor="center")

        scroll_y = ttk.Scrollbar(table_container, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll_y.set)
        scroll_y.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)

        self.tree.bind("<<TreeviewSelect>>", self._on_item_select)

    def cargar_roles(self):
        roles = UsuarioController.listar_roles()
        self.roles_map = {r.nombre: r.id_rol for r in roles}
        if self.roles_map:
            nombres = list(self.roles_map.keys())
            self.combo_rol.configure(values=nombres)
            self.combo_rol.set(nombres[0])

    def cargar_datos(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        termino = self.entry_buscar.get()
        # Mostramos tanto activos como inactivos para gestión de usuarios
        usuarios = UsuarioController.listar_usuarios(search_term=termino, solo_activos=False)

        for u in usuarios:
            estado_txt = "🟢 Activo" if u.activo == 1 else "🔴 Inactivo"
            self.tree.insert("", "end", values=(
                u.id_usuario,
                u.username,
                u.nombre_completo,
                u.rol_nombre,
                estado_txt,
                u.creado_en
            ))

    def _on_item_select(self, event):
        seleccion = self.tree.selection()
        if not seleccion:
            return

        item = self.tree.item(seleccion[0])
        vals = item["values"]
        self.usuario_seleccionado_id = vals[0]

        usuario = UsuarioController.obtener_usuario(self.usuario_seleccionado_id)
        if usuario:
            self.entry_username.delete(0, "end")
            self.entry_username.insert(0, usuario.username)
            self.entry_username.configure(state="disabled") # Username inmutable

            self.entry_nombre.delete(0, "end")
            self.entry_nombre.insert(0, usuario.nombre_completo)

            self.combo_rol.set(usuario.rol_nombre)

            self.entry_password.delete(0, "end")
            self.entry_password.configure(placeholder_text="Sin cambios (usar botón reset)")

            self.btn_guardar.configure(text="✏️ Actualizar Usuario")
            if usuario.activo == 1:
                self.btn_eliminar.configure(text="🗑️ Desactivar Usuario", fg_color=BTN_DANGER_COLOR)
            else:
                self.btn_eliminar.configure(text="🔄 Reactivar Usuario", fg_color="#16A34A")

    def limpiar_formulario(self):
        self.usuario_seleccionado_id = None
        self.entry_username.configure(state="normal")
        self.entry_username.delete(0, "end")
        self.entry_nombre.delete(0, "end")
        self.entry_password.configure(placeholder_text="Contraseña inicial")
        self.entry_password.delete(0, "end")
        if self.roles_map:
            self.combo_rol.set(list(self.roles_map.keys())[0])
        self.btn_guardar.configure(text="💾 Registrar Usuario")
        self.btn_eliminar.configure(text="🗑️ Desactivar (Baja Lógica)", fg_color=BTN_DANGER_COLOR)

    def guardar_usuario(self):
        nombre_rol = self.combo_rol.get()
        id_rol = self.roles_map.get(nombre_rol, 1)
        nombre = self.entry_nombre.get().strip()

        if self.usuario_seleccionado_id is None:
            # Nuevo usuario
            username = self.entry_username.get().strip()
            pwd = self.entry_password.get().strip()
            ok, nuevo_u, msg = UsuarioController.registrar_usuario(
                id_rol=id_rol,
                username=username,
                contrasena=pwd,
                nombre_completo=nombre
            )
            if ok:
                messagebox.showinfo("Éxito", msg)
                self.limpiar_formulario()
                self.cargar_datos()
            else:
                messagebox.showwarning("Atención", msg)
        else:
            # Actualizar existente
            ok, msg = UsuarioController.actualizar_usuario(
                id_usuario=self.usuario_seleccionado_id,
                id_rol=id_rol,
                nombre_completo=nombre,
                activo=1
            )
            if ok:
                messagebox.showinfo("Éxito", msg)
                self.limpiar_formulario()
                self.cargar_datos()
            else:
                messagebox.showwarning("Atención", msg)

    def restablecer_pwd(self):
        if self.usuario_seleccionado_id is None:
            messagebox.showwarning("Atención", "Seleccione un usuario de la lista para restablecer su contraseña.")
            return

        nueva_pass = simpledialog.askstring("Nueva Contraseña", "Introduzca la nueva contraseña (mínimo 4 caracteres):", show="*")
        if nueva_pass is not None:
            ok, msg = UsuarioController.restablecer_contrasena(self.usuario_seleccionado_id, nueva_pass)
            if ok:
                messagebox.showinfo("Éxito", msg)
            else:
                messagebox.showwarning("Error", msg)

    def eliminar_usuario(self):
        if self.usuario_seleccionado_id is None:
            messagebox.showwarning("Atención", "Seleccione un usuario de la lista.")
            return

        u = UsuarioController.obtener_usuario(self.usuario_seleccionado_id)
        if not u:
            return

        if u.activo == 1:
            if messagebox.askyesno("Confirmar", f"¿Desea dar de baja lógicamente al usuario '{u.username}'?"):
                ok, msg = UsuarioController.eliminar_usuario(self.usuario_seleccionado_id, logico=True)
                if ok:
                    messagebox.showinfo("Éxito", msg)
                    self.limpiar_formulario()
                    self.cargar_datos()
                else:
                    messagebox.showwarning("Atención", msg)
        else:
            # Reactivar
            UsuarioController.actualizar_usuario(u.id_usuario, u.id_rol, u.nombre_completo, activo=1)
            messagebox.showinfo("Éxito", f"Usuario '{u.username}' reactivado exitosamente.")
            self.limpiar_formulario()
            self.cargar_datos()
