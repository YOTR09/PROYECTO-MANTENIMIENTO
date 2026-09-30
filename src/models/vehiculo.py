from src.models.base_model import BaseModel
from typing import Dict, Any, Optional

class Vehiculo(BaseModel):
    def __init__(
        self,
        id_vehiculo: Optional[int],
        id_socio: int,
        numero_unidad: str,
        placa: str,
        marca_modelo: str,
        ano: Optional[int] = None,
        kilometraje_actual: int = 0,
        status: str = "Activo",
        activo: int = 1,
        socio_nombre: str = "",
        socio_cedula: str = ""
    ):
        self.id_vehiculo = id_vehiculo
        self.id_socio = id_socio
        self.numero_unidad = numero_unidad
        self.placa = placa
        self.marca_modelo = marca_modelo
        self.ano = ano
        self.kilometraje_actual = kilometraje_actual
        self.status = status
        self.activo = activo
        self.socio_nombre = socio_nombre
        self.socio_cedula = socio_cedula

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Vehiculo":
        if not data:
            return None
        return cls(
            id_vehiculo=data.get("id_vehiculo"),
            id_socio=data.get("id_socio", 0),
            numero_unidad=data.get("numero_unidad", ""),
            placa=data.get("placa", ""),
            marca_modelo=data.get("marca_modelo", ""),
            ano=data.get("ano"),
            kilometraje_actual=data.get("kilometraje_actual", 0),
            status=data.get("status", "Activo"),
            activo=data.get("activo", 1),
            socio_nombre=data.get("socio_nombre", ""),
            socio_cedula=data.get("socio_cedula", "")
        )
