from config.database import get_db_cursor

class SocioRepository:
    @staticmethod
    def get_all(search_term=None, solo_activos=True):
        with get_db_cursor() as cursor:
            query = """
                SELECT id_socio, cedula, nombre_completo, telefono, estado, activo 
                FROM socio 
                WHERE 1=1
            """
            params = []
            if solo_activos:
                query += " AND activo = 1"

            if search_term:
                query += " AND (cedula LIKE ? OR nombre_completo LIKE ? OR telefono LIKE ?)"
                wildcard = f"%{search_term.strip()}%"
                params.extend([wildcard, wildcard, wildcard])

            query += " ORDER BY nombre_completo ASC"
            cursor.execute(query, params)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

    @staticmethod
    def get_by_id(id_socio):
        with get_db_cursor() as cursor:
            cursor.execute("SELECT * FROM socio WHERE id_socio = ?", (id_socio,))
            row = cursor.fetchone()
            return dict(row) if row else None

    @staticmethod
    def get_by_cedula(cedula, solo_activos=True):
        with get_db_cursor() as cursor:
            query = "SELECT * FROM socio WHERE cedula = ?"
            if solo_activos:
                query += " AND activo = 1"
            cursor.execute(query, (cedula.strip(),))
            row = cursor.fetchone()
            return dict(row) if row else None

    @staticmethod
    def create(cedula, nombre_completo, telefono, estado="Activo"):
        with get_db_cursor(commit=True) as cursor:
            cursor.execute(
                "INSERT INTO socio (cedula, nombre_completo, telefono, estado, activo) VALUES (?, ?, ?, ?, 1)",
                (cedula.strip(), nombre_completo.strip(), telefono.strip() if telefono else "", estado)
            )
            return cursor.lastrowid

    @staticmethod
    def update(id_socio, cedula, nombre_completo, telefono, estado):
        with get_db_cursor(commit=True) as cursor:
            cursor.execute(
                "UPDATE socio SET cedula = ?, nombre_completo = ?, telefono = ?, estado = ? WHERE id_socio = ?",
                (cedula.strip(), nombre_completo.strip(), telefono.strip() if telefono else "", estado, id_socio)
            )
            return cursor.rowcount > 0

    @staticmethod
    def delete(id_socio, logico=True):
        """Eliminación lógica por defecto (activo = 0); física opcional"""
        with get_db_cursor(commit=True) as cursor:
            if logico:
                cursor.execute("UPDATE socio SET activo = 0 WHERE id_socio = ?", (id_socio,))
            else:
                cursor.execute("DELETE FROM socio WHERE id_socio = ?", (id_socio,))
            return cursor.rowcount > 0

    @staticmethod
    def restore(id_socio):
        """Restaura un socio dado de baja lógicamente"""
        with get_db_cursor(commit=True) as cursor:
            cursor.execute("UPDATE socio SET activo = 1 WHERE id_socio = ?", (id_socio,))
            return cursor.rowcount > 0

