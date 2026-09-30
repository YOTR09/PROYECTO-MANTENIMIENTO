import hashlib
import secrets

class SeguridadService:
    ITERACIONES = 100_000
    ALGORITMO = "sha256"

    @classmethod
    def generar_salt(cls) -> str:
        """Genera una sal criptográfica segura de 16 bytes en formato hexadecimal."""
        return secrets.token_hex(16)

    @classmethod
    def hashear_contrasena(cls, contrasena: str, salt: str) -> str:
        """Genera un hash PBKDF2-HMAC-SHA256 para la contraseña usando la sal provista."""
        hash_bytes = hashlib.pbkdf2_hmac(
            cls.ALGORITMO,
            contrasena.encode("utf-8"),
            salt.encode("utf-8"),
            cls.ITERACIONES
        )
        return hash_bytes.hex()

    @classmethod
    def verificar_contrasena(cls, contrasena_plana: str, salt: str, password_hash: str) -> bool:
        """Verifica en tiempo constante si la contraseña plana coincide con el hash almacenado."""
        nuevo_hash = cls.hashear_contrasena(contrasena_plana, salt)
        return secrets.compare_digest(nuevo_hash, password_hash)
