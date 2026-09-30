from src.models.base_model import BaseModel
from typing import Dict, Any, Optional

class TipoMantenimiento(BaseModel):
    def __init__(
        self,
        id_tipo: Optional[int],
        nombre: str,
        descripcion: str = "",
        intervalo_km: int = 0,
        intervalo_dias: int = 0,
        activo: int = 1
    ):
        self.id_tipo = id_tipo
        self.nombre = nombre
        self.descripcion = descripcion
        self.intervalo_km = intervalo_km
        self.intervalo_dias = intervalo_dias
        self.activo = activo

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TipoMantenimiento":
        if not data:
            return None
        return cls(
            id_tipo=data.get("id_tipo"),
            nombre=data.get("nombre", ""),
            descripcion=data.get("descripcion", ""),
            intervalo_km=data.get("intervalo_km", 0),
            intervalo_dias=data.get("intervalo_dias", 0),
            activo=data.get("activo", 1)
        )
