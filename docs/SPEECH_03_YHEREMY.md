# Guion de Exposición — Integrante 3: Yheremy Oliver Tinoco Ramirez
**Rol:** Arquitectura de Software, Diagramas UML, Algoritmo de Semaforización Dual, Demostración Funcional y Conclusiones  
**Tiempo estimado:** 7 a 9 minutos  
**Secciones cubiertas:** Capítulo IV (Arquitectura MVC, UML, Algoritmo, Flujos Transaccionales), Capítulo V (Conclusiones y Recomendaciones)

---

## 1. Conexión y Casos de Uso del Sistema (0:00 - 1:15)
> *"Muchas gracias, Jose Gregorio. Continuando con el núcleo de ingeniería del software en el **Capítulo IV**, el sistema fue concebido bajo el principio de menor privilegio y separación de funciones mediante un esquema jerárquico de control de acceso por roles, como se aprecia en el **Diagrama de Casos de Uso** (Figura 1):*
> - *El **Operador/Auditor** es el rol base: puede consultar el panel principal de KPIs, visualizar el inventario de la flota, consultar historiales, cambiar el tema visual de la interfaz y exportar reportes.*
> - *El **Mecánico** hereda los permisos del Operador e incorpora la operativa técnica: actualizar el odómetro diario, programar mantenimientos y registrar los servicios ejecutados.*
> - *El **Administrador** posee control absoluto: gestión completa de usuarios, restablecimiento de contraseñas, administración del catálogo de rutinas y altas/bajas lógicas de socios y busetas.*
> 
> *En materia de seguridad criptográfica, las contraseñas nunca se guardan en texto plano; se implementó el algoritmo `PBKDF2-HMAC-SHA256` con un salt aleatorio de 16 bytes y clave maestra de emergencia."*

---

## 2. Arquitectura de Software y Diagramas de Clases (1:15 - 2:45)
> *"La solución adopta una **Arquitectura en Tres Capas desacoplada** combinada con el patrón **Modelo-Vista-Controlador (MVC)** (Figuras 2 y 3):*
> - *Capa 1 — Presentación: Vistas desarrolladas en `CustomTkinter` que ofrecen una interfaz contemporánea, reactiva y con conmutación en tiempo real de modo claro y oscuro.*
> - *Capa 2 — Controladores y Servicios: Centralizados en `BaseController`, encapsulan las reglas de negocio, validaciones y la comunicación con servicios especializados como `SeguridadService`, `PDFReportGenerator` (con ReportLab) y `ExcelReportGenerator` (con openpyxl).*
> - *Capa 3 — Acceso a Datos: Patrón Repositorio en SQLite con sentencias parametrizadas para neutralizar cualquier riesgo de inyección SQL.*
> 
> *Como se observa en los diagramas de clases UML (Figuras 4 a 7), existe un modelo de dominio transversal donde todas las entidades heredan de `BaseModel`, asegurando métodos estándar de serialización `from_dict` y `to_dict` que desacoplan la lógica de persistencia de la interfaz gráfica."*

---

## 3. Algoritmo de Semaforización Dual (2:45 - 4:15)
> *"El corazón lógico del software es el **Algoritmo de Semaforización Dual** (Figura 9). Un error común en talleres empíricos es controlar el mantenimiento únicamente por kilometraje o únicamente por tiempo. En una buseta urbana ambos factores desgastan el activo de manera independiente:*
> 
> *El motor evalúa en cada consulta dos diferenciales matemáticas:*
> 1. *Diferencial de Odómetro:* $\Delta_{km} = km_{proximo\_servicio} - kilometraje_{actual}$
> 2. *Diferencial de Calendario:* $\Delta_{dias} = fecha_{proximo\_servicio} - fecha_{actual}$
> 
> *Bajo estos cálculos, la máquina de estados clasifica cada servicio en tres condiciones operativas:*
> - **Rojo (Vencido):** *Si $\Delta_{km} \le 0$ Ó $\Delta_{dias} \le 0$. Demanda atención inmediata y retiro prioritario a taller.*
> - **Amarillo (Por Vencer):** *Si $0 < \Delta_{km} \le 500$ Ó $0 < \Delta_{dias} \le 10$. Actúa como alerta temprana de compra de repuestos y apartado de cita.*
> - **Verde (Al Día):** *Si $\Delta_{km} > 500$ Y $\Delta_{dias} > 10$. Unidad en condición óptima de operatividad.*
> 
> *El sistema incluye de forma predeterminada el catálogo de las 10 rutinas mecánicas esenciales para busetas Encava: cambios de aceite cada 5.000 km o 60 días, filtros de combustible a los 10.000 km, engrase de chasis y crucetas a los 3.000 km, frenos, valvulinas y suspensión."*

---

## 4. Demostración del Flujo Transaccional y Navegación (4:15 - 6:00)
> *(Dirigiendo la atención a la pantalla o a los diagramas de secuencia):*
> 
> *"En la navegación interactiva (Figura 10), el usuario inicia sesión mediante `LoginView` y accede al `DashboardView`, donde observa de un vistazo los indicadores globales de la flota: cantidad de busetas activas, unidades en taller y el semáforo preventivo consolidado.*
> 
> *El flujo crítico más relevante es el **Registro Transaccional de Mantenimiento Realizado** (Figura 11). Cuando el mecánico registra un servicio en `ProgramacionMantView`:*
> 1. *El controlador inicia una transacción atómica `BEGIN IMMEDIATE`.*
> 2. *Valida que los datos sean coherentes (kilometraje y costos positivos).*
> 3. *Inserta el registro histórico inmutable en `HISTORIAL_MANTENIMIENTO`.*
> 4. *Actualiza automáticamente el odómetro del vehículo si el valor ingresado es superior.*
> 5. *Ejecuta un `upsert` recalculando la próxima fecha y kilometraje según el catálogo.*
> 6. *Aplica el `COMMIT`. Si ocurre cualquier anomalía, el sistema ejecuta un `ROLLBACK` automático, garantizando cero inconsistencia en la base de datos.*
> 
> *Asimismo, el módulo de reportería permite exportar en segundos el padrón de socios, la programación preventiva en PDF y el balance de costos por taller en libros analíticos de Excel."*

---

## 5. Conclusiones y Recomendaciones (6:00 - 7:30)
> *"Para finalizar, en el **Capítulo V** exponemos las conclusiones correspondientes a cada objetivo específico:*
> 1. *Se diagnosticó la necesidad crítica de abandonar el registro verbal, validando la urgencia de una plataforma centralizada para las 20 busetas.*
> 2. *El diseño relacional de 7 tablas en SQLite garantizó una estructura íntegra, segura y ligera para trabajar de forma local.*
> 3. *El software desarrollado con Python y CustomTkinter demostró alta reactividad, estética moderna y una semaforización dual exacta.*
> 4. *Las pruebas de usabilidad e integración ratificaron que el tiempo de actualización de odómetros se reduce a segundos, logrando un control operativo total.*
> 
> *Recomendamos formalmente a la Junta Directiva institucionalizar el software como herramienta obligatoria, supervisar la toma de kilometraje diario al cierre de rutas y respaldar semanalmente el archivo `data/mantenimiento.db`.*
> 
> *Agradecemos a nuestro asesor, a nuestro tutor y al jurado por su tiempo y orientación. Quedamos a su entera disposición para la ronda de preguntas. Muchas gracias."*