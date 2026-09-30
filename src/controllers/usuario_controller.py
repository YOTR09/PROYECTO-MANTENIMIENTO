from src.controllers.base_controller import BaseController
from src.repositories.usuario_repository import UsuarioRepository
from src.services.seguridad_service import SeguridadService
from src.models.usuario import Usuario
from src.models.rol import Rol
from typing import List, Optional, Tuple

class UsuarioController(BaseController):
    @staticmethod
    def listar_usuarios(search_term: Optional[str] = None, solo_activos: bool = True) -> List[Usuario]:
        filas = UsuarioRepository.get_all(search_term=search_term, solo_activos=solo_activos)
        return [Usuario.from_dict(row) for row in filas]

    @staticmethod
    def obtener_usuario(id_usuario: int) -> Optional[Usuario]:
        fila = UsuarioRepository.get_by_id(id_usuario)
        return Usuario.from_dict(fila) if fila else None

    @staticmethod
    def listar_roles() -> List[Rol]:
        filas = UsuarioRepository.get_roles()
        return [Rol.from_dict(row) for row in filas]

    @staticmethod
    def registrar_usuario(
        id_rol: int,
        username: str,
        contrasena: str,
        nombre_completo: str
    ) -> Tuple[bool, Optional[Usuario], str]:
        if not id_rol:
            return False, None, "Debe seleccionar un rol o nivel de acceso."
        if not username or not username.strip():
            return False, None, "El nombre de usuario es obligatorio."
        if not contrasena or len(contrasena.strip()) < 4:
            return False, None, "La contraseña debe tener un mínimo de 4 caracteres."
        if not nombre_completo or not nombre_completo.strip():
            return False, None, "El nombre completo del usuario es obligatorio."

        usuario_existente = UsuarioRepository.get_by_username(username.strip())
        if usuario_existente:
            return False, None, f"El nombre de usuario '{username.strip()}' ya está registrado."

        salt = SeguridadService.generar_salt()
        pwd_hash = SeguridadService.hashear_contrasena(contrasena.strip(), salt)

        try:
            nuevo_id = UsuarioRepository.create(
                id_rol=id_rol,
                username=username.strip().lower(),
                password_hash=pwd_hash,
                salt=salt,
                nombre_completo=nombre_completo.strip(),
                activo=1
            )
            usuario = UsuarioController.obtener_usuario(nuevo_id)
            return True, usuario, "Usuario creado exitosamente con contraseña cifrada."
        except Exception as e:
            return False, None, f"Error al crear el usuario: {str(e)}"

    @staticmethod
    def actualizar_usuario(
        id_usuario: int,
        id_rol: int,
        nombre_completo: str,
        activo: int = 1
    ) -> Tuple[bool, str]:
        if not id_usuario:
            return False, "ID de usuario inválido."
        if not id_rol:
            return False, "Debe seleccionar un rol válido."
        if not nombre_completo or not nombre_completo.strip():
            return False, "El nombre completo es obligatorio."

        try:
            UsuarioRepository.update(
                id_usuario=id_usuario,
                id_rol=id_rol,
                nombre_completo=nombre_completo.strip(),
                activo=activo
            )
            return True, "Datos de usuario actualizados exitosamente."
        except Exception as e:
            return False, f"Error al actualizar el usuario: {str(e)}"

    @staticmethod
    def restablecer_contrasena(id_usuario: int, nueva_contrasena: str) -> Tuple[bool, str]:
        if not nueva_contrasena or len(nueva_contrasena.strip()) < 4:
            return False, "La nueva contraseña debe tener al menos 4 caracteres."

        salt = SeguridadService.generar_salt()
        pwd_hash = SeguridadService.hashear_contrasena(nueva_contrasena.strip(), salt)

        try:
            UsuarioRepository.update_password(id_usuario, pwd_hash, salt)
            return True, "Contraseña restablecida exitosamente."
        except Exception as e:
            return False, f"Error al restablecer la contraseña: {str(e)}"

    @staticmethod
    def eliminar_usuario(id_usuario: int, logico: bool = True) -> Tuple[bool, str]:
        if id_usuario == 1:
            return False, "No se puede dar de baja al usuario administrador principal del sistema."

        try:
            UsuarioRepository.delete(id_usuario, logico=logico)
            msg = "Usuario dado de baja (eliminación lógica) exitosamente." if logico else "Usuario eliminado físicamente."
            return True, msg
        except Exception as e:
            return False, f"Error al eliminar usuario: {str(e)}"
