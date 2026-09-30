from src.models.base_model import BaseModel
from typing import Dict, Any, Optional

class Socio(BaseModel):
    def __init__(
        self,
        id_socio: Optional[int],
        cedula: str,
        nombre_completo: str,
        telefono: str = "",
        estado: str = "Activo",
        activo: int = 1
    ):
        self.id_socio = id_socio
        self.cedula = cedula
        self.nombre_completo = nombre_completo
        self.telefono = telefono
        self.estado = estado
        self.activo = activo

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Socio":
        if not data:
            return None
        return cls(
            id_socio=data.get("id_socio"),
            cedula=data.get("cedula", ""),
            nombre_completo=data.get("nombre_completo", ""),
            telefono=data.get("telefono", ""),
            estado=data.get("estado", "Activo"),
            activo=data.get("activo", 1)
        )
