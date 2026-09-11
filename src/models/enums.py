from enum import Enum

class EstadoVehiculo(str, Enum):
    ACTIVO = "Activo"
    EN_TALLER = "En Taller"
    INACTIVO = "Inactivo"

class EstadoSocio(str, Enum):
    ACTIVO = "Activo"
    INACTIVO = "Inactivo"

class EstadoMantenimiento(str, Enum):
    AL_DIA = "Al Día"
    POR_VENCER = "Por Vencer"
    VENCIDO = "Vencido"

