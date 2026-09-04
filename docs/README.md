# 📚 Centro de Documentación
## Sistema de Control de Mantenimiento Preventivo — Brisas del Palmar

Bienvenido al centro de documentación técnica y operativa del proyecto. Aquí encontrarás toda la información necesaria para comprender la arquitectura del sistema, desplegarlo y utilizarlo eficientemente.

---

## 📑 Índice de Documentos

1. ### [🏛️ Arquitectura y Estructura del Sistema (ARQUITECTURA.md)](ARQUITECTURA.md)
   - **Patrón de Arquitectura en 3 Capas:** Presentación (CustomTkinter), Lógica de Negocio (Services) y Acceso a Datos (Repositories).
   - **Justificación de SQLite:** Portabilidad, cero configuración y rendimiento local.
   - **Modelo de Datos y Diagrama ER:** Entidades `socio`, `vehiculo`, `tipo_mantenimiento`, `mantenimiento_programado` e `historial_mantenimiento`.
   - **Motor de Semaforización Preventiva:** Algoritmo y fórmulas para los estados 🟢 *Al Día*, 🟡 *Por Vencer* y 🔴 *Vencido*.
   - **Estructura detallada del proyecto:** Explicación de cada archivo y directorio.

2. ### [📖 Guía de Instalación y Manual de Usuario (GUIA_INSTALACION_Y_USO.md)](GUIA_INSTALACION_Y_USO.md)
   - **Requisitos del Sistema:** Versiones compatibles de Python y soporte de Tkinter.
   - **Instalación paso a paso:** Creación de entorno virtual e instalación de dependencias con `pip`.
   - **Manual de Usuario por Módulos:**
     - Módulo 1: Gestión de Socios y Afiliados.
     - Módulo 2: Gestión de Flota (N° de Unidad, Placa, Odómetro) y actualización rápida de kilometraje.
     - Módulo 3: Catálogo de Mantenimientos (CRUD y las 10 rutinas precargadas).
     - Módulo 4: Control Preventivo y registro de mantenimientos ejecutados.
     - Módulo 5: Dashboard y lectura de alertas urgentes.
     - Módulo 6: Bitácora Histórica y auditoría de costos.
     - Módulo 7: Cambio de Modo Visual (Oscuro / Claro).
   - **Copias de Seguridad (Backups):** Cómo respaldar y restaurar la base de datos `data/mantenimiento.db`.
   - **Pruebas Automatizadas:** Cómo ejecutar los tests unitarios.

---

Para volver a la raíz del proyecto, consulta el [`README.md`](../README.md) principal.

