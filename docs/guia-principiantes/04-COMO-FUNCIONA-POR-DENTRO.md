# ⚙️ ¿Cómo funciona el programa por dentro?

> **Nivel:** Principiante-intermedio — aquí explicamos la arquitectura MVC con analogías.

---

## 🏗️ El patrón MVC: la gran idea detrás del proyecto

El código de este proyecto no está escrito de forma desordenada. Sigue un **patrón de diseño** llamado **MVC**, que significa:

- **M**odelo (Model)
- **V**ista (View)
- **C**ontrolador (Controller)

Este patrón divide el código en capas con responsabilidades bien definidas, igual que en una empresa los empleados tienen roles distintos.

---

## 🍕 La analogía de la pizzería

Para entender MVC, imaginemos una pizzería:

```
👤 CLIENTE
    │
    │  "Quiero una pizza margarita"
    ▼
🧑‍💼 MESERO (= VISTA / VIEW)
    │   Toma el pedido y lo pasa al
    ▼
🧠 GERENTE (= CONTROLADOR / CONTROLLER)
    │   Coordina y da instrucciones al
    ▼
👨‍🍳 COCINERO + RECETAS + DESPENSA (= MODELO + REPOSITORIO)
    │   Prepara la pizza según la receta
    ▼
🍕 PIZZA LISTA → vuelve al MESERO → llega al CLIENTE
```

En el programa:
- El **Cliente** = Tú, usando la pantalla
- El **Mesero (Vista)** = Los archivos en `src/views/` — muestra la información, captura lo que escribes
- El **Gerente (Controlador)** = Los archivos en `src/controllers/` — coordina y decide qué hacer
- El **Cocinero + Recetas + Despensa (Modelo + Repositorio)** = Los archivos en `src/models/` y `src/repositories/` — definen los datos y los guardan/recuperan

---

> 📐 Los diagramas formales (MVC, UML de clases, secuencia, ER) están en [`../DIAGRAMAS.md`](../DIAGRAMAS.md).

## 🔄 Las capas del sistema explicadas

### 1️⃣ CAPA DE VISTA (`src/views/`) — Lo que ves
**Responsabilidad:** Mostrar información en pantalla y capturar lo que el usuario hace (clics, texto escrito, etc.).

**Regla de oro:** Las vistas **nunca** acceden directamente a la base de datos. Solo "hablan" con los controladores.

**Ejemplo:** Cuando haces clic en "Guardar Vehículo", la vista le dice al controlador: "El usuario quiere guardar esto", y el controlador hace el resto.

---

### 2️⃣ CAPA DE CONTROLADOR (`src/controllers/`) — El coordinador
**Responsabilidad:** Recibir lo que pide la vista, validar los datos, aplicar las reglas de negocio, llamar al repositorio correcto y devolver el resultado como `(ok, dato, mensaje)`.

**Los controladores del proyecto:**
| Archivo | ¿Qué coordina? |
|---|---|
| `auth_controller.py` | El inicio y cierre de sesión |
| `vehiculo_controller.py` | Las acciones sobre vehículos |
| `socio_controller.py` | Las acciones sobre socios |
| `mantenimiento_controller.py` | Las acciones sobre mantenimientos |
| `usuario_controller.py` | La gestión de usuarios |
| `reporte_controller.py` | La generación de reportes |

---

### 3️⃣ CAPA DE SERVICIO (`src/services/`) — Heredada, con una pieza activa
En la versión 1.x las reglas de negocio vivían aquí. Desde la versión 2.0 esas reglas se movieron a los **controladores**. Hoy:

- **`seguridad_service.py`** — ✅ **ACTIVO**: cifra y verifica contraseñas (PBKDF2) y normaliza respuestas secretas. Lo usan `AuthController` y `UsuarioController`.
- El resto (`mantenimiento_service.py`, `vehiculo_service.py`, `socio_service.py`, `tipo_mantenimiento_service.py`, `autenticacion_service.py`) es **heredado (legacy)**: la aplicación no lo usa; solo lo ejercitan las pruebas de `tests/test_services.py`.

