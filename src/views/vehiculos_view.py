import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from src.services.vehiculo_service import VehiculoService
from src.services.socio_service import SocioService
from src.models.enums import EstadoVehiculo

class VehiculosView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, corner_radius=10)
        self.vehiculo_seleccionado_id = None
        self.dict_socios = {} # Mapeo "Nombre (Cédula)" -> id_socio
        self._setup_ui()
        self.cargar_socios()
        self.cargar_datos()

    def _setup_ui(self):
        # Cabecera
        top_frame = ctk.CTkFrame(self, fg_color="transparent")
        top_frame.pack(fill="x", padx=20, pady=(15, 10))

        lbl_titulo = ctk.CTkLabel(
            top_frame,
            text="🚐 Gestión de Flota y Unidades de Transporte",
            font=ctk.CTkFont(size=22, weight="bold")
        )
        lbl_titulo.pack(side="left")

        # Filtros a la derecha
        self.filtro_status = ctk.CTkComboBox(
            top_frame,
            values=["Todos", EstadoVehiculo.ACTIVO.value, EstadoVehiculo.EN_TALLER.value, EstadoVehiculo.INACTIVO.value],
            width=130,
            command=lambda v: self.cargar_datos(),
            state="readonly"
        )
        self.filtro_status.set("Todos")
        self.filtro_status.pack(side="right", padx=(10, 0))

        self.entry_buscar = ctk.CTkEntry(
            top_frame,
            placeholder_text="Buscar por unidad, placa, modelo...",
            width=260
        )
        self.entry_buscar.pack(side="right", padx=(10, 0))
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
            text="Datos de la Unidad",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        lbl_form.pack(pady=(12, 8))

        # Socio Propietario
        ctk.CTkLabel(self.form_card, text="Socio Propietario:", anchor="w").pack(fill="x", padx=20, pady=(3, 0))
        self.var_socio = tk.StringVar()
        self.combo_socios = ctk.CTkComboBox(self.form_card, variable=self.var_socio, state="readonly", values=[])
        self.combo_socios.pack(fill="x", padx=20, pady=(0, 8))

        # N° de Unidad y Placa (En dos columnas)
        row_unidad_placa = ctk.CTkFrame(self.form_card, fg_color="transparent")
        row_unidad_placa.pack(fill="x", padx=20, pady=(0, 8))

        col_u = ctk.CTkFrame(row_unidad_placa, fg_color="transparent")
        col_u.pack(side="left", fill="x", expand=True, padx=(0, 5))
        ctk.CTkLabel(col_u, text="N° de Unidad:", anchor="w").pack(fill="x")
        self.var_unidad = tk.StringVar()
        self.entry_unidad = ctk.CTkEntry(col_u, textvariable=self.var_unidad, placeholder_text="Ej: 01")
        self.entry_unidad.pack(fill="x")

        col_p = ctk.CTkFrame(row_unidad_placa, fg_color="transparent")
        col_p.pack(side="right", fill="x", expand=True, padx=(5, 0))
        ctk.CTkLabel(col_p, text="Placa:", anchor="w").pack(fill="x")
        self.var_placa = tk.StringVar()
        self.entry_placa = ctk.CTkEntry(col_p, textvariable=self.var_placa, placeholder_text="Ej: A12BC3D")
        self.entry_placa.pack(fill="x")

        # Marca y Modelo
        ctk.CTkLabel(self.form_card, text="Marca y Modelo:", anchor="w").pack(fill="x", padx=20, pady=(3, 0))
        self.var_marca = tk.StringVar()
        self.entry_marca = ctk.CTkEntry(self.form_card, textvariable=self.var_marca, placeholder_text="Ej: Encava NT-610")
        self.entry_marca.pack(fill="x", padx=20, pady=(0, 8))

        # Año y Odómetro Actual
        row_ano_km = ctk.CTkFrame(self.form_card, fg_color="transparent")
        row_ano_km.pack(fill="x", padx=20, pady=(0, 8))

        col_a = ctk.CTkFrame(row_ano_km, fg_color="transparent")
        col_a.pack(side="left", fill="x", expand=True, padx=(0, 5))
        ctk.CTkLabel(col_a, text="Año:", anchor="w").pack(fill="x")
        self.var_ano = tk.StringVar()
        self.entry_ano = ctk.CTkEntry(col_a, textvariable=self.var_ano, placeholder_text="Ej: 2015")
        self.entry_ano.pack(fill="x")

        col_k = ctk.CTkFrame(row_ano_km, fg_color="transparent")
        col_k.pack(side="right", fill="x", expand=True, padx=(5, 0))
        ctk.CTkLabel(col_k, text="Odómetro (Km):", anchor="w").pack(fill="x")
        self.var_km = tk.StringVar(value="0")
        self.entry_km = ctk.CTkEntry(col_k, textvariable=self.var_km, placeholder_text="0")
        self.entry_km.pack(fill="x")

        # Estado Operativo
        ctk.CTkLabel(self.form_card, text="Estado Operativo:", anchor="w").pack(fill="x", padx=20, pady=(3, 0))
        self.var_status = ctk.StringVar(value=EstadoVehiculo.ACTIVO.value)
        self.combo_status = ctk.CTkComboBox(self.form_card, values=[EstadoVehiculo.ACTIVO.value, EstadoVehiculo.EN_TALLER.value, EstadoVehiculo.INACTIVO.value], variable=self.var_status, state="readonly")
        self.combo_status.pack(fill="x", padx=20, pady=(0, 12))

        # Botones
        self.btn_guardar = ctk.CTkButton(self.form_card, text="➕ Guardar Unidad", fg_color="#10B981", hover_color="#059669", command=self.guardar)
        self.btn_guardar.pack(fill="x", padx=20, pady=4)

        self.btn_actualizar = ctk.CTkButton(self.form_card, text="✏️ Actualizar Unidad", fg_color="#3B82F6", hover_color="#2563EB", command=self.actualizar)
        self.btn_actualizar.pack(fill="x", padx=20, pady=4)

        self.btn_odometro = ctk.CTkButton(self.form_card, text="⚡ Actualizar Solo Odómetro", fg_color="#F59E0B", hover_color="#D97706", command=self.actualizar_solo_odometro)
        self.btn_odometro.pack(fill="x", padx=20, pady=4)

        self.btn_limpiar = ctk.CTkButton(self.form_card, text="🧹 Limpiar Campos", fg_color="#6B7280", hover_color="#4B5563", command=self.limpiar_formulario)
        self.btn_limpiar.pack(fill="x", padx=20, pady=4)

        self.btn_eliminar = ctk.CTkButton(self.form_card, text="🗑️ Eliminar Unidad", fg_color="#EF4444", hover_color="#DC2626", command=self.eliminar)
        self.btn_eliminar.pack(fill="x", padx=20, pady=(4, 10))

        # ---------------- TABLA DE DATOS ----------------
        table_container = ctk.CTkFrame(content_frame, corner_radius=10)
        table_container.pack(side="right", fill="both", expand=True, pady=5)

        columnas = ("id", "unidad", "placa", "marca", "ano", "km", "status", "socio")
        self.tree = ttk.Treeview(table_container, columns=columnas, show="headings", selectmode="browse")

        self.tree.heading("id", text="ID")
        self.tree.heading("unidad", text="Unidad")
        self.tree.heading("placa", text="Placa")
        self.tree.heading("marca", text="Marca / Modelo")
        self.tree.heading("ano", text="Año")
        self.tree.heading("km", text="Odómetro Actual")
        self.tree.heading("status", text="Estado")
        self.tree.heading("socio", text="Propietario")

        self.tree.column("id", width=40, anchor="center")
        self.tree.column("unidad", width=80, anchor="center")
        self.tree.column("placa", width=90, anchor="center")
        self.tree.column("marca", width=160, anchor="w")
        self.tree.column("ano", width=60, anchor="center")
        self.tree.column("km", width=120, anchor="e")
        self.tree.column("status", width=90, anchor="center")
        self.tree.column("socio", width=180, anchor="w")

        # Scrollbars
        scroll_y = ttk.Scrollbar(table_container, orient="vertical", command=self.tree.yview)
        scroll_x = ttk.Scrollbar(table_container, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")
        self.tree.pack(fill="both", expand=True, padx=5, pady=5)

        self.tree.bind("<<TreeviewSelect>>", self.seleccionar_fila)

    def cargar_socios(self):
        socios = SocioService.listar_socios()
        self.dict_socios.clear()
        opciones = []
        for s in socios:
            etiqueta = f"{s['nombre_completo']} ({s['cedula']})"
            self.dict_socios[etiqueta] = s["id_socio"]
            opciones.append(etiqueta)

        if opciones:
            self.combo_socios.configure(values=opciones)
            self.combo_socios.set(opciones[0])
        else:
            self.combo_socios.configure(values=["No hay socios registrados"])
            self.combo_socios.set("No hay socios registrados")

    def cargar_datos(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        termino = self.entry_buscar.get()
        status_filtro = self.filtro_status.get()
        vehiculos = VehiculoService.listar_vehiculos(termino, status_filtro)

        for v in vehiculos:
            self.tree.insert("", "end", values=(
                v["id_vehiculo"],
                v["numero_unidad"],
                v["placa"],
                v["marca_modelo"],
                v["ano"] or "-",
                f"{v['kilometraje_actual']:,} km",
                v["status"],
                v["socio_nombre"]
            ))

    def seleccionar_fila(self, event):
        seleccion = self.tree.selection()
        if seleccion:
            item = self.tree.item(seleccion[0])
            valores = item["values"]
            self.vehiculo_seleccionado_id = valores[0]
            self.var_unidad.set(valores[1])
            self.var_placa.set(valores[2])
            self.var_marca.set(valores[3])
            self.var_ano.set("" if valores[4] == "-" else str(valores[4]))
            
            # Limpiar formato de km (ej: '100,000 km' -> '100000')
            km_str = str(valores[5]).replace(" km", "").replace(",", "").replace(".", "")
            self.var_km.set(km_str)
            self.var_status.set(valores[6])

            # Buscar socio en el combo
            socio_nombre = valores[7]
            for etiqueta, id_s in self.dict_socios.items():
                if socio_nombre in etiqueta:
                    self.var_socio.set(etiqueta)
                    break

    def guardar(self):
        socio_etiqueta = self.var_socio.get()
        id_socio = self.dict_socios.get(socio_etiqueta)
        if not id_socio:
            messagebox.showerror("Error", "Debe seleccionar un socio propietario válido.")
            return

        try:
            VehiculoService.registrar_vehiculo(
                id_socio=id_socio,
                numero_unidad=self.var_unidad.get(),
                placa=self.var_placa.get(),
                marca_modelo=self.var_marca.get(),
                ano=self.var_ano.get() if self.var_ano.get().strip() else None,
                kilometraje_actual=self.var_km.get(),
                status=self.var_status.get()
            )
            messagebox.showinfo("Éxito", "Unidad registrada correctamente.")
            self.limpiar_formulario()
            self.cargar_datos()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def actualizar(self):
        if not self.vehiculo_seleccionado_id:
            messagebox.showwarning("Atención", "Seleccione una unidad de la lista para actualizar.")
            return

        socio_etiqueta = self.var_socio.get()
        id_socio = self.dict_socios.get(socio_etiqueta)
        if not id_socio:
            messagebox.showerror("Error", "Seleccione un socio válido.")
            return

        try:
            VehiculoService.actualizar_vehiculo(
                id_vehiculo=self.vehiculo_seleccionado_id,
                id_socio=id_socio,
                numero_unidad=self.var_unidad.get(),
                placa=self.var_placa.get(),
                marca_modelo=self.var_marca.get(),
                ano=self.var_ano.get() if self.var_ano.get().strip() else None,
                kilometraje_actual=self.var_km.get(),
                status=self.var_status.get()
            )
            messagebox.showinfo("Éxito", "Datos de la unidad actualizados.")
            self.limpiar_formulario()
            self.cargar_datos()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def actualizar_solo_odometro(self):
        if not self.vehiculo_seleccionado_id:
            messagebox.showwarning("Atención", "Seleccione una unidad para actualizar su odómetro.")
            return

        dialogo = ctk.CTkInputDialog(
            text=f"Ingrese el nuevo kilometraje para la Unidad {self.var_unidad.get()} (Placa: {self.var_placa.get()}):",
            title="Actualización Rápida de Odómetro"
        )
        nuevo_km_str = dialogo.get_input()
        if nuevo_km_str is not None and nuevo_km_str.strip():
            try:
                VehiculoService.actualizar_kilometraje(self.vehiculo_seleccionado_id, nuevo_km_str.strip())
                messagebox.showinfo("Éxito", "Odómetro actualizado. Los estados de mantenimiento preventivo se han recalculado.")
                self.limpiar_formulario()
                self.cargar_datos()
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def eliminar(self):
        if not self.vehiculo_seleccionado_id:
            messagebox.showwarning("Atención", "Seleccione una unidad para eliminar.")
            return

        if messagebox.askyesno("Confirmar", f"¿Está seguro de eliminar la Unidad {self.var_unidad.get()} ({self.var_placa.get()})? Se eliminará también su plan de mantenimientos."):
            try:
                VehiculoService.eliminar_vehiculo(self.vehiculo_seleccionado_id)
                messagebox.showinfo("Éxito", "Unidad eliminada.")
                self.limpiar_formulario()
                self.cargar_datos()
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def limpiar_formulario(self):
        self.vehiculo_seleccionado_id = None
        self.var_unidad.set("")
        self.var_placa.set("")
        self.var_marca.set("")
        self.var_ano.set("")
        self.var_km.set("0")
        self.var_status.set("Activo")
        self.var_status.set(EstadoVehiculo.ACTIVO.value)
        if self.tree.selection():
            self.tree.selection_remove(self.tree.selection())

