# 🔐 Acceso al Sistema y Seguridad de Autenticación

El sistema implementa un módulo de autenticación robusto y persistente en base de datos con **3 niveles de acceso (roles)**, protección criptográfica de contraseñas mediante **PBKDF2-HMAC-SHA256** y mecanismos de recuperación de cuenta.

---

## 👥 Credenciales de Acceso por Rol

El sistema cuenta con 3 cuentas predeterminadas precargadas en la base de datos:

| Rol / Perfil | Usuario | Contraseña | Permisos y Alcance |
|---|---|---|---|
| 🔑 **Administrador** | `admin` | `admin123` | Control total: gestión de usuarios, unidades, socios, planes preventivos, bitácora y emisión de reportes. |
| 🔧 **Mecánico** | `mecanico` | `mecanico123` | Gestión operativa de taller: registro y programación de servicios, actualización de odómetros y consulta de flota. |
| 👁️ **Operador / Auditor** | `auditor` | `auditor123` | Modo consulta y auditoría: lectura de KPIs en dashboard, estado de flota y generación de reportes oficiales. |

> [!NOTE]
> Al pulsar **Enter** desde los campos de usuario o contraseña, se enviará automáticamente el formulario de inicio de sesión.

---

## 🛡️ Estándar de Seguridad Criptográfica

A diferencia de un login básico, la seguridad del sistema está respaldada en base de datos (`usuario`):

1. **Hashing con Sal Aleatoria (Salt):**
   - Cada contraseña se procesa con **PBKDF2-HMAC-SHA256** utilizando **100,000 iteraciones** y una sal criptográfica única de 16 bytes generada con [`secrets.token_hex(16)`](file:///home/yheremyt/PROYECTO-MANTENIMIENTO/src/services/seguridad_service.py).
   - Ninguna contraseña se almacena en texto plano en la base de datos ni en el código.

2. **Comparación en Tiempo Constante:**
   - Para mitigar ataques de temporización (*timing attacks*), la verificación compara los hashes mediante [`secrets.compare_digest`](file:///home/yheremyt/PROYECTO-MANTENIMIENTO/src/services/seguridad_service.py).

3. **Control de Sesiones Inactivas:**
   - Las cuentas dadas de baja lógica (`activo = 0`) no pueden iniciar sesión; el sistema rechaza el intento informando el estado de la cuenta.

---

## 🔑 Recuperación de Contraseña

En la pantalla de acceso, el enlace **"¿Olvidaste tu contraseña?"** abre un modal de recuperación con dos métodos:

### Método 1: Pregunta Secreta de Seguridad
- El usuario introduce su nombre de cuenta y el sistema consulta su pregunta secreta configurada.
- Las respuestas se normalizan eliminando acentos, espacios superfluos y convirtiendo a minúsculas (`unicodedata.normalize`), permitiendo respuestas flexibles y seguras.
- Respuestas predeterminadas para los usuarios iniciales:
  - `admin`: *"Brisas del Palmar"*
  - `mecanico`: *"Cummins"*
  - `auditor`: *"Operaciones"*

### Método 2: Clave Maestra de Emergencia
- Permite a la gerencia técnica restablecer credenciales en caso de olvido de la pregunta secreta.
- Configurable mediante la variable de entorno `BRISAS_MASTER_KEY` (por defecto: `BRISAS-MASTER-2026`).

---

Para volver al índice de documentación, consulta el [`README.md`](README.md) de la carpeta `docs/` o el [`README.md`](../README.md) principal.
