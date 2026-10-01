from src.models.base_model import BaseModel
from typing import Dict, Any, Optional

class Usuario(BaseModel):
    def __init__(
        self,
        id_usuario: Optional[int],
        id_rol: int,
        username: str,
        nombre_completo: str,
        password_hash: str = "",
        salt: str = "",
        pregunta_seguridad: str = "¿Nombre de la empresa de transporte colectivo?",
        respuesta_seguridad: str = "Brisas del Palmar",
        activo: int = 1,
        creado_en: str = "",
        rol_nombre: str = ""
    ):
        self.id_usuario = id_usuario
        self.id_rol = id_rol
        self.username = username
        self.nombre_completo = nombre_completo
        self.password_hash = password_hash
        self.salt = salt
        self.pregunta_seguridad = pregunta_seguridad
        self.respuesta_seguridad = respuesta_seguridad
        self.activo = activo
        self.creado_en = creado_en
        self.rol_nombre = rol_nombre

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Usuario":
        if not data:
            return None
        return cls(
            id_usuario=data.get("id_usuario"),
            id_rol=data.get("id_rol", 0),
            username=data.get("username", ""),
            nombre_completo=data.get("nombre_completo", ""),
            password_hash=data.get("password_hash", ""),
            salt=data.get("salt", ""),
            pregunta_seguridad=data.get("pregunta_seguridad", "¿Nombre de la empresa de transporte colectivo?"),
            respuesta_seguridad=data.get("respuesta_seguridad", "Brisas del Palmar"),
            activo=data.get("activo", 1),
            creado_en=data.get("creado_en", ""),
            rol_nombre=data.get("rol_nombre", "")
        )

    # Métodos de validación de roles y permisos (POO Encapsulación)
    @property
    def es_admin(self) -> bool:
        return self.rol_nombre.lower() == "administrador" or self.id_rol == 1

    @property
    def es_mecanico(self) -> bool:
        return self.rol_nombre.lower() == "mecanico" or self.id_rol == 2

    @property
    def es_operador(self) -> bool:
        return self.rol_nombre.lower() == "operador" or self.id_rol == 3

    def puede_gestionar_usuarios(self) -> bool:
        """Solo el Administrador puede crear, editar o dar de baja usuarios."""
        return self.es_admin

    def puede_eliminar(self) -> bool:
        """Solo el Administrador puede realizar eliminaciones (lógicas) en el sistema."""
        return self.es_admin

    def puede_modificar_flota(self) -> bool:
        """Solo el Administrador puede crear o alterar datos de unidades y socios."""
        return self.es_admin

    def puede_gestionar_mantenimiento(self) -> bool:
        """Administrador y Mecánico pueden programar y registrar mantenimientos ejecutados."""
        return self.es_admin or self.es_mecanico

    def puede_generar_reportes(self) -> bool:
        """Todos los niveles activos tienen acceso a la generación y visualización de reportes."""
        return self.activo == 1
