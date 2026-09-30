from typing import Any, Dict, Optional, Tuple

class BaseController:
    """
    Controlador base para la arquitectura MVC.
    Proporciona métodos auxiliares para formatear respuestas y validar estados.
    """

    @staticmethod
    def respuesta_exito(datos: Any = None, mensaje: str = "Operación realizada con éxito") -> Dict[str, Any]:
        return {
            "exito": True,
            "datos": datos,
            "mensaje": mensaje,
            "error": None
        }

    @staticmethod
    def respuesta_error(mensaje: str, datos: Any = None) -> Dict[str, Any]:
        return {
            "exito": False,
            "datos": datos,
            "mensaje": mensaje,
            "error": mensaje
        }
