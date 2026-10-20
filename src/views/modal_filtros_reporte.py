import calendar
from datetime import date
from tkinter import messagebox
import customtkinter as ctk
from src.controllers.reporte_controller import ReporteController
from src.views.theme import (
    BTN_PRIMARY_COLOR,
    BTN_PRIMARY_HOVER,
    BTN_NEUTRAL_COLOR,
    BTN_NEUTRAL_HOVER,
    TEXT_MUTED,
)

ESTATUS_VEHICULO = ["Todos", "Activo", "En Taller", "Inactivo"]
SEMAFOROS = ["Todos", "Vencido", "Por Vencer", "Al Día", "Críticos"]
ESTADOS_SOCIO = ["Todos", "Activo", "Inactivo"]
TENENCIA = ["Todos", "Con unidades", "Sin unidades"]

# Definición declarativa de los campos de filtro por reporte.
# tipo: combo (catálogo/lista fija) | entry (texto/número) | fecha
CAMPOS_POR_REPORTE = {
    1: [
        ("status", "Estatus operativo", "combo", "estatus"),
        ("id_socio", "Socio propietario", "combo", "socios"),
        ("km_min", "Odómetro mínimo (km)", "entry", None),
        ("km_max", "Odómetro máximo (km)", "entry", None),
    ],
    2: [
        ("estado_alerta", "Nivel de semáforo", "combo", "semaforos"),
        ("id_vehiculo", "Unidad / vehículo", "combo", "vehiculos"),
        ("id_tipo", "Rutina de mantenimiento", "combo", "tipos"),
        ("fecha_desde", "Próx. fecha desde (AAAA-MM-DD)", "fecha", None),
        ("fecha_hasta", "Próx. fecha hasta (AAAA-MM-DD)", "fecha", None),
    ],
    3: [
        ("fecha_desde", "Fecha desde (AAAA-MM-DD)", "fecha", None),
        ("fecha_hasta", "Fecha hasta (AAAA-MM-DD)", "fecha", None),
        ("id_vehiculo", "Unidad / vehículo", "combo", "vehiculos"),
        ("taller", "Taller mecánico / proveedor", "combo", "talleres"),
        ("id_tipo", "Rutina ejecutada", "combo", "tipos"),
    ],
    4: [
        ("estado", "Estado de afiliación", "combo", "estados_socio"),
        ("tenencia", "Tenencia de unidades", "combo", "tenencia"),
        ("id_socio", "Socio individual", "combo", "socios"),
    ],
    5: [
        ("fecha_desde", "Fecha desde (AAAA-MM-DD)", "fecha", None),
        ("fecha_hasta", "Fecha hasta (AAAA-MM-DD)", "fecha", None),
        ("id_vehiculo", "Alcance de flota (unidad)", "combo", "vehiculos"),
        ("taller", "Taller mecánico", "combo", "talleres"),
    ],
}


