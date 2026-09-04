from src.repositories.socio_repository import SocioRepository
from config.database import get_db_connection

class SocioService:
    @staticmethod
    def listar_socios(search_term=None):
        return SocioRepository.get_all(search_term)

    @staticmethod
    def obtener_socio(id_socio):
        return SocioRepository.get_by_id(id_socio)

    @staticmethod
    def registrar_socio(cedula, nombre_completo, telefono="", estado="Activo"):
        if not cedula or not cedula.strip():
            raise ValueError("La cédula o documento de identidad es obligatorio.")
        if not nombre_completo or not nombre_completo.strip():
            raise ValueError("El nombre completo del socio es obligatorio.")

        existente = SocioRepository.get_by_cedula(cedula)
        if existente:
            raise ValueError(f"Ya existe un socio registrado con la cédula '{cedula}'.")

        return SocioRepository.create(cedula, nombre_completo, telefono, estado)

    @staticmethod
    def actualizar_socio(id_socio, cedula, nombre_completo, telefono="", estado="Activo"):
        if not id_socio:
            raise ValueError("ID de socio inválido.")
        if not cedula or not cedula.strip():
            raise ValueError("La cédula es obligatoria.")
        if not nombre_completo or not nombre_completo.strip():
            raise ValueError("El nombre completo es obligatorio.")

        existente = SocioRepository.get_by_cedula(cedula)
        if existente and existente["id_socio"] != id_socio:
            raise ValueError(f"La cédula '{cedula}' ya pertenece a otro socio.")

        return SocioRepository.update(id_socio, cedula, nombre_completo, telefono, estado)

    @staticmethod
    def eliminar_socio(id_socio):
        # Validar si tiene vehículos asociados antes de eliminar
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM vehiculo WHERE id_socio = ?", (id_socio,))
        unidades = cursor.fetchone()[0]
        conn.close()

        if unidades > 0:
            raise ValueError(f"No se puede eliminar el socio porque tiene {unidades} unidad(es) asociada(s). Reasigne o elimine primero sus vehículos.")

        return SocioRepository.delete(id_socio)

