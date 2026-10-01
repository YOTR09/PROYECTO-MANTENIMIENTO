import warnings
from src.controllers.auth_controller import AuthController

class AutenticacionService:
    """
    [DEPRECADO] Este servicio legado ha sido reemplazado por AuthController y SeguridadService.
    Se mantiene por compatibilidad hacia atrás delegando en la autenticación oficial con PBKDF2.
    """
    @classmethod
    def validar_credenciales(cls, usuario: str, contrasena: str) -> bool:
        warnings.warn(
            "AutenticacionService está deprecado. Utilice AuthController.login() en su lugar.",
            DeprecationWarning,
            stacklevel=2
        )
        ok, _, _ = AuthController.login(usuario, contrasena)
        return ok