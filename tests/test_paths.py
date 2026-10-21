import os
import sys
import unittest
from unittest.mock import patch
from config.paths import is_frozen, get_resource_dir, get_app_dir, get_asset_path


class TestPaths(unittest.TestCase):

    def test_modo_desarrollo_normal(self):
        """En desarrollo normal, is_frozen es False y las rutas apuntan a la raíz del proyecto."""
        self.assertFalse(is_frozen())
        root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.assertEqual(get_resource_dir(), root_dir)
        self.assertEqual(get_app_dir(), root_dir)
        self.assertTrue(os.path.exists(get_asset_path("icono_empresa.png")))
        self.assertTrue(os.path.exists(get_asset_path("icono_empresa.ico")))

    def test_modo_ejecutable_congelado_pyinstaller(self):
        """En modo PyInstaller (--onefile), recursos van a _MEIPASS y app_dir al directorio del ejecutable."""
        import tempfile
        base_temp = tempfile.gettempdir()
        fake_meipass = os.path.join(base_temp, "fake_meipass_dir")
        expected_app_dir = os.path.abspath(os.path.join(base_temp, "portable"))
        fake_exe = os.path.join(expected_app_dir, "BrisasDelPalmar")
        with patch.object(sys, "frozen", True, create=True), \
             patch.object(sys, "_MEIPASS", fake_meipass, create=True), \
             patch.object(sys, "executable", fake_exe):
            self.assertTrue(is_frozen())
            self.assertEqual(get_resource_dir(), fake_meipass)
            self.assertEqual(get_app_dir(), expected_app_dir)
            self.assertEqual(
                get_asset_path("logo_empresa_dark.png"),
                os.path.join(fake_meipass, "assets", "logo_empresa_dark.png"),
            )


if __name__ == "__main__":
    unittest.main()

