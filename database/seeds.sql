-- =========================================================
-- SEMILLAS INICIALES: ROLES, USUARIOS Y TIPOS DE MANTENIMIENTO
-- Catálogo estándar para flota de transporte colectivo: Brisas del Palmar
-- =========================================================

-- 1. Semillas de Roles / Niveles de Acceso
INSERT OR IGNORE INTO rol (id_rol, nombre, descripcion) VALUES
(1, 'Administrador', 'Control total del sistema: gestión de usuarios, catálogos, unidades, socios, reportes y configuraciones.'),
(2, 'Mecanico', 'Gestión operativa de taller: programación de mantenimientos, registro de intervenciones mecánicas e historial técnico.'),
(3, 'Operador', 'Modo consulta y auditoría: visualización de KPIs en dashboard, estado de flota y emisión de reportes sin permisos de modificación.');

-- 2. Semillas de Usuarios Iniciales (Contraseñas PBKDF2-HMAC-SHA256 con salt)
-- admin: admin123 (Pregunta: ¿Nombre de la empresa de transporte colectivo? -> Brisas del Palmar)
-- mecanico: mecanico123 (Pregunta: ¿Tipo de motor principal de la flota? -> Cummins)
-- auditor: auditor123 (Pregunta: ¿Departamento operativo de auditoría? -> Operaciones)
INSERT OR IGNORE INTO usuario (id_usuario, id_rol, username, password_hash, salt, nombre_completo, pregunta_seguridad, respuesta_seguridad, activo) VALUES
(1, 1, 'admin', 'a4a642c23a6355db30b7b6c452ac05ad009de4eb81088520ded9f77a07633ac6', '01bfbf868af0527ab98e4fe098533002', 'Administrador General', '¿Nombre de la empresa de transporte colectivo?', 'Brisas del Palmar', 1),
(2, 2, 'mecanico', '06d353fcc7fa9ddb4b412a1e69d718e41375aac833ec037fe51f43db24def532', '2b23579cb397f67553024e73258a6b60', 'Jefe de Taller Mecánico', '¿Tipo de motor principal de la flota?', 'Cummins', 1),
(3, 3, 'auditor', 'f286040dcff2dc669e5183726f1377779e323c618e11001ebfb9b028690b8f02', 'dd7d6b3be88a8b4c58bcf5431d48e545', 'Auditor de Operaciones', '¿Departamento operativo de auditoría?', 'Operaciones', 1);

-- 3. Catálogo de Mantenimientos Preventivos
INSERT OR IGNORE INTO tipo_mantenimiento (nombre, descripcion, intervalo_km, intervalo_dias) VALUES
('Cambio de Aceite y Filtro de Motor', 'Sustitución de lubricante de motor (15W-40/20W-50) y filtro de aceite para prevenir desgaste interno.', 5000, 60),
('Filtros de Combustible y Trampa de Agua', 'Reemplazo de filtro de combustible primario/secundario y drenaje/limpieza de sedimentador trampa de agua.', 10000, 90),
('Inspección y Cambio de Filtro de Aire', 'Limpieza o sustitución del elemento filtrante de aire para optimizar combustión y rendimiento de combustible.', 7500, 60),
('Engrase de Chasis, Crucetas y Terminales', 'Lubricación a presión de terminales de dirección, muñones, pasadores de ballesta y crucetas del cardán.', 3000, 30),
('Revisión y Ajuste del Sistema de Frenos', 'Calibración y revisión de desgaste de bandas, zapatas, pastillas, tambores y mangueras neumáticas/hidráulicas.', 10000, 60),
('Rotación, Alineación y Balanceo de Neumáticos', 'Inspección de desgaste parejo, torque de tuercas, presión de inflado y rotación de cauchos.', 10000, 90),
('Valvulina de Transmisión (Caja) y Corona', 'Cambio o nivelación de aceite de caja de velocidades y diferencial para alta fricción.', 30000, 180),
('Inspección de Sistema de Enfriamiento', 'Chequeo de refrigerante, tensión de correas de ventilador/alternador, estado de mangueras y tapa de radiador.', 15000, 90),
('Inspección Eléctrica, Batería y Alternador', 'Limpieza de bornes, medición de voltaje de carga del alternador, nivel de electrolito y cableado general.', 0, 60),
('Inspección de Suspensión y Ballestas', 'Revisión de hojas de ballesta, abrazaderas U, amortiguadores y bujes de goma/bronce.', 15000, 120);
