# Registro de Cambios (Changelog)

Todas las modificaciones notables de este proyecto serán documentadas en este archivo.
El formato se basa en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/).

## [2.0.0] - 2026-09-30

### Agregado
- Implementación completa del patrón de desarrollo **MVC (Modelo - Vista - Controlador)** con directorio `src/controllers/` (`AuthController`, `VehiculoController`, `SocioController`, `MantenimientoController`, `UsuarioController`, `ReporteController`).
- Capa de **Modelos POO** con herencia de `BaseModel` (`Usuario`, `Rol`, `Socio`, `Vehiculo`, `TipoMantenimiento`, `MantenimientoProgramado`, `HistorialMantenimiento`).
- Soporte de **3 niveles de acceso funcionales** (`Administrador`, `Mecanico`, `Operador`) con control de permisos y vistas según rol.
- Módulo de **Gestión de Usuarios** (`usuarios_view.py`) para administradores con restablecimiento de contraseñas y desactivación.
- Seguridad robusta con **PBKDF2-HMAC-SHA256**, sal criptográfica de 16 bytes y verificación de tiempo constante (`seguridad_service.py`).
- Implementación de **Eliminación Lógica (*Soft Delete*)** mediante campo `activo` en las tablas `socio`, `vehiculo`, `tipo_mantenimiento`, `mantenimiento_programado` y `usuario`.
- Módulo de generación de **5 Reportes Oficiales**:
  - Reporte 1: Ficha Técnica y Estado General de la Flota (PDF con ReportLab).
  - Reporte 2: Plan Preventivo y Alertas Semaforizadas (PDF con ReportLab).
  - Reporte 3: Bitácora Histórica de Mantenimiento y Costos (Excel con OpenPyXL y fórmulas automáticas `=SUM(...)`).
  - Reporte 4: Directorio Institucional de Socios y Unidades Asignadas (PDF con ReportLab).
  - Reporte 5: Resumen Ejecutivo y Métricas de Rendimiento por Taller (Excel con OpenPyXL).
- Nueva vista interactiva de exportación de reportes (`reportes_view.py`).
- Identidad visual corporativa con **logotipo e isotipo en PNG de alta resolución con transparencia** cargado mediante `customtkinter.CTkImage` y `Pillow`.
- Base de datos ampliada a **7 entidades normalizadas en 3FN** (añadidas tablas `rol` y `usuario`).
- Suite de pruebas unitarias ampliada a 8 pruebas automatizadas (`test_sistema_integral.py`).

### Modificado
- Vistas refactorizadas para consumir los controladores MVC.
- Actualización de `main_window.py` para soportar cierre de sesión (`Logout`) y navegación dinámica por roles.
- `requirements.txt` ampliado con `reportlab`, `openpyxl` y `pillow`.

## [1.2.0] - 2026-09-30

### Agregado
- Pantalla de inicio de sesión y autenticación previa ([`login_view.py`](src/views/login_view.py)).
- Servicio de validación de credenciales de administrador ([`autenticacion_service.py`](src/services/autenticacion_service.py)).
- Documentación de acceso al sistema y alcance de seguridad ([`LOGIN.md`](docs/LOGIN.md)).
- Prueba unitaria de autenticación ([`test_services.py`](tests/test_services.py)) elevando la suite a 3 pruebas automáticas.

### Modificado
- Integración en [`main_window.py`](src/views/main_window.py) para requerir autenticación exitosa antes de inicializar la barra de navegación y las vistas de gestión.
- Actualización de manuales de usuario y diagramas arquitectónicos para reflejar la ventana modal de login.

## [1.1.0] - 2026-09-27

### Agregado
- Módulo centralizado de temas y estilos visuales ([`theme.py`](src/views/theme.py)).
- Paleta unificada de colores para botones (éxito, primario, neutral, peligro, advertencia, acento).
- Estilos y tags globales para semáforos en tablas `ttk.Treeview`.
- Tipografías y dimensiones estándar para componentes de interfaz gráfica.
- Modelos de enumeraciones para estados del sistema ([`enums.py`](src/models/enums.py)).

### Modificado
- Refactorización de vistas ([`dashboard_view.py`](src/views/dashboard_view.py), [`vehiculos_view.py`](src/views/vehiculos_view.py), [`socios_view.py`](src/views/socios_view.py), [`programacion_mant_view.py`](src/views/programacion_mant_view.py), [`tipos_mant_view.py`](src/views/tipos_mant_view.py)) para consumir [`theme.py`](src/views/theme.py).
- Mejorada la legibilidad y espaciado de columnas en tablas de datos.

## [1.0.0] - 2026-09-15

### Agregado
- Versión inicial del Sistema de Control de Mantenimiento Preventivo para *Brisas del Palmar*.
- Arquitectura desacoplada en 3 capas: Presentación (`views`), Lógica de Negocio (`services`) y Acceso a Datos (`repositories`).
- Base de datos SQLite portable con inicialización automática de esquema DDL ([`schema.sql`](database/schema.sql)).
- Catálogo de 10 rutinas estándar precargadas ([`seeds.sql`](database/seeds.sql)).
- Módulos funcionales:
  - Dashboard con KPIs y alertas críticas en tiempo real.
  - Gestión de Flota y Unidades con actualización rápida de odómetro.
  - Gestión de Socios y Propietarios con restricciones de integridad.
  - Tablero de Control Preventivo con motor de semaforización (🟢 Al Día, 🟡 Por Vencer, 🔴 Vencido).
  - Catálogo CRUD de tipos de mantenimiento preventivo.
  - Bitácora e historial detallado de servicios ejecutados y auditoría de costos.
- Soporte para cambio de tema visual dinámico (Oscuro / Claro / Sistema).
- Suite de pruebas unitarias automáticas ([`test_services.py`](tests/test_services.py)).
