from src.controllers.base_controller import BaseController
from src.repositories.socio_repository import SocioRepository
from src.repositories.vehiculo_repository import VehiculoRepository
from src.models.socio import Socio
from typing import List, Optional, Tuple

class SocioController(BaseController):
    @staticmethod
    def listar_socios(search_term: Optional[str] = None, solo_activos: bool = True) -> List[Socio]:
        filas = SocioRepository.get_all(search_term=search_term, solo_activos=solo_activos)
        return [Socio.from_dict(row) for row in filas]

    @staticmethod
    def obtener_socio(id_socio: int) -> Optional[Socio]:
        fila = SocioRepository.get_by_id(id_socio)
        return Socio.from_dict(fila) if fila else None

    @staticmethod
    def registrar_socio(cedula: str, nombre_completo: str, telefono: str = "", estado: str = "Activo") -> Tuple[bool, Optional[Socio], str]:
        if not cedula or not cedula.strip():
            return False, None, "La cédula o documento de identidad es obligatorio."
        if not nombre_completo or not nombre_completo.strip():
            return False, None, "El nombre completo del socio es obligatorio."

        existente = SocioRepository.get_by_cedula(cedula, solo_activos=True)
        if existente:
            return False, None, f"Ya existe un socio registrado con la cédula '{cedula.strip()}'."

        try:
            nuevo_id = SocioRepository.create(
                cedula=cedula.strip(),
                nombre_completo=nombre_completo.strip(),
                telefono=telefono.strip() if telefono else "",
                estado=estado
            )
            socio = SocioController.obtener_socio(nuevo_id)
            return True, socio, "Socio registrado exitosamente."
        except Exception as e:
            return False, None, f"Error al registrar el socio: {str(e)}"

    @staticmethod
    def actualizar_socio(id_socio: int, cedula: str, nombre_completo: str, telefono: str = "", estado: str = "Activo") -> Tuple[bool, str]:
        if not id_socio:
            return False, "ID de socio inválido."
        if not cedula or not cedula.strip():
            return False, "La cédula es obligatoria."
        if not nombre_completo or not nombre_completo.strip():
            return False, "El nombre completo es obligatorio."

        existente = SocioRepository.get_by_cedula(cedula, solo_activos=False)
        if existente and existente["id_socio"] != id_socio:
            return False, f"La cédula '{cedula.strip()}' ya pertenece a otro socio."

        try:
            SocioRepository.update(
                id_socio=id_socio,
                cedula=cedula.strip(),
                nombre_completo=nombre_completo.strip(),
                telefono=telefono.strip() if telefono else "",
                estado=estado
            )
            return True, "Datos del socio actualizados exitosamente."
        except Exception as e:
            return False, f"Error al actualizar el socio: {str(e)}"

    @staticmethod
    def eliminar_socio(id_socio: int, logico: bool = True) -> Tuple[bool, str]:
        # Validar si tiene vehículos activos asociados
        vehiculos = VehiculoRepository.get_all(solo_activos=True)
        asociados = [v for v in vehiculos if v["id_socio"] == id_socio]
        if asociados:
            return False, f"No se puede dar de baja al socio porque tiene {len(asociados)} vehículo(s) activo(s) asignado(s). Reasigne o elimine primero sus unidades."

        try:
            exito = SocioRepository.delete(id_socio, logico=logico)
            if exito:
                msg = "Socio dado de baja (eliminación lógica) exitosamente." if logico else "Socio eliminado físicamente."
                return True, msg
            return False, "No se encontró el socio especificado."
        except Exception as e:
            return False, f"Error al procesar la baja del socio: {str(e)}"
