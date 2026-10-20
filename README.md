# Sistema de Control de Mantenimiento Preventivo — Brisas del Palmar

Aplicación de escritorio moderna y profesional desarrollada en **Python** con **CustomTkinter** y patrón de diseño **MVC (Modelo - Vista - Controlador)** para la gestión de flota y control de mantenimientos preventivos de la empresa de transporte público **Brisas del Palmar**.

---

## 🚀 Características Principales

1. **Patrón Arquitectónico MVC (Modelo - Vista - Controlador):**
   - **Vistas (`src/views/`):** Interfaz gráfica moderna, reactiva y estilizada con CustomTkinter.
   - **Controladores (`src/controllers/`):** Orquestación desacoplada de la lógica, validaciones y permisos.
   - **Modelos (`src/models/`):** Entidades de dominio con programación orientada a objetos (POO).
   - **Repositorios (`src/repositories/`):** Consultas SQL parametrizadas y aisladas del motor SQLite (acceso a datos del Modelo).
   - Diagramas MVC y UML: [`docs/DIAGRAMAS.md`](docs/DIAGRAMAS.md).

2. **Seguridad Robusta y 3 Niveles de Acceso (Roles):**
   - Autenticación persistida en base de datos con **PBKDF2-HMAC-SHA256**, sal criptográfica de 16 bytes y verificación de tiempo constante (`secrets.compare_digest`).
   - **3 Perfiles de Usuario Funcionales:**
     * **Administrador (`admin` / `admin123`):** Acceso total y gestión de usuarios.
     * **Mecánico (`mecanico` / `mecanico123`):** Gestión de taller, programación y registro de mantenimientos.
     * **Operador / Auditor (`auditor` / `auditor123`):** Modo consulta de flota y emisión de reportes.

3. **Operaciones CRUD con Eliminación Lógica (*Soft Delete*):**
   - Las operaciones de baja desactivan los registros (`activo = 0`), preservando intacto el historial técnico, las auditorías y los costos pasados.

4. **Identidad Visual Corporativa:**
   - Logotipo e isotipo institucional de "Brisas del Palmar" integrado en alta resolución con canal alfa mediante `customtkinter.CTkImage` y `Pillow`.

5. **Módulo de Reportes Oficiales (PDF y Excel):**
   - **Reporte 1 (PDF):** Ficha Técnica y Estado General de la Flota Vehicular.
   - **Reporte 2 (PDF):** Plan de Mantenimiento Preventivo y Alertas Semaforizadas (🔴, 🟡, 🟢).
   - **Reporte 3 (Excel):** Bitácora Histórica y Costos con Fórmulas Automáticas (`=SUM(...)`).
   - **Reporte 4 (PDF):** Directorio Institucional de Socios y Unidades Asignadas.
   - **Reporte 5 (Excel):** Resumen Ejecutivo y Métricas de Rendimiento por Taller Mecánico.

6. **Base de Datos Normalizada (7 Entidades en 3FN):**
   - `rol`, `usuario`, `socio`, `vehiculo`, `tipo_mantenimiento`, `mantenimiento_programado`, `historial_mantenimiento`.

---

## 💻 Instalación y Ejecución

```bash
# 1. Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Iniciar la aplicación
python3 main.py
```

### Ejecución de Pruebas Unitarias
```bash
python3 -m unittest discover tests -v
```
La suite incluye 21 pruebas (3 + 8 + 10) y requiere las dependencias de `requirements.txt` instaladas.

---

## 👥 Credenciales de Prueba

| Nivel de Acceso | Usuario | Contraseña |
|---|---|---|
| **Administrador** | `admin` | `admin123` |
| **Mecánico** | `mecanico` | `mecanico123` |
| **Operador / Auditor** | `auditor` | `auditor123` |

## 📚 Documentación

| Documento | Contenido |
|---|---|
| [`docs/README.md`](docs/README.md) | Índice general |
| [`docs/ARQUITECTURA.md`](docs/ARQUITECTURA.md) | Arquitectura MVC/capas, BD, semáforo, estructura de carpetas |
| [`docs/DIAGRAMAS.md`](docs/DIAGRAMAS.md) | **Todos los diagramas:** MVC, UML de clases, ER, casos de uso, secuencia, estados, actividad, despliegue |
| [`docs/GUIA_INSTALACION_Y_USO.md`](docs/GUIA_INSTALACION_Y_USO.md) | Instalación y manual de usuario |
| [`docs/LOGIN.md`](docs/LOGIN.md) | Autenticación y seguridad |
| [`docs/guia-principiantes/`](docs/guia-principiantes/00-INDICE.md) | Guía para principiantes |
| [`CHANGELOG.md`](CHANGELOG.md) | Historial de versiones |
