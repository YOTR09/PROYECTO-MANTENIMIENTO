import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from datetime import date
from src.services.mantenimiento_service import MantenimientoService
from src.services.vehiculo_service import VehiculoService
from src.services.tipo_mantenimiento_service import TipoMantenimientoService

class ProgramacionMantView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, corner_radius=10)
        self.item_seleccionado_id = None
        self._setup_ui()
        self.cargar_datos()

    def _setup_ui(self):
        # Cabecera
        top_frame = ctk.CTkFrame(self, fg_color="transparent")
        top_frame.pack(fill="x", padx=20, pady=(15, 10))

        lbl_titulo = ctk.CTkLabel(
            top_frame,
            text="🛠️ Control y Semaforización de Mantenimiento Preventivo",
            font=ctk.CTkFont(size=22, weight="bold")
        )
        lbl_titulo.pack(side="left")

        # Filtro de Semáforo
        self.filtro_estado = ctk.CTkComboBox(
            top_frame,
            values=["Todos", "Vencido", "Por Vencer", "Al Día"],
            width=140,
            command=lambda v: self.cargar_datos(),
            state="readonly"
        )
        self.filtro_estado.set("Todos")
        self.filtro_estado.pack(side="right", padx=(10, 0))

        self.entry_buscar = ctk.CTkEntry(
            top_frame,
            placeholder_text="Buscar unidad, placa, rutina...",
            width=250
        )
        self.entry_buscar.pack(side="right")
        self.entry_buscar.bind("<KeyRelease>", lambda e: self.cargar_datos())

        # Barra de botones de acción
        action_bar = ctk.CTkFrame(self, fg_color="transparent")
        action_bar.pack(fill="x", padx=20, pady=(0, 10))

        btn_asignar = ctk.CTkButton(
            action_bar,
            text="➕ Programar Rutina a Unidad",
            fg_color="#10B981",
            hover_color="#059669",
            command=self.abrir_modal_programar
        )
        btn_asignar.pack(side="left", padx=(0, 10))

        btn_ejecutar = ctk.CTkButton(
            action_bar,
            text="✅ Registrar Mantenimiento Realizado",
            fg_color="#3B82F6",
            hover_color="#2563EB",
            command=self.abrir_modal_realizado
        )
        btn_ejecutar.pack(side="left", padx=(0, 10))

        btn_eliminar = ctk.CTkButton(
            action_bar,
            text="🗑️ Quitar Programación",
            fg_color="#EF4444",
            hover_color="#DC2626",
            command=self.eliminar_programacion
        )
        btn_eliminar.pack(side="left", padx=(0, 10))

        btn_refrescar = ctk.CTkButton(
            action_bar,
            text="🔄 Refrescar",
            fg_color="#6B7280",
            hover_color="#4B5563",
            width=100,
            command=self.cargar_datos
        )
        btn_refrescar.pack(side="right")

        # ---------------- TABLA DE CONTROL PREVENTIVO ----------------
        table_container = ctk.CTkFrame(self, corner_radius=10)
        table_container.pack(fill="both", expand=True, padx=20, pady=(0, 15))

        columnas = (
            "id", "unidad", "placa", "rutina", "km_actual", 
            "prox_km", "prox_fecha", "estado_badge", "detalle"
        )
        self.tree = ttk.Treeview(table_container, columns=columnas, show="headings", selectmode="browse")

        self.tree.heading("id", text="ID")
        self.tree.heading("unidad", text="Unidad")
        self.tree.heading("placa", text="Placa")
        self.tree.heading("rutina", text="Rutina Preventiva")
        self.tree.heading("km_actual", text="Odómetro Actual")
        self.tree.heading("prox_km", text="Próximo Km")
        self.tree.heading("prox_fecha", text="Próxima Fecha")
        self.tree.heading("estado_badge", text="Semáforo")
        self.tree.heading("detalle", text="Diagnóstico y Alerta")

        self.tree.column("id", width=35, anchor="center")
        self.tree.column("unidad", width=75, anchor="center")
        self.tree.column("placa", width=85, anchor="center")
        self.tree.column("rutina", width=220, anchor="w")
        self.tree.column("km_actual", width=110, anchor="e")
        self.tree.column("prox_km", width=105, anchor="e")
        self.tree.column("prox_fecha", width=100, anchor="center")
        self.tree.column("estado_badge", width=110, anchor="center")
        self.tree.column("detalle", width=240, anchor="w")

        # Configuración de tags de color para las filas
        self.tree.tag_configure("vencido", background="#FEE2E2", foreground="#991B1B")       # Rojo suave
        self.tree.tag_configure("por_vencer", background="#FEF3C7", foreground="#92400E")    # Amarillo suave
        self.tree.tag_configure("al_dia", background="#D1FAE5", foreground="#065F46")        # Verde suave

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
        estado_filtro = self.filtro_estado.get()
        programaciones = MantenimientoService.listar_programaciones(
            search_term=termino,
            estado_filtro=estado_filtro
        )

        for p in programaciones:
            tag = "al_dia"
            if p["estado"] == "Vencido":
                tag = "vencido"
            elif p["estado"] == "Por Vencer":
                tag = "por_vencer"

            prox_km_txt = f"{p['km_proximo_servicio']:,} km" if p["km_proximo_servicio"] > 0 else "N/A"
            prox_fecha_txt = p["fecha_proximo_servicio"] or "N/A"

            self.tree.insert("", "end", values=(
                p["id_programacion"],
                p["numero_unidad"],
                p["placa"],
                p["tipo_nombre"],
                f"{p['kilometraje_actual']:,} km",
                prox_km_txt,
                prox_fecha_txt,
                p["badge"],
                p["resumen_alerta"]
            ), tags=(tag,))

    def seleccionar_fila(self, event):
        seleccion = self.tree.selection()
        if seleccion:
            item = self.tree.item(seleccion[0])
            self.item_seleccionado_id = item["values"][0]

    def abrir_modal_programar(self):
        """Abre ventana modal para asociar una rutina preventiva a un vehículo"""
        modal = ctk.CTkToplevel(self)
        modal.title("Programar Rutina de Mantenimiento a Unidad")
        modal.geometry("520x460")
        modal.transient(self.winfo_toplevel())
        modal.grab_set()

        ctk.CTkLabel(
            modal,
            text="Programar Servicio Preventivo",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=(15, 10))

        # 1. Selector de Vehículo
        vehiculos = VehiculoService.listar_vehiculos()
        if not vehiculos:
            messagebox.showwarning("Atención", "No hay unidades registradas en el sistema. Registre un vehículo primero.")
            modal.destroy()
            return

        dict_veh = {f"Unidad {v['numero_unidad']} - {v['placa']} ({v['marca_modelo']})": v for v in vehiculos}
        ctk.CTkLabel(modal, text="Seleccionar Unidad / Vehículo:", anchor="w").pack(fill="x", padx=30, pady=(5, 0))
        var_veh = ctk.StringVar(value=list(dict_veh.keys())[0])
        combo_veh = ctk.CTkComboBox(modal, values=list(dict_veh.keys()), variable=var_veh, state="readonly")
        combo_veh.pack(fill="x", padx=30, pady=(0, 10))

        # 2. Selector de Rutina
        tipos = TipoMantenimientoService.listar_tipos()
        if not tipos:
            messagebox.showwarning("Atención", "No hay tipos de mantenimiento en el catálogo.")
            modal.destroy()
            return

        dict_tipos = {f"{t['nombre']} (Cada {t['intervalo_km']} km / {t['intervalo_dias']} d)": t["id_tipo"] for t in tipos}
        ctk.CTkLabel(modal, text="Seleccionar Rutina Preventiva:", anchor="w").pack(fill="x", padx=30, pady=(5, 0))
        var_tipo = ctk.StringVar(value=list(dict_tipos.keys())[0])
        combo_tipo = ctk.CTkComboBox(modal, values=list(dict_tipos.keys()), variable=var_tipo, state="readonly")
        combo_tipo.pack(fill="x", padx=30, pady=(0, 10))

        # 3. Odómetro y Fecha del Último Servicio Realizado
        row_params = ctk.CTkFrame(modal, fg_color="transparent")
        row_params.pack(fill="x", padx=30, pady=(0, 10))

        col_km = ctk.CTkFrame(row_params, fg_color="transparent")
        col_km.pack(side="left", fill="x", expand=True, padx=(0, 5))
        ctk.CTkLabel(col_km, text="Km Último Servicio:", anchor="w").pack(fill="x")
        var_km_ult = ctk.StringVar(value=str(dict_veh[var_veh.get()]["kilometraje_actual"]))
        entry_km_ult = ctk.CTkEntry(col_km, textvariable=var_km_ult)
        entry_km_ult.pack(fill="x")

        col_fecha = ctk.CTkFrame(row_params, fg_color="transparent")
        col_fecha.pack(side="right", fill="x", expand=True, padx=(5, 0))
        ctk.CTkLabel(col_fecha, text="Fecha Último Servicio (AAAA-MM-DD):", anchor="w").pack(fill="x")
        var_fecha_ult = ctk.StringVar(value=date.today().strftime("%Y-%m-%d"))
        entry_fecha_ult = ctk.CTkEntry(col_fecha, textvariable=var_fecha_ult)
        entry_fecha_ult.pack(fill="x")

        # Actualizar km cuando cambia vehículo
        def on_veh_change(choice):
            v_obj = dict_veh.get(choice)
            if v_obj:
                var_km_ult.set(str(v_obj["kilometraje_actual"]))
        combo_veh.configure(command=on_veh_change)

        # Observaciones
        ctk.CTkLabel(modal, text="Observaciones iniciales (opcional):", anchor="w").pack(fill="x", padx=30, pady=(5, 0))
        entry_obs = ctk.CTkEntry(modal, placeholder_text="Ej: Servicio de mantenimiento regular")
        entry_obs.pack(fill="x", padx=30, pady=(0, 15))

        def guardar_prog():
            v_obj = dict_veh[var_veh.get()]
            id_tipo = dict_tipos[var_tipo.get()]
            try:
                MantenimientoService.programar_mantenimiento(
                    id_vehiculo=v_obj["id_vehiculo"],
                    id_tipo=id_tipo,
                    fecha_ultimo=var_fecha_ult.get().strip(),
                    km_ultimo=var_km_ult.get().strip(),
                    observaciones=entry_obs.get().strip()
                )
                messagebox.showinfo("Éxito", "Rutina programada correctamente. Próximos servicios y semáforo calculados.")
                modal.destroy()
                self.cargar_datos()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ctk.CTkButton(modal, text="Guardar Programación", fg_color="#10B981", hover_color="#059669", command=guardar_prog).pack(fill="x", padx=30, pady=10)

    def abrir_modal_realizado(self):
        """Abre ventana modal para registrar la ejecución de un mantenimiento"""
        if not self.item_seleccionado_id:
            messagebox.showwarning("Atención", "Seleccione un mantenimiento programado de la lista para registrar su ejecución.")
            return

        item = self.tree.item(self.tree.selection()[0])
        valores = item["values"]
        id_prog = valores[0]
        unidad = valores[1]
        placa = valores[2]
        rutina = valores[3]
        km_actual_str = str(valores[4]).replace(" km", "").replace(",", "")

        # Obtener detalle de la programación
        from src.repositories.mantenimiento_repository import MantenimientoRepository
        prog_data = MantenimientoRepository.get_programacion_by_id(id_prog)
        if not prog_data:
            messagebox.showerror("Error", "No se encontró el registro seleccionado.")
            return

        modal = ctk.CTkToplevel(self)
        modal.title(f"Registrar Mantenimiento Realizado - Unidad {unidad}")
        modal.geometry("540x500")
        modal.transient(self.winfo_toplevel())
        modal.grab_set()

        ctk.CTkLabel(
            modal,
            text=f"✅ Registro de Mantenimiento Ejecutado",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=(15, 5))

        ctk.CTkLabel(
            modal,
            text=f"Unidad {unidad} ({placa}) - {rutina}",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#3B82F6"
        ).pack(pady=(0, 15))

        # Fecha y Odómetro de la intervención
        row_km_fec = ctk.CTkFrame(modal, fg_color="transparent")
        row_km_fec.pack(fill="x", padx=30, pady=(0, 10))

        col_f = ctk.CTkFrame(row_km_fec, fg_color="transparent")
        col_f.pack(side="left", fill="x", expand=True, padx=(0, 5))
        ctk.CTkLabel(col_f, text="Fecha Realizado (AAAA-MM-DD):", anchor="w").pack(fill="x")
        var_fecha_real = ctk.StringVar(value=date.today().strftime("%Y-%m-%d"))
        ctk.CTkEntry(col_f, textvariable=var_fecha_real).pack(fill="x")

        col_k = ctk.CTkFrame(row_km_fec, fg_color="transparent")
        col_k.pack(side="right", fill="x", expand=True, padx=(5, 0))
        ctk.CTkLabel(col_k, text="Odómetro al Momento (Km):", anchor="w").pack(fill="x")
        var_km_real = ctk.StringVar(value=km_actual_str)
        ctk.CTkEntry(col_k, textvariable=var_km_real).pack(fill="x")

        # Costo y Taller / Mecánico
        row_cos_tal = ctk.CTkFrame(modal, fg_color="transparent")
        row_cos_tal.pack(fill="x", padx=30, pady=(0, 10))

        col_c = ctk.CTkFrame(row_cos_tal, fg_color="transparent")
        col_c.pack(side="left", fill="x", expand=True, padx=(0, 5))
        ctk.CTkLabel(col_c, text="Costo Total ($):", anchor="w").pack(fill="x")
        var_costo = ctk.StringVar(value="0.00")
        ctk.CTkEntry(col_c, textvariable=var_costo).pack(fill="x")

        col_t = ctk.CTkFrame(row_cos_tal, fg_color="transparent")
        col_t.pack(side="right", fill="x", expand=True, padx=(5, 0))
        ctk.CTkLabel(col_t, text="Taller o Mecánico:", anchor="w").pack(fill="x")
        var_taller = ctk.StringVar()
        ctk.CTkEntry(col_t, textvariable=var_taller, placeholder_text="Ej: Taller Central").pack(fill="x")

        # Detalle o Repuestos utilizados
        ctk.CTkLabel(modal, text="Detalle de trabajos y repuestos utilizados:", anchor="w").pack(fill="x", padx=30, pady=(5, 0))
        text_desc = ctk.CTkTextbox(modal, height=80)
        text_desc.pack(fill="x", padx=30, pady=(0, 15))

        def confirmar_ejecucion():
            try:
                MantenimientoService.registrar_mantenimiento_realizado(
                    id_vehiculo=prog_data["id_vehiculo"],
                    id_tipo=prog_data["id_tipo"],
                    fecha_realizado=var_fecha_real.get().strip(),
                    km_al_momento=var_km_real.get().strip(),
                    costo=var_costo.get().strip(),
                    taller=var_taller.get().strip(),
                    descripcion=text_desc.get("1.0", tk.END).strip()
                )
                messagebox.showinfo(
                    "Éxito", 
                    f"¡Mantenimiento guardado en el historial con éxito!\n\n"
                    f"Se actualizó automáticamente el odómetro y se calculó el próximo servicio preventivo."
                )
                modal.destroy()
                self.cargar_datos()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ctk.CTkButton(
            modal,
            text="Confirmar Mantenimiento Realizado",
            fg_color="#10B981",
            hover_color="#059669",
            command=confirmar_ejecucion
        ).pack(fill="x", padx=30, pady=10)

    def eliminar_programacion(self):
        if not self.item_seleccionado_id:
            messagebox.showwarning("Atención", "Seleccione una programación para quitar.")
            return

        if messagebox.askyesno("Confirmar", "¿Desea quitar esta rutina preventiva para la unidad seleccionada? El historial pasado se conservará."):
            try:
                MantenimientoService.eliminar_programacion(self.item_seleccionado_id)
                messagebox.showinfo("Éxito", "Programación eliminada.")
                self.item_seleccionado_id = None
                self.cargar_datos()
            except Exception as e:
                messagebox.showerror("Error", str(e))

