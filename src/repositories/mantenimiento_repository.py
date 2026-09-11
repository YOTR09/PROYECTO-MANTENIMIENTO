from config.database import get_db_connection, get_db_cursor

class MantenimientoRepository:
    @staticmethod
    def get_programaciones(id_vehiculo=None, search_term=None):
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            SELECT 
                mp.id_programacion,
                mp.id_vehiculo,
                mp.id_tipo,
                mp.fecha_ultimo_servicio,
                mp.km_ultimo_servicio,
                mp.fecha_proximo_servicio,
                mp.km_proximo_servicio,
                mp.observaciones,
                v.numero_unidad,
                v.placa,
                v.marca_modelo,
                v.kilometraje_actual,
                v.status AS vehiculo_status,
                tm.nombre AS tipo_nombre,
                tm.intervalo_km,
                tm.intervalo_dias,
                s.nombre_completo AS socio_nombre
            FROM mantenimiento_programado mp
            INNER JOIN vehiculo v ON mp.id_vehiculo = v.id_vehiculo
            INNER JOIN socio s ON v.id_socio = s.id_socio
            INNER JOIN tipo_mantenimiento tm ON mp.id_tipo = tm.id_tipo
            WHERE 1=1
        """
        params = []
        if id_vehiculo:
            query += " AND mp.id_vehiculo = ?"
            params.append(id_vehiculo)
        
        if search_term:
            query += " AND (v.numero_unidad LIKE ? OR v.placa LIKE ? OR tm.nombre LIKE ? OR s.nombre_completo LIKE ?)"
            wildcard = f"%{search_term.strip()}%"
            params.extend([wildcard, wildcard, wildcard, wildcard])
        with get_db_cursor() as cursor:
            query = """
                SELECT 
                    mp.id_programacion,
                    mp.id_vehiculo,
                    mp.id_tipo,
                    mp.fecha_ultimo_servicio,
                    mp.km_ultimo_servicio,
                    mp.fecha_proximo_servicio,
                    mp.km_proximo_servicio,
                    mp.observaciones,
                    v.numero_unidad,
                    v.placa,
                    v.marca_modelo,
                    v.kilometraje_actual,
                    v.status AS vehiculo_status,
                    tm.nombre AS tipo_nombre,
                    tm.intervalo_km,
                    tm.intervalo_dias,
                    s.nombre_completo AS socio_nombre
                FROM mantenimiento_programado mp
                INNER JOIN vehiculo v ON mp.id_vehiculo = v.id_vehiculo
                INNER JOIN socio s ON v.id_socio = s.id_socio
                INNER JOIN tipo_mantenimiento tm ON mp.id_tipo = tm.id_tipo
                WHERE 1=1
            """
            params = []
            if id_vehiculo:
                query += " AND mp.id_vehiculo = ?"
                params.append(id_vehiculo)
            
            if search_term:
                query += " AND (v.numero_unidad LIKE ? OR v.placa LIKE ? OR tm.nombre LIKE ? OR s.nombre_completo LIKE ?)"
                wildcard = f"%{search_term.strip()}%"
                params.extend([wildcard, wildcard, wildcard, wildcard])

        query += " ORDER BY v.numero_unidad ASC, mp.km_proximo_servicio ASC"
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
            query += " ORDER BY v.numero_unidad ASC, mp.km_proximo_servicio ASC"
            cursor.execute(query, params)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

    @staticmethod
    def get_programacion_by_id(id_programacion):
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            SELECT 
                mp.*,
                v.numero_unidad,
                v.placa,
                v.kilometraje_actual,
                tm.nombre AS tipo_nombre,
                tm.intervalo_km,
                tm.intervalo_dias
            FROM mantenimiento_programado mp
            INNER JOIN vehiculo v ON mp.id_vehiculo = v.id_vehiculo
            INNER JOIN tipo_mantenimiento tm ON mp.id_tipo = tm.id_tipo
            WHERE mp.id_programacion = ?
        """
        cursor.execute(query, (id_programacion,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None
        with get_db_cursor() as cursor:
            query = """
                SELECT 
                    mp.*,
                    v.numero_unidad,
                    v.placa,
                    v.kilometraje_actual,
                    tm.nombre AS tipo_nombre,
                    tm.intervalo_km,
                    tm.intervalo_dias
                FROM mantenimiento_programado mp
                INNER JOIN vehiculo v ON mp.id_vehiculo = v.id_vehiculo
                INNER JOIN tipo_mantenimiento tm ON mp.id_tipo = tm.id_tipo
                WHERE mp.id_programacion = ?
            """
            cursor.execute(query, (id_programacion,))
            row = cursor.fetchone()
            return dict(row) if row else None

    @staticmethod
    def upsert_programacion(id_vehiculo, id_tipo, fecha_ultimo, km_ultimo, fecha_proximo, km_proximo, observaciones=""):
        with get_db_cursor(commit=True) as cursor:
            # Revisa si ya existe para hacer update o insert
            cursor.execute(
                "SELECT id_programacion FROM mantenimiento_programado WHERE id_vehiculo = ? AND id_tipo = ?",
                (id_vehiculo, id_tipo)
            )
            existente = cursor.fetchone()
            if existente:
                cursor.execute(
                    """
                    UPDATE mantenimiento_programado
                    SET fecha_ultimo_servicio = ?, km_ultimo_servicio = ?, fecha_proximo_servicio = ?, km_proximo_servicio = ?, observaciones = ?
                    WHERE id_programacion = ?
                    """,
                    (fecha_ultimo, km_ultimo, fecha_proximo, km_proximo, observaciones, existente[0])
                )
                return existente[0]
            else:
                cursor.execute(
                    """
                    INSERT INTO mantenimiento_programado 
                        (id_vehiculo, id_tipo, fecha_ultimo_servicio, km_ultimo_servicio, fecha_proximo_servicio, km_proximo_servicio, observaciones)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (id_vehiculo, id_tipo, fecha_ultimo, km_ultimo, fecha_proximo, km_proximo, observaciones)
                )
                return cursor.lastrowid

    @staticmethod
    def delete_programacion(id_programacion):
        with get_db_cursor(commit=True) as cursor:
            cursor.execute("DELETE FROM mantenimiento_programado WHERE id_programacion = ?", (id_programacion,))
            return cursor.rowcount > 0

    @staticmethod
    def add_historial(id_vehiculo, id_tipo, fecha_realizado, km_al_momento, costo, taller_mecanico, descripcion_trabajo):
        with get_db_cursor(commit=True) as cursor:
            cursor.execute(
                """
                INSERT INTO historial_mantenimiento
                    (id_vehiculo, id_tipo, fecha_realizado, km_al_momento, costo, taller_mecanico, descripcion_trabajo)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (id_vehiculo, id_tipo, fecha_realizado, km_al_momento, costo, taller_mecanico, descripcion_trabajo)
            )
            return cursor.lastrowid

    @staticmethod
    def get_historial(id_vehiculo=None, search_term=None, limit=200):
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            SELECT 
                h.id_historial,
                h.id_vehiculo,
                h.id_tipo,
                h.fecha_realizado,
                h.km_al_momento,
                h.costo,
                h.taller_mecanico,
                h.descripcion_trabajo,
                v.numero_unidad,
                v.placa,
                tm.nombre AS tipo_nombre,
                s.nombre_completo AS socio_nombre
            FROM historial_mantenimiento h
            INNER JOIN vehiculo v ON h.id_vehiculo = v.id_vehiculo
            INNER JOIN socio s ON v.id_socio = s.id_socio
            INNER JOIN tipo_mantenimiento tm ON h.id_tipo = tm.id_tipo
            WHERE 1=1
        """
        params = []
        if id_vehiculo:
            query += " AND h.id_vehiculo = ?"
            params.append(id_vehiculo)
        with get_db_cursor() as cursor:
            query = """
                SELECT 
                    h.id_historial,
                    h.id_vehiculo,
                    h.id_tipo,
                    h.fecha_realizado,
                    h.km_al_momento,
                    h.costo,
                    h.taller_mecanico,
                    h.descripcion_trabajo,
                    v.numero_unidad,
                    v.placa,
                    tm.nombre AS tipo_nombre,
                    s.nombre_completo AS socio_nombre
                FROM historial_mantenimiento h
                INNER JOIN vehiculo v ON h.id_vehiculo = v.id_vehiculo
                INNER JOIN socio s ON v.id_socio = s.id_socio
                INNER JOIN tipo_mantenimiento tm ON h.id_tipo = tm.id_tipo
                WHERE 1=1
            """
            params = []
            if id_vehiculo:
                query += " AND h.id_vehiculo = ?"
                params.append(id_vehiculo)

        if search_term:
            query += " AND (v.numero_unidad LIKE ? OR v.placa LIKE ? OR tm.nombre LIKE ? OR h.taller_mecanico LIKE ?)"
            wildcard = f"%{search_term.strip()}%"
            params.extend([wildcard, wildcard, wildcard, wildcard])
            if search_term:
                query += " AND (v.numero_unidad LIKE ? OR v.placa LIKE ? OR tm.nombre LIKE ? OR h.taller_mecanico LIKE ?)"
                wildcard = f"%{search_term.strip()}%"
                params.extend([wildcard, wildcard, wildcard, wildcard])

        query += " ORDER BY h.fecha_realizado DESC, h.id_historial DESC LIMIT ?"
        params.append(limit)
            query += " ORDER BY h.fecha_realizado DESC, h.id_historial DESC LIMIT ?"
            params.append(limit)

        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
            cursor.execute(query, params)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

