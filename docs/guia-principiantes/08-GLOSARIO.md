# 📖 Glosario: Diccionario de Términos Técnicos

> Aquí encontrarás todos los términos técnicos del proyecto explicados en lenguaje sencillo, ordenados alfabéticamente.

---

## A

### Algoritmo
Una serie de pasos ordenados para resolver un problema. Como una receta de cocina: paso 1, paso 2, paso 3... la computadora sigue los pasos y llega a un resultado.

### Aplicación de escritorio
Un programa que se instala directamente en tu computadora (como Microsoft Word o VLC). Se diferencia de una aplicación web (como Gmail), que funciona en el navegador. Este proyecto es una **aplicación de escritorio**.

### Arquitectura
La forma en que está organizado y estructurado un programa. Como los planos de un edificio que definen dónde va cada habitación y para qué sirve.

---

## B

### Base de datos (BD)
Un sistema organizado para guardar y recuperar información. Piénsalo como un archivero digital muy eficiente que puede encontrar cualquier dato en fracciones de segundo.

### Backup (Respaldo)
Una copia de seguridad de los datos. En este proyecto, hacer un backup significa copiar el archivo `data/mantenimiento.db` a otro lugar.

---

## C

### Campo
Una columna en una tabla de base de datos. Es como la "categoría" de información. Por ejemplo, en la tabla de vehículos, `placa` es un campo.

### Cifrado / Hashing
El proceso de convertir información legible en un código incomprensible para protegerla. La diferencia entre cifrado y hashing es que el cifrado se puede revertir, pero el **hashing NO** — es de una sola vía.

### Clase (en programación)
Un molde o plantilla para crear objetos. Por ejemplo, la clase `Vehiculo` define qué propiedades tiene todo vehículo: placa, marca, modelo, kilometraje...

### Controlador (Controller)
En el patrón MVC, el controlador es el "coordinador" que recibe pedidos de la vista y los dirige al servicio correcto. Es como el mesero de un restaurante.

### CRUD
Acrónimo de las 4 operaciones básicas con datos:
- **C**reate (Crear) — Agregar nuevos registros
- **R**ead (Leer) — Consultar registros existentes
- **U**pdate (Actualizar) — Modificar registros
- **D**elete (Eliminar) — Borrar registros

---

## D

### Dashboard
Pantalla principal que muestra un resumen con los datos más importantes del sistema, como los indicadores de alerta del mantenimiento y estadísticas de la flota.

### Dependencias / Librerías
Son "paquetes" de código hechos por otras personas que podemos usar en nuestro proyecto sin tener que escribirlo desde cero. Las dependencias de este proyecto están en `requirements.txt`.

---

## E

### Entorno Virtual (venv)
Una copia aislada de Python que solo tiene las librerías de este proyecto. Evita conflictos con otros proyectos en la misma computadora. La carpeta `venv/` es el entorno virtual.

### Excel (`.xlsx`)
Formato de archivo de hojas de cálculo de Microsoft Office. El sistema puede generar reportes en este formato usando la librería OpenPyXL.

---

## F

### Flota
El conjunto de vehículos que posee y opera una empresa.

### Foreign Key (Llave Foránea)
Un campo en una tabla que hace referencia a un registro en otra tabla. Por ejemplo, `id_socio` en la tabla `vehiculo` es una llave foránea que conecta cada vehículo con su propietario.

---

## G

### Git
Sistema de control de versiones. Permite guardar el historial de todos los cambios hechos al código. La carpeta `.git/` en el proyecto guarda este historial.

---

## H

### Hash / Hashing
Ver **Cifrado / Hashing**. Específicamente, un hash es el resultado de pasar un texto por un algoritmo de hashing. Es como una huella digital del texto original.

---

## I

### Índice (de base de datos)
Una estructura interna de la base de datos que acelera las búsquedas. Como el índice al final de un libro — en lugar de buscar página por página, saltas directamente al dato que necesitas.

### Interfaz Gráfica (GUI)
Graphical User Interface — todo lo que ves en pantalla: ventanas, botones, formularios, tablas. Sin interfaz gráfica, el programa solo mostraría texto.

---

## K

### KPI
Key Performance Indicator — Indicador Clave de Rendimiento. Son los números más importantes que muestran cómo va el negocio. En el dashboard del sistema, los KPIs son: unidades activas, mantenimientos vencidos, por vencer, y al día.

---

## L

### Librería / Library
Ver **Dependencias**. Un conjunto de código pre-escrito que podemos usar gratuitamente.

### Login
El proceso de iniciar sesión en un sistema introduciendo usuario y contraseña.

### Logout
El proceso de cerrar sesión y salir del sistema.

---

## M

### Mantenimiento Preventivo
Mantenimiento que se hace ANTES de que algo se rompa, de forma planificada y en intervalos regulares. Se diferencia del mantenimiento correctivo, que es cuando algo ya se dañó.

