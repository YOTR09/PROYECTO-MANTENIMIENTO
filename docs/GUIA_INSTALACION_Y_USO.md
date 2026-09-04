# 📖 Guía de Instalación y Manual de Usuario
## Sistema de Control de Mantenimiento Preventivo — Brisas del Palmar

---

## 📋 Requisitos Previos

Antes de instalar y ejecutar la aplicación, asegúrate de contar con:
- **Python 3.10 o superior** instalado en el sistema.
- Soporte para **Tkinter** habilitado en Python.
  - En Linux (Ubuntu/Debian): `sudo apt-get install python3-tk`
  - En Linux (Arch/Manjaro): `sudo pacman -S tk`
  - En Windows y macOS: Tkinter viene incluido por defecto en el instalador oficial de Python.

---

## ⚙️ Instalación Paso a Paso

### 1. Clonar o descargar el repositorio
Navega a la carpeta del proyecto en tu terminal:
```bash
cd PROYECTO-MANTENIMIENTO
```

### 2. Crear y activar el Entorno Virtual (Recomendado)

- **En Linux / macOS:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

- **En Windows:**
  ```cmd
  python -m venv venv
  venv\Scripts\activate
  ```

### 3. Instalar las dependencias
Con el entorno virtual activado, ejecuta:
```bash
pip install -r requirements.txt
```
*(Instalará `customtkinter>=6.0.0` y sus utilidades complementarias).*

---

## 🚀 Ejecución de la Aplicación

Para iniciar la aplicación de escritorio, ejecuta:

```bash
python main.py
```
o directamente con el intérprete del entorno virtual:
```bash
venv/bin/python main.py
```

> [!NOTE]
> **Inicialización Automática en el Primer Arranque:**
> La primera vez que abras el programa, el sistema creará automáticamente la carpeta `data/` y el archivo de base de datos `data/mantenimiento.db`. Además, cargará el catálogo inicial con las **10 rutinas de mantenimiento preventivo** investigadas para transporte colectivo. No necesitas ejecutar scripts SQL manuales.

---

## 🧭 Manual de Uso del Sistema

La ventana principal cuenta con una **barra lateral izquierda (Sidebar)** que te permite cambiar entre los distintos módulos con un solo clic.

```text
[ Barra Lateral ]           [ Área de Trabajo Principal ]
- 📊 Dashboard              -> Resumen, KPIs y semáforo de urgencias
- 🚐 Flota y Unidades       -> Registro de vehículos, placas y odómetro
- 👥 Socios y Propietarios  -> Registro de afiliados y datos de contacto
- 🛠️ Control Preventivo     -> Programación de servicios y registro de hechos
- 📋 Catálogo Rutinas       -> CRUD para crear/editar rutinas preventivas
- 📜 Bitácora Histórica     -> Historial de gastos, talleres y mantenimientos
```

---

### Módulo 1: Gestión de Socios y Propietarios (`👥 Socios`)
En las empresas de transporte, las unidades pertenecen a socios o afiliados:
1. Dirígete a la sección **"👥 Socios y Propietarios"**.
2. **Registrar un nuevo socio:**
   - Llena la Cédula (ej. `V-14567890`), Nombre Completo, Teléfono y Estado.
   - Haz clic en **"➕ Guardar Socio"**.
3. **Editar o Consultar:**
   - Puedes buscar cualquier socio usando la barra de búsqueda en la parte superior derecha.
   - Haz clic sobre un socio en la tabla para cargar sus datos en el formulario y pulsa **"✏️ Actualizar"**.
4. **Seguridad:** El sistema no permitirá borrar un socio si este tiene unidades registradas a su nombre, evitando dejar vehículos huérfanos.

---

### Módulo 2: Gestión de Flota y Unidades (`🚐 Flota y Unidades`)
Permite registrar y controlar cada autobús, microbús o camioneta:
1. Haz clic en **"🚐 Flota y Unidades"**.
2. **Registrar un Vehículo:**
   - Selecciona el **Socio Propietario** en el menú desplegable.
   - Asigna el **N° de Unidad** (código de control interno, ej. `01`, `14`, `Bus 25`).
   - Ingresa la **Placa** (ej. `A12BC3D`).
   - Ingresa Marca/Modelo (ej. `Encava NT-610`, `Toyota Coaster`) y Año.
   - Ingresa el **Odómetro Inicial (Km)** (ej. `125000`).
   - Selecciona el estado (`Activo`, `En Taller`, `Inactivo`).
   - Haz clic en **"➕ Guardar Unidad"**.
3. **⚡ Actualización Rápida de Odómetro:**
   - Al finalizar una jornada o semana, no necesitas editar todo el vehículo.
   - Selecciona la unidad en la tabla y pulsa el botón amarillo **"⚡ Actualizar Solo Odómetro"**.
   - Escribe el nuevo kilometraje; el sistema validará que sea mayor al anterior y recalculará automáticamente todos los semáforos preventivos de esa unidad.

---

