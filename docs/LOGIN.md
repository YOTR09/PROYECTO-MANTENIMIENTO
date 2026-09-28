# Acceso al Sistema

La aplicación muestra una pantalla de inicio de sesión antes de abrir los módulos de gestión. Introduce estas credenciales para acceder:

 Usuario `admin123` 
 Contraseña  `adminx123`

Al escribirlas correctamente se abre el dashboard. Si los datos no coinciden, se muestra un mensaje y se puede volver a intentarlo. También se puede pulsar **Enter** desde cualquiera de los campos.

## Alcance de seguridad

Este acceso es una protección básica de la interfaz para una instalación local y de un solo administrador. Las credenciales están definidas en el código; no hay gestión de usuarios, almacenamiento de contraseñas con hash ni control de acceso a la base de datos. Por tanto, no debe considerarse una medida de seguridad para una aplicación expuesta a terceros o a equipos no confiables. Para ese escenario se necesitaría autenticación persistente y controles de acceso adicionales.