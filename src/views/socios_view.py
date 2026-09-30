import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from src.controllers.socio_controller import SocioController
from src.models.usuario import Usuario
from src.models.enums import EstadoSocio
from src.views.theme import (
    BTN_SUCCESS_COLOR,
    BTN_SUCCESS_HOVER,
    BTN_PRIMARY_COLOR,
    BTN_PRIMARY_HOVER,
    BTN_NEUTRAL_COLOR,
    BTN_NEUTRAL_HOVER,
    BTN_DANGER_COLOR,
    BTN_DANGER_HOVER,
)
from typing import Optional

class SociosView(ctk.CTkFrame):
    def __init__(self, parent, usuario_actual: Optional[Usuario] = None):
        super().__init__(parent, corner_radius=10)
        self.usuario_actual = usuario_actual
        self.socio_seleccionado_id = None
        self._setup_ui()
        self._aplicar_permisos()
        self.cargar_datos()

    def _setup_ui(self):
        # Cabecera
        top_frame = ctk.CTkFrame(self, fg_color="transparent")
        top_frame.pack(fill="x", padx=20, pady=(15, 10))

        lbl_titulo = ctk.CTkLabel(
            top_frame,
            text="👥 Gestión de Socios y Propietarios",
            font=ctk.CTkFont(size=22, weight="bold")
        )
        lbl_titulo.pack(side="left")

        # Barra de búsqueda
        self.entry_buscar = ctk.CTkEntry(
            top_frame,
            placeholder_text="Buscar por cédula, nombre o teléfono...",
            width=300
        )
        self.entry_buscar.pack(side="right")
        self.entry_buscar.bind("<KeyRelease>", lambda e: self.cargar_datos())

        # Contenedor con dos columnas (Formulario a la izquierda, Tabla a la derecha)
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=(0, 15))

        # ---------------- FORMULARIO LATERAL ----------------
        self.form_card = ctk.CTkFrame(content_frame, width=320, corner_radius=10)
        self.form_card.pack(side="left", fill="y", padx=(0, 15), pady=5)
        self.form_card.pack_propagate(False)

        lbl_form = ctk.CTkLabel(self.form_card, text="Ficha del Socio", font=ctk.CTkFont(size=16, weight="bold"))
        lbl_form.pack(padx=20, pady=(15, 10), anchor="w")

        # Cédula o RIF
        ctk.CTkLabel(self.form_card, text="Cédula / Documento (*):", anchor="w").pack(fill="x", padx=20, pady=(4, 0))
        self.var_cedula = ctk.StringVar()
        self.entry_cedula = ctk.CTkEntry(self.form_card, textvariable=self.var_cedula, placeholder_text="Ej: V-12345678")
        self.entry_cedula.pack(fill="x", padx=20, pady=(0, 8))

        # Nombre Completo
        ctk.CTkLabel(self.form_card, text="Nombre Completo (*):", anchor="w").pack(fill="x", padx=20, pady=(4, 0))
        self.var_nombre = ctk.StringVar()
        self.entry_nombre = ctk.CTkEntry(self.form_card, textvariable=self.var_nombre, placeholder_text="Ej: Juan Pérez")
        self.entry_nombre.pack(fill="x", padx=20, pady=(0, 8))

        # Teléfono
        ctk.CTkLabel(self.form_card, text="Teléfono / Contacto:", anchor="w").pack(fill="x", padx=20, pady=(4, 0))
        self.var_telefono = ctk.StringVar()
        self.entry_telefono = ctk.CTkEntry(self.form_card, textvariable=self.var_telefono, placeholder_text="Ej: 0414-1234567")
        self.entry_telefono.pack(fill="x", padx=20, pady=(0, 8))

        # Estado del Socio
        ctk.CTkLabel(self.form_card, text="Estado de Afiliación:", anchor="w").pack(fill="x", padx=20, pady=(4, 0))
        self.var_estado = ctk.StringVar(value=EstadoSocio.ACTIVO.value)
        self.combo_estado = ctk.CTkComboBox(
            self.form_card,
            values=[EstadoSocio.ACTIVO.value, EstadoSocio.INACTIVO.value],
            variable=self.var_estado,
            state="readonly"
        )
        self.combo_estado.pack(fill="x", padx=20, pady=(0, 15))

        # Botones de Acción
        self.btn_guardar = ctk.CTkButton(self.form_card, text="➕ Guardar Socio", fg_color=BTN_SUCCESS_COLOR, hover_color=BTN_SUCCESS_HOVER, command=self.guardar)
        self.btn_guardar.pack(fill="x", padx=20, pady=4)

        self.btn_actualizar = ctk.CTkButton(self.form_card, text="✏️ Actualizar", fg_color=BTN_PRIMARY_COLOR, hover_color=BTN_PRIMARY_HOVER, command=self.actualizar)
        self.btn_actualizar.pack(fill="x", padx=20, pady=4)

        self.btn_limpiar = ctk.CTkButton(self.form_card, text="🧹 Limpiar Campos", fg_color=BTN_NEUTRAL_COLOR, hover_color=BTN_NEUTRAL_HOVER, command=self.limpiar_formulario)
        self.btn_limpiar.pack(fill="x", padx=20, pady=4)

        self.btn_eliminar = ctk.CTkButton(self.form_card, text="🗑️ Baja Lógica de Socio", fg_color=BTN_DANGER_COLOR, hover_color=BTN_DANGER_HOVER, command=self.eliminar)
        self.btn_eliminar.pack(fill="x", padx=20, pady=(4, 15))

        # ---------------- TABLA DE DATOS ----------------
        table_container = ctk.CTkFrame(content_frame, corner_radius=10)
        table_container.pack(side="right", fill="both", expand=True, pady=5)

        columnas = ("id", "cedula", "nombre", "telefono", "estado")
        self.tree = ttk.Treeview(table_container, columns=columnas, show="headings", selectmode="browse")

        self.tree.heading("id", text="ID")
        self.tree.heading("cedula", text="Cédula")
        self.tree.heading("nombre", text="Nombre Completo")
        self.tree.heading("telefono", text="Teléfono")
        self.tree.heading("estado", text="Estado")

        self.tree.column("id", width=50, anchor="center")
        self.tree.column("cedula", width=120, anchor="center")
        self.tree.column("nombre", width=220, anchor="w")
        self.tree.column("telefono", width=130, anchor="center")
        self.tree.column("estado", width=100, anchor="center")

        scroll_y = ttk.Scrollbar(table_container, orient="vertical", command=self.tree.yview)
        scroll_x = ttk.Scrollbar(table_container, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")
        self.tree.pack(fill="both", expand=True, padx=5, pady=5)

        self.tree.bind("<<TreeviewSelect>>", self.al_seleccionar_fila)

    def _aplicar_permisos(self):
        if not self.usuario_actual:
            return
        if not self.usuario_actual.es_admin:
            self.btn_guardar.configure(state="disabled")
            self.btn_actualizar.configure(state="disabled")
            self.btn_eliminar.configure(state="disabled")

    def cargar_datos(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        termino = self.entry_buscar.get()
        socios = SocioController.listar_socios(search_term=termino, solo_activos=True)

        for s in socios:
            self.tree.insert("", "end", values=(
                s.id_socio,
                s.cedula,
                s.nombre_completo,
                s.telefono or "-",
                s.estado
            ))

    def al_seleccionar_fila(self, event):
        seleccion = self.tree.selection()
        if not seleccion:
            return

        item = self.tree.item(seleccion[0])
        valores = item["values"]
        self.socio_seleccionado_id = valores[0]

        socio = SocioController.obtener_socio(self.socio_seleccionado_id)
        if socio:
            self.var_cedula.set(socio.cedula)
            self.var_nombre.set(socio.nombre_completo)
            self.var_telefono.set(socio.telefono or "")
            self.var_estado.set(socio.estado)

    def limpiar_formulario(self):
        self.socio_seleccionado_id = None
        self.var_cedula.set("")
        self.var_nombre.set("")
        self.var_telefono.set("")
        self.var_estado.set(EstadoSocio.ACTIVO.value)
        self.tree.selection_remove(self.tree.selection())

    def guardar(self):
        ok, nuevo_s, msg = SocioController.registrar_socio(
            cedula=self.var_cedula.get(),
            nombre_completo=self.var_nombre.get(),
            telefono=self.var_telefono.get(),
            estado=self.var_estado.get()
        )
        if ok:
            messagebox.showinfo("Éxito", msg)
            self.limpiar_formulario()
            self.cargar_datos()
        else:
            messagebox.showwarning("Atención", msg)

    def actualizar(self):
        if not self.socio_seleccionado_id:
            messagebox.showwarning("Atención", "Seleccione un socio de la lista para actualizar.")
            return

        ok, msg = SocioController.actualizar_socio(
            id_socio=self.socio_seleccionado_id,
            cedula=self.var_cedula.get(),
            nombre_completo=self.var_nombre.get(),
            telefono=self.var_telefono.get(),
            estado=self.var_estado.get()
        )
        if ok:
            messagebox.showinfo("Éxito", msg)
            self.limpiar_formulario()
            self.cargar_datos()
        else:
            messagebox.showwarning("Atención", msg)

    def eliminar(self):
        if not self.socio_seleccionado_id:
            messagebox.showwarning("Atención", "Seleccione un socio de la lista para dar de baja.")
            return

        if messagebox.askyesno("Confirmar Baja Lógica", "¿Está seguro de dar de baja al socio seleccionado?\nEl socio quedará inactivo pero su histórico se conservará."):
            ok, msg = SocioController.eliminar_socio(self.socio_seleccionado_id, logico=True)
            if ok:
                messagebox.showinfo("Baja Lógica Exitosa", msg)
                self.limpiar_formulario()
                self.cargar_datos()
            else:
                messagebox.showerror("Error", msg)
