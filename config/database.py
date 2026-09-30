import sqlite3
import os
from contextlib import contextmanager

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_PATH = os.path.join(DATA_DIR, "mantenimiento.db")

def is_testing_env():
    return os.environ.get("TESTING") == "1"

def get_current_db_path():
    if is_testing_env():
        return os.path.join(DATA_DIR, "test_mantenimiento.db")
    return DB_PATH

SCHEMA_PATH = os.path.join(BASE_DIR, "database", "schema.sql")
SEEDS_PATH = os.path.join(BASE_DIR, "database", "seeds.sql")

def ensure_data_dir():
    """Asegura que el directorio data exista"""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR, exist_ok=True)

def get_db_connection():
    """Obtiene una conexión directa a la base de datos con foreign keys habilitadas"""
    ensure_data_dir()
    db_file = get_current_db_path()
    conn = sqlite3.connect(db_file)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

@contextmanager
def get_db_cursor(commit=False):
    """Context manager para ejecutar sentencias de forma segura"""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        yield cursor
        if commit:
            conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def _migrar_columnas_activo(conn):
    """Garantiza compatibilidad con BD existentes agregando la columna activo si no existe"""
    cursor = conn.cursor()
    tablas = ["socio", "vehiculo", "tipo_mantenimiento", "mantenimiento_programado"]
    for tabla in tablas:
        try:
            cursor.execute(f"PRAGMA table_info({tabla})")
            columnas = [row["name"] for row in cursor.fetchall()]
            if columnas and "activo" not in columnas:
                cursor.execute(f"ALTER TABLE {tabla} ADD COLUMN activo INTEGER NOT NULL DEFAULT 1")
                conn.commit()
        except Exception:
            pass

def init_db():
    """Inicializa la base de datos ejecutando el esquema, migraciones y semillas si es nueva"""
    ensure_data_dir()
    conn = get_db_connection()
    try:
        _migrar_columnas_activo(conn)

        with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
            conn.executescript(f.read())

        _migrar_columnas_activo(conn)

        # Verificar e insertar semillas si faltan roles, usuarios o mantenimientos
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM rol")
        count_roles = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM tipo_mantenimiento")
        count_tipos = cursor.fetchone()[0]

        if (count_roles == 0 or count_tipos == 0) and os.path.exists(SEEDS_PATH):
            with open(SEEDS_PATH, "r", encoding="utf-8") as f:
                conn.executescript(f.read())
        conn.commit()
    finally:
        conn.close()
