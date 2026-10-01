# 📁 ¿Cómo está organizado el proyecto?

> **Nivel:** Principiante — explicamos cada carpeta como si fuera un cajón de un escritorio.

---

## 🗂️ ¿Qué es la "estructura de carpetas"?

Cuando abres el proyecto en tu computadora, ves un montón de carpetas y archivos. Esto puede parecer confuso al principio, pero tiene una lógica muy clara. Cada carpeta tiene **un propósito específico**, como los cajones de un escritorio organizado.

---

## 🗺️ Vista general del proyecto

```
PROYECTO-MANTENIMIENTO/        ← La carpeta raíz (la principal de todo)
│
├── 📄 main.py                 ← El punto de arranque del programa
├── 📄 requirements.txt        ← Lista de herramientas necesarias
├── 📄 README.md               ← Resumen del proyecto
├── 📄 CHANGELOG.md            ← Historial de cambios y mejoras
│
├── 📂 src/                    ← Todo el código fuente del programa
├── 📂 config/                 ← Configuración de la base de datos
├── 📂 database/               ← Plantillas de la base de datos (SQL)
├── 📂 data/                   ← Aquí se guarda la base de datos real
├── 📂 assets/                 ← Imágenes y logos del sistema
├── 📂 docs/                   ← Toda la documentación (¡incluida esta guía!)
├── 📂 tests/                  ← Pruebas automáticas del código
└── 📂 venv/                   ← El entorno virtual de Python (no tocar)
```

---

## 📂 Carpeta por carpeta: ¿qué hay adentro?

### 📄 `main.py` — El punto de arranque
Este es el archivo que le dices a Python que ejecute para iniciar el programa. Es como el botón de encendido. Solo hace dos cosas:
1. Prepara la base de datos si es la primera vez.
2. Abre la ventana principal de la aplicación.

---

### 📄 `requirements.txt` — La lista de compras
Tiene la lista de todas las librerías externas que el proyecto necesita. Cuando ejecutas `pip install -r requirements.txt`, Python va y descarga todo lo de esa lista.

Contenido actual:
```
customtkinter>=6.0.0    ← Para la interfaz gráfica
reportlab>=4.0.0        ← Para generar PDFs
openpyxl>=3.1.0         ← Para generar Excel
pillow>=10.0.0          ← Para manejar imágenes
```

---

### 📂 `src/` — El corazón del programa
Esta es la carpeta más importante. Contiene todo el código que hace funcionar el programa. Está dividida en subcarpetas especializadas:

```
src/
├── 📂 views/           ← Lo que el usuario VE (pantallas, botones)
├── 📂 controllers/     ← El "cerebro" que coordina todo
├── 📂 models/          ← La definición de los datos (qué es un vehículo, etc.)
├── 📂 services/        ← Las reglas del negocio (cómo calcular alertas, etc.)
├── 📂 repositories/    ← Cómo se guarda y recupera información de la BD
└── 📂 reports/         ← Cómo se generan los PDF y Excel
```

> Esto se explica en detalle en el [documento 04](./04-COMO-FUNCIONA-POR-DENTRO.md).

---

### 📂 `config/` — La configuración
Contiene `database.py`, que es el archivo que sabe:
- Dónde está guardada la base de datos
- Cómo conectarse a ella
- Cómo inicializarla si es nueva

---

### 📂 `database/` — Los planos de la base de datos
Contiene dos archivos SQL (instrucciones para la base de datos):

- **`schema.sql`** — Define la estructura: qué tablas existen, qué columnas tienen. Es como el plano de un edificio.
- **`seeds.sql`** — Carga los datos iniciales: los 10 tipos de mantenimiento que vienen preinstalados. Es como el mobiliario inicial.

---

### 📂 `data/` — Los datos reales
Aquí vive el archivo que contiene toda la información real del sistema:
- **`mantenimiento.db`** — La base de datos real con vehículos, socios, historial, etc.
- **`test_mantenimiento.db`** — Una copia separada que se usa para pruebas (no afecta los datos reales).

> ⚠️ **¡Importante!** Si quieres hacer un respaldo del sistema, **copia este archivo**. Todo está ahí.

---

### 📂 `assets/` — Las imágenes
Contiene los logos e íconos de la empresa:
- `logo_empresa.png` — Logo principal
- `logo_empresa_dark.png` — Versión del logo para pantallas oscuras
- `logo_empresa_light.png` — Versión del logo para pantallas claras
- `icono_empresa.png` — Ícono pequeño de la empresa

---

### 📂 `docs/` — La documentación
Es donde está toda la documentación del proyecto, ¡incluyendo esta guía que estás leyendo ahora!

---

### 📂 `tests/` — Las pruebas automáticas
Contiene programas especiales que prueban automáticamente que el código funcione bien. Son como el "control de calidad" del software.

---

### 📂 `venv/` — El entorno virtual
Esta carpeta la crea Python automáticamente y contiene una copia aislada de Python con todas las librerías instaladas solo para este proyecto. **No necesitas tocarla nunca**, pero tampoco la borres.

---

## 🧩 Dentro de `src/views/` — Las pantallas del programa

Esta es la subcarpeta más grande. Cada archivo corresponde a una pantalla del programa:

| Archivo | Pantalla que crea |
|---|---|
| `login_view.py` | Pantalla de inicio de sesión |
| `main_window.py` | Ventana principal con menú lateral |
| `dashboard_view.py` | Panel de control con alertas y KPIs |
| `vehiculos_view.py` | Gestión de la flota de autobuses |
| `socios_view.py` | Gestión de socios y propietarios |
| `programacion_mant_view.py` | Tablero de mantenimientos programados |
| `tipos_mant_view.py` | Catálogo de tipos de mantenimiento |
| `historial_mant_view.py` | Bitácora histórica de servicios |
| `reportes_view.py` | Centro de generación de reportes |
| `usuarios_view.py` | Gestión de usuarios del sistema |
| `theme.py` | Colores, estilos y diseño visual |
| `recuperar_password_modal.py` | Ventana para recuperar contraseña |

---

⬅️ [Anterior: Herramientas y tecnologías](./02-HERRAMIENTAS-Y-TECNOLOGIAS.md) | ➡️ [Siguiente: Cómo funciona por dentro](./04-COMO-FUNCIONA-POR-DENTRO.md)
