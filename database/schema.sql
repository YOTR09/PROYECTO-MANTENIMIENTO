-- =========================================================
-- ESQUEMA DE BASE DE DATOS: BRISAS DEL PALMAR
-- Sistema de Control de Mantenimiento Preventivo
-- Motor: SQLite3 (7 Entidades Normalizadas en 3FN)
-- =========================================================

PRAGMA foreign_keys = ON;

-- 1. Tabla de Roles / Niveles de Acceso
CREATE TABLE IF NOT EXISTS rol (
    id_rol INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL UNIQUE CHECK(nombre IN ('Administrador', 'Mecanico', 'Operador')),
    descripcion TEXT
);

-- 2. Tabla de Usuarios del Sistema (Seguridad y Hashing PBKDF2)
CREATE TABLE IF NOT EXISTS usuario (
    id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
    id_rol INTEGER NOT NULL,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    salt TEXT NOT NULL,
    nombre_completo TEXT NOT NULL,
    pregunta_seguridad TEXT NOT NULL DEFAULT '¿Nombre de la empresa de transporte colectivo?',
    respuesta_seguridad TEXT NOT NULL DEFAULT 'Brisas del Palmar',
    activo INTEGER NOT NULL DEFAULT 1 CHECK(activo IN (0, 1)),
    creado_en TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
    FOREIGN KEY (id_rol) REFERENCES rol(id_rol) ON DELETE RESTRICT
);

-- 3. Tabla de Socios (Propietarios / Afiliados)
CREATE TABLE IF NOT EXISTS socio (
    id_socio INTEGER PRIMARY KEY AUTOINCREMENT,
    cedula TEXT NOT NULL UNIQUE,
    nombre_completo TEXT NOT NULL,
    telefono TEXT,
    estado TEXT NOT NULL DEFAULT 'Activo' CHECK(estado IN ('Activo', 'Inactivo')),
    activo INTEGER NOT NULL DEFAULT 1 CHECK(activo IN (0, 1)) -- Eliminación lógica
);

-- 4. Tabla de Vehículos / Unidades de Transporte
CREATE TABLE IF NOT EXISTS vehiculo (
    id_vehiculo INTEGER PRIMARY KEY AUTOINCREMENT,
    id_socio INTEGER NOT NULL,
    numero_unidad TEXT NOT NULL UNIQUE,
    placa TEXT NOT NULL UNIQUE,
    marca_modelo TEXT NOT NULL,
    ano INTEGER,
    kilometraje_actual INTEGER NOT NULL DEFAULT 0,
    status TEXT NOT NULL DEFAULT 'Activo' CHECK(status IN ('Activo', 'En Taller', 'Inactivo')),
    activo INTEGER NOT NULL DEFAULT 1 CHECK(activo IN (0, 1)), -- Eliminación lógica
    FOREIGN KEY (id_socio) REFERENCES socio(id_socio) ON DELETE RESTRICT
);

-- 5. Catálogo de Tipos de Mantenimiento Preventivo
CREATE TABLE IF NOT EXISTS tipo_mantenimiento (
    id_tipo INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL UNIQUE,
    descripcion TEXT,
    intervalo_km INTEGER NOT NULL DEFAULT 0,
    intervalo_dias INTEGER NOT NULL DEFAULT 0,
    activo INTEGER NOT NULL DEFAULT 1 CHECK(activo IN (0, 1)) -- Eliminación lógica
);

-- 6. Plan de Mantenimiento Programado por Unidad
CREATE TABLE IF NOT EXISTS mantenimiento_programado (
    id_programacion INTEGER PRIMARY KEY AUTOINCREMENT,
    id_vehiculo INTEGER NOT NULL,
    id_tipo INTEGER NOT NULL,
    fecha_ultimo_servicio TEXT,
    km_ultimo_servicio INTEGER NOT NULL DEFAULT 0,
    fecha_proximo_servicio TEXT,
    km_proximo_servicio INTEGER NOT NULL DEFAULT 0,
    observaciones TEXT,
    activo INTEGER NOT NULL DEFAULT 1 CHECK(activo IN (0, 1)), -- Eliminación lógica
    FOREIGN KEY (id_vehiculo) REFERENCES vehiculo(id_vehiculo) ON DELETE CASCADE,
    FOREIGN KEY (id_tipo) REFERENCES tipo_mantenimiento(id_tipo) ON DELETE CASCADE,
    UNIQUE(id_vehiculo, id_tipo)
);

-- 7. Historial / Bitácora de Mantenimientos Ejecutados
CREATE TABLE IF NOT EXISTS historial_mantenimiento (
    id_historial INTEGER PRIMARY KEY AUTOINCREMENT,
    id_vehiculo INTEGER NOT NULL,
    id_tipo INTEGER NOT NULL,
    fecha_realizado TEXT NOT NULL,
    km_al_momento INTEGER NOT NULL,
    costo REAL NOT NULL DEFAULT 0.0,
    taller_mecanico TEXT,
    descripcion_trabajo TEXT,
    FOREIGN KEY (id_vehiculo) REFERENCES vehiculo(id_vehiculo) ON DELETE CASCADE,
    FOREIGN KEY (id_tipo) REFERENCES tipo_mantenimiento(id_tipo) ON DELETE RESTRICT
);

-- Índices para optimizar búsquedas y filtrado de registros activos
CREATE INDEX IF NOT EXISTS idx_rol_nombre ON rol(nombre);
CREATE INDEX IF NOT EXISTS idx_usuario_username ON usuario(username);
CREATE INDEX IF NOT EXISTS idx_usuario_rol ON usuario(id_rol);
CREATE INDEX IF NOT EXISTS idx_usuario_activo ON usuario(activo);

CREATE INDEX IF NOT EXISTS idx_socio_cedula ON socio(cedula);
CREATE INDEX IF NOT EXISTS idx_socio_activo ON socio(activo);

CREATE INDEX IF NOT EXISTS idx_vehiculo_unidad ON vehiculo(numero_unidad);
CREATE INDEX IF NOT EXISTS idx_vehiculo_placa ON vehiculo(placa);
CREATE INDEX IF NOT EXISTS idx_vehiculo_activo ON vehiculo(activo);

CREATE INDEX IF NOT EXISTS idx_tipo_mant_activo ON tipo_mantenimiento(activo);
CREATE INDEX IF NOT EXISTS idx_mant_prog_vehiculo ON mantenimiento_programado(id_vehiculo);
CREATE INDEX IF NOT EXISTS idx_mant_prog_activo ON mantenimiento_programado(activo);
CREATE INDEX IF NOT EXISTS idx_mant_hist_vehiculo ON historial_mantenimiento(id_vehiculo);
