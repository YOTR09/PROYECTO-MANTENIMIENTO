import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from src.services.tipo_mantenimiento_service import TipoMantenimientoService

class TiposMantView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, corner_radius=10)
        self.tipo_seleccionado_id = None
        self._setup_ui()
        self.cargar_datos()

    def _setup_ui(self):
        # Cabecera
        top_frame = ctk.CTkFrame(self, fg_color="transparent")
        top_frame.pack(fill="x", padx=20, pady=(15, 10))

        lbl_titulo = ctk.CTkLabel(
            top_frame,
            text="📋 Catálogo de Mantenimientos Preventivos (CRUD)",
            font=ctk.CTkFont(size=22, weight="bold")
        )
        lbl_titulo.pack(side="left")

        # Barra de búsqueda
        self.entry_buscar = ctk.CTkEntry(
            top_frame,
            placeholder_text="Buscar mantenimiento...",
            width=260
        )
        self.entry_buscar.pack(side="right")
        self.entry_buscar.bind("<KeyRelease>", lambda e: self.cargar_datos())

        # Contenedor principal
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # ---------------- FORMULARIO ----------------
        self.form_card = ctk.CTkFrame(content_frame, width=330, corner_radius=10)
        self.form_card.pack(side="left", fill="y", padx=(0, 15), pady=5)
        self.form_card.pack_propagate(False)

        lbl_form = ctk.CTkLabel(
            self.form_card,
            text="Datos de la Rutina",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        lbl_form.pack(pady=(15, 10))

        # Nombre
        ctk.CTkLabel(self.form_card, text="Nombre del Mantenimiento:", anchor="w").pack(fill="x", padx=20, pady=(5, 0))
        self.var_nombre = tk.StringVar()
        self.entry_nombre = ctk.CTkEntry(self.form_card, textvariable=self.var_nombre, placeholder_text="Ej: Cambio de Aceite y Filtro")
        self.entry_nombre.pack(fill="x", padx=20, pady=(0, 10))

        # Intervalos (Km y Días)
        row_intervalos = ctk.CTkFrame(self.form_card, fg_color="transparent")
        row_intervalos.pack(fill="x", padx=20, pady=(0, 10))

        col_km = ctk.CTkFrame(row_intervalos, fg_color="transparent")
        col_km.pack(side="left", fill="x", expand=True, padx=(0, 5))
        ctk.CTkLabel(col_km, text="Cada cuántos Km:", anchor="w").pack(fill="x")
        self.var_km = tk.StringVar(value="5000")
        self.entry_km = ctk.CTkEntry(col_km, textvariable=self.var_km, placeholder_text="0 si no aplica")
        self.entry_km.pack(fill="x")

        col_dias = ctk.CTkFrame(row_intervalos, fg_color="transparent")
        col_dias.pack(side="right", fill="x", expand=True, padx=(5, 0))
        ctk.CTkLabel(col_dias, text="Cada cuántos Días:", anchor="w").pack(fill="x")
        self.var_dias = tk.StringVar(value="60")
        self.entry_dias = ctk.CTkEntry(col_dias, textvariable=self.var_dias, placeholder_text="0 si no aplica")
        self.entry_dias.pack(fill="x")

        # Descripción
        ctk.CTkLabel(self.form_card, text="Descripción y Procedimiento:", anchor="w").pack(fill="x", padx=20, pady=(5, 0))
        self.text_descripcion = ctk.CTkTextbox(self.form_card, height=100)
        self.text_descripcion.pack(fill="x", padx=20, pady=(0, 15))

        # Botones
        self.btn_guardar = ctk.CTkButton(self.form_card, text="➕ Guardar Rutina", fg_color="#10B981", hover_color="#059669", command=self.guardar)
        self.btn_guardar.pack(fill="x", padx=20, pady=5)

        self.btn_actualizar = ctk.CTkButton(self.form_card, text="✏️ Actualizar Rutina", fg_color="#3B82F6", hover_color="#2563EB", command=self.actualizar)
        self.btn_actualizar.pack(fill="x", padx=20, pady=5)

        self.btn_limpiar = ctk.CTkButton(self.form_card, text="🧹 Limpiar Campos", fg_color="#6B7280", hover_color="#4B5563", command=self.limpiar_formulario)
        self.btn_limpiar.pack(fill="x", padx=20, pady=5)

        self.btn_eliminar = ctk.CTkButton(self.form_card, text="🗑️ Eliminar Rutina", fg_color="#EF4444", hover_color="#DC2626", command=self.eliminar)
        self.btn_eliminar.pack(fill="x", padx=20, pady=(5, 15))

        # ---------------- TABLA DE DATOS ----------------
        table_container = ctk.CTkFrame(content_frame, corner_radius=10)
        table_container.pack(side="right", fill="both", expand=True, pady=5)

        columnas = ("id", "nombre", "km", "dias", "descripcion")
        self.tree = ttk.Treeview(table_container, columns=columnas, show="headings", selectmode="browse")

        self.tree.heading("id", text="ID")
        self.tree.heading("nombre", text="Nombre de la Rutina")
        self.tree.heading("km", text="Frecuencia Km")
        self.tree.heading("dias", text="Frecuencia Días")
        self.tree.heading("descripcion", text="Descripción Operativa")

        self.tree.column("id", width=40, anchor="center")
        self.tree.column("nombre", width=230, anchor="w")
        self.tree.column("km", width=110, anchor="center")
        self.tree.column("dias", width=110, anchor="center")
        self.tree.column("descripcion", width=300, anchor="w")

        # Scrollbars
        scroll_y = ttk.Scrollbar(table_container, orient="vertical", command=self.tree.yview)
        scroll_x = ttk.Scrollbar(table_container, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")
        self.tree.pack(fill="both", expand=True, padx=5, pady=5)

        self.tree.bind("<<TreeviewSelect>>", self.seleccionar_fila)

    def cargar_datos(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        termino = self.entry_buscar.get()
        tipos = TipoMantenimientoService.listar_tipos(termino)

        for t in tipos:
            km_txt = f"{t['intervalo_km']:,} km" if t["intervalo_km"] > 0 else "N/A"
            dias_txt = f"{t['intervalo_dias']} días" if t["intervalo_dias"] > 0 else "N/A"
            self.tree.insert("", "end", values=(
                t["id_tipo"],
                t["nombre"],
                km_txt,
                dias_txt,
                t["descripcion"]
            ))

    def seleccionar_fila(self, event):
        seleccion = self.tree.selection()
        if seleccion:
            item = self.tree.item(seleccion[0])
            valores = item["values"]
            self.tipo_seleccionado_id = valores[0]
            self.var_nombre.set(valores[1])

            km_val = str(valores[2]).replace(" km", "").replace(",", "").replace("N/A", "0")
            dias_val = str(valores[3]).replace(" días", "").replace("N/A", "0")
            self.var_km.set(km_val)
            self.var_dias.set(dias_val)

            self.text_descripcion.delete("1.0", tk.END)
            self.text_descripcion.insert("1.0", valores[4])

    def guardar(self):
        try:
            TipoMantenimientoService.registrar_tipo(
                nombre=self.var_nombre.get(),
                descripcion=self.text_descripcion.get("1.0", tk.END).strip(),
                intervalo_km=self.var_km.get(),
                intervalo_dias=self.var_dias.get()
            )
            messagebox.showinfo("Éxito", "Rutina preventiva agregada al catálogo.")
            self.limpiar_formulario()
            self.cargar_datos()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def actualizar(self):
        if not self.tipo_seleccionado_id:
            messagebox.showwarning("Atención", "Seleccione una rutina del catálogo para actualizar.")
            return

        try:
            TipoMantenimientoService.actualizar_tipo(
                id_tipo=self.tipo_seleccionado_id,
                nombre=self.var_nombre.get(),
                descripcion=self.text_descripcion.get("1.0", tk.END).strip(),
                intervalo_km=self.var_km.get(),
                intervalo_dias=self.var_dias.get()
            )
            messagebox.showinfo("Éxito", "Rutina preventiva actualizada.")
            self.limpiar_formulario()
            self.cargar_datos()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def eliminar(self):
        if not self.tipo_seleccionado_id:
            messagebox.showwarning("Atención", "Seleccione una rutina para eliminar.")
            return

        if messagebox.askyesno("Confirmar", f"¿Eliminar la rutina '{self.var_nombre.get()}'? Si hay mantenimientos programados con esta rutina, podrían verse afectados."):
            try:
                TipoMantenimientoService.eliminar_tipo(self.tipo_seleccionado_id)
                messagebox.showinfo("Éxito", "Rutina eliminada del catálogo.")
                self.limpiar_formulario()
                self.cargar_datos()
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def limpiar_formulario(self):
        self.tipo_seleccionado_id = None
        self.var_nombre.set("")
        self.var_km.set("5000")
        self.var_dias.set("60")
        self.text_descripcion.delete("1.0", tk.END)
        if self.tree.selection():
            self.tree.selection_remove(self.tree.selection())

