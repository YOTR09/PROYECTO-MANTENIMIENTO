# Guion de Exposición — Integrante 2: Jose Gregorio Moncada Primo
**Rol:** Marco Conceptual, Metodología, Procedimiento Técnico, Modelo Entidad-Relación y Factibilidad  
**Tiempo estimado:** 5 a 6 minutos  
**Secciones cubiertas:** Capítulo II (2.1 al 2.4), Capítulo III (3.1 al 3.7), Capítulo IV (Diseño E-R y Factibilidad)

---

## 1. Conexión y Marco Conceptual (0:00 - 1:15)
> *"Muchas gracias, compañero Edixon. Continuando con la fundamentación del proyecto, en el **Capítulo II** revisamos antecedentes clave ordenados cronológicamente:*
> - *Anguisaca y Peñafiel (2021) en Ecuador, quienes demostraron que el control sistemático de mantenimiento por kilometraje reduce significativamente los tiempos de parada en busetas.*
> - *Rodríguez (2022), quien implementó una solución relacional para la trazabilidad de talleres automotrices.*
> - *Y a nivel nacional, Espinoza (2023) en la Universidad José Antonio Páez, cuyo sistema de mantenimiento aumentó en un 35% la disponibilidad operativa de flotas de carga pesada.*
> 
> *En el Cuadro de Unidad de Análisis se estructuraron las cuatro categorías rectoras: Gestión de Mantenimiento Vehicular, Bases de Datos Relacionales, Ingeniería de Software con Tecnologías Libres y Calidad de Software, respaldadas legalmente bajo el Artículo 110 de la Constitución, la Ley de Infogobierno y la Ley de Transporte Terrestre."*

---

## 2. Marco Metodológico y Procedimiento Técnico (1:15 - 2:30)
> *"En el **Capítulo III**, la investigación adoptó un enfoque estrictamente cuantitativo, fundamentado en el levantamiento métrico continuo de odómetros, intervalos de mantenimiento y costos de taller.*
> 
> *El tipo de estudio corresponde a una investigación aplicada bajo la modalidad de **Proyecto Factible** con diseño de campo. Se aplicó un muestreo censal donde la población y la muestra fueron idénticas: las veinte (20) busetas que componen el parque vehicular de la línea.*
> 
> *Para la recolección de datos empleamos fichas de arqueo numérico, matrices de costos y un cuestionario estructurado aplicado a los propietarios, el cual fue validado por Juicio de Expertos con tres docentes especialistas de la UPTAIET en áreas de Sistemas, Computación y Metodología, obteniendo además alta confiabilidad mediante el coeficiente Alfa de Cronbach.*
> 
> *En el procedimiento técnico, se siguió un ciclo de vida iterativo e incremental por módulos, aplicando Programación Orientada a Objetos para encapsular el dominio, Programación Dirigida por Eventos en la interfaz y arquitectura en tres capas."*

---

## 3. Plan de Acción y Modelo Entidad-Relación (2:30 - 4:00)
> *"El desarrollo del proyecto se ejecutó a lo largo de 16 semanas académicas estructuradas en el Plan de Acción, cubriendo preparación, configuración del entorno, carga inicial de datos, pruebas funcionales y socialización final.*
> 
> *Entrando en el **Capítulo IV**, en lo relativo al diseño de la base de datos relacional, implementamos un esquema normalizado en SQLite compuesto por **siete (7) entidades** interrelacionadas:*
> 1. *`ROL`: Catálogo de perfiles (Administrador, Mecánico y Operador).*
> 2. *`USUARIO`: Credenciales seguras, salt aleatorio y pregunta de seguridad.*
> 3. *`SOCIO`: Padrón de propietarios afiliados.*
> 4. *`VEHICULO`: Registro técnico de unidades, placas, modelos y odómetro.*
> 5. *`TIPO_MANTENIMIENTO`: Catálogo maestro de rutinas preventivas.*
> 6. *`MANTENIMIENTO_PROGRAMADO`: Registro de alertas preventivas activas.*
> 7. *`HISTORIAL_MANTENIMIENTO`: Bitácora inmutable de servicios ejecutados y costos en divisas.*
> 
> *Para garantizar la robustez del almacenamiento local, activamos la directiva `PRAGMA foreign_keys = ON`, establecimos reglas referenciales `RESTRICT` para evitar eliminar socios o vehículos con historial asociado, e implementamos el atributo booleano `activo` para borrado lógico, garantizando cero pérdida accidental de datos."*

---

## 4. Evaluación de Factibilidad Integral (4:00 - 5:15)
> *"Asimismo, se demostró la viabilidad del proyecto evaluando sus cinco dimensiones de factibilidad:*
> - *Factibilidad Técnica: Plenamente viable al ejecutarse en equipos estándar de oficina con Python 3.12 y SQLite en un solo archivo local, sin requerir servidores externos ni conexión permanente a internet.*
> - *Factibilidad Económica: Costo cero en licencias de software propietario, generando un ahorro directo al prevenir roturas de motor y caja de cambios.*
> - *Factibilidad Social: Garantiza la estabilidad de ingresos de las 20 familias de los socios y la continuidad del servicio para más de 4.300 usuarios diarios.*
> - *Factibilidad Ambiental: El reemplazo puntual de lubricantes y filtros reduce emisiones tóxicas y evita derrames de fluidos en las vías.*
> - *Factibilidad Cultural: Impulsa la transición del registro manual en papel hacia una cultura digital organizada.*
> 
> *Para presentar la arquitectura de software, la lógica matemática del semáforo dual, los diagramas de ingeniería y la demostración funcional del sistema, cedo el control de la exposición a mi compañero Yheremy Tinoco."*