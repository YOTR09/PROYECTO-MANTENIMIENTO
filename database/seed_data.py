#!/usr/bin/env python3
"""
=========================================================
SCRIPT DE HIDRATACIÓN DE DATOS DE PRUEBA
Empresa de Transporte Público: Brisas del Palmar
=========================================================
Permite poblar o restaurar la base de datos con un conjunto
realista y completo de datos de prueba (socios, flota vehicular,
mantenimientos programados con semáforos e historial de bitácora).

Uso:
    python database/seed_data.py          # Hidrata si las tablas están vacías
    python database/seed_data.py --reset  # Limpia y vuelve a hidratar desde cero
"""

import sys
import os

# Asegurar raíz del proyecto en sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.database import get_db_connection, SEEDS_PATH, SCHEMA_PATH

def hidratar(forzar=False):
    print("=" * 60)
    print("🚌 SISTEMA BRISAS DEL PALMAR — HIDRATACIÓN DE DATOS")
    print("=" * 60)

    conn = get_db_connection()
    try:
        cursor = conn.cursor()

        # 1. Aplicar esquema si hace falta
        if os.path.exists(SCHEMA_PATH):
            with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
                conn.executescript(f.read())

        # 2. Si se solicita reset, limpiar tablas operativas respetando integridad
        if forzar:
            print("⚠️ Modo --reset activado: limpiando datos operativos previos...")
            cursor.execute("DELETE FROM historial_mantenimiento;")
            cursor.execute("DELETE FROM mantenimiento_programado;")
            cursor.execute("DELETE FROM vehiculo;")
            cursor.execute("DELETE FROM socio;")
            conn.commit()

        # 3. Ejecutar semillas
        if os.path.exists(SEEDS_PATH):
            print(f"📄 Ejecutando semillas desde: {SEEDS_PATH}")
            with open(SEEDS_PATH, "r", encoding="utf-8") as f:
                conn.executescript(f.read())
            conn.commit()
            print("✅ Semillas ejecutadas exitosamente.")
        else:
            print(f"❌ Error: No se encontró el archivo de semillas en {SEEDS_PATH}")
            return False

        # 4. Mostrar resumen de datos cargados
        tablas = [
            ("rol", "Roles de acceso"),
            ("usuario", "Usuarios del sistema"),
            ("tipo_mantenimiento", "Catálogo de rutinas"),
            ("socio", "Socios y propietarios"),
            ("vehiculo", "Flota vehicular"),
            ("mantenimiento_programado", "Planes y semáforos"),
            ("historial_mantenimiento", "Bitácora histórica"),
        ]

        print("\n📊 RESUMEN DE REGISTROS EN BASE DE DATOS:")
        print("-" * 60)
        for tab, desc in tablas:
            cursor.execute(f"SELECT COUNT(*) FROM {tab}")
            cnt = cursor.fetchone()[0]
            print(f"  • {desc:<26} ({tab}): {cnt:>3} registros")

        # Conteo semafórico preventivo
        cursor.execute("""
            SELECT 
                SUM(CASE WHEN (mp.km_proximo_servicio - v.kilometraje_actual <= 0) OR (mp.fecha_proximo_servicio <= date('now','localtime')) THEN 1 ELSE 0 END) AS vencidos,
                SUM(CASE WHEN ((mp.km_proximo_servicio - v.kilometraje_actual > 0 AND mp.km_proximo_servicio - v.kilometraje_actual <= 500) OR (mp.fecha_proximo_servicio > date('now','localtime') AND mp.fecha_proximo_servicio <= date('now','localtime','+10 days'))) THEN 1 ELSE 0 END) AS por_vencer,
                SUM(CASE WHEN (mp.km_proximo_servicio - v.kilometraje_actual > 500) AND (mp.fecha_proximo_servicio > date('now','localtime','+10 days')) THEN 1 ELSE 0 END) AS al_dia
            FROM mantenimiento_programado mp
            JOIN vehiculo v ON mp.id_vehiculo = v.id_vehiculo
        """)
        row_sem = cursor.fetchone()
        if row_sem and row_sem[0] is not None:
            print("\n🚦 TABLERO SEMAFÓRICO PREVENTIVO INICIAL:")
            print(f"  🔴 Vencidos:    {row_sem[0]}")
            print(f"  🟡 Por Vencer:  {row_sem[1]}")
            print(f"  🟢 Al Día:      {row_sem[2]}")

        # Total histórico de costos
        cursor.execute("SELECT COUNT(*), SUM(costo) FROM historial_mantenimiento")
        row_hist = cursor.fetchone()
        if row_hist and row_hist[0] > 0:
            total_gasto = row_hist[1] or 0.0
            print(f"\n💰 BITÁCORA HISTÓRICA: {row_hist[0]} intervenciones con inversión total de ${total_gasto:,.2f}")

        print("=" * 60)
        print("🎉 ¡La base de datos está completamente hidratada y lista para operar!")
        print("=" * 60)
        return True
    finally:
        conn.close()

if __name__ == "__main__":
    reset_arg = "--reset" in sys.argv or "-r" in sys.argv
    hidratar(forzar=reset_arg)
