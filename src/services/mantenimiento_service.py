from datetime import datetime, date, timedelta
from src.repositories.mantenimiento_repository import MantenimientoRepository
from src.repositories.vehiculo_repository import VehiculoRepository
from src.repositories.tipo_mantenimiento_repository import TipoMantenimientoRepository

class MantenimientoService:
    @staticmethod
    def calcular_estado_alerta(item):
        """
        Calcula el estado de semaforización (Al Día, Por Vencer, Vencido)
        para una programación de mantenimiento.
        """
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
                hoy = date.today()
                diff_dias = (fecha_prox - hoy).days
            except ValueError:
                pass

        # Determinar estado
        # 1. Vencido: Si superó los km o la fecha ya pasó
        if (diff_km is not None and diff_km <= 0) or (diff_dias is not None and diff_dias <= 0):
            estado = "Vencido"
            color_hex = "#EF4444" # Rojo
            badge = "🔴 Vencido"
        # 2. Por Vencer: Restan 500 km o menos, o 10 días o menos
        elif (diff_km is not None and diff_km <= 500) or (diff_dias is not None and diff_dias <= 10):
            estado = "Por Vencer"
            color_hex = "#F59E0B" # Amarillo / Naranja
            badge = "🟡 Por Vencer"
        # 3. Al Día
        else:
            estado = "Al Día"
            color_hex = "#10B981" # Verde
            badge = "🟢 Al Día"

        detalle_alerta = []
        if diff_km is not None:
            if diff_km < 0:
                detalle_alerta.append(f"Excedido por {abs(diff_km):,} km")
            elif diff_km == 0:
                detalle_alerta.append("Alcanzó el kilometraje límite")
            else:
                detalle_alerta.append(f"Faltan {diff_km:,} km")

        if diff_dias is not None:
            if diff_dias < 0:
                detalle_alerta.append(f"Venció hace {abs(diff_dias)} días")
            elif diff_dias == 0:
                detalle_alerta.append("Vence hoy")
            else:
                detalle_alerta.append(f"Faltan {diff_dias} días")

        return {
            "estado": estado,
            "badge": badge,
            "color_hex": color_hex,
            "diff_km": diff_km,
            "diff_dias": diff_dias,
            "resumen_alerta": " | ".join(detalle_alerta) if detalle_alerta else "Sin límites fijados"
        }

    @staticmethod
    def listar_programaciones(id_vehiculo=None, search_term=None, estado_filtro=None):
        items = MantenimientoRepository.get_programaciones(id_vehiculo, search_term)
        resultados = []
        for item in items:
            alerta = MantenimientoService.calcular_estado_alerta(item)
            item.update(alerta)
            if not estado_filtro or estado_filtro == "Todos" or item["estado"] == estado_filtro:
                resultados.append(item)
        return resultados

    @staticmethod
    def programar_mantenimiento(id_vehiculo, id_tipo, fecha_ultimo=None, km_ultimo=0, observaciones=""):
        if not id_vehiculo:
            raise ValueError("Debe seleccionar un vehículo.")
        if not id_tipo:
            raise ValueError("Debe seleccionar una rutina de mantenimiento.")

        tipo = TipoMantenimientoRepository.get_by_id(id_tipo)
        if not tipo:
            raise ValueError("El tipo de mantenimiento seleccionado no existe.")

        try:
            km_ult = int(km_ultimo) if km_ultimo else 0
            if km_ult < 0:
                raise ValueError()
        except ValueError:
            raise ValueError("El kilometraje del último servicio debe ser un número entero mayor o igual a cero.")

        # Calcular próximo KM
        km_proximo = 0
        if tipo["intervalo_km"] > 0:
            km_proximo = km_ult + tipo["intervalo_km"]

        # Calcular próxima Fecha
        fecha_proxima_str = None
        if tipo["intervalo_dias"] > 0:
            base_date = date.today()
            if fecha_ultimo:
                try:
                    base_date = datetime.strptime(fecha_ultimo, "%Y-%m-%d").date()
                except ValueError:
                    raise ValueError("Formato de fecha inválido. Utilice el formato AAAA-MM-DD.")
            proxima_fecha = base_date + timedelta(days=tipo["intervalo_dias"])
            fecha_proxima_str = proxima_fecha.strftime("%Y-%m-%d")

        fecha_ultimo_str = fecha_ultimo if fecha_ultimo else date.today().strftime("%Y-%m-%d")

        return MantenimientoRepository.upsert_programacion(
            id_vehiculo=id_vehiculo,
            id_tipo=id_tipo,
            fecha_ultimo=fecha_ultimo_str,
            km_ultimo=km_ult,
            fecha_proximo=fecha_proxima_str,
            km_proximo=km_proximo,
            observaciones=observaciones.strip() if observaciones else ""
        )

    @staticmethod
    def registrar_mantenimiento_realizado(id_vehiculo, id_tipo, fecha_realizado, km_al_momento, costo=0.0, taller="", descripcion=""):
        if not id_vehiculo:
            raise ValueError("Debe indicar el vehículo.")
        if not id_tipo:
            raise ValueError("Debe indicar el tipo de mantenimiento.")
        if not fecha_realizado:
            fecha_realizado = date.today().strftime("%Y-%m-%d")
        else:
            try:
                datetime.strptime(fecha_realizado, "%Y-%m-%d")
            except ValueError:
                raise ValueError("Formato de fecha inválido. Utilice AAAA-MM-DD.")

        try:
            km = int(km_al_momento)
            if km < 0:
                raise ValueError()
        except ValueError:
            raise ValueError("El kilometraje al momento del mantenimiento debe ser un número entero.")

        try:
            costo_val = float(costo) if costo else 0.0
            if costo_val < 0:
                raise ValueError()
        except ValueError:
            raise ValueError("El costo debe ser un valor numérico válido.")

        # 1. Guardar en la bitácora histórica
        id_hist = MantenimientoRepository.add_historial(
            id_vehiculo=id_vehiculo,
            id_tipo=id_tipo,
            fecha_realizado=fecha_realizado,
            km_al_momento=km,
            costo=costo_val,
            taller_mecanico=taller.strip() if taller else "",
            descripcion_trabajo=descripcion.strip() if descripcion else ""
        )

        # 2. Actualizar kilometraje del vehículo si el odómetro registrado es superior
        vehiculo = VehiculoRepository.get_by_id(id_vehiculo)
        if vehiculo and km > vehiculo["kilometraje_actual"]:
            VehiculoRepository.update_kilometraje(id_vehiculo, km)

        # 3. Recalcular y reprogramar el próximo mantenimiento automáticamente
        MantenimientoService.programar_mantenimiento(
            id_vehiculo=id_vehiculo,
            id_tipo=id_tipo,
            fecha_ultimo=fecha_realizado,
            km_ultimo=km,
            observaciones=f"Servicio ejecutado el {fecha_realizado} a los {km:,} km."
        )

        return id_hist

    @staticmethod
    def eliminar_programacion(id_programacion):
        return MantenimientoRepository.delete_programacion(id_programacion)

    @staticmethod
    def listar_historial(id_vehiculo=None, search_term=None, limit=200):
        return MantenimientoRepository.get_historial(id_vehiculo, search_term, limit)

    @staticmethod
    def obtener_resumen_dashboard():
        vehiculos = VehiculoRepository.get_all()
        programaciones = MantenimientoService.listar_programaciones()

        total_vehiculos = len(vehiculos)
        activos = sum(1 for v in vehiculos if v["status"] == "Activo")
        en_taller = sum(1 for v in vehiculos if v["status"] == "En Taller")
        inactivos = sum(1 for v in vehiculos if v["status"] == "Inactivo")

        vencidos = sum(1 for p in programaciones if p["estado"] == "Vencido")
        por_vencer = sum(1 for p in programaciones if p["estado"] == "Por Vencer")
        al_dia = sum(1 for p in programaciones if p["estado"] == "Al Día")

        # Alertas críticas ordenadas (primero vencidos, luego por vencer)
        alertas_urgentes = [p for p in programaciones if p["estado"] in ("Vencido", "Por Vencer")]

        return {
            "total_vehiculos": total_vehiculos,
            "vehiculos_activos": activos,
            "vehiculos_en_taller": en_taller,
            "vehiculos_inactivos": inactivos,
            "total_programados": len(programaciones),
            "mantenimientos_vencidos": vencidos,
            "mantenimientos_por_vencer": por_vencer,
            "mantenimientos_al_dia": al_dia,
            "alertas_urgentes": alertas_urgentes[:8]
        }

