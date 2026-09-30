from datetime import datetime, date, timedelta
from src.controllers.base_controller import BaseController
from src.repositories.mantenimiento_repository import MantenimientoRepository
from src.repositories.vehiculo_repository import VehiculoRepository
from src.repositories.tipo_mantenimiento_repository import TipoMantenimientoRepository
from src.models.mantenimiento import MantenimientoProgramado, HistorialMantenimiento
from src.models.tipo_mantenimiento import TipoMantenimiento
from typing import List, Dict, Any, Optional, Tuple

class MantenimientoController(BaseController):

    # ------------------ CATÁLOGO DE RUTINAS ------------------

    @staticmethod
    def listar_tipos(search_term: Optional[str] = None, solo_activos: bool = True) -> List[TipoMantenimiento]:
        filas = TipoMantenimientoRepository.get_all(search_term=search_term, solo_activos=solo_activos)
        return [TipoMantenimiento.from_dict(row) for row in filas]

    @staticmethod
    def obtener_tipo(id_tipo: int) -> Optional[TipoMantenimiento]:
        fila = TipoMantenimientoRepository.get_by_id(id_tipo)
        return TipoMantenimiento.from_dict(fila) if fila else None

    @staticmethod
    def registrar_tipo(nombre: str, descripcion: str = "", intervalo_km: int = 0, intervalo_dias: int = 0) -> Tuple[bool, Optional[TipoMantenimiento], str]:
        if not nombre or not nombre.strip():
            return False, None, "El nombre de la rutina de mantenimiento es obligatorio."

        try:
            km = int(intervalo_km) if intervalo_km else 0
            dias = int(intervalo_dias) if intervalo_dias else 0
            if km < 0 or dias < 0:
                raise ValueError()
        except (ValueError, TypeError):
            return False, None, "Los intervalos de kilómetros y días deben ser números enteros no negativos."

        if km == 0 and dias == 0:
            return False, None, "Debe especificar al menos un intervalo mayor a cero (por km o por días)."

        try:
            nuevo_id = TipoMantenimientoRepository.create(nombre.strip(), descripcion.strip() if descripcion else "", km, dias)
            tipo = MantenimientoController.obtener_tipo(nuevo_id)
            return True, tipo, "Rutina de mantenimiento registrada exitosamente."
        except Exception as e:
            return False, None, f"Error al registrar la rutina: {str(e)}"

    @staticmethod
    def actualizar_tipo(id_tipo: int, nombre: str, descripcion: str = "", intervalo_km: int = 0, intervalo_dias: int = 0) -> Tuple[bool, str]:
        if not id_tipo:
            return False, "ID de tipo inválido."
        if not nombre or not nombre.strip():
            return False, "El nombre es obligatorio."

        try:
            km = int(intervalo_km) if intervalo_km else 0
            dias = int(intervalo_dias) if intervalo_dias else 0
            if km < 0 or dias < 0:
                raise ValueError()
        except (ValueError, TypeError):
            return False, "Los intervalos deben ser números enteros válidos."

        if km == 0 and dias == 0:
            return False, "Debe especificar al menos un intervalo mayor a cero."

        try:
            TipoMantenimientoRepository.update(id_tipo, nombre.strip(), descripcion.strip() if descripcion else "", km, dias)
            return True, "Rutina de mantenimiento actualizada con éxito."
        except Exception as e:
            return False, f"Error al actualizar la rutina: {str(e)}"

    @staticmethod
    def eliminar_tipo(id_tipo: int, logico: bool = True) -> Tuple[bool, str]:
        try:
            TipoMantenimientoRepository.delete(id_tipo, logico=logico)
            return True, "Rutina de mantenimiento dada de baja exitosamente."
        except Exception as e:
            return False, f"Error al dar de baja la rutina: {str(e)}"

    # ------------------ SEMAFORIZACIÓN Y PROGRAMACIÓN ------------------

    @staticmethod
    def calcular_estado_alerta(item: Dict[str, Any]) -> Dict[str, Any]:
        km_proximo = item.get("km_proximo_servicio") or 0
        km_actual = item.get("kilometraje_actual") or 0
        fecha_proxima_str = item.get("fecha_proximo_servicio")

        diff_km = None
        if km_proximo > 0:
            diff_km = km_proximo - km_actual

        diff_dias = None
        if fecha_proxima_str:
            try:
                fecha_prox = datetime.strptime(fecha_proxima_str, "%Y-%m-%d").date()
                diff_dias = (fecha_prox - date.today()).days
            except ValueError:
                pass

        if (diff_km is not None and diff_km <= 0) or (diff_dias is not None and diff_dias <= 0):
            estado = "Vencido"
            badge = "🔴 Vencido"
            color_hex = "#EF4444"
        elif (diff_km is not None and diff_km <= 500) or (diff_dias is not None and diff_dias <= 10):
            estado = "Por Vencer"
            badge = "🟡 Por Vencer"
            color_hex = "#F59E0B"
        else:
            estado = "Al Día"
            badge = "🟢 Al Día"
            color_hex = "#10B981"

        detalles = []
        if diff_km is not None:
            if diff_km < 0:
                detalles.append(f"Excedido por {abs(diff_km):,} km")
            elif diff_km == 0:
                detalles.append("Límite de kilometraje alcanzado")
            else:
                detalles.append(f"Faltan {diff_km:,} km")

        if diff_dias is not None:
            if diff_dias < 0:
                detalles.append(f"Venció hace {abs(diff_dias)} días")
            elif diff_dias == 0:
                detalles.append("Vence hoy")
            else:
                detalles.append(f"Faltan {diff_dias} días")

        return {
            "estado": estado,
            "badge": badge,
            "color_hex": color_hex,
            "diff_km": diff_km,
            "diff_dias": diff_dias,
            "resumen_alerta": " | ".join(detalles) if detalles else "Sin límites fijados"
        }

    @staticmethod
    def listar_programaciones(id_vehiculo: Optional[int] = None, search_term: Optional[str] = None, estado_filtro: Optional[str] = None, solo_activos: bool = True) -> List[MantenimientoProgramado]:
        filas = MantenimientoRepository.get_programaciones(id_vehiculo=id_vehiculo, search_term=search_term, solo_activos=solo_activos)
        resultado = []
        for f in filas:
            alerta = MantenimientoController.calcular_estado_alerta(f)
            f.update(alerta)
            if not estado_filtro or estado_filtro == "Todos" or f["estado"] == estado_filtro:
                resultado.append(MantenimientoProgramado.from_dict(f))
        return resultado

    @staticmethod
    def programar_mantenimiento(id_vehiculo: int, id_tipo: int, fecha_ultimo: Optional[str] = None, km_ultimo: int = 0, observaciones: str = "") -> Tuple[bool, Optional[int], str]:
        if not id_vehiculo:
            return False, None, "Debe seleccionar un vehículo."
        if not id_tipo:
            return False, None, "Debe seleccionar una rutina de mantenimiento."

        tipo = TipoMantenimientoRepository.get_by_id(id_tipo)
        if not tipo:
            return False, None, "La rutina de mantenimiento no existe."

        try:
            km_ult = int(km_ultimo) if km_ultimo else 0
            if km_ult < 0:
                raise ValueError()
        except (ValueError, TypeError):
            return False, None, "El kilometraje del último servicio debe ser un entero mayor o igual a cero."

        km_proximo = 0
        if tipo["intervalo_km"] > 0:
            km_proximo = km_ult + tipo["intervalo_km"]

        fecha_proxima_str = None
        if tipo["intervalo_dias"] > 0:
            base_date = date.today()
            if fecha_ultimo:
                try:
                    base_date = datetime.strptime(fecha_ultimo, "%Y-%m-%d").date()
                except ValueError:
                    return False, None, "Formato de fecha inválido. Utilice el formato AAAA-MM-DD."
            fecha_proxima_str = (base_date + timedelta(days=tipo["intervalo_dias"])).strftime("%Y-%m-%d")

        fecha_ultimo_str = fecha_ultimo if fecha_ultimo else date.today().strftime("%Y-%m-%d")

        try:
            id_prog = MantenimientoRepository.upsert_programacion(
                id_vehiculo=id_vehiculo,
                id_tipo=id_tipo,
                fecha_ultimo=fecha_ultimo_str,
                km_ultimo=km_ult,
                fecha_proximo=fecha_proxima_str,
                km_proximo=km_proximo,
                observaciones=observaciones.strip() if observaciones else ""
            )
            return True, id_prog, "Mantenimiento programado exitosamente."
        except Exception as e:
            return False, None, f"Error al programar: {str(e)}"

    @staticmethod
    def eliminar_programacion(id_programacion: int, logico: bool = True) -> Tuple[bool, str]:
        try:
            MantenimientoRepository.delete_programacion(id_programacion, logico=logico)
            return True, "Plan de mantenimiento retirado exitosamente."
        except Exception as e:
            return False, f"Error al eliminar la programación: {str(e)}"

    # ------------------ REGISTRO DE SERVICIOS E HISTORIAL ------------------

    @staticmethod
    def registrar_servicio_realizado(
        id_vehiculo: int,
        id_tipo: int,
        fecha_realizado: Optional[str],
        km_al_momento: int,
        costo: float = 0.0,
        taller: str = "",
        descripcion: str = ""
    ) -> Tuple[bool, Optional[int], str]:
        if not id_vehiculo:
            return False, None, "Debe seleccionar un vehículo."
        if not id_tipo:
            return False, None, "Debe seleccionar la rutina ejecutada."

        if not fecha_realizado:
            fecha_realizado = date.today().strftime("%Y-%m-%d")
        else:
            try:
                datetime.strptime(fecha_realizado, "%Y-%m-%d")
            except ValueError:
                return False, None, "Formato de fecha inválido. Use AAAA-MM-DD."

        try:
            km = int(km_al_momento)
            if km < 0:
                raise ValueError()
        except (ValueError, TypeError):
            return False, None, "El odómetro al momento de la intervención debe ser un número entero no negativo."

        try:
            costo_val = float(costo) if costo else 0.0
            if costo_val < 0:
                raise ValueError()
        except (ValueError, TypeError):
            return False, None, "El costo debe ser un monto numérico válido."

        try:
            # 1. Registrar en bitácora histórica
            id_hist = MantenimientoRepository.add_historial(
                id_vehiculo=id_vehiculo,
                id_tipo=id_tipo,
                fecha_realizado=fecha_realizado,
                km_al_momento=km,
                costo=costo_val,
                taller_mecanico=taller.strip() if taller else "",
                descripcion_trabajo=descripcion.strip() if descripcion else ""
            )

            # 2. Actualizar odómetro del vehículo si es mayor
            vehiculo = VehiculoRepository.get_by_id(id_vehiculo)
            if vehiculo and km > vehiculo["kilometraje_actual"]:
                VehiculoRepository.update_kilometraje(id_vehiculo, km)

            # 3. Reprogramar próximo servicio automáticamente
            MantenimientoController.programar_mantenimiento(
                id_vehiculo=id_vehiculo,
                id_tipo=id_tipo,
                fecha_ultimo=fecha_realizado,
                km_ultimo=km,
                observaciones=f"Ejecutado el {fecha_realizado} a los {km:,} km en {taller or 'Taller interno'}."
            )

            return True, id_hist, "Mantenimiento registrado y próximo ciclo reprogramado con éxito."
        except Exception as e:
            return False, None, f"Error al registrar la intervención: {str(e)}"

    @staticmethod
    def listar_historial(id_vehiculo: Optional[int] = None, search_term: Optional[str] = None, limit: int = 500) -> List[HistorialMantenimiento]:
        filas = MantenimientoRepository.get_historial(id_vehiculo=id_vehiculo, search_term=search_term, limit=limit)
        return [HistorialMantenimiento.from_dict(row) for row in filas]

    @staticmethod
    def obtener_resumen_dashboard() -> Dict[str, Any]:
        vehiculos = VehiculoRepository.get_all(solo_activos=True)
        programaciones = MantenimientoController.listar_programaciones(solo_activos=True)

        total_vehiculos = len(vehiculos)
        activos = sum(1 for v in vehiculos if v["status"] == "Activo")
        en_taller = sum(1 for v in vehiculos if v["status"] == "En Taller")
        inactivos = sum(1 for v in vehiculos if v["status"] == "Inactivo")

        vencidos = sum(1 for p in programaciones if p.estado_alerta == "Vencido")
        por_vencer = sum(1 for p in programaciones if p.estado_alerta == "Por Vencer")
        al_dia = sum(1 for p in programaciones if p.estado_alerta == "Al Día")

        alertas_urgentes = [p for p in programaciones if p.estado_alerta in ("Vencido", "Por Vencer")]

        return {
            "total_vehiculos": total_vehiculos,
            "vehiculos_activos": activos,
            "vehiculos_en_taller": en_taller,
            "vehiculos_inactivos": inactivos,
            "total_programados": len(programaciones),
            "mantenimientos_vencidos": vencidos,
            "mantenimientos_por_vencer": por_vencer,
            "mantenimientos_al_dia": al_dia,
            "alertas_urgentes": alertas_urgentes[:10]
        }