### Módulo 3: Catálogo de Mantenimientos (`📋 Catálogo Rutinas`)
Aquí se definen las tareas de mantenimiento preventivo y sus frecuencias:
1. Haz clic en **"📋 Catálogo Rutinas"**.
2. Verás precargadas las **10 rutinas recomendadas** para transporte público:
   - *Cambio de Aceite y Filtro de Motor* (cada 5.000 km / 60 días)
   - *Filtros de Combustible y Trampa de Agua* (cada 10.000 km / 90 días)
   - *Inspección y Filtro de Aire* (cada 7.500 km / 60 días)
   - *Engrase de Chasis y Crucetas* (cada 3.000 km / 30 días)
   - *Frenos y Bandas* (cada 10.000 km / 60 días)
   - *Rotación de Neumáticos* (cada 10.000 km / 90 días)
   - *Valvulina de Caja y Diferencial* (cada 30.000 km / 180 días)
   - *Enfriamiento y Mangueras* (cada 15.000 km / 90 días)
   - *Sistema Eléctrico y Batería* (cada 60 días)
   - *Suspensión y Ballestas* (cada 15.000 km / 120 días)
3. **Crear o Modificar Rutinas:**
   - Puedes cambiar las frecuencias en kilómetros o en días para adaptarlas a los manuales de tus autobuses.
   - Puedes crear nuevas tareas (ej. *"Cambio de kit de embrague"*, *"Limpieza de inyectores"*).

---

### Módulo 4: Control Preventivo y Semaforización (`🛠️ Control Preventivo`)
Es el panel central de control de la empresa:
1. **Programar una rutina a una unidad:**
   - Pulsa **"➕ Programar Rutina a Unidad"**.
   - Selecciona la unidad y la rutina que deseas monitorear.
   - Ingresa el kilometraje y fecha en que se le hizo por última vez (o deja el odómetro actual).
   - Haz clic en **Guardar Programación**. El sistema calculará la fecha y kilometraje exacto del próximo servicio.
2. **Lectura del Semáforo:**
   - 🟢 **Al Día:** La unidad está operando dentro del margen seguro.
   - 🟡 **Por Vencer:** Faltan menos de 500 km o menos de 10 días para el límite.
   - 🔴 **Vencido:** Se superó el kilometraje o la fecha límite; la unidad requiere atención inmediata.
3. **✅ Registrar Mantenimiento Realizado:**
   - Cuando el autobús regrese del taller con el servicio hecho, selecciona la fila en la tabla y pulsa **"✅ Registrar Mantenimiento Realizado"**.
   - Se abrirá una ventana para ingresar:
     - Fecha real del trabajo.
     - Kilometraje al momento del servicio.
     - Costo total ($).
     - Nombre del taller o mecánico.
     - Repuestos o detalles adicionales.
   - Al confirmar:
     - Se guarda en la bitácora histórica.
     - Se actualiza el odómetro de la unidad.
     - **Se recalcula automáticamente el próximo servicio preventivo**, pasando de nuevo el semáforo a 🟢 **Al Día**.

---

### Módulo 5: Dashboard y Métricas (`📊 Dashboard`)
- Muestra tarjetas resumen con el total de unidades activas, en taller, y el conteo de mantenimientos vencidos, por vencer y al día.
- Incluye la tabla de **Alertas Críticas y Próximos Vencimientos**, mostrando únicamente las unidades que requieren atención urgente.
- El botón **"Ir a Control Preventivo ➔"** te traslada directamente para gestionar el servicio.

---

### Módulo 6: Bitácora Histórica (`📜 Bitácora Histórica`)
- Permite auditar todos los trabajos realizados en la historia de la empresa.
- Muestra fecha, unidad, placa, costo, taller y los repuestos que se instalaron.
- Permite buscar por placa, unidad o taller para auditorías de gastos mecánicos.

---

### Módulo 7: Cambio de Modo Visual (Oscuro / Claro)
- En la parte inferior de la barra lateral izquierda encontrarás el selector de tema:
  - **Dark:** Ideal para trabajo nocturno o reducir fatiga visual.
  - **Light:** Modo claro para oficinas muy iluminadas o impresiones de pantalla.
  - **System:** Se adapta al tema configurado en tu sistema operativo.

---

## 💾 Copias de Seguridad (Backups)

Respaldar toda la información de Brisas del Palmar es sumamente sencillo:

1. Cierra la aplicación.
2. Copia el archivo ubicado en:
   ```text
   PROYECTO-MANTENIMIENTO/data/mantenimiento.db
   ```
3. Guárdalo en una memoria USB, disco externo o almacenamiento en la nube (Google Drive, Dropbox, OneDrive).
4. Para restaurar en caso de formateo o cambio de computadora, simplemente pega el archivo `mantenimiento.db` dentro de la carpeta `data/`.

---

## 🧪 Ejecución de Pruebas Unitarias

El proyecto incluye pruebas automatizadas para verificar la integridad de los servicios y el cálculo de alertas preventivas. Para ejecutarlas:

```bash
python -m unittest discover tests
```

Salida esperada:
```text
..
----------------------------------------------------------------------
Ran 2 tests in 0.050s

OK
```

