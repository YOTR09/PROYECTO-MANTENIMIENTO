from config.database import get_db_cursor

class SocioRepository:
    @staticmethod
    def get_all(search_term=None):
        with get_db_cursor() as cursor:
            if search_term:
                query = """
                    SELECT id_socio, cedula, nombre_completo, telefono, estado 
                    FROM socio 
                    WHERE cedula LIKE ? OR nombre_completo LIKE ? OR telefono LIKE ?
                    ORDER BY nombre_completo ASC
                """
                wildcard = f"%{search_term.strip()}%"
                cursor.execute(query, (wildcard, wildcard, wildcard))
            else:
                cursor.execute("SELECT id_socio, cedula, nombre_completo, telefono, estado FROM socio ORDER BY nombre_completo ASC")
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

    @staticmethod
    def get_by_id(id_socio):
        with get_db_cursor() as cursor:
            cursor.execute("SELECT * FROM socio WHERE id_socio = ?", (id_socio,))
            row = cursor.fetchone()
            return dict(row) if row else None

    @staticmethod
    def get_by_cedula(cedula):
        with get_db_cursor() as cursor:
            cursor.execute("SELECT * FROM socio WHERE cedula = ?", (cedula.strip(),))
            row = cursor.fetchone()
            return dict(row) if row else None

    @staticmethod
    def create(cedula, nombre_completo, telefono, estado="Activo"):
        with get_db_cursor(commit=True) as cursor:
            cursor.execute(
                "INSERT INTO socio (cedula, nombre_completo, telefono, estado) VALUES (?, ?, ?, ?)",
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
    def delete(id_socio):
        with get_db_cursor(commit=True) as cursor:
            cursor.execute("DELETE FROM socio WHERE id_socio = ?", (id_socio,))
            return cursor.rowcount > 0

