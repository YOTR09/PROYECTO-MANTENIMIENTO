# 🚌 ¿Qué es este proyecto y para qué sirve?

> **Nivel:** Principiante total — no necesitas saber nada de programación para leer esto.

---

## 🏢 El contexto: Una empresa de transporte

Imagina que trabajas en una empresa de autobuses llamada **"Brisas del Palmar"**. Esa empresa tiene muchos autobuses (los llaman "unidades") circulando por la ciudad todos los días.

Cada autobús necesita **mantenimiento regular**, como un carro que llevas al mecánico cada ciertos kilómetros:
- Cambio de aceite
- Cambio de filtros
- Revisión de frenos
- Cambio de neumáticos
- Y muchas cosas más...

Si no haces esos mantenimientos a tiempo, los autobuses se dañan, dejan de funcionar, y la empresa pierde dinero — ¡o peor, puede haber accidentes!

---

## 💻 ¿Qué hace este programa?

Este programa es como un **asistente digital** que le ayuda a la empresa a:

### 1. 🚐 Controlar su flota de vehículos
Sabe qué autobuses tiene la empresa, cuántos kilómetros llevan recorridos, quién es el dueño de cada uno, y en qué estado se encuentran.

### 2. 📅 Programar los mantenimientos
El sistema sabe automáticamente cuándo le toca el mantenimiento a cada autobús, basándose en:
- **Los kilómetros recorridos** — por ejemplo, "cambio de aceite cada 5,000 km"
- **El tiempo transcurrido** — por ejemplo, "revisión de frenos cada 6 meses"

### 3. 🚦 Alertar cuando algo urge
Usando un **sistema de semáforos de colores**, el programa avisa:
- 🔴 **Rojo:** ¡El mantenimiento está VENCIDO! El autobús necesita entrar al taller YA.
- 🟡 **Amarillo:** El mantenimiento está próximo a vencer. Hay que planificarlo pronto.
- 🟢 **Verde:** Todo está bien, el autobús puede operar normalmente.

### 4. 📜 Guardar el historial
Cada vez que se hace un mantenimiento, el sistema guarda:
- Qué se hizo
- Cuándo se hizo
- Cuánto costó
- En qué taller se realizó

Esto crea un **historial completo** de cada autobús, muy útil para auditorías y seguros.

### 5. 📊 Generar reportes
El programa puede crear documentos en **PDF** y **Excel** con toda la información organizada, para que los jefes puedan verla fácilmente.

### 6. 👥 Gestionar personas
- **Socios/Propietarios:** Las personas dueñas de los autobuses.
- **Usuarios del sistema:** Las personas que pueden usar el programa (mecánicos, administradores, auditores).

---

## 👤 ¿Quiénes usan este programa?

El sistema tiene **3 tipos de usuarios**, cada uno con diferentes permisos:

| Tipo de Usuario | ¿Qué puede hacer? | Usuario de prueba |
|---|---|---|
| 🔑 **Administrador** | Todo: gestionar usuarios, vehículos, socios, mantenimientos | `admin` |
| 🔧 **Mecánico** | Registrar y programar mantenimientos, ver la flota | `mecanico` |
| 👁️ **Operador/Auditor** | Solo consultar información y generar reportes | `auditor` |

---

## 🎯 En resumen

> Este programa es un **sistema de escritorio** (se instala en la computadora, como Microsoft Word) que ayuda a la empresa de transporte "Brisas del Palmar" a **nunca olvidarse de darle mantenimiento a sus autobuses**.

---

⬅️ [Volver al índice](./00-INDICE.md) | ➡️ [Siguiente: Las herramientas usadas](./02-HERRAMIENTAS-Y-TECNOLOGIAS.md)
