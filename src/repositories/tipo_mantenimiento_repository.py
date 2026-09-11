from config.database import get_db_connection, get_db_cursor

class TipoMantenimientoRepository:
    @staticmethod
    def get_all(search_term=None):
        conn = get_db_connection()
        cursor = conn.cursor()
        if search_term:
            query = """
                SELECT id_tipo, nombre, descripcion, intervalo_km, intervalo_dias
                FROM tipo_mantenimiento
                WHERE nombre LIKE ? OR descripcion LIKE ?
                ORDER BY nombre ASC
            """
            wildcard = f"%{search_term.strip()}%"
            cursor.execute(query, (wildcard, wildcard))
        else:
            cursor.execute("SELECT id_tipo, nombre, descripcion, intervalo_km, intervalo_dias FROM tipo_mantenimiento ORDER BY id_tipo ASC")
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
        with get_db_cursor() as cursor:
            if search_term:
                query = """
                    SELECT id_tipo, nombre, descripcion, intervalo_km, intervalo_dias
                    FROM tipo_mantenimiento
                    WHERE nombre LIKE ? OR descripcion LIKE ?
                    ORDER BY nombre ASC
                """
                wildcard = f"%{search_term.strip()}%"
                cursor.execute(query, (wildcard, wildcard))
            else:
                cursor.execute("SELECT id_tipo, nombre, descripcion, intervalo_km, intervalo_dias FROM tipo_mantenimiento ORDER BY id_tipo ASC")
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

    @staticmethod
    def get_by_id(id_tipo):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tipo_mantenimiento WHERE id_tipo = ?", (id_tipo,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None
        with get_db_cursor() as cursor:
            cursor.execute("SELECT * FROM tipo_mantenimiento WHERE id_tipo = ?", (id_tipo,))
            row = cursor.fetchone()
            return dict(row) if row else None

    @staticmethod
    def create(nombre, descripcion, intervalo_km, intervalo_dias):
        with get_db_cursor(commit=True) as cursor:
            cursor.execute(
                """
                INSERT INTO tipo_mantenimiento (nombre, descripcion, intervalo_km, intervalo_dias)
                VALUES (?, ?, ?, ?)
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
    def delete(id_tipo):
        with get_db_cursor(commit=True) as cursor:
            cursor.execute("DELETE FROM tipo_mantenimiento WHERE id_tipo = ?", (id_tipo,))
            return cursor.rowcount > 0

