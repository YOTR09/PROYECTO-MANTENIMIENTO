import os
from src.controllers.base_controller import BaseController
from src.repositories.vehiculo_repository import VehiculoRepository
from src.repositories.socio_repository import SocioRepository
from src.repositories.mantenimiento_repository import MantenimientoRepository
from src.controllers.mantenimiento_controller import MantenimientoController
from src.reports.pdf_generator import PDFReportGenerator
from src.reports.excel_generator import ExcelReportGenerator
from typing import Tuple

class ReporteController(BaseController):

    @staticmethod
    def generar_reporte_1_flota_pdf(ruta_destino: str) -> Tuple[bool, str]:
        """Reporte 1: Ficha Técnica y Estado General de la Flota Vehicular (PDF)"""
        try:
            vehiculos = VehiculoRepository.get_all(solo_activos=True)
            PDFReportGenerator.generar_reporte_flota(vehiculos, ruta_destino)
            return True, f"Reporte de Flota generado exitosamente en:\n{ruta_destino}"
        except Exception as e:
            return False, f"Error al generar reporte de flota: {str(e)}"

    @staticmethod
    def generar_reporte_2_preventivo_pdf(ruta_destino: str) -> Tuple[bool, str]:
        """Reporte 2: Plan de Mantenimiento Preventivo y Alertas de Vencimiento (PDF)"""
        try:
            progs = MantenimientoController.listar_programaciones(solo_activos=True)
            progs_dicts = [p.to_dict() for p in progs]
            PDFReportGenerator.generar_reporte_preventivo(progs_dicts, ruta_destino)
            return True, f"Reporte Preventivo generado exitosamente en:\n{ruta_destino}"
        except Exception as e:
            return False, f"Error al generar reporte preventivo: {str(e)}"

    @staticmethod
    def generar_reporte_3_historial_excel(ruta_destino: str) -> Tuple[bool, str]:
        """Reporte 3: Bitácora Histórica de Mantenimientos y Costos Operativos (Excel)"""
        try:
            historial = MantenimientoRepository.get_historial(limit=1000)
            ExcelReportGenerator.generar_reporte_historial_costos(historial, ruta_destino)
            return True, f"Libro Excel de Bitácora y Costos generado exitosamente en:\n{ruta_destino}"
        except Exception as e:
            return False, f"Error al generar bitácora en Excel: {str(e)}"

    @staticmethod
    def generar_reporte_4_socios_pdf(ruta_destino: str) -> Tuple[bool, str]:
        """Reporte 4: Directorio Institucional de Socios y Unidades Asignadas (PDF)"""
        try:
            socios = SocioRepository.get_all(solo_activos=True)
            vehiculos = VehiculoRepository.get_all(solo_activos=True)

            # Mapear unidades por socio
            unidades_por_socio = {}
            for v in vehiculos:
                id_s = v["id_socio"]
                if id_s not in unidades_por_socio:
                    unidades_por_socio[id_s] = []
                unidades_por_socio[id_s].append(f"Unidad {v['numero_unidad']} ({v['placa']})")

            datos_combinados = []
            for s in socios:
                s_dict = dict(s)
                unidades_list = unidades_por_socio.get(s["id_socio"], [])
                s_dict["unidades_resumen"] = ", ".join(unidades_list) if unidades_list else "Sin unidades"
                datos_combinados.append(s_dict)

            PDFReportGenerator.generar_reporte_socios(datos_combinados, ruta_destino)
            return True, f"Directorio de Socios generado exitosamente en:\n{ruta_destino}"
        except Exception as e:
            return False, f"Error al generar directorio de socios: {str(e)}"

    @staticmethod
    def generar_reporte_5_metricas_excel(ruta_destino: str) -> Tuple[bool, str]:
        """Reporte 5: Resumen Ejecutivo y Métricas de Rendimiento Operativo (Excel)"""
        try:
            historial = MantenimientoRepository.get_historial(limit=1000)
            vehiculos = VehiculoRepository.get_all(solo_activos=True)
            ExcelReportGenerator.generar_reporte_metricas_talleres(historial, vehiculos, ruta_destino)
            return True, f"Libro Excel de Métricas y Talleres generado exitosamente en:\n{ruta_destino}"
        except Exception as e:
            return False, f"Error al generar reporte de métricas en Excel: {str(e)}"
