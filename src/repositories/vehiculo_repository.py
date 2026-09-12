from config.database import get_db_connection, get_db_cursor

class VehiculoRepository:
    @staticmethod
    def get_all(search_term=None, status_filter=None):
        with get_db_cursor() as cursor:
            query = """
                SELECT 
                    v.id_vehiculo,
                    v.id_socio,
                    v.numero_unidad,
                    v.placa,
                    v.marca_modelo,
                    v.ano,
                    v.kilometraje_actual,
                    v.status,
                    s.nombre_completo AS socio_nombre,
                    s.cedula AS socio_cedula
                FROM vehiculo v
                INNER JOIN socio s ON v.id_socio = s.id_socio
                WHERE 1=1
            """
            params = []
            if search_term:
                query += " AND (v.numero_unidad LIKE ? OR v.placa LIKE ? OR v.marca_modelo LIKE ? OR s.nombre_completo LIKE ?)"
                wildcard = f"%{search_term.strip()}%"
                params.extend([wildcard, wildcard, wildcard, wildcard])
            
            if status_filter and status_filter != "Todos":
                query += " AND v.status = ?"
                params.append(status_filter)

            query += " ORDER BY v.numero_unidad ASC"
            cursor.execute(query, params)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

    @staticmethod
    def get_by_id(id_vehiculo):
        with get_db_cursor() as cursor:
            query = """
                SELECT 
                    v.*, 
                    s.nombre_completo AS socio_nombre 
                FROM vehiculo v
                INNER JOIN socio s ON v.id_socio = s.id_socio
                WHERE v.id_vehiculo = ?
            """
            cursor.execute(query, (id_vehiculo,))
            row = cursor.fetchone()
            return dict(row) if row else None

    @staticmethod
    def get_by_placa(placa):
        with get_db_cursor() as cursor:
            cursor.execute("SELECT * FROM vehiculo WHERE UPPER(placa) = UPPER(?)", (placa.strip(),))
            row = cursor.fetchone()
            return dict(row) if row else None

    @staticmethod
    def get_by_unidad(numero_unidad):
        with get_db_cursor() as cursor:
            cursor.execute("SELECT * FROM vehiculo WHERE UPPER(numero_unidad) = UPPER(?)", (numero_unidad.strip(),))
            row = cursor.fetchone()
            return dict(row) if row else None

    @staticmethod
    def create(id_socio, numero_unidad, placa, marca_modelo, ano, kilometraje_actual=0, status="Activo"):
        with get_db_cursor(commit=True) as cursor:
            cursor.execute(
                """
                INSERT INTO vehiculo 
                    (id_socio, numero_unidad, placa, marca_modelo, ano, kilometraje_actual, status)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (id_socio, numero_unidad.strip(), placa.strip().upper(), marca_modelo.strip(), ano, kilometraje_actual, status)
            )
            return cursor.lastrowid

    @staticmethod
    def update(id_vehiculo, id_socio, numero_unidad, placa, marca_modelo, ano, kilometraje_actual, status):
        with get_db_cursor(commit=True) as cursor:
            cursor.execute(
                """
                UPDATE vehiculo
                SET id_socio = ?, numero_unidad = ?, placa = ?, marca_modelo = ?, ano = ?, kilometraje_actual = ?, status = ?
                WHERE id_vehiculo = ?
                """,
                (id_socio, numero_unidad.strip(), placa.strip().upper(), marca_modelo.strip(), ano, kilometraje_actual, status, id_vehiculo)
            )
            return cursor.rowcount > 0

    @staticmethod
    def update_kilometraje(id_vehiculo, nuevo_km):
        with get_db_cursor(commit=True) as cursor:
            cursor.execute(
                "UPDATE vehiculo SET kilometraje_actual = ? WHERE id_vehiculo = ?",
                (nuevo_km, id_vehiculo)
            )
            return cursor.rowcount > 0

    @staticmethod
    def delete(id_vehiculo):
        with get_db_cursor(commit=True) as cursor:
            cursor.execute("DELETE FROM vehiculo WHERE id_vehiculo = ?", (id_vehiculo,))
            return cursor.rowcount > 0
