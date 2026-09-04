from src.repositories.tipo_mantenimiento_repository import TipoMantenimientoRepository

class TipoMantenimientoService:
    @staticmethod
    def listar_tipos(search_term=None):
        return TipoMantenimientoRepository.get_all(search_term)

    @staticmethod
    def obtener_tipo(id_tipo):
        return TipoMantenimientoRepository.get_by_id(id_tipo)

    @staticmethod
    def registrar_tipo(nombre, descripcion="", intervalo_km=0, intervalo_dias=0):
        if not nombre or not nombre.strip():
            raise ValueError("El nombre de la rutina de mantenimiento es obligatorio.")

        try:
            km = int(intervalo_km) if intervalo_km else 0
            dias = int(intervalo_dias) if intervalo_dias else 0
            if km < 0 or dias < 0:
                raise ValueError()
        except ValueError:
            raise ValueError("Los intervalos de kilómetros y días deben ser números enteros no negativos.")

        if km == 0 and dias == 0:
            raise ValueError("Debe especificar al menos un intervalo mayor a cero (por kilómetros o por días).")

        return TipoMantenimientoRepository.create(nombre, descripcion, km, dias)

    @staticmethod
    def actualizar_tipo(id_tipo, nombre, descripcion="", intervalo_km=0, intervalo_dias=0):
        if not id_tipo:
            raise ValueError("ID de tipo de mantenimiento inválido.")
        if not nombre or not nombre.strip():
            raise ValueError("El nombre es obligatorio.")

        try:
            km = int(intervalo_km) if intervalo_km else 0
            dias = int(intervalo_dias) if intervalo_dias else 0
            if km < 0 or dias < 0:
                raise ValueError()
        except ValueError:
            raise ValueError("Los intervalos de kilómetros y días deben ser números válidos.")

        if km == 0 and dias == 0:
            raise ValueError("Debe especificar al menos un intervalo mayor a cero (por km o días).")

        return TipoMantenimientoRepository.update(id_tipo, nombre, descripcion, km, dias)

    @staticmethod
    def eliminar_tipo(id_tipo):
        return TipoMantenimientoRepository.delete(id_tipo)

