# 🛠️ ¿Qué herramientas y tecnologías usa este proyecto?

> **Nivel:** Principiante — explicamos cada herramienta con analogías del mundo real.

---

## 🐍 Python — El lenguaje de programación

**¿Qué es un lenguaje de programación?**
Piénsalo como el idioma que usas para hablarle a la computadora. Así como los humanos hablamos español o inglés, las computadoras "hablan" lenguajes como Python.

**¿Por qué Python?**
Python es uno de los lenguajes más populares del mundo porque:
- Es **fácil de leer** — se parece mucho al inglés normal.
- Es muy **versátil** — sirve para hacer casi cualquier cosa.
- Tiene una enorme **comunidad** de programadores que crean herramientas gratuitas.

Todo el código de este proyecto está escrito en Python. El archivo principal se llama `main.py`.

---

## 🖥️ CustomTkinter — La interfaz visual

**¿Qué es una interfaz gráfica?**
Es todo lo que ves en pantalla: ventanas, botones, formularios, tablas... Sin una interfaz gráfica, solo verías texto negro sobre fondo blanco.

**CustomTkinter** es una librería de Python (una colección de herramientas listas para usar) que permite crear interfaces modernas y atractivas. Es una versión mejorada de "Tkinter", que es la herramienta de interfaces incluida por defecto en Python.

**En este proyecto, CustomTkinter crea:**
- La ventana de inicio de sesión (login)
- La barra lateral de navegación
- Los paneles del dashboard
- Los formularios para agregar vehículos, socios, etc.
- Las tablas de datos

> 💡 **Analogía:** Si Python es como los planos de una casa, CustomTkinter es como los muebles y la decoración que hacen que la casa sea bonita y funcional.

---

## 🗄️ SQLite — La base de datos

**¿Qué es una base de datos?**
Es un lugar donde se guarda información de forma organizada, como un archivero digital muy ordenado. En lugar de guardar todo en una hoja de cálculo de Excel, una base de datos puede manejar miles de registros de forma eficiente.

**SQLite** es una base de datos especial porque:
- **No necesita instalación separada** — vive dentro del mismo programa.
- **Toda la información queda en un solo archivo** (`mantenimiento.db`) que puedes copiar fácilmente como respaldo.
- Es perfecta para aplicaciones de escritorio como esta.

> 💡 **Analogía:** SQLite es como una libreta muy organizada que vive dentro de tu mochila. No necesitas ir a ningún servidor ni Internet — todo está ahí contigo.

**¿Cómo se le "habla" a SQLite?**
Se usa un lenguaje especial llamado **SQL** (Structured Query Language). Por ejemplo, para pedir todos los vehículos activos, se escribe algo así:
```sql
SELECT * FROM vehiculo WHERE activo = 1;
```
Traducido: "Selecciona todo de la tabla vehículo donde estén activos"

---

## 📄 ReportLab — Generador de PDFs

**ReportLab** es una librería de Python que permite crear archivos PDF desde cero, con el código.

Este proyecto la usa para generar reportes oficiales como:
- Fichas técnicas de los vehículos
- Planes de mantenimiento preventivo con los semáforos de colores
- Directorios de socios

> 💡 **Analogía:** ReportLab es como una impresora muy inteligente que sabe dónde poner cada dato, tabla e imagen en el papel.

---

## 📊 OpenPyXL — Generador de archivos Excel

**OpenPyXL** es una librería de Python que permite crear y modificar archivos de **Microsoft Excel** (`.xlsx`).

Este proyecto la usa para:
- Crear la bitácora histórica de mantenimientos en Excel, con fórmulas automáticas de suma
- Generar resúmenes ejecutivos con métricas por taller

> 💡 **Analogía:** OpenPyXL es como tener un asistente que llena las hojas de cálculo de Excel automáticamente, sin que tengas que escribir nada a mano.

---

## 🖼️ Pillow — Manejo de imágenes

**Pillow** es una librería de Python para trabajar con imágenes (PNG, JPG, etc.).

En este proyecto se usa para:
- Cargar el logotipo corporativo de "Brisas del Palmar"
- Mostrarlo en la interfaz con buena calidad y transparencia

> 💡 **Analogía:** Pillow es como un marco de fotos digital que sabe mostrar las imágenes correctamente en la pantalla.

---

## 📋 Resumen de herramientas

| Herramienta | ¿Para qué sirve? | ¿Dónde se ve en el proyecto? |
|---|---|---|
| **Python** | Lenguaje principal del programa | Todos los archivos `.py` |
| **CustomTkinter** | Crear la interfaz gráfica (ventanas, botones) | `src/views/` |
| **SQLite** | Guardar todos los datos | Archivo `data/mantenimiento.db` |
| **ReportLab** | Generar reportes en PDF | `src/reports/pdf_generator.py` |
| **OpenPyXL** | Generar reportes en Excel | `src/reports/excel_generator.py` |
| **Pillow** | Mostrar imágenes y logos | `src/views/main_window.py` |

---

## 📦 ¿Cómo se instalan estas herramientas?

Todas se instalan con un solo comando, gracias al archivo `requirements.txt` que ya tiene la lista:

```bash
pip install -r requirements.txt
```

`pip` es el "gestor de paquetes" de Python — es como una tienda de aplicaciones para programadores donde puedes descargar e instalar librerías gratuitas.

---

⬅️ [Anterior: ¿Qué es el proyecto?](./01-QUE-ES-EL-PROYECTO.md) | ➡️ [Siguiente: Cómo está organizado](./03-COMO-ESTA-ORGANIZADO.md)
