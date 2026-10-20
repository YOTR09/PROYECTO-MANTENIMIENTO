-- =========================================================
-- SEMILLAS INICIALES Y DATOS DE PRUEBA / HIDRATACIÓN
-- Flota de transporte colectivo: Brisas del Palmar
-- =========================================================

-- 1. Semillas de Roles / Niveles de Acceso
INSERT OR IGNORE INTO rol (id_rol, nombre, descripcion) VALUES
(1, 'Administrador', 'Control total del sistema: gestión de usuarios, catálogos, unidades, socios, reportes y configuraciones.'),
(2, 'Mecanico', 'Gestión operativa de taller: programación de mantenimientos, registro de intervenciones mecánicas e historial técnico.'),
(3, 'Operador', 'Modo consulta y auditoría: visualización de KPIs en dashboard, estado de flota y emisión de reportes sin permisos de modificación.');

-- 2. Semillas de Usuarios Iniciales (Contraseñas PBKDF2-HMAC-SHA256 con salt)
-- admin: admin123
-- mecanico: mecanico123
-- auditor: auditor123
INSERT OR IGNORE INTO usuario (id_usuario, id_rol, username, password_hash, salt, nombre_completo, pregunta_seguridad, respuesta_seguridad, activo) VALUES
(1, 1, 'admin', 'a4a642c23a6355db30b7b6c452ac05ad009de4eb81088520ded9f77a07633ac6', '01bfbf868af0527ab98e4fe098533002', 'Administrador General', '¿Nombre de la empresa de transporte colectivo?', 'Brisas del Palmar', 1),
(2, 2, 'mecanico', '06d353fcc7fa9ddb4b412a1e69d718e41375aac833ec037fe51f43db24def532', '2b23579cb397f67553024e73258a6b60', 'Jefe de Taller Mecánico', '¿Tipo de motor principal de la flota?', 'Cummins', 1),
(3, 3, 'auditor', 'f286040dcff2dc669e5183726f1377779e323c618e11001ebfb9b028690b8f02', 'dd7d6b3be88a8b4c58bcf5431d48e545', 'Auditor de Operaciones', '¿Departamento operativo de auditoría?', 'Operaciones', 1);

-- 3. Catálogo de Mantenimientos Preventivos
INSERT OR IGNORE INTO tipo_mantenimiento (id_tipo, nombre, descripcion, intervalo_km, intervalo_dias, activo) VALUES
(1, 'Cambio de Aceite y Filtro de Motor', 'Sustitución de lubricante de motor (15W-40/20W-50) y filtro de aceite para prevenir desgaste interno.', 5000, 60, 1),
(2, 'Filtros de Combustible y Trampa de Agua', 'Reemplazo de filtro de combustible primario/secundario y drenaje/limpieza de sedimentador trampa de agua.', 10000, 90, 1),
(3, 'Inspección y Cambio de Filtro de Aire', 'Limpieza o sustitución del elemento filtrante de aire para optimizar combustión y rendimiento de combustible.', 7500, 60, 1),
(4, 'Engrase de Chasis, Crucetas y Terminales', 'Lubricación a presión de terminales de dirección, muñones, pasadores de ballesta y crucetas del cardán.', 3000, 30, 1),
(5, 'Revisión y Ajuste del Sistema de Frenos', 'Calibración y revisión de desgaste de bandas, zapatas, pastillas, tambores y mangueras neumáticas/hidráulicas.', 10000, 60, 1),
(6, 'Rotación, Alineación y Balanceo de Neumáticos', 'Inspección de desgaste parejo, torque de tuercas, presión de inflado y rotación de cauchos.', 10000, 90, 1),
(7, 'Valvulina de Transmisión (Caja) y Corona', 'Cambio o nivelación de aceite de caja de velocidades y diferencial para alta fricción.', 30000, 180, 1),
(8, 'Inspección de Sistema de Enfriamiento', 'Chequeo de refrigerante, tensión de correas de ventilador/alternador, estado de mangueras y tapa de radiador.', 15000, 90, 1),
(9, 'Inspección Eléctrica, Batería y Alternador', 'Limpieza de bornes, medición de voltaje de carga del alternador, nivel de electrolito y cableado general.', 0, 60, 1),
(10, 'Inspección de Suspensión y Ballestas', 'Revisión de hojas de ballesta, abrazaderas U, amortiguadores y bujes de goma/bronce.', 15000, 120, 1);

-- 4. Padrón Institucional de Socios Propietarios
INSERT OR IGNORE INTO socio (id_socio, cedula, nombre_completo, telefono, estado, activo) VALUES
(1, 'V-14258963', 'Carlos Eduardo Mendoza', '0414-5236987', 'Activo', 1),
(2, 'V-11852963', 'Roberto Antonio Silva', '0424-6321458', 'Activo', 1),
(3, 'V-16987452', 'María Alejandra Torrealba', '0412-8745632', 'Activo', 1),
(4, 'V-10321456', 'José Gregorio Morales', '0416-9852147', 'Activo', 1),
(5, 'V-13654789', 'Nelson Enrique Colmenares', '0424-7412589', 'Activo', 1),
(6, 'V-15478963', 'Carmen Alicia Giménez', '0412-1234567', 'Activo', 1),
(7, 'V-18965412', 'Francisco Javier Escalona', '0414-3698521', 'Inactivo', 1);

