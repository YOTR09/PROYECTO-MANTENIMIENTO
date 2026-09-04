import sqlite3
import os
from contextlib import contextmanager

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_PATH = os.path.join(DATA_DIR, "mantenimiento.db")
SCHEMA_PATH = os.path.join(BASE_DIR, "database", "schema.sql")
SEEDS_PATH = os.path.join(BASE_DIR, "database", "seeds.sql")

def ensure_data_dir():
    """Asegura que el directorio data exista"""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR, exist_ok=True)

def get_db_connection():
    """Obtiene una conexión directa a la base de datos con foreign keys habilitadas"""
    ensure_data_dir()
    conn = sqlite3.connect(DB_PATH)
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

def init_db():
    """Inicializa la base de datos ejecutando el esquema y las semillas si es nueva"""
    ensure_data_dir()
    conn = get_db_connection()
    try:
        with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
            conn.executescript(f.read())
        
        # Verificar si ya existen tipos de mantenimiento precargados
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM tipo_mantenimiento")
        count = cursor.fetchone()[0]
        if count == 0 and os.path.exists(SEEDS_PATH):
            with open(SEEDS_PATH, "r", encoding="utf-8") as f:
                conn.executescript(f.read())
        conn.commit()
    finally:
        conn.close()

