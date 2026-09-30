from src.controllers.base_controller import BaseController
from src.repositories.usuario_repository import UsuarioRepository
from src.services.seguridad_service import SeguridadService
from src.models.usuario import Usuario
from typing import Optional, Tuple

class AuthController(BaseController):
    _usuario_sesion: Optional[Usuario] = None

    @classmethod
    def login(cls, username: str, contrasena: str) -> Tuple[bool, Optional[Usuario], str]:
        """
        Valida las credenciales contra la base de datos utilizando PBKDF2 y salt.
        Retorna (exito, usuario_obj, mensaje).
        """
        if not username or not username.strip():
            return False, None, "Debe ingresar el nombre de usuario."
        if not contrasena:
            return False, None, "Debe ingresar la contraseña."

        datos_usuario = UsuarioRepository.get_by_username(username.strip())
        if not datos_usuario:
            return False, None, "Usuario o contraseña incorrectos."

        if datos_usuario.get("activo", 1) != 1:
            return False, None, "Esta cuenta de usuario se encuentra inactiva."

        salt = datos_usuario.get("salt", "")
        hash_almacenado = datos_usuario.get("password_hash", "")

        valida = SeguridadService.verificar_contrasena(contrasena, salt, hash_almacenado)
        if not valida:
            return False, None, "Usuario o contraseña incorrectos."

        usuario = Usuario.from_dict(datos_usuario)
        cls._usuario_sesion = usuario
        return True, usuario, "Autenticación exitosa."

    @classmethod
    def logout(cls):
        cls._usuario_sesion = None

    @classmethod
    def get_sesion_actual(cls) -> Optional[Usuario]:
        return cls._usuario_sesion

    @classmethod
    def cambiar_contrasena(cls, id_usuario: int, actual: str, nueva: str) -> Tuple[bool, str]:
        if not nueva or len(nueva) < 4:
            return False, "La nueva contraseña debe tener al menos 4 caracteres."

        datos = UsuarioRepository.get_by_id(id_usuario)
        if not datos:
            return False, "Usuario no encontrado."

        valida = SeguridadService.verificar_contrasena(actual, datos["salt"], datos["password_hash"])
        if not valida:
            return False, "La contraseña actual es incorrecta."

        nuevo_salt = SeguridadService.generar_salt()
        nuevo_hash = SeguridadService.hashear_contrasena(nueva, nuevo_salt)
        UsuarioRepository.update_password(id_usuario, nuevo_hash, nuevo_salt)
        return True, "Contraseña actualizada exitosamente."
