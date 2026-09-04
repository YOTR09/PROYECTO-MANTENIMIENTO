import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from src.services.mantenimiento_service import MantenimientoService

class HistorialMantView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, corner_radius=10)
        self._setup_ui()
        self.cargar_datos()

    def _setup_ui(self):
        # Cabecera
        top_frame = ctk.CTkFrame(self, fg_color="transparent")
        top_frame.pack(fill="x", padx=20, pady=(15, 10))

        lbl_titulo = ctk.CTkLabel(
            top_frame,
            text="📜 Bitácora e Historial de Mantenimientos Realizados",
            font=ctk.CTkFont(size=22, weight="bold")
        )
        lbl_titulo.pack(side="left")

        # Barra de búsqueda
        self.entry_buscar = ctk.CTkEntry(
            top_frame,
            placeholder_text="Buscar por unidad, placa, taller o rutina...",
            width=300
        )
        self.entry_buscar.pack(side="right")
        self.entry_buscar.bind("<KeyRelease>", lambda e: self.cargar_datos())

        # Contenedor de la tabla
        table_container = ctk.CTkFrame(self, corner_radius=10)
        table_container.pack(fill="both", expand=True, padx=20, pady=10)

        columnas = ("id", "fecha", "unidad", "placa", "rutina", "km", "costo", "taller", "detalle")
        self.tree = ttk.Treeview(table_container, columns=columnas, show="headings", selectmode="browse")

        self.tree.heading("id", text="ID")
        self.tree.heading("fecha", text="Fecha Realizado")
        self.tree.heading("unidad", text="Unidad")
        self.tree.heading("placa", text="Placa")
        self.tree.heading("rutina", text="Rutina Ejecutada")
        self.tree.heading("km", text="Odómetro al Servicio")
        self.tree.heading("costo", text="Costo ($)")
        self.tree.heading("taller", text="Taller / Mecánico")
        self.tree.heading("detalle", text="Detalle de Trabajos")

        self.tree.column("id", width=40, anchor="center")
        self.tree.column("fecha", width=110, anchor="center")
        self.tree.column("unidad", width=75, anchor="center")
        self.tree.column("placa", width=85, anchor="center")
        self.tree.column("rutina", width=200, anchor="w")
        self.tree.column("km", width=130, anchor="e")
        self.tree.column("costo", width=90, anchor="e")
        self.tree.column("taller", width=140, anchor="w")
        self.tree.column("detalle", width=250, anchor="w")

        # Scrollbars
        scroll_y = ttk.Scrollbar(table_container, orient="vertical", command=self.tree.yview)
        scroll_x = ttk.Scrollbar(table_container, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")
        self.tree.pack(fill="both", expand=True, padx=5, pady=5)

    def cargar_datos(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        termino = self.entry_buscar.get()
        historial = MantenimientoService.listar_historial(search_term=termino)

        for h in historial:
            costo_txt = f"${h['costo']:,.2f}" if h['costo'] else "$0.00"
            self.tree.insert("", "end", values=(
                h["id_historial"],
                h["fecha_realizado"],
                h["numero_unidad"],
                h["placa"],
                h["tipo_nombre"],
                f"{h['km_al_momento']:,} km",
                costo_txt,
                h["taller_mecanico"] or "-",
                h["descripcion_trabajo"] or "-"
            ))

