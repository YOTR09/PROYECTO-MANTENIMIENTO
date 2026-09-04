-- =========================================================
-- ESQUEMA DE BASE DE DATOS: BRISAS DEL PALMAR
-- Sistema de Control de Mantenimiento Preventivo
-- Motor: SQLite3
-- =========================================================

PRAGMA foreign_keys = ON;

-- 1. Tabla de Socios (Propietarios / Afiliados)
CREATE TABLE IF NOT EXISTS socio (
    id_socio INTEGER PRIMARY KEY AUTOINCREMENT,
    cedula TEXT NOT NULL UNIQUE,
    nombre_completo TEXT NOT NULL,
    telefono TEXT,
    estado TEXT NOT NULL DEFAULT 'Activo' CHECK(estado IN ('Activo', 'Inactivo'))
);

-- 2. Tabla de Vehículos / Unidades de Transporte
CREATE TABLE IF NOT EXISTS vehiculo (
    id_vehiculo INTEGER PRIMARY KEY AUTOINCREMENT,
    id_socio INTEGER NOT NULL,
    numero_unidad TEXT NOT NULL UNIQUE,       -- Ej: "01", "14", "Bus 25"
    placa TEXT NOT NULL UNIQUE,
    marca_modelo TEXT NOT NULL,
    ano INTEGER,
    kilometraje_actual INTEGER NOT NULL DEFAULT 0,
    status TEXT NOT NULL DEFAULT 'Activo' CHECK(status IN ('Activo', 'En Taller', 'Inactivo')),
    FOREIGN KEY (id_socio) REFERENCES socio(id_socio) ON DELETE RESTRICT
);

-- 3. Catálogo de Tipos de Mantenimiento Preventivo (CRUD)
CREATE TABLE IF NOT EXISTS tipo_mantenimiento (
    id_tipo INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL UNIQUE,
    descripcion TEXT,
    intervalo_km INTEGER NOT NULL DEFAULT 0,      -- 0 si aplica solo por días
    intervalo_dias INTEGER NOT NULL DEFAULT 0     -- 0 si aplica solo por km
);

-- 4. Plan de Mantenimiento Programado por Unidad
CREATE TABLE IF NOT EXISTS mantenimiento_programado (
    id_programacion INTEGER PRIMARY KEY AUTOINCREMENT,
    id_vehiculo INTEGER NOT NULL,
    id_tipo INTEGER NOT NULL,
    fecha_ultimo_servicio TEXT,                   -- Formato ISO: YYYY-MM-DD
    km_ultimo_servicio INTEGER NOT NULL DEFAULT 0,
    fecha_proximo_servicio TEXT,                  -- Formato ISO: YYYY-MM-DD
    km_proximo_servicio INTEGER NOT NULL DEFAULT 0,
    observaciones TEXT,
    FOREIGN KEY (id_vehiculo) REFERENCES vehiculo(id_vehiculo) ON DELETE CASCADE,
    FOREIGN KEY (id_tipo) REFERENCES tipo_mantenimiento(id_tipo) ON DELETE CASCADE,
    UNIQUE(id_vehiculo, id_tipo)
);

-- 5. Historial / Bitácora de Mantenimientos Ejecutados
CREATE TABLE IF NOT EXISTS historial_mantenimiento (
    id_historial INTEGER PRIMARY KEY AUTOINCREMENT,
    id_vehiculo INTEGER NOT NULL,
    id_tipo INTEGER NOT NULL,
    fecha_realizado TEXT NOT NULL,                -- Formato ISO: YYYY-MM-DD
    km_al_momento INTEGER NOT NULL,
    costo REAL NOT NULL DEFAULT 0.0,
    taller_mecanico TEXT,
    descripcion_trabajo TEXT,
    FOREIGN KEY (id_vehiculo) REFERENCES vehiculo(id_vehiculo) ON DELETE CASCADE,
    FOREIGN KEY (id_tipo) REFERENCES tipo_mantenimiento(id_tipo) ON DELETE RESTRICT
);

-- Índices para optimizar búsquedas frecuentes
CREATE INDEX IF NOT EXISTS idx_vehiculo_unidad ON vehiculo(numero_unidad);
CREATE INDEX IF NOT EXISTS idx_vehiculo_placa ON vehiculo(placa);
CREATE INDEX IF NOT EXISTS idx_socio_cedula ON socio(cedula);
CREATE INDEX IF NOT EXISTS idx_mant_prog_vehiculo ON mantenimiento_programado(id_vehiculo);
CREATE INDEX IF NOT EXISTS idx_mant_hist_vehiculo ON historial_mantenimiento(id_vehiculo);

