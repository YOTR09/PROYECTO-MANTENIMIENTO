# Registro de Cambios (Changelog)

Todas las modificaciones notables de este proyecto serán documentadas en este archivo.
El formato se basa en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/).

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
