# Sistema de Control de Mantenimiento Preventivo - Brisas del Palmar

Aplicación de escritorio moderna desarrollada en Python y CustomTkinter para la gestión de flota y control de mantenimientos preventivos de la empresa de transporte público **Brisas del Palmar**.

---

## 🚀 Características Principales

1. **Panel de Control (Dashboard):**
   - Indicadores en tiempo real: Unidades activas, en taller, mantenimientos al día, próximos a vencer y vencidos.
   - Tabla de atención inmediata con semaforización de alertas.
2. **Gestión de Flota y Unidades:**
   - Registro de vehículos con **Número de Unidad** (ej. *Unidad 01*, *Bus 14*), placa, marca/modelo, año y odómetro actual.
   - Botón de **"Actualización Rápida de Odómetro"** para registrar los kilómetros acumulados tras cada jornada sin editar toda la ficha.
3. **Gestión de Socios y Propietarios:**
   - Control de afiliados/dueños de las unidades con validación de documentos y protección contra borrado accidental de socios con vehículos asignados.
4. **Control y Semaforización Preventiva:**
   - Programación de servicios por **kilometraje** y/o **tiempo (días)**.
   - **Semáforo Dinámico:**
     - 🟢 **Al Día:** Operación segura.
     - 🟡 **Por Vencer:** Faltan menos de 500 km o menos de 10 días.
     - 🔴 **Vencido:** Kilometraje superado o fecha vencida sin registro.
   - Registro de mantenimientos ejecutados con actualización automática del odómetro y cálculo del próximo servicio.
5. **Catálogo de Mantenimientos (CRUD):**
   - Pre-cargado con las 10 rutinas estándar de la industria del transporte público (aceite, filtros, frenos, engrase, rodamientos, suspensión, etc.).
   - Capacidad de crear, editar o ajustar frecuencias de cualquier rutina.
6. **Bitácora Histórica:**
   - Registro detallado de costos, talleres, mecánicos y repuestos utilizados.

---

## 🛠️ Arquitectura del Sistema

El proyecto implementa una arquitectura en 3 capas desacopladas:

```text
PROYECTO-MANTENIMIENTO/
├── config/
│   └── database.py             # Conexión SQLite, esquema automático y transacciones
├── database/
│   ├── schema.sql              # Definición DDL de tablas e índices
│   └── seeds.sql               # Catálogo de 10 rutinas de mantenimiento preventivo
├── src/
│   ├── repositories/           # Capa de Acceso a Datos (Consultas SQL seguras)
│   ├── services/               # Lógica de Negocio, Validaciones y Semaforización
│   └── views/                  # Interfaz Gráfica Moderna (CustomTkinter)
├── tests/
│   └── test_services.py        # Suite de pruebas unitarias automáticas
├── data/
│   └── mantenimiento.db        # Base de datos local portable SQLite
├── main.py                     # Punto de entrada de la aplicación
└── requirements.txt            # Dependencias
```

---

## 💻 Instrucciones de Instalación y Uso

### 1. Activar el entorno virtual e instalar dependencias
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Iniciar la Aplicación
```bash
python main.py
```
*(Al iniciar por primera vez, el sistema creará automáticamente la base de datos `data/mantenimiento.db` y cargará el catálogo de mantenimientos iniciales).*

### 3. Ejecutar las Pruebas Unitarias
```bash
python -m unittest discover tests
```