-- 5. Flota Vehicular / Unidades de Transporte
INSERT OR IGNORE INTO vehiculo (id_vehiculo, id_socio, numero_unidad, placa, marca_modelo, ano, kilometraje_actual, status, activo) VALUES
(1, 1, '01', '23A45AA', 'Encava 610 Special', 2018, 145200, 'Activo', 1),
(2, 1, '02', '24B78BB', 'Encava ENT-610', 2019, 118500, 'Activo', 1),
(3, 2, '03', '25C12CC', 'Yutong ZK6852HG', 2017, 210400, 'Activo', 1),
(4, 2, '04', '26D34DD', 'Mercedes-Benz LO-915', 2016, 185600, 'Activo', 1),
(5, 3, '05', '27E56EE', 'Iveco Daily 59-12', 2020, 89300, 'Activo', 1),
(6, 3, '06', '28F78FF', 'Encava 3100 Isuzu', 2015, 275100, 'Activo', 1),
(7, 4, '07', '29G90GG', 'Isuzu NPR Carrozado', 2018, 162800, 'En Taller', 1),
(8, 4, '08', '30H12HH', 'Encava 610 Special', 2021, 64200, 'Activo', 1),
(9, 5, '09', '31I34II', 'Yutong ZK6852', 2019, 132400, 'Activo', 1),
(10, 5, '10', '32J56JJ', 'Encava ENT-900', 2014, 318900, 'En Taller', 1),
(11, 1, '11', '33K78KK', 'Mercedes-Benz LO-712', 2008, 412000, 'Inactivo', 1);

-- 6. Plan Preventivo y Semaforización (Fechas dinámicas relativas a la fecha actual)
-- 🔴 Vencidos:
-- Unidad 02: Tipo 1 (Cambio Aceite). Próx km 115000 vs actual 118500 (Excedido por 3,500 km) y fecha vencida hace 12 días
INSERT OR IGNORE INTO mantenimiento_programado (id_programacion, id_vehiculo, id_tipo, fecha_ultimo_servicio, km_ultimo_servicio, fecha_proximo_servicio, km_proximo_servicio, observaciones, activo) VALUES
(1, 2, 1, date('now', 'localtime', '-72 days'), 110000, date('now', 'localtime', '-12 days'), 115000, 'Servicio prioritario: límite de kilometraje y fecha excedido.', 1),
-- Unidad 07: Tipo 5 (Frenos). Próx km 160000 vs actual 162800 y vencido hace 8 días
(2, 7, 5, date('now', 'localtime', '-68 days'), 150000, date('now', 'localtime', '-8 days'), 160000, 'Unidad en taller por desgaste en zapatas de frenos traseros.', 1),
-- Unidad 06: Tipo 4 (Engrase). Próx km 274000 vs actual 275100 y vencido hace 5 días
(3, 6, 4, date('now', 'localtime', '-35 days'), 271000, date('now', 'localtime', '-5 days'), 274000, 'Requiere lubricación de terminales y crucetas urgente.', 1),

-- 🟡 Por Vencer:
-- Unidad 05: Tipo 2 (Filtros Combustible). Próx km 89550 vs actual 89300 (faltan 250 km) y fecha en 6 días
(4, 5, 2, date('now', 'localtime', '-84 days'), 79550, date('now', 'localtime', '+6 days'), 89550, 'Programado para revisión en jornada de fin de semana.', 1),
-- Unidad 01: Tipo 6 (Rotación Neumáticos). Próx km 145600 vs actual 145200 (faltan 400 km) y fecha en 8 días
(5, 1, 6, date('now', 'localtime', '-82 days'), 135600, date('now', 'localtime', '+8 days'), 145600, 'Chequeo de desgaste parejo y torque de tuercas.', 1),
-- Unidad 09: Tipo 8 (Enfriamiento). Próx km 132750 vs actual 132400 (faltan 350 km) y fecha en 5 días
(6, 9, 8, date('now', 'localtime', '-85 days'), 117750, date('now', 'localtime', '+5 days'), 132750, 'Chequeo de mangueras y tensión de correas de alternador.', 1),