**Ejemplo del semáforo** (hoy en `MantenimientoController.calcular_estado_alerta`; se evalúan km **y** días, y gana el más grave):
```
Si km_restantes <= 0   o  días_restantes <= 0    → VENCIDO 🔴
Si km_restantes <= 500 o  días_restantes <= 10   → POR VENCER 🟡
Si no                                            → AL DÍA 🟢
```

---

### 4️⃣ CAPA DE REPOSITORIO (`src/repositories/`) — El archivero
**Responsabilidad:** Guardar y recuperar datos de la base de datos. Aquí están todas las consultas SQL.

**Regla de oro:** Solo los repositorios "hablan" directamente con la base de datos. El resto del programa no sabe nada de SQL.

**Ejemplo:** Cuando necesitas la lista de vehículos activos, el repositorio ejecuta:
```sql
SELECT * FROM vehiculo WHERE activo = 1
```
Y devuelve una lista de objetos Python listos para usar.

---

## 🔁 Flujo completo: ¿qué pasa cuando abres el programa?

```
1. Ejecutas main.py
      │
      ▼
2. Se inicializa la base de datos (si es la primera vez)
      │
      ▼
3. Se abre la ventana de LOGIN (login_view.py)
      │
      ▼
4. Escribes usuario y contraseña → Clic en "Entrar"
      │
      ▼
5. AuthController busca el usuario (UsuarioRepository) y verifica la contraseña con SeguridadService
      │
      ├── Si es INCORRECTO → La vista muestra un mensaje de error
      │
      └── Si es CORRECTO → Se carga la ventana principal (main_window.py)
                │
                ▼
          6. Aparece el Dashboard con las alertas del día
                │
                ▼
          7. MantenimientoController consulta el MantenimientoRepository
                │
                ▼
          8. La base de datos devuelve los datos
                │
                ▼
          9. MantenimientoController calcula el estado de cada semáforo
                │
                ▼
         10. DashboardView muestra los datos con los colores correctos 🎨
```

---

## 📦 Los Modelos (`src/models/`) — La definición de los datos

Un **modelo** es simplemente la definición de cómo es un objeto. Por ejemplo, el modelo `Vehiculo` define que un vehículo tiene:
- Un número de unidad
- Una placa
- Una marca y modelo
- Un kilometraje actual
- Un estado (Activo, En Taller, Inactivo)
- etc.

Es como el molde de una galleta — define la forma que tendrán todos los datos de vehículos.

**Todos los modelos heredan de `BaseModel`** (clase base con `from_dict()` y `to_dict()`).

**Los modelos del proyecto:**
| Archivo | ¿Qué define? |
|---|---|
| `vehiculo.py` | Qué datos tiene un vehículo |
| `socio.py` | Qué datos tiene un socio/propietario |
| `usuario.py` | Qué datos tiene un usuario del sistema |
| `mantenimiento.py` | Mantenimiento programado e historial de mantenimiento |
| `base_model.py` | Clase base con `from_dict()` / `to_dict()` |
| `tipo_mantenimiento.py` | Qué datos tiene un tipo de mantenimiento |
| `rol.py` | Qué datos tiene un rol de usuario |
| `enums.py` | Listas fijas de valores (estados posibles) |

---

## 🎨 El tema visual (`src/views/theme.py`)

Este archivo centraliza todos los colores y estilos visuales del programa. En lugar de que cada pantalla invente sus propios colores, todas usan los colores definidos aquí.

Por ejemplo:
- 🔴 Rojo de peligro: `#EF4444`
- 🟡 Amarillo de advertencia: `#F59E0B`
- 🟢 Verde de éxito: `#10B981`
- 🔵 Azul de información: `#3B82F6`

---

⬅️ [Anterior: Cómo está organizado](./03-COMO-ESTA-ORGANIZADO.md) | ➡️ [Siguiente: La base de datos](./05-LA-BASE-DE-DATOS.md)
