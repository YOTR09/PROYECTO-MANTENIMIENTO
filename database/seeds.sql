-- =========================================================
-- SEMILLAS INICIALES: TIPOS DE MANTENIMIENTO PREVENTIVO
-- Catálogo estándar para flota de transporte colectivo
-- =========================================================

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