class ModalFiltrosReporte(ctk.CTkToplevel):
    """Ventana modal que configura los filtros de un reporte antes de exportarlo."""

    def __init__(self, parent, reporte: dict, on_exportar):
        super().__init__(parent)
        self.reporte = reporte
        self.on_exportar = on_exportar
        self.campos = CAMPOS_POR_REPORTE[reporte["id"]]
        self._getters = {}   # clave -> función que devuelve el valor actual
        self._setters = {}   # clave -> función que restablece el valor
        self._widgets_fecha = {}

        self.title(f"Filtros — Reporte {reporte['id']}")
        alto = 230 + 62 * len(self.campos)
        self.geometry(f"520x{alto}")
        self.resizable(False, False)
        self.transient(parent.winfo_toplevel())

        self.catalogos = ReporteController.obtener_catalogos_para_filtros()
        self._construir_ui()
        self._actualizar_conteo()
        self.after(100, self.grab_set)

    # ------------------ CATÁLOGOS ------------------

    def _opciones(self, nombre: str):
        """Devuelve (lista de etiquetas, dict etiqueta->valor) para un combo."""
        c = self.catalogos
        if nombre == "estatus":
            return ESTATUS_VEHICULO, {e: e for e in ESTATUS_VEHICULO}
        if nombre == "semaforos":
            etiquetas = {"Todos": "Todos", "Vencido": "Vencido", "Por Vencer": "Por Vencer",
                         "Al Día": "Al Día", "Críticos": "Críticos"}
            etiquetas = {("🚨 Críticos (Vencido + Por Vencer)" if k == "Críticos" else k): v
                         for k, v in etiquetas.items()}
            return list(etiquetas.keys()), etiquetas
        if nombre == "estados_socio":
            return ESTADOS_SOCIO, {e: e for e in ESTADOS_SOCIO}
        if nombre == "tenencia":
            return TENENCIA, {e: e for e in TENENCIA}
        if nombre == "socios":
            mapa = {"Todos": None}
            for s in c["socios"]:
                mapa[f"{s['nombre_completo']} ({s['cedula']})"] = s["id_socio"]
            return list(mapa.keys()), mapa
        if nombre == "vehiculos":
            mapa = {"Todas": None}
            for v in c["vehiculos"]:
                mapa[f"Unidad {v['numero_unidad']} - {v['placa']}"] = v["id_vehiculo"]
            return list(mapa.keys()), mapa
        if nombre == "tipos":
            mapa = {"Todas": None}
            for t in c["tipos"]:
                mapa[t["nombre"]] = t["id_tipo"]
            return list(mapa.keys()), mapa
        if nombre == "talleres":
            mapa = {"Todos": None}
            for t in c["talleres"]:
                mapa[t] = t
            return list(mapa.keys()), mapa
        return ["Todos"], {"Todos": None}

    # ------------------ UI ------------------

    def _construir_ui(self):
        ctk.CTkLabel(
            self,
            text=f"{self.reporte['icono']} Filtros del Reporte {self.reporte['id']}",
            font=ctk.CTkFont(size=18, weight="bold"),
        ).pack(pady=(15, 2))
        ctk.CTkLabel(
            self,
            text="Deje un filtro en «Todos» o vacío para no aplicarlo.",
            font=ctk.CTkFont(size=11),
            text_color=TEXT_MUTED,
        ).pack(pady=(0, 8))

        form = ctk.CTkFrame(self, fg_color="transparent")
        form.pack(fill="x", padx=30)

        for clave, etiqueta, tipo, origen in self.campos:
            ctk.CTkLabel(form, text=etiqueta + ":", anchor="w").pack(fill="x", pady=(4, 0))
            if tipo == "combo":
                self._crear_combo(form, clave, origen)
            else:
                self._crear_entry(form, clave, tipo == "fecha")

        if any(c[2] == "fecha" for c in self.campos):
            atajos = ctk.CTkFrame(form, fg_color="transparent")
            atajos.pack(fill="x", pady=(8, 0))
            for texto, cmd in (("Mes actual", self._mes_actual), ("Año actual", self._anio_actual), ("Limpiar fechas", self._limpiar_fechas)):
                ctk.CTkButton(
                    atajos, text=texto, width=100, height=26,
                    fg_color=BTN_NEUTRAL_COLOR, hover_color=BTN_NEUTRAL_HOVER, command=cmd
                ).pack(side="left", padx=(0, 6))

        self.lbl_conteo = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=13, weight="bold"))
        self.lbl_conteo.pack(pady=(14, 4))

        botones = ctk.CTkFrame(self, fg_color="transparent")
        botones.pack(fill="x", padx=30, pady=(4, 15))
        ctk.CTkButton(
            botones, text="🔄 Restablecer Filtros",
            fg_color=BTN_NEUTRAL_COLOR, hover_color=BTN_NEUTRAL_HOVER, command=self._restablecer
        ).pack(side="left")
        self.btn_generar = ctk.CTkButton(
            botones, text=f"📥 Generar {self.reporte['formato']}",
            fg_color=BTN_PRIMARY_COLOR, hover_color=BTN_PRIMARY_HOVER, command=self._generar
        )
        self.btn_generar.pack(side="right")

    def _crear_combo(self, parent, clave, origen):
        etiquetas, mapa = self._opciones(origen)
        combo = ctk.CTkComboBox(
            parent, values=etiquetas, state="readonly",
            command=lambda _v: self._actualizar_conteo()
        )
        combo.set(etiquetas[0])
        combo.pack(fill="x")
        self._getters[clave] = lambda c=combo, m=mapa: m.get(c.get())
        self._setters[clave] = lambda c=combo, e=etiquetas: c.set(e[0])

    def _crear_entry(self, parent, clave, es_fecha):
        entry = ctk.CTkEntry(parent, placeholder_text="AAAA-MM-DD" if es_fecha else "Ej: 150000")
        entry.pack(fill="x")
        entry.bind("<KeyRelease>", lambda _e: self._actualizar_conteo())
        self._getters[clave] = lambda e=entry: e.get().strip()
        self._setters[clave] = lambda e=entry: e.delete(0, "end")
        if es_fecha:
            self._widgets_fecha[clave] = entry

    # ------------------ ATAJOS DE FECHA ------------------

    def _set_fechas(self, desde: str, hasta: str):
        for clave, valor in (("fecha_desde", desde), ("fecha_hasta", hasta)):
            w = self._widgets_fecha.get(clave)
            if w is not None:
                w.delete(0, "end")
                w.insert(0, valor)
        self._actualizar_conteo()

    def _mes_actual(self):
        hoy = date.today()
        ultimo = calendar.monthrange(hoy.year, hoy.month)[1]
        self._set_fechas(f"{hoy.year}-{hoy.month:02d}-01", f"{hoy.year}-{hoy.month:02d}-{ultimo:02d}")

    def _anio_actual(self):
        y = date.today().year
        self._set_fechas(f"{y}-01-01", f"{y}-12-31")

    def _limpiar_fechas(self):
        self._set_fechas("", "")

    # ------------------ LÓGICA ------------------

    def obtener_filtros(self) -> dict:
        return {clave: getter() for clave, getter in self._getters.items()}

    def _restablecer(self):
        for setter in self._setters.values():
            setter()
        self._actualizar_conteo()

    def _actualizar_conteo(self):
        ok, total, msg = ReporteController.contar_registros(self.reporte["id"], self.obtener_filtros())
        if not ok:
            self.lbl_conteo.configure(text=f"⚠️ {msg}", text_color="#EF4444")
            self.btn_generar.configure(state="disabled")
            return
        color = "#10B981" if total > 0 else "#F59E0B"
        self.lbl_conteo.configure(text=f"Registros coincidentes: {total}", text_color=color)
        self.btn_generar.configure(state="normal")

    def _generar(self):
        filtros = self.obtener_filtros()
        ok, total, msg = ReporteController.contar_registros(self.reporte["id"], filtros)
        if not ok:
            messagebox.showerror("Filtros inválidos", msg, parent=self)
            return
        if total == 0 and not messagebox.askyesno(
            "Sin registros",
            "Ningún registro cumple los filtros seleccionados.\n¿Desea generar el documento vacío de todas formas?",
            parent=self,
        ):
            return
        self.destroy()
        self.on_exportar(filtros)
