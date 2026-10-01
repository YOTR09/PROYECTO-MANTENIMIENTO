# 📊 Los Reportes: ¿Cómo genera documentos el sistema?

> **Nivel:** Principiante — explicamos cómo el programa crea PDFs y archivos Excel automáticamente.

---

## 🗂️ ¿Qué es un reporte en este sistema?

Un **reporte** es un documento oficial que el sistema genera automáticamente con la información más reciente de la base de datos.

En lugar de que alguien tenga que copiar datos manualmente a un Word o Excel, el programa lo hace en segundos, con formato profesional.

---

## 📑 Los 5 reportes disponibles

### 📄 Reporte 1 — Ficha Técnica de la Flota (PDF)
**¿Para quién?** Gerentes, directivos, auditorías.

**¿Qué contiene?**
- Lista de todos los vehículos activos
- Placa, número de unidad, marca/modelo
- Año, kilometraje actual
- Estado actual (Activo, En Taller, Inactivo)
- Nombre del propietario (socio)

**Formato:** PDF con encabezado corporativo y tabla organizada.

---

### 🚦 Reporte 2 — Plan Preventivo con Semáforos (PDF)
**¿Para quién?** Jefe de taller, mecánicos, supervisores.

**¿Qué contiene?**
- Estado de todos los mantenimientos programados
- Los semáforos de color para identificar urgencias:
  - 🔴 **VENCIDO** — Necesita atención inmediata
  - 🟡 **POR VENCER** — Planificar pronto
  - 🟢 **AL DÍA** — En buen estado
- Fecha del último servicio y del próximo
- Kilómetros del último y próximo servicio

**Formato:** PDF con filas coloreadas según el estado de alerta.

---

### 📋 Reporte 3 — Bitácora Histórica y Costos (Excel)
**¿Para quién?** Contabilidad, administración, auditorías económicas.

**¿Qué contiene?**
- Todo el historial de mantenimientos realizados
- Fecha, vehículo, tipo de mantenimiento
- Taller donde se realizó
- **Costo de cada servicio**
- Fórmulas automáticas de suma (`=SUM(...)`) para calcular totales

**Formato:** Archivo `.xlsx` de Microsoft Excel, listo para abrir y analizar.

> 💡 Las fórmulas de suma son automáticas — si alguien edita un costo en Excel, los totales se actualizan solos.

---

### 👥 Reporte 4 — Directorio de Socios (PDF)
**¿Para quién?** Administración, secretaría, auditorías.

**¿Qué contiene?**
- Lista completa de todos los socios/propietarios
- Cédula, nombre completo, teléfono
- Vehículos que tiene asignados

**Formato:** PDF estilo directorio institucional.

---

### 📈 Reporte 5 — Resumen Ejecutivo por Taller (Excel)
**¿Para quién?** Gerencia, dirección general.

**¿Qué contiene?**
- Métricas de rendimiento agrupadas por taller mecánico
- Cuántos servicios realizó cada taller
- Costo total por taller
- Costo promedio por servicio

**Formato:** Archivo `.xlsx` con resumen ejecutivo y estadísticas.

---

## ⚙️ ¿Cómo se genera un reporte técnicamente?

```
1. El usuario hace clic en "Generar Reporte X"
         │
         ▼
2. ReportesView le avisa al ReporteController
         │
         ▼
3. ReporteController le pide los datos a los servicios (mantenimiento, vehículos, etc.)
         │
         ▼
4. Los servicios consultan los repositorios, que consultan la base de datos
         │
         ▼
5. Los datos regresan a ReporteController, que los pasa al generador
         │
         ├── Para PDFs → pdf_generator.py usa ReportLab para crear el archivo
         │
         └── Para Excel → excel_generator.py usa OpenPyXL para crear el archivo
                   │
                   ▼
6. El archivo se guarda en la computadora del usuario
         │
         ▼
7. Aparece un mensaje: "¡Reporte generado exitosamente en [ruta]!"
```

---

## 🖨️ ¿Dónde se guardan los reportes?

Los reportes se guardan en la computadora del usuario. Generalmente en la carpeta que el usuario elija mediante un diálogo de "Guardar como..." o en una ruta predeterminada del proyecto.

---

## 🎨 El aspecto visual de los reportes PDF

Los reportes en PDF incluyen:
- **Encabezado** con el logo de la empresa
- **Título** del reporte con fecha de generación
- **Tablas** con bordes y colores
- Para el reporte de semáforos: filas en **rojo**, **amarillo** o **verde** según el estado de alerta

Esto lo hace la librería **ReportLab**, que permite dibujar texto, tablas e imágenes en el PDF con precisión milimétrica.

---

## 📊 El aspecto visual de los reportes Excel

Los reportes en Excel incluyen:
- **Celdas con formato** (negrita, colores de fondo)
- **Columnas** con anchos apropiados para cada dato
- **Fórmulas automáticas** que calculan totales
- **Encabezados** con estilo para las columnas

Esto lo hace la librería **OpenPyXL**, que puede crear y editar archivos `.xlsx` sin necesidad de tener Excel instalado.

---

⬅️ [Anterior: Seguridad y usuarios](./06-SEGURIDAD-Y-USUARIOS.md) | ➡️ [Siguiente: Glosario](./08-GLOSARIO.md)
