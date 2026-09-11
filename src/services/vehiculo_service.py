from src.repositories.vehiculo_repository import VehiculoRepository
from src.models.enums import EstadoVehiculo

class VehiculoService:
    @staticmethod
    def listar_vehiculos(search_term=None, status_filter=None):
        return VehiculoRepository.get_all(search_term, status_filter)

    @staticmethod
    def obtener_vehiculo(id_vehiculo):
        return VehiculoRepository.get_by_id(id_vehiculo)

    @staticmethod
    def registrar_vehiculo(id_socio, numero_unidad, placa, marca_modelo, ano=None, kilometraje_actual=0, status="Activo"):
    def registrar_vehiculo(id_socio, numero_unidad, placa, marca_modelo, ano=None, kilometraje_actual=0, status=EstadoVehiculo.ACTIVO.value):
        if not id_socio:
            raise ValueError("Debe seleccionar un socio propietario.")
        if not numero_unidad or not numero_unidad.strip():
            raise ValueError("El número de unidad es obligatorio (ej. '01', '14').")
        if not placa or not placa.strip():
            raise ValueError("La placa del vehículo es obligatoria.")
        if not marca_modelo or not marca_modelo.strip():
            raise ValueError("La marca/modelo es obligatoria.")

        # Validar unicidad de placa
        placa_existente = VehiculoRepository.get_by_placa(placa)
        if placa_existente:
            raise ValueError(f"Ya existe un vehículo registrado con la placa '{placa.upper()}'.")

        # Validar unicidad de número de unidad
        unidad_existente = VehiculoRepository.get_by_unidad(numero_unidad)
        if unidad_existente:
            raise ValueError(f"El número de unidad '{numero_unidad}' ya está asignado a otro vehículo.")

        try:
            km = int(kilometraje_actual) if kilometraje_actual else 0
            if km < 0:
                raise ValueError()
        except ValueError:
            raise ValueError("El kilometraje actual debe ser un número entero mayor o igual a cero.")

        ano_val = None
        if ano:
            try:
                ano_val = int(ano)
                if ano_val < 1950 or ano_val > 2100:
                    raise ValueError()
            except ValueError:
                raise ValueError("El año debe ser un número válido (ej. 2012).")

        return VehiculoRepository.create(
            id_socio=id_socio,
            numero_unidad=numero_unidad,
            placa=placa,
            marca_modelo=marca_modelo,
            ano=ano_val,
            kilometraje_actual=km,
            status=status
        )

    @staticmethod
    def actualizar_vehiculo(id_vehiculo, id_socio, numero_unidad, placa, marca_modelo, ano, kilometraje_actual, status):
        if not id_vehiculo:
            raise ValueError("ID de vehículo inválido.")
        if not id_socio:
            raise ValueError("Debe seleccionar un socio propietario.")
        if not numero_unidad or not numero_unidad.strip():
            raise ValueError("El número de unidad es obligatorio.")
        if not placa or not placa.strip():
            raise ValueError("La placa es obligatoria.")
        if not marca_modelo or not marca_modelo.strip():
            raise ValueError("La marca/modelo es obligatoria.")

        # Validar que no choque con otra placa
        placa_existente = VehiculoRepository.get_by_placa(placa)
        if placa_existente and placa_existente["id_vehiculo"] != id_vehiculo:
            raise ValueError(f"La placa '{placa.upper()}' ya está registrada en otra unidad.")

        # Validar que no choque con otro número de unidad
        unidad_existente = VehiculoRepository.get_by_unidad(numero_unidad)
        if unidad_existente and unidad_existente["id_vehiculo"] != id_vehiculo:
            raise ValueError(f"El número de unidad '{numero_unidad}' ya está en uso por otra unidad.")

        try:
            km = int(kilometraje_actual) if kilometraje_actual else 0
            if km < 0:
                raise ValueError()
        except ValueError:
            raise ValueError("El kilometraje actual debe ser un número entero mayor o igual a cero.")

        ano_val = None
        if ano:
            try:
                ano_val = int(ano)
            except ValueError:
                raise ValueError("El año debe ser un número entero válido.")

        return VehiculoRepository.update(
            id_vehiculo=id_vehiculo,
            id_socio=id_socio,
            numero_unidad=numero_unidad,
            placa=placa,
            marca_modelo=marca_modelo,
            ano=ano_val,
            kilometraje_actual=km,
            status=status
        )

    @staticmethod
    def actualizar_kilometraje(id_vehiculo, nuevo_km):
        try:
            km = int(nuevo_km)
            if km < 0:
                raise ValueError()
        except ValueError:
            raise ValueError("El kilometraje debe ser un número entero positivo.")

        vehiculo = VehiculoRepository.get_by_id(id_vehiculo)
        if not vehiculo:
            raise ValueError("Vehículo no encontrado.")

        if km < vehiculo["kilometraje_actual"]:
            raise ValueError(f"El nuevo odómetro ({km} km) no puede ser inferior al actual ({vehiculo['kilometraje_actual']} km).")

        return VehiculoRepository.update_kilometraje(id_vehiculo, km)

    @staticmethod
    def eliminar_vehiculo(id_vehiculo):
        return VehiculoRepository.delete(id_vehiculo)

