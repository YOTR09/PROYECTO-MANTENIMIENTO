# 📚 Centro de Documentación

## Sistema de Control de Mantenimiento Preventivo — Brisas del Palmar

Bienvenido al centro de documentación técnica y operativa del proyecto. Aquí encontrarás toda la información necesaria para comprender la arquitectura del sistema, desplegarlo y utilizarlo eficientemente.

---

## 📑 Índice de Documentos

1. [🌱 Guía Técnica para Principiantes (guia-principiantes/00-INDICE.md)](guia-principiantes/00-INDICE.md)
   - Explicación paso a paso y sin tecnicismos del funcionamiento del sistema, herramientas, base de datos, seguridad, reportes y glosario. Ideal para inductores, directivos y nuevos programadores.

2. [📐 Catálogo de Diagramas (DIAGRAMAS.md)](DIAGRAMAS.md)
   - **16 diagramas:** MVC, capas y dependencias, UML de clases (modelos, controladores, vistas, reportes), ER, casos de uso por rol, secuencia (login, registrar servicio, reportes, recuperación), estados del semáforo, actividad de arranque, navegación y despliegue.

3. [🏛️ Arquitectura y Estructura del Sistema (ARQUITECTURA.md)](ARQUITECTURA.md)
   - **Patrón MVC por capas:** Vista (CustomTkinter), Controladores y Repositorios (acceso a SQLite), con modelos de dominio transversales.
   - **Modelo de Datos Normalizado (3FN):** Diagrama ER con las 7 entidades (`rol`, `usuario`, `socio`, `vehiculo`, `tipo_mantenimiento`, `mantenimiento_programado`, `historial_mantenimiento`).
   - **Motor de Semaforización:** Algoritmos y fórmulas para alertas 🟢 *Al Día*, 🟡 *Por Vencer* y 🔴 *Vencido*.
   - **Centro de Reportes:** Generadores independientes para PDF y Excel.

4. [📖 Guía de Instalación y Manual de Usuario (GUIA_INSTALACION_Y_USO.md)](GUIA_INSTALACION_Y_USO.md)
   - Requisitos previos, pasos de instalación con entorno virtual (`venv`) y manual detallado de los módulos (acceso, socios, flota, catálogo, preventivo, dashboard, bitácora, reportes, usuarios y tema) funcionales de la aplicación.
   - Procedimientos de respaldo (*backups*) y ejecución de la suite de 21 pruebas unitarias.

5. [🔐 Acceso al Sistema y Seguridad (LOGIN.md)](LOGIN.md)
   - Credenciales de prueba para los 3 perfiles funcionales (`admin`, `mecanico`, `auditor`).
   - Cifrado seguro con **PBKDF2-HMAC-SHA256**, sal aleatoria y verificación en tiempo constante.
   - Flujo de recuperación de contraseñas mediante preguntas secretas y clave maestra.

---
Para volver a la raíz del proyecto, consulta el [`README.md`](../README.md) principal.
