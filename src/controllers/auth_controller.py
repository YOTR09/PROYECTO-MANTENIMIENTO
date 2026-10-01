import os
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

    PREGUNTAS_PREDETERMINADAS = [
        "¿Nombre de la empresa de transporte colectivo?",
        "¿Nombre de tu primera mascota?",
        "¿Ciudad de nacimiento?",
        "¿Modelo de tu primer vehículo?",
        "¿Nombre de tu escuela primaria?",
        "¿Pregunta personalizada?"
    ]

    CLAVE_MAESTRA_EMERGENCIA = os.environ.get("BRISAS_MASTER_KEY", "BRISAS-MASTER-2026")

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

    @classmethod
    def obtener_pregunta_recuperacion(cls, username: str) -> Tuple[bool, Optional[str], str]:
        """Consulta la pregunta de seguridad configurada para un usuario activo."""
        if not username or not username.strip():
            return False, None, "Debe ingresar el nombre de usuario."

        datos = UsuarioRepository.get_by_username(username.strip())
        if not datos:
            return False, None, "El usuario especificado no existe en el sistema."

        if datos.get("activo", 1) != 1:
            return False, None, "Esta cuenta de usuario se encuentra inactiva."

        pregunta = datos.get("pregunta_seguridad") or "¿Nombre de la empresa de transporte colectivo?"
        return True, pregunta, "Pregunta obtenida exitosamente."

    @classmethod
    def restablecer_por_pregunta(cls, username: str, respuesta: str, nueva_contrasena: str, confirmacion: Optional[str] = None) -> Tuple[bool, str]:
        """Restablece la contraseña tras verificar la respuesta a la pregunta secreta."""
        if confirmacion is None:
            confirmacion = nueva_contrasena

        if not username or not username.strip():
            return False, "Debe ingresar el nombre de usuario."
        if not respuesta or not respuesta.strip():
            return False, "Debe ingresar la respuesta a la pregunta secreta."
        if not nueva_contrasena or len(nueva_contrasena) < 4:
            return False, "La nueva contraseña debe tener al menos 4 caracteres."
        if nueva_contrasena != confirmacion:
            return False, "Las contraseñas no coinciden. Verifique e intente nuevamente."

        datos = UsuarioRepository.get_by_username(username.strip())
        if not datos:
            return False, "Usuario no encontrado."
        if datos.get("activo", 1) != 1:
            return False, "Esta cuenta de usuario se encuentra inactiva."

        respuesta_guardada = datos.get("respuesta_seguridad", "")
        if not SeguridadService.verificar_respuesta_seguridad(respuesta, respuesta_guardada):
            return False, "Respuesta de seguridad incorrecta."

        nuevo_salt = SeguridadService.generar_salt()
        nuevo_hash = SeguridadService.hashear_contrasena(nueva_contrasena, nuevo_salt)
        UsuarioRepository.update_password(datos["id_usuario"], nuevo_hash, nuevo_salt)
        return True, "¡Contraseña restablecida exitosamente! Ya puede iniciar sesión con su nueva clave."

    @classmethod
    def restablecer_por_clave_maestra(cls, username: str, clave_maestra: str, nueva_contrasena: str, confirmacion: Optional[str] = None) -> Tuple[bool, str]:
        """Restablece la contraseña utilizando el código maestro de emergencia institucional."""
        if confirmacion is None:
            confirmacion = nueva_contrasena

        if not username or not username.strip():
            return False, "Debe ingresar el nombre de usuario."
        if not clave_maestra or not clave_maestra.strip():
            return False, "Debe ingresar el código maestro de soporte."
        if clave_maestra.strip() != cls.CLAVE_MAESTRA_EMERGENCIA:
            return False, "Código maestro de soporte inválido o no autorizado."
        if not nueva_contrasena or len(nueva_contrasena) < 4:
            return False, "La nueva contraseña debe tener al menos 4 caracteres."
        if nueva_contrasena != confirmacion:
            return False, "Las contraseñas no coinciden."

        datos = UsuarioRepository.get_by_username(username.strip())
        if not datos:
            return False, "Usuario no encontrado."
        if datos.get("activo", 1) != 1:
            return False, "Esta cuenta de usuario se encuentra inactiva."

        nuevo_salt = SeguridadService.generar_salt()
        nuevo_hash = SeguridadService.hashear_contrasena(nueva_contrasena, nuevo_salt)
        UsuarioRepository.update_password(datos["id_usuario"], nuevo_hash, nuevo_salt)
        return True, "¡Contraseña restablecida mediante código maestro! Ya puede iniciar sesión."
