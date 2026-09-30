from src.models.base_model import BaseModel
from typing import Dict, Any, Optional

class MantenimientoProgramado(BaseModel):
    def __init__(
        self,
        id_programacion: Optional[int],
        id_vehiculo: int,
        id_tipo: int,
        fecha_ultimo_servicio: Optional[str] = None,
        km_ultimo_servicio: int = 0,
        fecha_proximo_servicio: Optional[str] = None,
        km_proximo_servicio: int = 0,
        observaciones: str = "",
        activo: int = 1,
        numero_unidad: str = "",
        placa: str = "",
        marca_modelo: str = "",
        kilometraje_actual: int = 0,
        tipo_nombre: str = "",
        socio_nombre: str = "",
        estado_alerta: str = "Al Día",
        badge_alerta: str = "🟢 Al Día",
        color_hex: str = "#10B981"
    ):
        self.id_programacion = id_programacion
        self.id_vehiculo = id_vehiculo
        self.id_tipo = id_tipo
        self.fecha_ultimo_servicio = fecha_ultimo_servicio
        self.km_ultimo_servicio = km_ultimo_servicio
        self.fecha_proximo_servicio = fecha_proximo_servicio
        self.km_proximo_servicio = km_proximo_servicio
        self.observaciones = observaciones
        self.activo = activo
        self.numero_unidad = numero_unidad
        self.placa = placa
        self.marca_modelo = marca_modelo
        self.kilometraje_actual = kilometraje_actual
        self.tipo_nombre = tipo_nombre
        self.socio_nombre = socio_nombre
        self.estado_alerta = estado_alerta
        self.badge_alerta = badge_alerta
        self.color_hex = color_hex

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MantenimientoProgramado":
        if not data:
            return None
        return cls(
            id_programacion=data.get("id_programacion"),
            id_vehiculo=data.get("id_vehiculo", 0),
            id_tipo=data.get("id_tipo", 0),
            fecha_ultimo_servicio=data.get("fecha_ultimo_servicio"),
            km_ultimo_servicio=data.get("km_ultimo_servicio", 0),
            fecha_proximo_servicio=data.get("fecha_proximo_servicio"),
            km_proximo_servicio=data.get("km_proximo_servicio", 0),
            observaciones=data.get("observaciones", ""),
            activo=data.get("activo", 1),
            numero_unidad=data.get("numero_unidad", ""),
            placa=data.get("placa", ""),
            marca_modelo=data.get("marca_modelo", ""),
            kilometraje_actual=data.get("kilometraje_actual", 0),
            tipo_nombre=data.get("tipo_nombre", ""),
            socio_nombre=data.get("socio_nombre", ""),
            estado_alerta=data.get("estado", "Al Día"),
            badge_alerta=data.get("badge", "🟢 Al Día"),
            color_hex=data.get("color_hex", "#10B981")
        )


class HistorialMantenimiento(BaseModel):
    def __init__(
        self,
        id_historial: Optional[int],
        id_vehiculo: int,
        id_tipo: int,
        fecha_realizado: str,
        km_al_momento: int,
        costo: float = 0.0,
        taller_mecanico: str = "",
        descripcion_trabajo: str = "",
        numero_unidad: str = "",
        placa: str = "",
        tipo_nombre: str = "",
        socio_nombre: str = ""
    ):
        self.id_historial = id_historial
        self.id_vehiculo = id_vehiculo
        self.id_tipo = id_tipo
        self.fecha_realizado = fecha_realizado
        self.km_al_momento = km_al_momento
        self.costo = costo
        self.taller_mecanico = taller_mecanico
        self.descripcion_trabajo = descripcion_trabajo
        self.numero_unidad = numero_unidad
        self.placa = placa
        self.tipo_nombre = tipo_nombre
        self.socio_nombre = socio_nombre

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "HistorialMantenimiento":
        if not data:
            return None
        return cls(
            id_historial=data.get("id_historial"),
            id_vehiculo=data.get("id_vehiculo", 0),
            id_tipo=data.get("id_tipo", 0),
            fecha_realizado=data.get("fecha_realizado", ""),
            km_al_momento=data.get("km_al_momento", 0),
            costo=float(data.get("costo", 0.0)),
            taller_mecanico=data.get("taller_mecanico", ""),
            descripcion_trabajo=data.get("descripcion_trabajo", ""),
            numero_unidad=data.get("numero_unidad", ""),
            placa=data.get("placa", ""),
            tipo_nombre=data.get("tipo_nombre", ""),
            socio_nombre=data.get("socio_nombre", "")
        )
