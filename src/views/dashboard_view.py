import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from src.controllers.mantenimiento_controller import MantenimientoController
from src.views.theme import (
    KPI_INFO_COLOR,
    KPI_INFO_HOVER,
    KPI_DANGER_COLOR,
    KPI_WARNING_COLOR,
    KPI_SUCCESS_COLOR,
    BTN_ACCENT_COLOR,
    BTN_ACCENT_HOVER,
    TEXT_MUTED,
    TEXT_SECONDARY,
    configurar_tags_semaforo,
)

class DashboardView(ctk.CTkFrame):
    def __init__(self, parent, on_navigate=None):
        super().__init__(parent, corner_radius=10)
        self.on_navigate = on_navigate
        self._setup_ui()
        self.actualizar_dashboard()

    def _setup_ui(self):
        # Cabecera
        top_frame = ctk.CTkFrame(self, fg_color="transparent")
        top_frame.pack(fill="x", padx=20, pady=(15, 10))

        lbl_titulo = ctk.CTkLabel(
            top_frame,
            text="📊 Panel de Control y Estado de Flota",
            font=ctk.CTkFont(size=22, weight="bold")
        )
        lbl_titulo.pack(side="left")

        btn_refrescar = ctk.CTkButton(
            top_frame,
            text="🔄 Actualizar Panel",
            fg_color=KPI_INFO_COLOR,
            hover_color=KPI_INFO_HOVER,
            width=140,
            command=self.actualizar_dashboard
        )
        btn_refrescar.pack(side="right")

        # ---------------- TARJETAS RESUMEN (KPIs) ----------------
        cards_frame = ctk.CTkFrame(self, fg_color="transparent")
        cards_frame.pack(fill="x", padx=20, pady=(0, 15))

        # Tarjeta 1: Total Unidades
        self.card_unidades = self._crear_kpi_card(
            cards_frame,
            titulo="UNIDADES ACTIVAS",
            valor="0",
            subtitulo="0 unidades en total",
            color_borde=KPI_INFO_COLOR
        )
        self.card_unidades.pack(side="left", fill="both", expand=True, padx=(0, 10))

        # Tarjeta 2: Vencidos
        self.card_vencidos = self._crear_kpi_card(
            cards_frame,
            titulo="MANTENIMIENTOS VENCIDOS",
            valor="0",
            subtitulo="Requieren atención urgente",
            color_borde=KPI_DANGER_COLOR
        )
        self.card_vencidos.pack(side="left", fill="both", expand=True, padx=5)

        # Tarjeta 3: Por Vencer
        self.card_por_vencer = self._crear_kpi_card(
            cards_frame,
            titulo="PRÓXIMOS POR VENCER",
            valor="0",
            subtitulo="Próximos 500 km o 10 días",
            color_borde=KPI_WARNING_COLOR
        )
        self.card_por_vencer.pack(side="left", fill="both", expand=True, padx=5)

        # Tarjeta 4: Al Día
        self.card_al_dia = self._crear_kpi_card(
            cards_frame,
            titulo="AL DÍA / ÓPTIMOS",
            valor="0",
            subtitulo="Dentro de rango seguro",
            color_borde=KPI_SUCCESS_COLOR
        )
        self.card_al_dia.pack(side="left", fill="both", expand=True, padx=(10, 0))

        # ---------------- SECCIÓN ALERTAS URGENTES ----------------
        alertas_container = ctk.CTkFrame(self, corner_radius=10)
        alertas_container.pack(fill="both", expand=True, padx=20, pady=(0, 15))

        header_alertas = ctk.CTkFrame(alertas_container, fg_color="transparent")
        header_alertas.pack(fill="x", padx=15, pady=10)

        ctk.CTkLabel(
            header_alertas,
            text="⚠️ Alertas Críticas y Próximos Vencimientos",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(side="left")

        if self.on_navigate:
            btn_ir_preventivo = ctk.CTkButton(
                header_alertas,
                text="Ver Todo el Tablero Preventivo ➔",
                fg_color="transparent",
                text_color=BTN_ACCENT_COLOR,
                hover_color=("gray85", "gray25"),
                command=lambda: self.on_navigate("preventivo")
            )
            btn_ir_preventivo.pack(side="right")

        columnas = ("unidad", "placa", "rutina", "km_actual", "prox_km", "prox_fecha", "alerta")
        self.tree = ttk.Treeview(alertas_container, columns=columnas, show="headings", height=8, selectmode="browse")

        self.tree.heading("unidad", text="Unidad")
        self.tree.heading("placa", text="Placa")
        self.tree.heading("rutina", text="Rutina")
        self.tree.heading("km_actual", text="Odómetro Actual")
        self.tree.heading("prox_km", text="Próximo Servicio (Km)")
        self.tree.heading("prox_fecha", text="Fecha Límite")
        self.tree.heading("alerta", text="Estado de Alerta")

        self.tree.column("unidad", width=75, anchor="center")
        self.tree.column("placa", width=85, anchor="center")
        self.tree.column("rutina", width=220, anchor="w")
        self.tree.column("km_actual", width=120, anchor="e")
        self.tree.column("prox_km", width=130, anchor="e")
        self.tree.column("prox_fecha", width=105, anchor="center")
        self.tree.column("alerta", width=220, anchor="w")

        configurar_tags_semaforo(self.tree)

        scroll_y = ttk.Scrollbar(alertas_container, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll_y.set)
        scroll_y.pack(side="right", fill="y", padx=(0, 10), pady=(0, 10))
        self.tree.pack(fill="both", expand=True, padx=(15, 0), pady=(0, 10))

    def _crear_kpi_card(self, parent, titulo, valor, subtitulo, color_borde):
        card = ctk.CTkFrame(parent, corner_radius=10, border_width=2, border_color=color_borde)
        
        lbl_tit = ctk.CTkLabel(card, text=titulo, font=ctk.CTkFont(size=12, weight="bold"), text_color=TEXT_MUTED)
        lbl_tit.pack(pady=(12, 2))

        lbl_val = ctk.CTkLabel(card, text=valor, font=ctk.CTkFont(size=28, weight="bold"))
        lbl_val.pack(pady=(0, 2))

        lbl_sub = ctk.CTkLabel(card, text=subtitulo, font=ctk.CTkFont(size=11), text_color=TEXT_SECONDARY)
        lbl_sub.pack(pady=(0, 12))

        card.lbl_val = lbl_val
        card.lbl_sub = lbl_sub
        return card

    def actualizar_dashboard(self):
        resumen = MantenimientoController.obtener_resumen_dashboard()

        # Actualizar KPIs
        self.card_unidades.lbl_val.configure(text=f"{resumen['vehiculos_activos']}")
        self.card_unidades.lbl_sub.configure(text=f"Total: {resumen['total_vehiculos']} | Taller: {resumen['vehiculos_en_taller']}")

        self.card_vencidos.lbl_val.configure(text=f"{resumen['mantenimientos_vencidos']}")
        self.card_por_vencer.lbl_val.configure(text=f"{resumen['mantenimientos_por_vencer']}")
        self.card_al_dia.lbl_val.configure(text=f"{resumen['mantenimientos_al_dia']}")

        # Actualizar tabla de alertas críticas
        for item in self.tree.get_children():
            self.tree.delete(item)

        alertas = resumen["alertas_urgentes"]
        for a in alertas:
            tag = "vencido" if a.estado_alerta == "Vencido" else "por_vencer"
            prox_km = f"{a.km_proximo_servicio:,} km" if a.km_proximo_servicio > 0 else "N/A"
            prox_fec = a.fecha_proximo_servicio or "N/A"

            self.tree.insert("", "end", values=(
                a.numero_unidad,
                a.placa,
                a.tipo_nombre,
                f"{a.kilometraje_actual:,} km",
                prox_km,
                prox_fec,
                f"{a.badge_alerta} - {a.observaciones or 'Atención requerida'}"
            ), tags=(tag,))