### Modelo (Model)
En el patrón MVC, el modelo es la "definición" de cómo son los datos. Define qué campos tiene un vehículo, un socio, un usuario...

### MVC (Modelo-Vista-Controlador)
Patrón de diseño que divide el código en 3 partes:
- **Modelo:** Definición de los datos
- **Vista:** Lo que el usuario ve
- **Controlador:** El coordinador entre la vista y los datos

---

## O

### Odómetro
El instrumento que mide los kilómetros recorridos por un vehículo. En el sistema se llama `kilometraje_actual`.

### OOP (Programación Orientada a Objetos)
Un estilo de programación que organiza el código en "objetos" que tienen propiedades y comportamientos. Los modelos de este proyecto usan OOP.

---

## P

### Patrón de diseño
Una solución probada y reutilizable para problemas comunes en programación. El MVC es un patrón de diseño muy popular para aplicaciones con interfaz gráfica.

### PBKDF2-HMAC-SHA256
El algoritmo matemático que usa este proyecto para cifrar contraseñas. Son siglas técnicas que significan "Password-Based Key Derivation Function 2" usando HMAC con SHA-256. En términos simples: un proceso muy seguro que convierte tu contraseña en un código incomprensible.

### PDF (Portable Document Format)
Formato de archivo que preserva el diseño y formato del documento sin importar qué computadora lo abra. El sistema genera reportes en PDF usando ReportLab.

### pip
El "gestor de paquetes" de Python. Permite instalar librerías con un simple comando, como `pip install reportlab`.

### Primary Key (Llave Primaria)
Un campo único que identifica de forma inequívoca a cada registro en una tabla. Por ejemplo, `id_vehiculo` es la llave primaria de la tabla de vehículos — nunca hay dos vehículos con el mismo ID.

### Python
Lenguaje de programación de alto nivel, popular por su sintaxis clara y su amplio ecosistema de librerías. Todo este proyecto está escrito en Python.

---

## R

### Repositorio
En el patrón de este proyecto, es la capa de código que sabe cómo guardar y recuperar datos de la base de datos. Encapsula todas las consultas SQL.

### Rol
Un conjunto de permisos asignado a un usuario que define qué puede hacer en el sistema. Este proyecto tiene 3 roles: Administrador, Mecánico, Operador.

---

## S

### Salt (Sal criptográfica)
Un valor aleatorio único que se agrega a la contraseña antes de cifrarla, para que dos contraseñas iguales produzcan hashes diferentes. Protege contra ataques de diccionario.

### Semáforo (en sistemas)
Un indicador visual de color (rojo/amarillo/verde) que comunica el estado de algo de forma intuitiva. Este proyecto usa semáforos para indicar el estado de los mantenimientos.

### Servicio (Service)
En la arquitectura de este proyecto, los servicios contienen las "reglas del negocio" — la lógica de cómo funciona el sistema. Por ejemplo, el servicio de mantenimiento sabe cómo calcular si un servicio está vencido.

### Soft Delete (Eliminación Lógica)
Técnica donde los registros no se borran físicamente de la base de datos, sino que se marcan como "inactivos" (`activo = 0`). Preserva el historial pero los oculta de las listas normales.

### SQL (Structured Query Language)
El lenguaje estándar para comunicarse con bases de datos relacionales. Con SQL puedes pedir datos (`SELECT`), insertar datos (`INSERT`), actualizarlos (`UPDATE`) o eliminarlos (`DELETE`).

### SQLite
Un motor de base de datos ligero que guarda toda la información en un solo archivo en tu computadora. No necesita instalación de servidor.

---

## T

### Tabla
Una estructura de datos en una base de datos, organizada en filas y columnas, como una hoja de cálculo. Cada fila es un registro, cada columna es un campo.

### Terminal / Consola
Ventana de texto donde puedes escribir comandos directamente para la computadora. Para iniciar el proyecto se usa la terminal.

---

## U

### Username (Nombre de usuario)
El identificador único con el que un usuario se identifica en el sistema. Ejemplos: `admin`, `mecanico`, `auditor`.

---

## V

### Vista (View)
En el patrón MVC, la vista es la parte del código que muestra la información al usuario. Crea las ventanas, botones, formularios y tablas. En este proyecto, los archivos en `src/views/` son las vistas.

### venv
Abreviatura de "virtual environment" (entorno virtual). Ver **Entorno Virtual**.

---

## 📝 Acrónimos rápidos

| Acrónimo | Significado |
|---|---|
| BD | Base de Datos |
| GUI | Graphical User Interface (Interfaz Gráfica de Usuario) |
| KPI | Key Performance Indicator |
| MVC | Modelo-Vista-Controlador |
| OOP | Object-Oriented Programming (Programación Orientada a Objetos) |
| PDF | Portable Document Format |
| SQL | Structured Query Language |
| CRUD | Create, Read, Update, Delete |

---

⬅️ [Anterior: Los reportes](./07-LOS-REPORTES.md) | ⬆️ [Volver al índice](./00-INDICE.md)
