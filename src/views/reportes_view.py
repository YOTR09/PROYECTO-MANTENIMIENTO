import os
from datetime import datetime
from tkinter import filedialog, messagebox
import customtkinter as ctk
from src.controllers.reporte_controller import ReporteController
from src.views.theme import (
    KPI_INFO_COLOR,
    KPI_INFO_HOVER,
    KPI_SUCCESS_COLOR,
    KPI_SUCCESS_HOVER,
    TEXT_MUTED
)

class ReportesView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, corner_radius=10)
        self._setup_ui()

    def _setup_ui(self):
        # Cabecera
        top_frame = ctk.CTkFrame(self, fg_color="transparent")
        top_frame.pack(fill="x", padx=20, pady=(15, 10))

        ctk.CTkLabel(
            top_frame,
            text="📑 Centro de Reportes y Exportación Ejecutiva",
            font=ctk.CTkFont(size=22, weight="bold")
        ).pack(side="left")

        ctk.CTkLabel(
            top_frame,
            text="Formatos oficiales: PDF vectorial y Excel (.xlsx) con fórmulas",
            font=ctk.CTkFont(size=12),
            text_color=TEXT_MUTED
        ).pack(side="right", padx=5)

        # Scrollable Frame para albergar las tarjetas de los 5 reportes
        scroll_container = ctk.CTkScrollableFrame(self, corner_radius=10)
        scroll_container.pack(fill="both", expand=True, padx=20, pady=10)

        reportes = [
            {
                "id": 1,
                "titulo": "Reporte 1: Ficha Técnica y Estado de Flota Vehicular",
                "formato": "PDF",
                "icono": "🚌",
                "color_badge": "#1E3A8A",
                "descripcion": "Inventario completo de unidades activas, número de unidad, placa, modelo, año, odómetro actual acumulado, socio propietario asignado y estatus operativo en ruta o taller.",
                "def_nombre": f"Ficha_Flota_Brisas_{datetime.now().strftime('%Y%m%d')}.pdf",
                "tipo_archivo": [("Archivos PDF", "*.pdf")],
                "comando": self._generar_reporte_1
            },
            {
                "id": 2,
                "titulo": "Reporte 2: Plan Preventivo y Alertas de Vencimiento",
                "formato": "PDF",
                "icono": "⚠️",
                "color_badge": "#B45309",
                "descripcion": "Tablero semaforizado de mantenimiento con diagnósticos por color (🔴 Vencido, 🟡 Por Vencer, 🟢 Al Día), proyecciones de kilometraje restante y fechas límites de servicio.",
                "def_nombre": f"Plan_Preventivo_Semaforos_{datetime.now().strftime('%Y%m%d')}.pdf",
                "tipo_archivo": [("Archivos PDF", "*.pdf")],
                "comando": self._generar_reporte_2
            },
            {
                "id": 3,
                "titulo": "Reporte 3: Bitácora Histórica y Auditoría de Costos",
                "formato": "Excel (.xlsx)",
                "icono": "📊",
                "color_badge": "#15803D",
                "descripcion": "Libro de cálculo estructurado con todos los mantenimientos ejecutados, fechas, talleres mecánicos, odómetros de intervención, detalle de trabajos y fórmulas automáticas de suma total.",
                "def_nombre": f"Bitacora_Costos_Mantenimiento_{datetime.now().strftime('%Y%m%d')}.xlsx",
                "tipo_archivo": [("Libro de Excel", "*.xlsx")],
                "comando": self._generar_reporte_3
            },
            {
                "id": 4,
                "titulo": "Reporte 4: Directorio Institucional de Socios y Propietarios",
                "formato": "PDF",
                "icono": "👥",
                "color_badge": "#1E3A8A",
                "descripcion": "Padrón institucional de afiliados, documento de identidad (Cédula/RIF), teléfonos de contacto, estado de afiliación y desglose de las unidades de transporte asignadas.",
                "def_nombre": f"Directorio_Socios_Unidades_{datetime.now().strftime('%Y%m%d')}.pdf",
                "tipo_archivo": [("Archivos PDF", "*.pdf")],
                "comando": self._generar_reporte_4
            },
            {
                "id": 5,
                "titulo": "Reporte 5: Resumen Ejecutivo y Métricas de Rendimiento",
                "formato": "Excel (.xlsx)",
                "icono": "📈",
                "color_badge": "#15803D",
                "descripcion": "Estadísticas avanzadas con consolidado de gastos acumulados por taller y proveedor mecánico, costos promedio por intervención y frecuencia de ejecución por tipo de rutina.",
                "def_nombre": f"Metricas_Talleres_Rendimiento_{datetime.now().strftime('%Y%m%d')}.xlsx",
                "tipo_archivo": [("Libro de Excel", "*.xlsx")],
                "comando": self._generar_reporte_5
            },
        ]

        for rep in reportes:
            self._crear_tarjeta_reporte(scroll_container, rep)

    def _crear_tarjeta_reporte(self, contenedor, r):
        card = ctk.CTkFrame(contenedor, corner_radius=10)
        card.pack(fill="x", pady=8, padx=5)

        # Fila superior
        header_f = ctk.CTkFrame(card, fg_color="transparent")
        header_f.pack(fill="x", padx=15, pady=(12, 4))

        lbl_tit = ctk.CTkLabel(
            header_f,
            text=f"{r['icono']} {r['titulo']}",
            font=ctk.CTkFont(size=15, weight="bold")
        )
        lbl_tit.pack(side="left")

        lbl_badge = ctk.CTkLabel(
            header_f,
            text=f" Formato: {r['formato']} ",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color=r["color_badge"],
            corner_radius=6,
            text_color="white"
        )
        lbl_badge.pack(side="right")

        # Descripción
        lbl_desc = ctk.CTkLabel(
            card,
            text=r["descripcion"],
            font=ctk.CTkFont(size=12),
            text_color="#94A3B8",
            wraplength=760,
            justify="left"
        )
        lbl_desc.pack(fill="x", padx=15, pady=(4, 12))

        # Barra de acción
        action_f = ctk.CTkFrame(card, fg_color="transparent")
        action_f.pack(fill="x", padx=15, pady=(0, 12))

        btn = ctk.CTkButton(
            action_f,
            text=f"📥 Generar y Guardar {r['formato']}",
            font=ctk.CTkFont(size=13, weight="bold"),
            width=220,
            height=36,
            command=lambda rep=r: rep["comando"](rep)
        )
        btn.pack(side="left")

    def _solicitar_ruta_guardado(self, rep):
        return filedialog.asksaveasfilename(
            title=f"Guardar {rep['titulo']}",
            initialfile=rep["def_nombre"],
            filetypes=rep["tipo_archivo"],
            defaultextension=rep["tipo_archivo"][0][1]
        )

    def _generar_reporte_1(self, rep):
        ruta = self._solicitar_ruta_guardado(rep)
        if not ruta:
            return
        ok, msg = ReporteController.generar_reporte_1_flota_pdf(ruta)
        self._mostrar_resultado(ok, msg)

    def _generar_reporte_2(self, rep):
        ruta = self._solicitar_ruta_guardado(rep)
        if not ruta:
            return
        ok, msg = ReporteController.generar_reporte_2_preventivo_pdf(ruta)
        self._mostrar_resultado(ok, msg)

    def _generar_reporte_3(self, rep):
        ruta = self._solicitar_ruta_guardado(rep)
        if not ruta:
            return
        ok, msg = ReporteController.generar_reporte_3_historial_excel(ruta)
        self._mostrar_resultado(ok, msg)

    def _generar_reporte_4(self, rep):
        ruta = self._solicitar_ruta_guardado(rep)
        if not ruta:
            return
        ok, msg = ReporteController.generar_reporte_4_socios_pdf(ruta)
        self._mostrar_resultado(ok, msg)

    def _generar_reporte_5(self, rep):
        ruta = self._solicitar_ruta_guardado(rep)
        if not ruta:
            return
        ok, msg = ReporteController.generar_reporte_5_metricas_excel(ruta)
        self._mostrar_resultado(ok, msg)

    def _mostrar_resultado(self, ok: bool, msg: str):
        if ok:
            messagebox.showinfo("Reporte Generado", msg)
        else:
            messagebox.showerror("Error al Generar Reporte", msg)
