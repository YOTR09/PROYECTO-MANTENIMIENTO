# 🗄️ La Base de Datos: ¿Cómo se guarda la información?

> **Nivel:** Principiante — explicamos las bases de datos sin fórmulas ni tecnicismos.

---

## 📚 ¿Qué es una base de datos?

Imagina que tienes que llevar el registro de todos los autobuses de la empresa en papel. Tendrías:
- Una carpeta con las fichas de cada autobús
- Otra carpeta con los propietarios
- Otra carpeta con los mantenimientos realizados
- Etc.

Una **base de datos** es exactamente eso, pero digital y muchísimo más poderosa. Puede buscar, ordenar y relacionar información en fracciones de segundo.

---

## 🗃️ Las 7 "fichas" del sistema (Tablas)

La base de datos de este proyecto tiene **7 tablas**, que son como 7 tipos de fichas diferentes:

### 1. 📋 Tabla `rol` — Los tipos de usuarios
Define los 3 niveles de acceso al sistema.

| Campo | Descripción |
|---|---|
| `id_rol` | Número único del rol |
| `nombre` | Nombre del rol: Administrador, Mecanico u Operador |
| `descripcion` | Descripción del rol |

---

### 2. 👤 Tabla `usuario` — Las personas que usan el sistema
Guarda la información de cada persona que puede iniciar sesión.

| Campo | Descripción |
|---|---|
| `id_usuario` | Número único del usuario |
| `username` | Nombre de usuario (ej: `admin`) |
| `password_hash` | La contraseña cifrada (no se guarda en texto plano) |
| `nombre_completo` | Nombre real de la persona |
| `activo` | 1 = activo, 0 = desactivado |

---

### 3. 👥 Tabla `socio` — Los propietarios de los autobuses
Registra a los afiliados o dueños de las unidades de transporte.

| Campo | Descripción |
|---|---|
| `id_socio` | Número único del socio |
| `cedula` | Número de cédula o RIF |
| `nombre_completo` | Nombre del propietario |
| `telefono` | Número de contacto |
| `estado` | Activo o Inactivo |

---

### 4. 🚌 Tabla `vehiculo` — Los autobuses
Es el inventario de toda la flota vehicular.

| Campo | Descripción |
|---|---|
| `id_vehiculo` | Número único del vehículo |
| `numero_unidad` | Nombre interno (ej: "Unidad 01", "Bus 14") |
| `placa` | Matrícula del vehículo |
| `marca_modelo` | Ej: "Encava NT-610" |
| `kilometraje_actual` | Odómetro actual en kilómetros |
| `status` | Activo / En Taller / Inactivo |
| `id_socio` | A quién pertenece este autobús |

---

### 5. 🔧 Tabla `tipo_mantenimiento` — El catálogo de rutinas
Define qué tipos de mantenimiento existen y cada cuánto tiempo/km deben hacerse.

| Campo | Descripción |
|---|---|
| `nombre` | Ej: "Cambio de Aceite y Filtro" |
| `intervalo_km` | Cada cuántos km se repite (ej: 5000) |
| `intervalo_dias` | Cada cuántos días se repite (ej: 90) |

El sistema viene con **10 rutinas preinstaladas**, por ejemplo:
- Cambio de aceite cada 5,000 km
- Revisión de frenos cada 10,000 km
- Cambio de neumáticos cada 50,000 km

---

### 6. 📅 Tabla `mantenimiento_programado` — Los mantenimientos pendientes
Registra el plan de mantenimiento de cada vehículo: cuándo fue el último servicio y cuándo debe ser el próximo.

| Campo | Descripción |
|---|---|
| `id_vehiculo` | A qué autobús corresponde |
| `id_tipo` | Qué tipo de mantenimiento es |
| `fecha_ultimo_servicio` | Cuándo se hizo por última vez |
| `km_ultimo_servicio` | Con cuántos km se hizo |
| `fecha_proximo_servicio` | Cuándo debe hacerse el próximo |
| `km_proximo_servicio` | A qué km debe hacerse el próximo |

Esta tabla es la que alimenta los **semáforos de alerta** 🔴🟡🟢.

---

### 7. 📜 Tabla `historial_mantenimiento` — La bitácora
Guarda el registro permanente de cada mantenimiento que se realizó. Esta información **nunca se borra**.

| Campo | Descripción |
|---|---|
| `fecha_realizado` | Cuándo se hizo |
| `km_al_momento` | Con cuántos km estaba el autobús |
| `costo` | Cuánto costó el servicio |
| `taller_mecanico` | En qué taller se hizo |
| `descripcion_trabajo` | Qué se hizo exactamente |

---

## 🔗 ¿Cómo se relacionan las tablas entre sí?

Las tablas no están aisladas — están **conectadas** entre sí mediante "llaves" o IDs.

```
👥 SOCIO ──────────────────── 🚌 VEHÍCULO
   "Juan Pérez"               "Unidad 01" (de Juan Pérez)
   (id_socio = 5)             (id_socio = 5) ← ¡Conectado!

🚌 VEHÍCULO ────────────────── 📅 MANT. PROGRAMADO
   "Unidad 01"                Cambio de aceite programado
   (id_vehiculo = 1)          (id_vehiculo = 1) ← ¡Conectado!

🚌 VEHÍCULO ────────────────── 📜 HISTORIAL
   "Unidad 01"                "Se cambió aceite el 15/01/2026, costó $50"
   (id_vehiculo = 1)          (id_vehiculo = 1) ← ¡Conectado!
```

> 💡 **Analogía:** Es como las fichas de una biblioteca. El libro tiene el nombre del autor, y hay otra ficha con los datos del autor. Están conectadas por el mismo código, pero en fichas separadas para no repetir información.

---

## 🛡️ Eliminación lógica — ¿Qué significa que algo se "desactive"?

Cuando borras un vehículo o socio en este sistema, **no se borra realmente** de la base de datos. En cambio, se cambia un campo llamado `activo` de `1` (activo) a `0` (inactivo).

¿Por qué? Porque aunque el vehículo ya no opere, el **historial de mantenimiento pasado sigue siendo valioso** para auditorías, estadísticas, y registros legales.

```
ANTES: activo = 1  → El vehículo aparece en las listas
DESPUÉS DEL "BORRADO": activo = 0  → El vehículo no aparece, pero sus datos existen
```

> 💡 **Analogía:** Es como cuando un empleado renuncia a una empresa — no borran todos sus registros, simplemente ya no está "activo" en la nómina.

---

## 📁 El archivo de la base de datos

Toda esta información vive en UN SOLO ARCHIVO:

```
📁 data/
    └── 📄 mantenimiento.db   ← ¡Aquí está TODO!
```

Para hacer un **respaldo** (backup) de toda la información del sistema, simplemente copia este archivo a otro lugar. ¡Así de simple!

---

⬅️ [Anterior: Cómo funciona por dentro](./04-COMO-FUNCIONA-POR-DENTRO.md) | ➡️ [Siguiente: Seguridad y usuarios](./06-SEGURIDAD-Y-USUARIOS.md)
