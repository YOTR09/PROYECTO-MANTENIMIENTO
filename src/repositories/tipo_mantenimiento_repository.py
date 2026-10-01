from config.database import get_db_cursor

class TipoMantenimientoRepository:
    @staticmethod
    def get_all(search_term=None, solo_activos=True):
        with get_db_cursor() as cursor:
            query = """
                SELECT id_tipo, nombre, descripcion, intervalo_km, intervalo_dias, activo
                FROM tipo_mantenimiento
                WHERE 1=1
            """
            params = []
            if solo_activos:
                query += " AND activo = 1"

            if search_term:
                query += " AND (nombre LIKE ? OR descripcion LIKE ?)"
                wildcard = f"%{search_term.strip()}%"
                params.extend([wildcard, wildcard])

            query += " ORDER BY nombre ASC"
            cursor.execute(query, params)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

    @staticmethod
    def get_by_id(id_tipo):
        with get_db_cursor() as cursor:
            cursor.execute("SELECT * FROM tipo_mantenimiento WHERE id_tipo = ?", (id_tipo,))
            row = cursor.fetchone()
            return dict(row) if row else None

    @staticmethod
    def get_by_nombre(nombre, solo_activos=False):
        with get_db_cursor() as cursor:
            query = "SELECT * FROM tipo_mantenimiento WHERE LOWER(nombre) = LOWER(?)"
            if solo_activos:
                query += " AND activo = 1"
            cursor.execute(query, (nombre.strip(),))
            row = cursor.fetchone()
            return dict(row) if row else None

    @staticmethod
    def create(nombre, descripcion, intervalo_km, intervalo_dias):
        with get_db_cursor(commit=True) as cursor:
            cursor.execute(
                """
                INSERT INTO tipo_mantenimiento (nombre, descripcion, intervalo_km, intervalo_dias, activo)
                VALUES (?, ?, ?, ?, 1)
                """,
                (nombre.strip(), descripcion.strip() if descripcion else "", intervalo_km, intervalo_dias)
            )
            return cursor.lastrowid

    @staticmethod
    def update(id_tipo, nombre, descripcion, intervalo_km, intervalo_dias):
        with get_db_cursor(commit=True) as cursor:
            cursor.execute(
                """
                UPDATE tipo_mantenimiento
                SET nombre = ?, descripcion = ?, intervalo_km = ?, intervalo_dias = ?
                WHERE id_tipo = ?
                """,
                (nombre.strip(), descripcion.strip() if descripcion else "", intervalo_km, intervalo_dias, id_tipo)
            )
            return cursor.rowcount > 0

    @staticmethod
    def delete(id_tipo, logico=True):
        """Eliminación lógica por defecto (activo = 0); física opcional"""
        with get_db_cursor(commit=True) as cursor:
            if logico:
                cursor.execute("UPDATE tipo_mantenimiento SET activo = 0 WHERE id_tipo = ?", (id_tipo,))
            else:
                cursor.execute("DELETE FROM tipo_mantenimiento WHERE id_tipo = ?", (id_tipo,))
            return cursor.rowcount > 0

    @staticmethod
    def restore(id_tipo):
        """Restaura un tipo de mantenimiento eliminado lógicamente"""
        with get_db_cursor(commit=True) as cursor:
            cursor.execute("UPDATE tipo_mantenimiento SET activo = 1 WHERE id_tipo = ?", (id_tipo,))
            return cursor.rowcount > 0

