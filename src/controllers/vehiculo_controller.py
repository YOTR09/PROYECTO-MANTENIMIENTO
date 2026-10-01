from src.controllers.base_controller import BaseController
from src.repositories.vehiculo_repository import VehiculoRepository
from src.models.vehiculo import Vehiculo
from src.models.enums import EstadoVehiculo
from typing import List, Optional, Tuple

class VehiculoController(BaseController):
    @staticmethod
    def listar_vehiculos(search_term: Optional[str] = None, status_filter: Optional[str] = None, solo_activos: bool = True) -> List[Vehiculo]:
        filas = VehiculoRepository.get_all(search_term=search_term, status_filter=status_filter, solo_activos=solo_activos)
        return [Vehiculo.from_dict(row) for row in filas]

    @staticmethod
    def obtener_vehiculo(id_vehiculo: int) -> Optional[Vehiculo]:
        fila = VehiculoRepository.get_by_id(id_vehiculo)
        return Vehiculo.from_dict(fila) if fila else None

    @staticmethod
    def registrar_vehiculo(
        id_socio: int,
        numero_unidad: str,
        placa: str,
        marca_modelo: str,
        ano: Optional[int] = None,
        kilometraje_actual: int = 0,
        status: str = EstadoVehiculo.ACTIVO.value,
        permitir_reactivacion: bool = False
    ) -> Tuple[bool, Optional[Vehiculo], str]:
        if not id_socio:
            return False, None, "Debe seleccionar un socio propietario."
        if not numero_unidad or not numero_unidad.strip():
            return False, None, "El número de unidad es obligatorio (ej. '01', '14')."
        if not placa or not placa.strip():
            return False, None, "La placa del vehículo es obligatoria."
        if not marca_modelo or not marca_modelo.strip():
            return False, None, "La marca/modelo es obligatoria."

        km = int(kilometraje_actual) if kilometraje_actual else 0
        try:
            km = int(kilometraje_actual) if kilometraje_actual else 0
            if km < 0:
                raise ValueError()
        except (ValueError, TypeError):
            return False, None, "El kilometraje actual debe ser un número entero mayor o igual a cero."

        ano_val = None
        if ano:
            try:
                ano_val = int(ano)
                if ano_val < 1950 or ano_val > 2100:
                    raise ValueError()
            except (ValueError, TypeError):
                return False, None, "El año debe ser un número válido entre 1950 y 2100."

        # Validar unicidad de placa (activa o inactiva)
        placa_existente = VehiculoRepository.get_by_placa(placa, solo_activos=False)
        if placa_existente:
            if placa_existente["activo"] == 1:
                return False, None, f"Ya existe un vehículo activo registrado con la placa '{placa.upper().strip()}'."
            if permitir_reactivacion:
                return VehiculoController.reactivar_vehiculo(
                    id_vehiculo=placa_existente["id_vehiculo"],
                    id_socio=id_socio,
                    numero_unidad=numero_unidad.strip(),
                    placa=placa.strip().upper(),
                    marca_modelo=marca_modelo.strip(),
                    ano=ano_val,
                    kilometraje_actual=km,
                    status=status
                )
            return False, None, f"EXISTE_INACTIVO:{placa_existente['id_vehiculo']}:{placa_existente['numero_unidad']}"

        # Validar unicidad de número de unidad
        unidad_existente = VehiculoRepository.get_by_unidad(numero_unidad, solo_activos=False)
        if unidad_existente:
            if unidad_existente["activo"] == 1:
                return False, None, f"El número de unidad '{numero_unidad.strip()}' ya está asignado a otro vehículo activo."
            if permitir_reactivacion:
                return VehiculoController.reactivar_vehiculo(
                    id_vehiculo=unidad_existente["id_vehiculo"],
                    id_socio=id_socio,
                    numero_unidad=numero_unidad.strip(),
                    placa=placa.strip().upper(),
                    marca_modelo=marca_modelo.strip(),
                    ano=ano_val,
                    kilometraje_actual=km,
                    status=status
                )
            return False, None, f"EXISTE_INACTIVO:{unidad_existente['id_vehiculo']}:{unidad_existente['numero_unidad']}"

        try:
            nuevo_id = VehiculoRepository.create(
                id_socio=id_socio,
                numero_unidad=numero_unidad.strip(),
                placa=placa.strip().upper(),
                marca_modelo=marca_modelo.strip(),
                ano=ano_val,
                kilometraje_actual=km,
                status=status
            )
            vehiculo = VehiculoController.obtener_vehiculo(nuevo_id)
            return True, vehiculo, "Vehículo registrado exitosamente."
        except Exception as e:
            return False, None, f"Error al registrar la unidad: {str(e)}"

    @staticmethod
    def reactivar_vehiculo(
        id_vehiculo: int,
        id_socio: int,
        numero_unidad: str,
        placa: str,
        marca_modelo: str,
        ano: Optional[int],
        kilometraje_actual: int,
        status: str
    ) -> Tuple[bool, Optional[Vehiculo], str]:
        ok, msg = VehiculoController.actualizar_vehiculo(
            id_vehiculo=id_vehiculo,
            id_socio=id_socio,
            numero_unidad=numero_unidad,
            placa=placa,
            marca_modelo=marca_modelo,
            ano=ano,
            kilometraje_actual=kilometraje_actual,
            status=status
        )
        if not ok:
            return False, None, msg
        VehiculoRepository.restore(id_vehiculo)
        vehiculo = VehiculoController.obtener_vehiculo(id_vehiculo)
        return True, vehiculo, f"Unidad {numero_unidad} ({placa}) reactivada exitosamente."

    @staticmethod
    def actualizar_vehiculo(
        id_vehiculo: int,
        id_socio: int,
        numero_unidad: str,
        placa: str,
        marca_modelo: str,
        ano: Optional[int],
        kilometraje_actual: int,
        status: str
    ) -> Tuple[bool, str]:
        if not id_vehiculo:
            return False, "ID de vehículo inválido."
        if not id_socio:
            return False, "Debe seleccionar un socio propietario."
        if not numero_unidad or not numero_unidad.strip():
            return False, "El número de unidad es obligatorio."
        if not placa or not placa.strip():
            return False, "La placa es obligatoria."
        if not marca_modelo or not marca_modelo.strip():
            return False, "La marca/modelo es obligatoria."

        placa_existente = VehiculoRepository.get_by_placa(placa, solo_activos=True)
        if placa_existente and placa_existente["id_vehiculo"] != id_vehiculo:
            return False, f"La placa '{placa.upper().strip()}' ya pertenece a otra unidad activa."

        unidad_existente = VehiculoRepository.get_by_unidad(numero_unidad, solo_activos=True)
        if unidad_existente and unidad_existente["id_vehiculo"] != id_vehiculo:
            return False, f"El número de unidad '{numero_unidad.strip()}' ya está en uso por otra unidad activa."

        try:
            km = int(kilometraje_actual) if kilometraje_actual else 0
            if km < 0:
                raise ValueError()
        except (ValueError, TypeError):
            return False, "El kilometraje debe ser un entero mayor o igual a cero."

        ano_val = None
        if ano:
            try:
                ano_val = int(ano)
            except (ValueError, TypeError):
                return False, "El año debe ser un número entero válido."

        try:
            VehiculoRepository.update(
                id_vehiculo=id_vehiculo,
                id_socio=id_socio,
                numero_unidad=numero_unidad.strip(),
                placa=placa.strip().upper(),
                marca_modelo=marca_modelo.strip(),
                ano=ano_val,
                kilometraje_actual=km,
                status=status
            )
            return True, "Datos del vehículo actualizados exitosamente."
        except Exception as e:
            return False, f"Error al actualizar el vehículo: {str(e)}"

    @staticmethod
    def actualizar_kilometraje(id_vehiculo: int, nuevo_km: int) -> Tuple[bool, str]:
        try:
            km = int(nuevo_km)
            if km < 0:
                raise ValueError()
        except (ValueError, TypeError):
            return False, "El odómetro debe ser un número entero no negativo."

        vehiculo = VehiculoRepository.get_by_id(id_vehiculo)
        if not vehiculo:
            return False, "Vehículo no encontrado."

        if km < vehiculo["kilometraje_actual"]:
            return False, f"El nuevo odómetro ({km:,} km) no puede ser inferior al actual ({vehiculo['kilometraje_actual']:,} km)."

        VehiculoRepository.update_kilometraje(id_vehiculo, km)
        return True, "Kilometraje actualizado exitosamente."

    @staticmethod
    def eliminar_vehiculo(id_vehiculo: int, logico: bool = True) -> Tuple[bool, str]:
        try:
            exito = VehiculoRepository.delete(id_vehiculo, logico=logico)
            if exito:
                msg = "Vehículo retirado de flota (eliminación lógica) exitosamente." if logico else "Vehículo eliminado físicamente."
                return True, msg
            return False, "No se encontró el vehículo especificado."
        except Exception as e:
            return False, f"Error al dar de baja el vehículo: {str(e)}"
