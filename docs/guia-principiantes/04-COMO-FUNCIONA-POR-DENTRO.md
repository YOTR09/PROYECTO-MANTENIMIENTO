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
👨‍🍳 COCINERO + RECETAS (= MODELO + SERVICIO)
    │   Prepara la pizza según la receta
    ▼
🍕 PIZZA LISTA → vuelve al MESERO → llega al CLIENTE
```

En el programa:
- El **Cliente** = Tú, usando la pantalla
- El **Mesero (Vista)** = Los archivos en `src/views/` — muestra la información, captura lo que escribes
- El **Gerente (Controlador)** = Los archivos en `src/controllers/` — coordina y decide qué hacer
- El **Cocinero + Recetas (Servicio + Modelo)** = Los archivos en `src/services/` y `src/models/` — aplica las reglas del negocio

---

## 🔄 Las 4 capas del sistema explicadas

### 1️⃣ CAPA DE VISTA (`src/views/`) — Lo que ves
**Responsabilidad:** Mostrar información en pantalla y capturar lo que el usuario hace (clics, texto escrito, etc.).

**Regla de oro:** Las vistas **nunca** acceden directamente a la base de datos. Solo "hablan" con los controladores.

**Ejemplo:** Cuando haces clic en "Guardar Vehículo", la vista le dice al controlador: "El usuario quiere guardar esto", y el controlador hace el resto.

---

### 2️⃣ CAPA DE CONTROLADOR (`src/controllers/`) — El coordinador
**Responsabilidad:** Recibir lo que pide la vista, llamar al servicio correcto, y devolver el resultado.

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

### 3️⃣ CAPA DE SERVICIO (`src/services/`) — Las reglas del negocio
**Responsabilidad:** Aplicar la lógica de negocio. Por ejemplo: "¿Está vencido este mantenimiento?", "¿Es válida esta contraseña?", "¿Cuál es la fecha del próximo servicio?"

**Ejemplo del sistema de semáforo:**
```
Si (km_próximo - km_actual) <= 0    → Estado VENCIDO 🔴
Si (km_próximo - km_actual) <= 500  → Estado POR VENCER 🟡
Si no                               → Estado AL DÍA 🟢
```
Esta lógica vive en `mantenimiento_service.py`.

**Los servicios del proyecto:**
| Archivo | ¿Qué reglas aplica? |
|---|---|
| `mantenimiento_service.py` | Calcula alertas, próximos servicios, dashboard |
| `vehiculo_service.py` | Valida y gestiona vehículos |
| `socio_service.py` | Valida y gestiona socios |
| `seguridad_service.py` | Cifra y verifica contraseñas |
| `autenticacion_service.py` | Gestiona la sesión activa |
| `tipo_mantenimiento_service.py` | Gestiona el catálogo de rutinas |

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
5. AuthController verifica credenciales con SeguridadService
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
          9. MantenimientoService calcula el estado de cada semáforo
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

**Los modelos del proyecto:**
| Archivo | ¿Qué define? |
|---|---|
| `vehiculo.py` | Qué datos tiene un vehículo |
| `socio.py` | Qué datos tiene un socio/propietario |
| `usuario.py` | Qué datos tiene un usuario del sistema |
| `mantenimiento.py` | Qué datos tiene un mantenimiento |
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
