import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from src.services.socio_service import SocioService

class SociosView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, corner_radius=10)
        self.socio_seleccionado_id = None
        self._setup_ui()
        self.cargar_datos()

    def _setup_ui(self):
        # Título y barra superior
        top_frame = ctk.CTkFrame(self, fg_color="transparent")
        top_frame.pack(fill="x", padx=20, pady=(15, 10))

        lbl_titulo = ctk.CTkLabel(
            top_frame,
            text="👥 Gestión de Socios y Afiliados",
            font=ctk.CTkFont(size=22, weight="bold")
        )
        lbl_titulo.pack(side="left")

        # Barra de búsqueda
        self.entry_buscar = ctk.CTkEntry(
            top_frame,
            placeholder_text="Buscar por cédula o nombre...",
            width=260
        )
        self.entry_buscar.pack(side="right", padx=(10, 0))
        self.entry_buscar.bind("<KeyRelease>", lambda e: self.cargar_datos())

        btn_buscar = ctk.CTkButton(
            top_frame,
            text="Buscar",
            width=80,
            command=self.cargar_datos
        )
        btn_buscar.pack(side="right")

        # Contenedor principal (Formulario a la izquierda / Tabla a la derecha)
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # ---------------- FORMULARIO ----------------
        self.form_card = ctk.CTkFrame(content_frame, width=320, corner_radius=10)
        self.form_card.pack(side="left", fill="y", padx=(0, 15), pady=5)
        self.form_card.pack_propagate(False)

        lbl_form = ctk.CTkLabel(
            self.form_card,
            text="Datos del Socio",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        lbl_form.pack(pady=(15, 10))

        # Cédula
        ctk.CTkLabel(self.form_card, text="Cédula / Documento:", anchor="w").pack(fill="x", padx=20, pady=(5, 0))
        self.var_cedula = tk.StringVar()
        self.entry_cedula = ctk.CTkEntry(self.form_card, textvariable=self.var_cedula, placeholder_text="Ej: V-12345678")
        self.entry_cedula.pack(fill="x", padx=20, pady=(0, 10))

        # Nombre Completo
        ctk.CTkLabel(self.form_card, text="Nombre Completo:", anchor="w").pack(fill="x", padx=20, pady=(5, 0))
        self.var_nombre = tk.StringVar()
        self.entry_nombre = ctk.CTkEntry(self.form_card, textvariable=self.var_nombre, placeholder_text="Ej: Juan Perez")
        self.entry_nombre.pack(fill="x", padx=20, pady=(0, 10))

        # Teléfono
        ctk.CTkLabel(self.form_card, text="Teléfono:", anchor="w").pack(fill="x", padx=20, pady=(5, 0))
        self.var_telefono = tk.StringVar()
        self.entry_telefono = ctk.CTkEntry(self.form_card, textvariable=self.var_telefono, placeholder_text="Ej: 0414-1234567")
        self.entry_telefono.pack(fill="x", padx=20, pady=(0, 10))

        # Estado
        ctk.CTkLabel(self.form_card, text="Estado:", anchor="w").pack(fill="x", padx=20, pady=(5, 0))
        self.var_estado = ctk.StringVar(value="Activo")
        self.combo_estado = ctk.CTkComboBox(self.form_card, values=["Activo", "Inactivo"], variable=self.var_estado, state="readonly")
        self.combo_estado.pack(fill="x", padx=20, pady=(0, 15))

        # Botones de Acción
        self.btn_guardar = ctk.CTkButton(self.form_card, text="➕ Guardar Socio", fg_color="#10B981", hover_color="#059669", command=self.guardar)
        self.btn_guardar.pack(fill="x", padx=20, pady=5)

        self.btn_actualizar = ctk.CTkButton(self.form_card, text="✏️ Actualizar", fg_color="#3B82F6", hover_color="#2563EB", command=self.actualizar)
        self.btn_actualizar.pack(fill="x", padx=20, pady=5)

        self.btn_limpiar = ctk.CTkButton(self.form_card, text="🧹 Limpiar Campos", fg_color="#6B7280", hover_color="#4B5563", command=self.limpiar_formulario)
        self.btn_limpiar.pack(fill="x", padx=20, pady=5)

        self.btn_eliminar = ctk.CTkButton(self.form_card, text="🗑️ Eliminar", fg_color="#EF4444", hover_color="#DC2626", command=self.eliminar)
        self.btn_eliminar.pack(fill="x", padx=20, pady=(5, 15))

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
        self.tree.column("estado", width=90, anchor="center")

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
        socios = SocioService.listar_socios(termino)
        for s in socios:
            self.tree.insert("", "end", values=(
                s["id_socio"],
                s["cedula"],
                s["nombre_completo"],
                s["telefono"],
                s["estado"]
            ))

    def seleccionar_fila(self, event):
        seleccion = self.tree.selection()
        if seleccion:
            item = self.tree.item(seleccion[0])
            valores = item["values"]
            self.socio_seleccionado_id = valores[0]
            self.var_cedula.set(valores[1])
            self.var_nombre.set(valores[2])
            self.var_telefono.set(valores[3])
            self.var_estado.set(valores[4])

    def guardar(self):
        try:
            SocioService.registrar_socio(
                cedula=self.var_cedula.get(),
                nombre_completo=self.var_nombre.get(),
                telefono=self.var_telefono.get(),
                estado=self.var_estado.get()
            )
            messagebox.showinfo("Éxito", "Socio registrado correctamente.")
            self.limpiar_formulario()
            self.cargar_datos()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def actualizar(self):
        if not self.socio_seleccionado_id:
            messagebox.showwarning("Atención", "Seleccione un socio de la lista para actualizar.")
            return

        try:
            SocioService.actualizar_socio(
                id_socio=self.socio_seleccionado_id,
                cedula=self.var_cedula.get(),
                nombre_completo=self.var_nombre.get(),
                telefono=self.var_telefono.get(),
                estado=self.var_estado.get()
            )
            messagebox.showinfo("Éxito", "Datos del socio actualizados.")
            self.limpiar_formulario()
            self.cargar_datos()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def eliminar(self):
        if not self.socio_seleccionado_id:
            messagebox.showwarning("Atención", "Seleccione un socio de la lista para eliminar.")
            return

        if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar al socio seleccionado?"):
            try:
                SocioService.eliminar_socio(self.socio_seleccionado_id)
                messagebox.showinfo("Éxito", "Socio eliminado satisfactoriamente.")
                self.limpiar_formulario()
                self.cargar_datos()
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def limpiar_formulario(self):
        self.socio_seleccionado_id = None
        self.var_cedula.set("")
        self.var_nombre.set("")
        self.var_telefono.set("")
        self.var_estado.set("Activo")
        if self.tree.selection():
            self.tree.selection_remove(self.tree.selection())

