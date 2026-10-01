# 🔒 Seguridad y Usuarios: ¿Cómo protege el sistema la información?

> **Nivel:** Principiante — explicamos la seguridad informática sin jerga técnica.

---

## 🔑 El Sistema de Login (Inicio de Sesión)

Cuando abres el programa, lo primero que aparece es la **pantalla de login**. Esto es una medida de seguridad para que solo las personas autorizadas puedan usar el sistema.

Para entrar, necesitas:
- Un **nombre de usuario** (username)
- Una **contraseña** (password)

---

## 👥 Los 3 tipos de usuarios (Roles)

No todos los usuarios tienen los mismos permisos. El sistema tiene **3 roles** distintos:

### 🔑 Administrador
- **Tiene acceso a absolutamente todo.**
- Puede crear, modificar y desactivar usuarios.
- Puede gestionar vehículos, socios, mantenimientos.
- Puede generar todos los reportes.

Credenciales de prueba: `admin` / `admin123`

---

### 🔧 Mecánico
- **Acceso al taller.**
- Puede programar y registrar mantenimientos.
- Puede ver y actualizar la flota de vehículos.
- Puede ver socios y el historial de servicios.
- **No puede** gestionar usuarios del sistema.

Credenciales de prueba: `mecanico` / `mecanico123`

---

### 👁️ Operador / Auditor
- **Acceso de solo lectura.**
- Solo puede consultar información (ver, no modificar).
- Puede generar reportes para presentar a los directivos.
- **No puede** hacer cambios en los datos.

Credenciales de prueba: `auditor` / `auditor123`

---

## 🔐 ¿Cómo se guardan las contraseñas? (Sin guardarlas en texto plano)

Esta es una de las partes más importantes de la seguridad del sistema. Las contraseñas **nunca se guardan tal como las escribes**.

### El problema de guardar contraseñas en texto simple

Si guardáramos `admin123` directamente en la base de datos y alguien accediera al archivo, vería todas las contraseñas inmediatamente.

### La solución: Hashing con PBKDF2

El sistema usa un proceso llamado **hashing** para convertir la contraseña en un código incomprensible. Es un proceso de una sola vía — no se puede deshacer.

**¿Cómo funciona paso a paso?**

```
1. El usuario escribe su contraseña: "admin123"
         │
         ▼
2. El sistema genera un "salt" (una cadena aleatoria única):
   "a3f9b2c1d4e5..."   ← esto es diferente para cada usuario
         │
         ▼
3. Se combina la contraseña con el salt y se aplica el algoritmo PBKDF2-HMAC-SHA256
   durante 100,000 repeticiones:
   "admin123" + "a3f9b2c1..." → "7f4a9b3c2d1e0f8a7b6c5d4e3f2a1b0c..."
         │
         ▼
4. Solo ESE código cifrado se guarda en la base de datos, nunca "admin123"
```

**Cuando el usuario quiere entrar:**
```
1. Escribe "admin123"
2. El sistema lo combina con el salt guardado y aplica el mismo algoritmo
3. Compara el resultado con lo que está guardado
4. Si coinciden → acceso concedido ✅
5. Si no coinciden → acceso denegado ❌
```

> 💡 **Analogía:** Es como una huella dactilar. Puedes verificar si dos huellas coinciden sin necesidad de saber cómo se llama la persona.

---

## 🧂 ¿Qué es el "Salt" (Sal Criptográfica)?

El salt es una cadena aleatoria que se genera para cada usuario. Su función es evitar los "ataques de diccionario", donde los atacantes prueban contraseñas comunes pre-calculadas.

Incluso si dos usuarios tienen la misma contraseña (`1234`), sus hashes guardados serán completamente diferentes porque cada uno tiene un salt único.

---

## ❓ Recuperación de Contraseña

Si un usuario olvida su contraseña, puede recuperarla respondiendo su **pregunta de seguridad**.

Pregunta predeterminada: *¿Nombre de la empresa de transporte colectivo?*  
Respuesta: *Brisas del Palmar*

El sistema compara la respuesta de forma **flexible** — ignora mayúsculas, minúsculas y acentos. Entonces "brisas del palmar", "BRISAS DEL PALMAR" y "Brísas del Pálmar" se consideran equivalentes.

---

## 🚪 Cierre de Sesión (Logout)

Cuando terminas de usar el programa, puedes cerrar sesión con el botón **"🚪 Cerrar Sesión"** en la barra lateral. Esto borra completamente la sesión activa y vuelve a la pantalla de login.

---

## 🛡️ Resumen de medidas de seguridad

| Medida | ¿Qué protege? |
|---|---|
| Sistema de login | Que personas no autorizadas entren al programa |
| Roles y permisos | Que cada usuario solo pueda hacer lo que le corresponde |
| Contraseñas cifradas con PBKDF2 | Que las contraseñas no puedan leerse aunque alguien vea la BD |
| Salt único por usuario | Que la misma contraseña produzca hashes diferentes |
| 100,000 iteraciones | Que sea muy lento y costoso intentar adivinar contraseñas por fuerza bruta |
| Verificación de tiempo constante | Que no sea posible adivinar contraseñas analizando el tiempo de respuesta |

---

⬅️ [Anterior: La base de datos](./05-LA-BASE-DE-DATOS.md) | ➡️ [Siguiente: Los reportes](./07-LOS-REPORTES.md)
