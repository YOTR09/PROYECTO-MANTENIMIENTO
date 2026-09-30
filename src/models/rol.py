from src.models.base_model import BaseModel
from typing import Dict, Any, Optional

class Rol(BaseModel):
    def __init__(self, id_rol: Optional[int], nombre: str, descripcion: str = ""):
        self.id_rol = id_rol
        self.nombre = nombre
        self.descripcion = descripcion

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Rol":
        if not data:
            return None
        return cls(
            id_rol=data.get("id_rol"),
            nombre=data.get("nombre", ""),
            descripcion=data.get("descripcion", "")
        )
