import unittest
import os
import sqlite3
from datetime import date, timedelta

# Aseguramos importar con DB de test
os.environ["TESTING"] = "1"
from config.database import init_db, get_db_connection
from src.services.socio_service import SocioService
from src.services.vehiculo_service import VehiculoService
from src.services.tipo_mantenimiento_service import TipoMantenimientoService
from src.services.mantenimiento_service import MantenimientoService

class TestSistemaMantenimiento(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        init_db()

    def setUp(self):
        # Limpiar datos para pruebas limpias
        conn = get_db_connection()
        conn.execute("DELETE FROM historial_mantenimiento")
        conn.execute("DELETE FROM mantenimiento_programado")
        conn.execute("DELETE FROM vehiculo")
        conn.execute("DELETE FROM socio")
        conn.commit()
        conn.close()

    def test_flujo_socio_y_vehiculo(self):
        # 1. Registrar Socio
        id_socio = SocioService.registrar_socio(
            cedula="V-12345678",
            nombre_completo="Carlos Perez",
            telefono="0414-1234567"
        )
        self.assertIsNotNone(id_socio)
        
        # Validar no duplicar cédula
        with self.assertRaises(ValueError):
            SocioService.registrar_socio("V-12345678", "Otro Nombre")

        # 2. Registrar Vehículo con N° de Unidad
        id_vehiculo = VehiculoService.registrar_vehiculo(
            id_socio=id_socio,
            numero_unidad="01",
            placa="A12BC3D",
            marca_modelo="Encava NT-610",
            ano=2015,
            kilometraje_actual=100000,
            status="Activo"
        )
        self.assertIsNotNone(id_vehiculo)

        # Validar no duplicar placa ni unidad
        with self.assertRaises(ValueError):
            VehiculoService.registrar_vehiculo(id_socio, "02", "A12BC3D", "Toyota")
        with self.assertRaises(ValueError):
            VehiculoService.registrar_vehiculo(id_socio, "01", "XYZ999", "Toyota")

        # 3. No permitir borrar socio si tiene unidad
        with self.assertRaises(ValueError):
            SocioService.eliminar_socio(id_socio)

    def test_programacion_mantenimiento_y_alertas(self):
        # Setup socio y vehículo
        id_socio = SocioService.registrar_socio("V-999999", "Juan Conductor")
        id_vehiculo = VehiculoService.registrar_vehiculo(
            id_socio=id_socio,
            numero_unidad="10",
            placa="BB123CC",
            marca_modelo="Toyota Coaster",
            ano=2018,
            kilometraje_actual=50000
        )

        # Tipos de mantenimiento (el catálogo ya tiene semillas)
        tipos = TipoMantenimientoService.listar_tipos()
        tipo_aceite = next(t for t in tipos if "Aceite" in t["nombre"])
        
        # Programar mantenimiento: Aceite a los 50.000 km (intervalo es 5.000 km -> próximo a los 55.000 km)
        id_prog = MantenimientoService.programar_mantenimiento(
            id_vehiculo=id_vehiculo,
            id_tipo=tipo_aceite["id_tipo"],
            fecha_ultimo=date.today().strftime("%Y-%m-%d"),
            km_ultimo=50000
        )
        self.assertIsNotNone(id_prog)

        # 1. Estado inicial: km_actual = 50.000, prox = 55.000 -> Al Día (Verde)
        programaciones = MantenimientoService.listar_programaciones(id_vehiculo=id_vehiculo)
        self.assertEqual(len(programaciones), 1)
        self.assertEqual(programaciones[0]["estado"], "Al Día")

        # 2. Actualizar odómetro a 54.600 km (faltan 400 km -> Por Vencer / Amarillo)
        VehiculoService.actualizar_kilometraje(id_vehiculo, 54600)
        programaciones = MantenimientoService.listar_programaciones(id_vehiculo=id_vehiculo)
        self.assertEqual(programaciones[0]["estado"], "Por Vencer")

        # 3. Actualizar odómetro a 55.100 km (superó el límite -> Vencido / Rojo)
        VehiculoService.actualizar_kilometraje(id_vehiculo, 55100)
        programaciones = MantenimientoService.listar_programaciones(id_vehiculo=id_vehiculo)
        self.assertEqual(programaciones[0]["estado"], "Vencido")

        # 4. Registrar mantenimiento realizado:
        # Debe registrar en historial y reprogramar próximo para 55.100 + 5.000 = 60.100 km
        MantenimientoService.registrar_mantenimiento_realizado(
            id_vehiculo=id_vehiculo,
            id_tipo=tipo_aceite["id_tipo"],
            fecha_realizado=date.today().strftime("%Y-%m-%d"),
            km_al_momento=55100,
            costo=45.0,
            taller="Taller Central Brisas",
            descripcion="Cambio de aceite 15W-40 y filtro nuevo"
        )

        historial = MantenimientoService.listar_historial(id_vehiculo=id_vehiculo)
        self.assertEqual(len(historial), 1)
        self.assertEqual(historial[0]["km_al_momento"], 55100)

        # Verificar que el nuevo estado sea Al Día con próximo servicio en 60.100
        programaciones = MantenimientoService.listar_programaciones(id_vehiculo=id_vehiculo)
        self.assertEqual(programaciones[0]["km_proximo_servicio"], 60100)
        self.assertEqual(programaciones[0]["estado"], "Al Día")

if __name__ == "__main__":
    unittest.main()

