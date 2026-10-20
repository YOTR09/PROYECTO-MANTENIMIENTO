import os
from datetime import datetime
from src.controllers.base_controller import BaseController
from src.repositories.vehiculo_repository import VehiculoRepository
from src.repositories.socio_repository import SocioRepository
from src.repositories.mantenimiento_repository import MantenimientoRepository
from src.repositories.tipo_mantenimiento_repository import TipoMantenimientoRepository
from src.controllers.mantenimiento_controller import MantenimientoController
from src.reports.pdf_generator import PDFReportGenerator
from src.reports.excel_generator import ExcelReportGenerator
from typing import Tuple, Optional, Dict, Any

TODOS = "Todos"


class FiltroInvalidoError(ValueError):
    """Error de validación de los filtros de un reporte."""


class ReporteController(BaseController):

    # ------------------ UTILIDADES DE FILTROS ------------------

    @staticmethod
    def _limpio(valor):
        """Normaliza vacíos y 'Todos' a None."""
        if valor is None:
            return None
        if isinstance(valor, str):
            valor = valor.strip()
            if not valor or valor.lower().startswith("todo"):
                return None
        return valor

    @staticmethod
    def _parse_fecha(valor, etiqueta: str) -> Optional[str]:
        valor = ReporteController._limpio(valor)
        if valor is None:
            return None
        try:
            return datetime.strptime(str(valor), "%Y-%m-%d").strftime("%Y-%m-%d")
        except ValueError:
            raise FiltroInvalidoError(f"{etiqueta} inválida. Use el formato AAAA-MM-DD.")

    @staticmethod
    def _parse_entero(valor, etiqueta: str) -> Optional[int]:
        valor = ReporteController._limpio(valor)
        if valor is None:
            return None
        try:
            n = int(str(valor).replace(",", "").replace(".", ""))
        except ValueError:
            raise FiltroInvalidoError(f"{etiqueta} debe ser un número entero.")
        if n < 0:
            raise FiltroInvalidoError(f"{etiqueta} no puede ser negativo.")
        return n

    @staticmethod
    def normalizar_filtros(filtros: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Valida y normaliza el diccionario de filtros. Lanza FiltroInvalidoError."""
        f = filtros or {}
        c = ReporteController
        norm = {
            "status": c._limpio(f.get("status")),
            "id_socio": c._parse_entero(f.get("id_socio"), "El socio"),
            "km_min": c._parse_entero(f.get("km_min"), "El kilometraje mínimo"),
            "km_max": c._parse_entero(f.get("km_max"), "El kilometraje máximo"),
            "estado_alerta": c._limpio(f.get("estado_alerta")),
            "id_vehiculo": c._parse_entero(f.get("id_vehiculo"), "La unidad"),
            "id_tipo": c._parse_entero(f.get("id_tipo"), "La rutina"),
            "fecha_desde": c._parse_fecha(f.get("fecha_desde"), "La fecha desde"),
            "fecha_hasta": c._parse_fecha(f.get("fecha_hasta"), "La fecha hasta"),
            "taller": c._limpio(f.get("taller")),
            "estado": c._limpio(f.get("estado")),
            "tenencia": c._limpio(f.get("tenencia")),
        }
        if norm["fecha_desde"] and norm["fecha_hasta"] and norm["fecha_desde"] > norm["fecha_hasta"]:
            raise FiltroInvalidoError("La fecha 'desde' no puede ser posterior a la fecha 'hasta'.")
        if norm["km_min"] is not None and norm["km_max"] is not None and norm["km_min"] > norm["km_max"]:
            raise FiltroInvalidoError("El kilometraje mínimo no puede superar al máximo.")
        return norm

    @staticmethod
    def _fmt_fecha(f: str) -> str:
        return datetime.strptime(f, "%Y-%m-%d").strftime("%d/%m/%Y")

    @staticmethod
    def describir_filtros(filtros: Dict[str, Any]) -> str:
        """Texto legible con los criterios activos (ya normalizados). Vacío si no hay."""
        partes = []
        if filtros.get("status"):
            partes.append(f"Estatus: {filtros['status']}")
        if filtros.get("id_socio"):
            s = SocioRepository.get_by_id(filtros["id_socio"])
            partes.append(f"Socio: {s['nombre_completo'] if s else filtros['id_socio']}")
        if filtros.get("km_min") is not None:
            partes.append(f"Km mín: {filtros['km_min']:,}")
        if filtros.get("km_max") is not None:
            partes.append(f"Km máx: {filtros['km_max']:,}")
        if filtros.get("estado_alerta"):
            etiqueta = "Críticos (Vencido + Por Vencer)" if filtros["estado_alerta"] == "Críticos" else filtros["estado_alerta"]
            partes.append(f"Semáforo: {etiqueta}")
        if filtros.get("id_vehiculo"):
            v = VehiculoRepository.get_by_id(filtros["id_vehiculo"])
            partes.append(f"Unidad: {v['numero_unidad'] if v else filtros['id_vehiculo']}")
        if filtros.get("id_tipo"):
            t = TipoMantenimientoRepository.get_by_id(filtros["id_tipo"])
            partes.append(f"Rutina: {t['nombre'] if t else filtros['id_tipo']}")
        if filtros.get("fecha_desde") or filtros.get("fecha_hasta"):
            d = ReporteController._fmt_fecha(filtros["fecha_desde"]) if filtros.get("fecha_desde") else "inicio"
            h = ReporteController._fmt_fecha(filtros["fecha_hasta"]) if filtros.get("fecha_hasta") else "hoy"
            partes.append(f"Período: {d} al {h}")
        if filtros.get("taller"):
            partes.append(f"Taller: {filtros['taller']}")
        if filtros.get("estado"):
            partes.append(f"Afiliación: {filtros['estado']}")
        if filtros.get("tenencia"):
            partes.append(f"Unidades: {filtros['tenencia']}")
        return " | ".join(partes)

    @staticmethod
    def obtener_catalogos_para_filtros() -> Dict[str, Any]:
        """Catálogos para poblar los selectores de la interfaz de filtros."""
        return {
            "vehiculos": VehiculoRepository.get_all(solo_activos=True),
            "socios": SocioRepository.get_all(solo_activos=True),
            "tipos": TipoMantenimientoRepository.get_all(solo_activos=True),
            "talleres": MantenimientoRepository.get_talleres_registrados(),
        }

    # ------------------ CONSULTAS FILTRADAS ------------------

    @staticmethod
    def _consultar_flota(f):
        return VehiculoRepository.get_all(
            solo_activos=True, status_filter=f["status"], id_socio=f["id_socio"],
            km_min=f["km_min"], km_max=f["km_max"]
        )

    @staticmethod
    def _consultar_preventivo(f):
        progs = MantenimientoController.listar_programaciones(
            id_vehiculo=f["id_vehiculo"], estado_filtro=f["estado_alerta"], solo_activos=True,
            id_tipo=f["id_tipo"], fecha_desde=f["fecha_desde"], fecha_hasta=f["fecha_hasta"]
        )
        return [p.to_dict() for p in progs]

    @staticmethod
    def _consultar_historial(f):
        return MantenimientoRepository.get_historial(
            id_vehiculo=f["id_vehiculo"], limit=100000, fecha_desde=f["fecha_desde"],
            fecha_hasta=f["fecha_hasta"], id_tipo=f["id_tipo"], taller_mecanico=f["taller"]
        )

    @staticmethod
    def _consultar_socios(f):
        con_unidades = None
        if f["tenencia"]:
            con_unidades = f["tenencia"].lower().startswith("con")
        socios = SocioRepository.get_all(
            solo_activos=True, estado_filter=f["estado"], id_socio=f["id_socio"], con_unidades=con_unidades
        )
        vehiculos = VehiculoRepository.get_all(solo_activos=True)
        unidades_por_socio = {}
        for v in vehiculos:
            unidades_por_socio.setdefault(v["id_socio"], []).append(f"Unidad {v['numero_unidad']} ({v['placa']})")
        datos = []
        for s in socios:
            s_dict = dict(s)
            lista = unidades_por_socio.get(s["id_socio"], [])
            s_dict["unidades_resumen"] = ", ".join(lista) if lista else "Sin unidades"
            datos.append(s_dict)
        return datos

    @staticmethod
    def contar_registros(numero_reporte: int, filtros: Optional[Dict[str, Any]] = None) -> Tuple[bool, int, str]:
        """Cantidad de registros que cumplen los filtros (vista previa en vivo). (ok, total, mensaje)"""
        try:
            f = ReporteController.normalizar_filtros(filtros)
            consulta = {
                1: ReporteController._consultar_flota,
                2: ReporteController._consultar_preventivo,
                3: ReporteController._consultar_historial,
                4: ReporteController._consultar_socios,
                5: ReporteController._consultar_historial,
            }[numero_reporte]
            return True, len(consulta(f)), ""
        except FiltroInvalidoError as e:
            return False, 0, str(e)
        except Exception as e:
            return False, 0, f"Error al consultar registros: {str(e)}"

    # ------------------ REPORTES ------------------

    @staticmethod
    def generar_reporte_1_flota_pdf(ruta_destino: str, filtros: Optional[Dict[str, Any]] = None) -> Tuple[bool, str]:
        """Reporte 1: Ficha Técnica y Estado General de la Flota Vehicular (PDF)"""
        try:
            f = ReporteController.normalizar_filtros(filtros)
            vehiculos = ReporteController._consultar_flota(f)
            PDFReportGenerator.generar_reporte_flota(vehiculos, ruta_destino, ReporteController.describir_filtros(f))
            return True, f"Reporte de Flota generado exitosamente en:\n{ruta_destino}"
        except FiltroInvalidoError as e:
            return False, str(e)
        except Exception as e:
            return False, f"Error al generar reporte de flota: {str(e)}"

    @staticmethod
    def generar_reporte_2_preventivo_pdf(ruta_destino: str, filtros: Optional[Dict[str, Any]] = None) -> Tuple[bool, str]:
        """Reporte 2: Plan de Mantenimiento Preventivo y Alertas de Vencimiento (PDF)"""
        try:
            f = ReporteController.normalizar_filtros(filtros)
            progs_dicts = ReporteController._consultar_preventivo(f)
            PDFReportGenerator.generar_reporte_preventivo(progs_dicts, ruta_destino, ReporteController.describir_filtros(f))
            return True, f"Reporte Preventivo generado exitosamente en:\n{ruta_destino}"
        except FiltroInvalidoError as e:
            return False, str(e)
        except Exception as e:
            return False, f"Error al generar reporte preventivo: {str(e)}"

    @staticmethod
    def generar_reporte_3_historial_excel(ruta_destino: str, filtros: Optional[Dict[str, Any]] = None) -> Tuple[bool, str]:
        """Reporte 3: Bitácora Histórica de Mantenimientos y Costos Operativos (Excel)"""
        try:
            f = ReporteController.normalizar_filtros(filtros)
            historial = ReporteController._consultar_historial(f)
            ExcelReportGenerator.generar_reporte_historial_costos(historial, ruta_destino, ReporteController.describir_filtros(f))
            return True, f"Libro Excel de Bitácora y Costos generado exitosamente en:\n{ruta_destino}"
        except FiltroInvalidoError as e:
            return False, str(e)
        except Exception as e:
            return False, f"Error al generar bitácora en Excel: {str(e)}"

    @staticmethod
    def generar_reporte_4_socios_pdf(ruta_destino: str, filtros: Optional[Dict[str, Any]] = None) -> Tuple[bool, str]:
        """Reporte 4: Directorio Institucional de Socios y Unidades Asignadas (PDF)"""
        try:
            f = ReporteController.normalizar_filtros(filtros)
            datos_combinados = ReporteController._consultar_socios(f)
            PDFReportGenerator.generar_reporte_socios(datos_combinados, ruta_destino, ReporteController.describir_filtros(f))
            return True, f"Directorio de Socios generado exitosamente en:\n{ruta_destino}"
        except FiltroInvalidoError as e:
            return False, str(e)
        except Exception as e:
            return False, f"Error al generar directorio de socios: {str(e)}"

    @staticmethod
    def generar_reporte_5_metricas_excel(ruta_destino: str, filtros: Optional[Dict[str, Any]] = None) -> Tuple[bool, str]:
        """Reporte 5: Resumen Ejecutivo y Métricas de Rendimiento Operativo (Excel)"""
        try:
            f = ReporteController.normalizar_filtros(filtros)
            historial = ReporteController._consultar_historial(f)
            vehiculos = VehiculoRepository.get_all(solo_activos=True)
            ExcelReportGenerator.generar_reporte_metricas_talleres(historial, vehiculos, ruta_destino, ReporteController.describir_filtros(f))
            return True, f"Libro Excel de Métricas y Talleres generado exitosamente en:\n{ruta_destino}"
        except FiltroInvalidoError as e:
            return False, str(e)
        except Exception as e:
            return False, f"Error al generar reporte de métricas en Excel: {str(e)}"
