import unittest
import os
import tempfile
from datetime import date
from config.database import init_db, get_db_cursor
from src.services.seguridad_service import SeguridadService
from src.controllers.auth_controller import AuthController
from src.controllers.socio_controller import SocioController
from src.controllers.vehiculo_controller import VehiculoController
from src.controllers.mantenimiento_controller import MantenimientoController
from src.controllers.usuario_controller import UsuarioController
from src.controllers.reporte_controller import ReporteController
from src.models.usuario import Usuario

class TestSistemaIntegral(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.environ["TESTING"] = "1"
        init_db()

    def setUp(self):
        # Limpiar datos asegurando consistencia de pruebas
        with get_db_cursor(commit=True) as cur:
            cur.execute("DELETE FROM historial_mantenimiento")
            cur.execute("DELETE FROM mantenimiento_programado")
            cur.execute("DELETE FROM vehiculo")
            cur.execute("DELETE FROM socio")
            # Dejamos usuario 1 (admin), 2 (mecanico), 3 (auditor)
            cur.execute("DELETE FROM usuario WHERE id_usuario > 3")
            cur.execute("UPDATE usuario SET activo = 1")

    # 1. PRUEBAS DE SEGURIDAD, HASHING Y ROLES
    def test_hashing_seguro_pbkdf2(self):
        salt1 = SeguridadService.generar_salt()
        salt2 = SeguridadService.generar_salt()
        self.assertNotEqual(salt1, salt2, "Las sales deben ser únicas y aleatorias")

        pwd = "miClaveSegura2026*"
        hash1 = SeguridadService.hashear_contrasena(pwd, salt1)
        hash2 = SeguridadService.hashear_contrasena(pwd, salt2)
        self.assertNotEqual(hash1, hash2, "El mismo password con diferente sal debe producir hashes distintos")

        self.assertTrue(SeguridadService.verificar_contrasena(pwd, salt1, hash1))
        self.assertFalse(SeguridadService.verificar_contrasena("otraClave", salt1, hash1))

    def test_autenticacion_3_niveles(self):
        # 1. Administrador
        ok, user_admin, _ = AuthController.login("admin", "admin123")
        self.assertTrue(ok)
        self.assertTrue(user_admin.es_admin)
        self.assertTrue(user_admin.puede_eliminar())
        self.assertTrue(user_admin.puede_gestionar_usuarios())

        # 2. Mecánico
        ok, user_mec, _ = AuthController.login("mecanico", "mecanico123")
        self.assertTrue(ok)
        self.assertTrue(user_mec.es_mecanico)
        self.assertFalse(user_mec.puede_eliminar())
        self.assertFalse(user_mec.puede_gestionar_usuarios())
        self.assertTrue(user_mec.puede_gestionar_mantenimiento())

        # 3. Operador
        ok, user_op, _ = AuthController.login("auditor", "auditor123")
        self.assertTrue(ok)
        self.assertTrue(user_op.es_operador)
        self.assertFalse(user_op.puede_eliminar())
        self.assertFalse(user_op.puede_modificar_flota())
        self.assertTrue(user_op.puede_generar_reportes())

        # 4. Credencial errónea
        ok, user_bad, msg = AuthController.login("admin", "claveIncorrecta")
        self.assertFalse(ok)
        self.assertIsNone(user_bad)

    # 2. PRUEBAS DE ELIMINACIÓN LÓGICA (SOFT DELETE)
    def test_eliminacion_logica_socio_y_vehiculo(self):
        # Registrar Socio
        ok, socio, _ = SocioController.registrar_socio("V-88888888", "Socio Prueba SoftDelete", "0412-1112233")
        self.assertTrue(ok)
        id_socio = socio.id_socio

        # Registrar Vehículo
        ok, vehiculo, _ = VehiculoController.registrar_vehiculo(
            id_socio=id_socio,
            numero_unidad="99",
            placa="AB999CD",
            marca_modelo="Yutong ZK6100",
            ano=2016,
            kilometraje_actual=80000
        )
        self.assertTrue(ok)
        id_veh = vehiculo.id_vehiculo

        # Validar que aparecen en listado activo
        activos_v = VehiculoController.listar_vehiculos(solo_activos=True)
        self.assertTrue(any(v.id_vehiculo == id_veh for v in activos_v))

        # Realizar baja lógica del vehículo
        ok, msg = VehiculoController.eliminar_vehiculo(id_veh, logico=True)
        self.assertTrue(ok)

        # Ya NO debe aparecer en la lista de activos
        activos_v_post = VehiculoController.listar_vehiculos(solo_activos=True)
        self.assertFalse(any(v.id_vehiculo == id_veh for v in activos_v_post), "El vehículo eliminado lógicamente no debe figurar en activos")

        # Pero DEBE existir en la base de datos con activo = 0
        todos_v = VehiculoController.listar_vehiculos(solo_activos=False)
        v_en_bd = next((v for v in todos_v if v.id_vehiculo == id_veh), None)
        self.assertIsNotNone(v_en_bd)
        self.assertEqual(v_en_bd.activo, 0, "El campo activo debe ser 0 en la BD")

        # Ahora el socio ya no tiene vehículos activos, se puede dar de baja lógica
        ok, msg = SocioController.eliminar_socio(id_socio, logico=True)
        self.assertTrue(ok)

        activos_s_post = SocioController.listar_socios(solo_activos=True)
        self.assertFalse(any(s.id_socio == id_socio for s in activos_s_post))

    # 3. PRUEBAS DE CONTROLADOR DE USUARIOS
    def test_gestion_usuarios_controller(self):
        # Registrar nuevo usuario
        ok, nuevo_u, _ = UsuarioController.registrar_usuario(
            id_rol=2,
            username="tecnico_nuevo",
            contrasena="segura123",
            nombre_completo="Técnico de Turno"
        )
        self.assertTrue(ok)
        self.assertIsNotNone(nuevo_u)

        # Probar login con el nuevo usuario
        ok_login, u_log, _ = AuthController.login("tecnico_nuevo", "segura123")
        self.assertTrue(ok_login)
        self.assertEqual(u_log.username, "tecnico_nuevo")

        # Baja lógica del usuario
        ok_del, _ = UsuarioController.eliminar_usuario(nuevo_u.id_usuario, logico=True)
        self.assertTrue(ok_del)

        # Intento de login de usuario inactivo debe ser rechazado
        ok_login_inactivo, _, msg = AuthController.login("tecnico_nuevo", "segura123")
        self.assertFalse(ok_login_inactivo)
        self.assertIn("inactiva", msg.lower())

    # 4. PRUEBA DE GENERACIÓN DE LOS 5 REPORTES
    def test_generacion_cinco_reportes(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            r1_path = os.path.join(tmpdir, "r1.pdf")
            r2_path = os.path.join(tmpdir, "r2.pdf")
            r3_path = os.path.join(tmpdir, "r3.xlsx")
            r4_path = os.path.join(tmpdir, "r4.pdf")
            r5_path = os.path.join(tmpdir, "r5.xlsx")

            # Reporte 1: PDF Flota
            ok1, _ = ReporteController.generar_reporte_1_flota_pdf(r1_path)
            self.assertTrue(ok1)
            self.assertTrue(os.path.exists(r1_path))
            with open(r1_path, "rb") as f:
                self.assertTrue(f.read().startswith(b"%PDF"), "Debe ser un archivo PDF válido")

            # Reporte 2: PDF Preventivo
            ok2, _ = ReporteController.generar_reporte_2_preventivo_pdf(r2_path)
            self.assertTrue(ok2)
            self.assertTrue(os.path.exists(r2_path))
            with open(r2_path, "rb") as f:
                self.assertTrue(f.read().startswith(b"%PDF"))

            # Reporte 3: Excel Historial
            ok3, _ = ReporteController.generar_reporte_3_historial_excel(r3_path)
            self.assertTrue(ok3)
            self.assertTrue(os.path.exists(r3_path))
            self.assertGreater(os.path.getsize(r3_path), 1000)

            # Reporte 4: PDF Socios
            ok4, _ = ReporteController.generar_reporte_4_socios_pdf(r4_path)
            self.assertTrue(ok4)
            self.assertTrue(os.path.exists(r4_path))
            with open(r4_path, "rb") as f:
                self.assertTrue(f.read().startswith(b"%PDF"))

            # Reporte 5: Excel Métricas
            ok5, _ = ReporteController.generar_reporte_5_metricas_excel(r5_path)
            self.assertTrue(ok5)
            self.assertTrue(os.path.exists(r5_path))
            self.assertGreater(os.path.getsize(r5_path), 1000)

if __name__ == "__main__":
    unittest.main()
