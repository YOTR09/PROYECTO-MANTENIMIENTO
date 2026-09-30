import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from src.controllers.mantenimiento_controller import MantenimientoController
from src.models.usuario import Usuario
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

class TiposMantView(ctk.CTkFrame):
    def __init__(self, parent, usuario_actual: Optional[Usuario] = None):
        super().__init__(parent, corner_radius=10)
        self.usuario_actual = usuario_actual
        self.tipo_seleccionado_id = None
        self._setup_ui()
        self._aplicar_permisos()
        self.cargar_datos()

    def _setup_ui(self):
        # Cabecera
        top_frame = ctk.CTkFrame(self, fg_color="transparent")
        top_frame.pack(fill="x", padx=20, pady=(15, 10))

        lbl_titulo = ctk.CTkLabel(
            top_frame,
            text="📋 Catálogo de Rutinas de Mantenimiento Preventivo",
            font=ctk.CTkFont(size=22, weight="bold")
        )
        lbl_titulo.pack(side="left")

        # Barra de búsqueda
        self.entry_buscar = ctk.CTkEntry(
            top_frame,
            placeholder_text="Buscar rutina por nombre o descripción...",
            width=300
        )
        self.entry_buscar.pack(side="right")
        self.entry_buscar.bind("<KeyRelease>", lambda e: self.cargar_datos())

        # Contenedor con dos columnas
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=(0, 15))

        # ---------------- FORMULARIO LATERAL ----------------
        self.form_card = ctk.CTkFrame(content_frame, width=320, corner_radius=10)
        self.form_card.pack(side="left", fill="y", padx=(0, 15), pady=5)
        self.form_card.pack_propagate(False)

        lbl_form = ctk.CTkLabel(self.form_card, text="Definición de Rutina", font=ctk.CTkFont(size=16, weight="bold"))
        lbl_form.pack(padx=20, pady=(15, 10), anchor="w")

        # Nombre de la Rutina
        ctk.CTkLabel(self.form_card, text="Nombre del Mantenimiento (*):", anchor="w").pack(fill="x", padx=20, pady=(4, 0))
        self.var_nombre = ctk.StringVar()
        self.entry_nombre = ctk.CTkEntry(self.form_card, textvariable=self.var_nombre, placeholder_text="Ej: Cambio de Filtro de Aire")
        self.entry_nombre.pack(fill="x", padx=20, pady=(0, 8))

        # Intervalo en Kilómetros
        ctk.CTkLabel(self.form_card, text="Intervalo por Kilometraje (Km):", anchor="w").pack(fill="x", padx=20, pady=(4, 0))
        self.var_km = ctk.StringVar()
        self.entry_km = ctk.CTkEntry(self.form_card, textvariable=self.var_km, placeholder_text="0 si aplica solo por días")
        self.entry_km.pack(fill="x", padx=20, pady=(0, 8))

        # Intervalo en Días
        ctk.CTkLabel(self.form_card, text="Intervalo por Tiempo (Días):", anchor="w").pack(fill="x", padx=20, pady=(4, 0))
        self.var_dias = ctk.StringVar()
        self.entry_dias = ctk.CTkEntry(self.form_card, textvariable=self.var_dias, placeholder_text="0 si aplica solo por km")
        self.entry_dias.pack(fill="x", padx=20, pady=(0, 8))

        # Descripción
        ctk.CTkLabel(self.form_card, text="Detalle / Especificaciones:", anchor="w").pack(fill="x", padx=20, pady=(4, 0))
        self.entry_desc = ctk.CTkTextbox(self.form_card, height=80)
        self.entry_desc.pack(fill="x", padx=20, pady=(0, 15))

        # Botones de Acción
        self.btn_guardar = ctk.CTkButton(self.form_card, text="➕ Guardar Rutina", fg_color=BTN_SUCCESS_COLOR, hover_color=BTN_SUCCESS_HOVER, command=self.guardar)
        self.btn_guardar.pack(fill="x", padx=20, pady=4)

        self.btn_actualizar = ctk.CTkButton(self.form_card, text="✏️ Actualizar Rutina", fg_color=BTN_PRIMARY_COLOR, hover_color=BTN_PRIMARY_HOVER, command=self.actualizar)
        self.btn_actualizar.pack(fill="x", padx=20, pady=4)

        self.btn_limpiar = ctk.CTkButton(self.form_card, text="🧹 Limpiar Campos", fg_color=BTN_NEUTRAL_COLOR, hover_color=BTN_NEUTRAL_HOVER, command=self.limpiar_formulario)
        self.btn_limpiar.pack(fill="x", padx=20, pady=4)

        self.btn_eliminar = ctk.CTkButton(self.form_card, text="🗑️ Baja Lógica de Rutina", fg_color=BTN_DANGER_COLOR, hover_color=BTN_DANGER_HOVER, command=self.eliminar)
        self.btn_eliminar.pack(fill="x", padx=20, pady=(4, 15))

        # ---------------- TABLA DE DATOS ----------------
        table_container = ctk.CTkFrame(content_frame, corner_radius=10)
        table_container.pack(side="right", fill="both", expand=True, pady=5)

        columnas = ("id", "nombre", "km", "dias", "descripcion")
        self.tree = ttk.Treeview(table_container, columns=columnas, show="headings", selectmode="browse")

        self.tree.heading("id", text="ID")
        self.tree.heading("nombre", text="Nombre de la Rutina")
        self.tree.heading("km", text="Frecuencia (Km)")
        self.tree.heading("dias", text="Frecuencia (Días)")
        self.tree.heading("descripcion", text="Especificaciones Técnicas")

        self.tree.column("id", width=40, anchor="center")
        self.tree.column("nombre", width=220, anchor="w")
        self.tree.column("km", width=120, anchor="e")
        self.tree.column("dias", width=120, anchor="e")
        self.tree.column("descripcion", width=260, anchor="w")

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
        if self.usuario_actual.es_operador:
            self.btn_guardar.configure(state="disabled")
            self.btn_actualizar.configure(state="disabled")
            self.btn_eliminar.configure(state="disabled")
        elif self.usuario_actual.es_mecanico:
            self.btn_guardar.configure(state="normal")
            self.btn_actualizar.configure(state="normal")
            self.btn_eliminar.configure(state="disabled")
        elif self.usuario_actual.es_admin:
            self.btn_guardar.configure(state="normal")
            self.btn_actualizar.configure(state="normal")
            self.btn_eliminar.configure(state="normal")

    def cargar_datos(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        termino = self.entry_buscar.get()
        tipos = MantenimientoController.listar_tipos(search_term=termino, solo_activos=True)

        for t in tipos:
            km_txt = f"{t.intervalo_km:,} km" if t.intervalo_km > 0 else "-"
            dias_txt = f"{t.intervalo_dias} días" if t.intervalo_dias > 0 else "-"

            self.tree.insert("", "end", values=(
                t.id_tipo,
                t.nombre,
                km_txt,
                dias_txt,
                t.descripcion or "-"
            ))

    def al_seleccionar_fila(self, event):
        seleccion = self.tree.selection()
        if not seleccion:
            return

        item = self.tree.item(seleccion[0])
        valores = item["values"]
        self.tipo_seleccionado_id = valores[0]

        tipo = MantenimientoController.obtener_tipo(self.tipo_seleccionado_id)
        if tipo:
            self.var_nombre.set(tipo.nombre)
            self.var_km.set(str(tipo.intervalo_km))
            self.var_dias.set(str(tipo.intervalo_dias))
            self.entry_desc.delete("1.0", "end")
            self.entry_desc.insert("1.0", tipo.descripcion or "")

    def limpiar_formulario(self):
        self.tipo_seleccionado_id = None
        self.var_nombre.set("")
        self.var_km.set("")
        self.var_dias.set("")
        self.entry_desc.delete("1.0", "end")
        self.tree.selection_remove(self.tree.selection())

    def guardar(self):
        ok, nuevo_t, msg = MantenimientoController.registrar_tipo(
            nombre=self.var_nombre.get(),
            descripcion=self.entry_desc.get("1.0", "end").strip(),
            intervalo_km=self.var_km.get(),
            intervalo_dias=self.var_dias.get()
        )
        if ok:
            messagebox.showinfo("Éxito", msg)
            self.limpiar_formulario()
            self.cargar_datos()
        else:
            messagebox.showwarning("Atención", msg)

    def actualizar(self):
        if not self.tipo_seleccionado_id:
            messagebox.showwarning("Atención", "Seleccione una rutina de la lista para actualizar.")
            return

        ok, msg = MantenimientoController.actualizar_tipo(
            id_tipo=self.tipo_seleccionado_id,
            nombre=self.var_nombre.get(),
            descripcion=self.entry_desc.get("1.0", "end").strip(),
            intervalo_km=self.var_km.get(),
            intervalo_dias=self.var_dias.get()
        )
        if ok:
            messagebox.showinfo("Éxito", msg)
            self.limpiar_formulario()
            self.cargar_datos()
        else:
            messagebox.showwarning("Atención", msg)

    def eliminar(self):
        if not self.tipo_seleccionado_id:
            messagebox.showwarning("Atención", "Seleccione una rutina para dar de baja.")
            return

        if messagebox.askyesno("Confirmar Baja Lógica", "¿Está seguro de retirar esta rutina del catálogo?\nLas programaciones e historiales previos se mantendrán."):
            ok, msg = MantenimientoController.eliminar_tipo(self.tipo_seleccionado_id, logico=True)
            if ok:
                messagebox.showinfo("Baja Lógica Exitosa", msg)
                self.limpiar_formulario()
                self.cargar_datos()
            else:
                messagebox.showerror("Error", msg)