-- 🟢 Al Día:
-- Unidad 01: Tipo 1 (Cambio Aceite). Próx km 150000 vs actual 145200 (faltan 4,800 km) y fecha en 52 días
(7, 1, 1, date('now', 'localtime', '-8 days'), 145000, date('now', 'localtime', '+52 days'), 150000, 'Último cambio realizado recientemente con aceite 15W-40.', 1),
-- Unidad 03: Tipo 1 (Cambio Aceite). Próx km 215000 vs actual 210400 (faltan 4,600 km) y fecha en 48 días
(8, 3, 1, date('now', 'localtime', '-12 days'), 210000, date('now', 'localtime', '+48 days'), 215000, 'Motor afinado y filtro nuevo Baldwin.', 1),
-- Unidad 04: Tipo 3 (Filtro Aire). Próx km 192000 vs actual 185600 (faltan 6,400 km) y fecha en 40 días
(9, 4, 3, date('now', 'localtime', '-20 days'), 184500, date('now', 'localtime', '+40 days'), 192000, 'Filtro primario y secundario cambiados.', 1),
-- Unidad 08: Tipo 1 (Cambio Aceite). Próx km 69000 vs actual 64200 (faltan 4,800 km) y fecha en 55 días
(10, 8, 1, date('now', 'localtime', '-5 days'), 64000, date('now', 'localtime', '+55 days'), 69000, 'Unidad seminueva en óptimo estado operativo.', 1),
-- Unidad 08: Tipo 5 (Frenos). Próx km 74000 vs actual 64200 (faltan 9,800 km) y fecha en 60 días
(11, 8, 5, date('now', 'localtime', '-45 days'), 58000, date('now', 'localtime', '+60 days'), 74000, 'Sistema de frenos neumático verificado sin fugas.', 1);

-- 7. Bitácora Histórica y Auditoría de Costos de Mantenimiento
INSERT OR IGNORE INTO historial_mantenimiento (id_historial, id_vehiculo, id_tipo, fecha_realizado, km_al_momento, costo, taller_mecanico, descripcion_trabajo) VALUES
(1, 1, 1, date('now', 'localtime', '-8 days'), 145000, 65.00, 'Servicio Rápido Lubri-Express', 'Cambio de aceite 15W-40 semisintético y filtro primario.'),
(2, 1, 4, date('now', 'localtime', '-25 days'), 143200, 25.00, 'Taller Mecánico Central El Palmar', 'Engrase completo a presión de muñones, terminales y crucetas.'),
(3, 2, 1, date('now', 'localtime', '-72 days'), 110000, 65.00, 'Servicio Rápido Lubri-Express', 'Mantenimiento rutinario de lubricación de motor.'),
(4, 3, 1, date('now', 'localtime', '-12 days'), 210000, 70.00, 'Taller Especializado Cummins', 'Sustitución de lubricante para motor diésel y filtros Baldwin.'),
(5, 3, 7, date('now', 'localtime', '-90 days'), 195000, 180.00, 'Taller Mecánico Central El Palmar', 'Reemplazo de valvulina 85W-140 en caja de velocidades y corona diferencial.'),
(6, 4, 3, date('now', 'localtime', '-20 days'), 184500, 40.00, 'Servicio Rápido Lubri-Express', 'Cambio de filtro de aire primario y secundario.'),
(7, 4, 5, date('now', 'localtime', '-65 days'), 178000, 150.00, 'Frenos y Ballestas San Juan', 'Remachado de bandas de freno traseras y calibración de matracas neumáticas.'),
(8, 5, 2, date('now', 'localtime', '-84 days'), 79500, 55.00, 'Inversiones y Servicios Diésel C.A.', 'Cambio de filtros de combustible diésel y purga de sedimentador trampa de agua.'),
(9, 6, 10, date('now', 'localtime', '-110 days'), 260000, 220.00, 'Frenos y Ballestas San Juan', 'Cambio de bujes de bronce de ballesta traseros y sustitución de hoja maestra.'),
(10, 7, 1, date('now', 'localtime', '-40 days'), 158000, 65.00, 'Taller Mecánico Central El Palmar', 'Cambio de aceite de motor 20W-50 y sustitución de filtro.'),
(11, 7, 9, date('now', 'localtime', '-15 days'), 162500, 90.00, 'Electro-Auto Los Andes', 'Reparación de solenoide de arranque, limpieza de bornes y prueba de carga del alternador.'),
(12, 8, 1, date('now', 'localtime', '-5 days'), 64000, 65.00, 'Servicio Rápido Lubri-Express', 'Servicio de lubricación preventivo reglamentario de 60,000 km.'),
(13, 8, 5, date('now', 'localtime', '-45 days'), 58000, 120.00, 'Frenos y Ballestas San Juan', 'Revisión general de sistema de frenos neumático y calibración de zapatas.'),
(14, 9, 6, date('now', 'localtime', '-82 days'), 122000, 80.00, 'Taller Mecánico Central El Palmar', 'Rotación de cauchos, balanceo dinámico y alineación delantera computarizada.'),
(15, 10, 7, date('now', 'localtime', '-30 days'), 315000, 340.00, 'Taller Mecánico Central El Palmar', 'Desmontaje de transmisión para cambio de rodamientos desgastados y valvulina nueva.'),
(16, 10, 1, date('now', 'localtime', '-60 days'), 310000, 75.00, 'Taller Especializado Cummins', 'Servicio completo de aceite 15W-40 y filtros de motor.'),
(17, 2, 4, date('now', 'localtime', '-105 days'), 105000, 25.00, 'Taller Mecánico Central El Palmar', 'Engrase general de chasis y pasadores.'),
(18, 5, 1, date('now', 'localtime', '-120 days'), 75000, 60.00, 'Servicio Rápido Lubri-Express', 'Cambio preventivo de aceite y filtro de motor.');
