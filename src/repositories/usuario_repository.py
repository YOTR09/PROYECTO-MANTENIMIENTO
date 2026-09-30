from config.database import get_db_cursor

class UsuarioRepository:
    @staticmethod
    def get_all(search_term=None, solo_activos=True):
        with get_db_cursor() as cursor:
            query = """
                SELECT 
                    u.id_usuario,
                    u.id_rol,
                    u.username,
                    u.nombre_completo,
                    u.activo,
                    u.creado_en,
                    r.nombre AS rol_nombre,
                    r.descripcion AS rol_descripcion
                FROM usuario u
                INNER JOIN rol r ON u.id_rol = r.id_rol
                WHERE 1=1
            """
            params = []
            if solo_activos:
                query += " AND u.activo = 1"

            if search_term:
                query += " AND (u.username LIKE ? OR u.nombre_completo LIKE ? OR r.nombre LIKE ?)"
                wildcard = f"%{search_term.strip()}%"
                params.extend([wildcard, wildcard, wildcard])

            query += " ORDER BY u.id_usuario ASC"
            cursor.execute(query, params)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

    @staticmethod
    def get_by_id(id_usuario):
        with get_db_cursor() as cursor:
            query = """
                SELECT 
                    u.id_usuario,
                    u.id_rol,
                    u.username,
                    u.password_hash,
                    u.salt,
                    u.nombre_completo,
                    u.activo,
                    u.creado_en,
                    r.nombre AS rol_nombre
                FROM usuario u
                INNER JOIN rol r ON u.id_rol = r.id_rol
                WHERE u.id_usuario = ?
            """
            cursor.execute(query, (id_usuario,))
            row = cursor.fetchone()
            return dict(row) if row else None

    @staticmethod
    def get_by_username(username):
        with get_db_cursor() as cursor:
            query = """
                SELECT 
                    u.id_usuario,
                    u.id_rol,
                    u.username,
                    u.password_hash,
                    u.salt,
                    u.nombre_completo,
                    u.activo,
                    u.creado_en,
                    r.nombre AS rol_nombre
                FROM usuario u
                INNER JOIN rol r ON u.id_rol = r.id_rol
                WHERE LOWER(u.username) = LOWER(?)
            """
            cursor.execute(query, (username.strip(),))
            row = cursor.fetchone()
            return dict(row) if row else None

    @staticmethod
    def create(id_rol, username, password_hash, salt, nombre_completo, activo=1):
        with get_db_cursor(commit=True) as cursor:
            cursor.execute(
                """
                INSERT INTO usuario (id_rol, username, password_hash, salt, nombre_completo, activo)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (id_rol, username.strip().lower(), password_hash, salt, nombre_completo.strip(), activo)
            )
            return cursor.lastrowid

    @staticmethod
    def update(id_usuario, id_rol, nombre_completo, activo=1):
        with get_db_cursor(commit=True) as cursor:
            cursor.execute(
                """
                UPDATE usuario 
                SET id_rol = ?, nombre_completo = ?, activo = ?
                WHERE id_usuario = ?
                """,
                (id_rol, nombre_completo.strip(), activo, id_usuario)
            )
            return cursor.rowcount > 0

    @staticmethod
    def update_password(id_usuario, password_hash, salt):
        with get_db_cursor(commit=True) as cursor:
            cursor.execute(
                "UPDATE usuario SET password_hash = ?, salt = ? WHERE id_usuario = ?",
                (password_hash, salt, id_usuario)
            )
            return cursor.rowcount > 0

    @staticmethod
    def delete(id_usuario, logico=True):
        """Eliminación lógica por defecto (activo=0); eliminación física opcional para tests"""
        with get_db_cursor(commit=True) as cursor:
            if logico:
                cursor.execute("UPDATE usuario SET activo = 0 WHERE id_usuario = ?", (id_usuario,))
            else:
                cursor.execute("DELETE FROM usuario WHERE id_usuario = ?", (id_usuario,))
            return cursor.rowcount > 0

    @staticmethod
    def restore(id_usuario):
        """Restaura un usuario eliminado lógicamente"""
        with get_db_cursor(commit=True) as cursor:
            cursor.execute("UPDATE usuario SET activo = 1 WHERE id_usuario = ?", (id_usuario,))
            return cursor.rowcount > 0

    @staticmethod
    def get_roles():
        with get_db_cursor() as cursor:
            cursor.execute("SELECT id_rol, nombre, descripcion FROM rol ORDER BY id_rol ASC")
            return [dict(row) for row in cursor.fetchall()]
