class AutenticacionService:
    USUARIO_ADMIN = "admin123"
    CONTRASENA_ADMIN = "adminx123"

    @classmethod
    def validar_credenciales(cls, usuario, contrasena):
        return usuario.strip() == cls.USUARIO_ADMIN and contrasena == cls.CONTRASENA_ADMIN