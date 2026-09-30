from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseModel(ABC):
    """
    Clase base para todos los modelos de dominio orientados a objetos.
    Proporciona serialización, deserialización y representación estándar.
    """

    @classmethod
    @abstractmethod
    def from_dict(cls, data: Dict[str, Any]):
        """Crea una instancia del modelo a partir de un diccionario o fila de base de datos."""
        pass

    def to_dict(self) -> Dict[str, Any]:
        """Serializa la instancia a un diccionario de Python."""
        return {
            key: value for key, value in self.__dict__.items()
            if not key.startswith("_")
        }

    def __repr__(self) -> str:
        attrs = ", ".join(f"{k}={v!r}" for k, v in self.to_dict().items())
        return f"{self.__class__.__name__}({attrs})"
