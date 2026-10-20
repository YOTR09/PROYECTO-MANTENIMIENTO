# 📐 Catálogo de Diagramas del Sistema

## Sistema de Control de Mantenimiento Preventivo — Brisas del Palmar

Este documento reúne **todos los diagramas** del proyecto (MVC, capas, UML de clases, ER, casos de uso, secuencia, estados, actividad y despliegue). Están escritos en [Mermaid](https://mermaid.js.org/), por lo que se visualizan directamente en GitHub, VS Code (extensión Markdown Preview Mermaid) y la mayoría de visores Markdown.

> [!NOTE]
> Los diagramas reflejan el código real de `src/`, `config/` y `database/` (verificado contra el repositorio). Si cambias la estructura, actualiza este archivo y [`ARQUITECTURA.md`](ARQUITECTURA.md).

> [!TIP]
> Versiones en imagen (PNG alta resolución y SVG vectorial, fondo blanco) para tesis: carpeta [`imagenes-diagramas/`](imagenes-diagramas/README.md).

## Índice

| # | Diagrama | Tipo |
|---|---|---|
| 1 | [Patrón MVC](#1-patrón-mvc) | Arquitectura |
| 2 | [Arquitectura en capas y dependencias](#2-arquitectura-en-capas-y-dependencias) | Paquetes / componentes |
| 3 | [UML de clases — Modelos de dominio](#3-uml-de-clases--modelos-de-dominio) | UML clases |
| 4 | [UML de clases — Controladores, Repositorios y Servicios](#4-uml-de-clases--controladores-repositorios-y-servicios) | UML clases |
| 5 | [UML de clases — Vistas](#5-uml-de-clases--vistas) | UML clases |
| 6 | [UML de clases — Generación de reportes](#6-uml-de-clases--generación-de-reportes) | UML clases |
| 7 | [Modelo Entidad-Relación](#7-modelo-entidad-relación-base-de-datos) | ER |
| 8 | [Casos de uso por rol](#8-casos-de-uso-por-rol) | UML casos de uso |
| 9 | [Secuencia: inicio de sesión](#91-inicio-de-sesión) | UML secuencia |
| 10 | [Secuencia: registrar mantenimiento realizado](#92-registrar-mantenimiento-realizado-transacción-atómica) | UML secuencia |
| 11 | [Secuencia: generar reporte](#93-generar-un-reporte-con-filtros) | UML secuencia |
| 12 | [Secuencia: recuperar contraseña](#94-recuperación-de-contraseña) | UML secuencia |
| 13 | [Estados del semáforo](#10-máquina-de-estados-del-semáforo-preventivo) | UML estados |
| 14 | [Actividad: arranque de la aplicación](#11-diagrama-de-actividad-arranque-de-la-aplicación) | UML actividad |
| 15 | [Navegación de la interfaz](#12-mapa-de-navegación-de-la-interfaz) | Flujo |
| 16 | [Despliegue](#13-diagrama-de-despliegue) | UML despliegue |

---

## 1. Patrón MVC

El proyecto aplica **MVC** adaptado a una aplicación de escritorio. La capa **Modelo** se compone de las entidades de dominio (`src/models/`) y del acceso a datos (`src/repositories/` + `config/database.py`). Las **Vistas** nunca tocan SQL; los **Controladores** validan, aplican reglas y orquestan.

```mermaid
flowchart LR
    U(["Usuario"])

    subgraph V ["VISTA - src/views/"]
        direction TB
        V1["MainWindow<br/>LoginView<br/>DashboardView"]
        V2["VehiculosView<br/>SociosView<br/>UsuariosView"]
        V3["ProgramacionMantView<br/>TiposMantView<br/>HistorialMantView"]
        V4["ReportesView<br/>ModalFiltrosReporte<br/>RecuperarPasswordModal"]
        V5["theme.py"]
    end

    subgraph C ["CONTROLADOR - src/controllers/"]
        direction TB
        C0["BaseController"]
        C1["AuthController<br/>UsuarioController"]
        C2["VehiculoController<br/>SocioController"]
        C3["MantenimientoController<br/>ReporteController"]
    end

    subgraph M ["MODELO - src/models/, src/repositories/, config/"]
        direction TB
        M1["Entidades de dominio<br/>Usuario, Rol, Socio, Vehiculo,<br/>TipoMantenimiento,<br/>MantenimientoProgramado,<br/>HistorialMantenimiento"]
        M2["Repositorios<br/>SQL parametrizado"]
        M3[("SQLite<br/>data/mantenimiento.db")]
        M1 --> M2 --> M3
    end

    U -- "1. clic / texto" --> V
    V -- "2. invoca metodo estatico" --> C
    C -- "3. consulta / persiste" --> M
    M -. "4. modelos / dicts" .-> C
    C -. "5. (ok, dato, mensaje)" .-> V
    V -. "6. renderiza" .-> U
```

### Responsabilidad de cada componente MVC

| Componente | Carpeta | Responsabilidad | Prohibido |
|---|---|---|---|
| **Modelo** | `src/models/`, `src/repositories/`, `config/` | Entidades, reglas de dominio (permisos de `Usuario`), SQL y transacciones | Conocer la UI |
| **Vista** | `src/views/` | Dibujar widgets, capturar eventos, mostrar mensajes y aplicar visibilidad por rol | Ejecutar SQL |
| **Controlador** | `src/controllers/` | Validar entradas, reglas de negocio (semáforo, unicidad, reactivación), orquestar transacciones, devolver `(ok, dato, mensaje)` | Dibujar widgets |

---

## 2. Arquitectura en capas y dependencias

Dependencias **reales** de importación (verificadas en el código). Observa que `src/services/` es una **capa heredada (legacy)**: la aplicación ya no la usa (las vistas llaman a controladores); solo se conserva `SeguridadService` (activo) y el resto se mantiene por compatibilidad con `tests/test_services.py`.

```mermaid
flowchart TB
    MAIN["main.py<br/>punto de entrada"]

    subgraph L1 ["CAPA 1 - PRESENTACION  (src/views/)"]
        P1["MainWindow, LoginView, RecuperarPasswordModal, DashboardView,<br/>VehiculosView, SociosView, ProgramacionMantView, TiposMantView,<br/>HistorialMantView, ReportesView, ModalFiltrosReporte, UsuariosView, theme.py"]
    end

    subgraph L2 ["CAPA 2 - CONTROLADORES  (src/controllers/)"]
        C1["BaseController"]
        C2["AuthController, UsuarioController, SocioController,<br/>VehiculoController, MantenimientoController, ReporteController"]
    end

    subgraph LX ["SERVICIOS Y REPORTES"]
        direction LR
        S1["SeguridadService<br/>PBKDF2-HMAC-SHA256<br/>(src/services/, activo)"]
        S2["PDFReportGenerator (ReportLab)<br/>ExcelReportGenerator (openpyxl)<br/>(src/reports/)"]
        S3["Servicios heredados (legacy)<br/>Socio, Vehiculo, TipoMantenimiento,<br/>Mantenimiento, Autenticacion"]
    end

    subgraph L3 ["CAPA 3 - ACCESO A DATOS  (src/repositories/)"]
        R1["UsuarioRepository, SocioRepository, VehiculoRepository,<br/>TipoMantenimientoRepository, MantenimientoRepository"]
    end

    subgraph L4 ["INFRAESTRUCTURA"]
        direction LR
        CFG["config/database.py<br/>init_db, get_db_transaction"]
        DB[("SQLite<br/>data/mantenimiento.db")]
        CFG --> DB
    end

    DOM["DOMINIO (transversal)<br/>src/models/: BaseModel, 7 entidades, enums.py"]

    MAIN --> L1
    L1 -- "invoca" --> L2
    L2 --> S1
    L2 --> S2
    L2 -- "consulta / persiste" --> L3
    L3 --> CFG
    S3 -.-> L3
    DOM -. "usado por todas las capas" .- L2
```

**Reglas de dependencia:** `Vista → Controlador → Repositorio → config → SQLite`. Las flechas nunca van en sentido contrario. `models` es transversal (lo usan todas las capas, no depende de ninguna).

---

## 3. UML de clases — Modelos de dominio

Archivos: `src/models/*.py`. Todos los modelos heredan de `BaseModel` (clase abstracta) y se construyen con `from_dict()`.

```mermaid
classDiagram
    direction TB

    class BaseModel {
        <<abstract>>
        +from_dict(data)$ BaseModel
        +to_dict() Dict
        +__repr__() str
    }

    class Rol {
        +int id_rol
        +str nombre
        +str descripcion
        +from_dict(data)$ Rol
    }

    class Usuario {
        +int id_usuario
        +int id_rol
        +str username
        +str nombre_completo
        +str password_hash
        +str salt
        +str pregunta_seguridad
        +str respuesta_seguridad
        +int activo
        +str creado_en
        +str rol_nombre
        +es_admin bool
        +es_mecanico bool
        +es_operador bool
        +puede_gestionar_usuarios() bool
        +puede_eliminar() bool
        +puede_modificar_flota() bool
        +puede_gestionar_mantenimiento() bool
        +puede_generar_reportes() bool
    }

    class Socio {
        +int id_socio
        +str cedula
        +str nombre_completo
        +str telefono
        +str estado
        +int activo
    }

    class Vehiculo {
        +int id_vehiculo
        +int id_socio
        +str numero_unidad
        +str placa
        +str marca_modelo
        +int ano
        +int kilometraje_actual
        +str status
        +int activo
        +str socio_nombre
        +str socio_cedula
    }

    class TipoMantenimiento {
        +int id_tipo
        +str nombre
        +str descripcion
        +int intervalo_km
        +int intervalo_dias
        +int activo
    }

    class MantenimientoProgramado {
        +int id_programacion
        +int id_vehiculo
        +int id_tipo
        +str fecha_ultimo_servicio
        +int km_ultimo_servicio
        +str fecha_proximo_servicio
        +int km_proximo_servicio
        +str observaciones
        +int activo
        +str estado_alerta
        +str badge_alerta
        +str color_hex
    }

    class HistorialMantenimiento {
        +int id_historial
        +int id_vehiculo
        +int id_tipo
        +str fecha_realizado
        +int km_al_momento
        +float costo
        +str taller_mecanico
        +str descripcion_trabajo
    }

    class EstadoVehiculo {
        <<enumeration>>
        ACTIVO
        EN_TALLER
        INACTIVO
    }
    class EstadoSocio {
        <<enumeration>>
        ACTIVO
        INACTIVO
    }
    class EstadoMantenimiento {
        <<enumeration>>
        AL_DIA
        POR_VENCER
        VENCIDO
    }
    class RolUsuario {
        <<enumeration>>
        ADMINISTRADOR
        MECANICO
        OPERADOR
    }

    BaseModel <|-- Rol
    BaseModel <|-- Usuario
    BaseModel <|-- Socio
    BaseModel <|-- Vehiculo
    BaseModel <|-- TipoMantenimiento
    BaseModel <|-- MantenimientoProgramado
    BaseModel <|-- HistorialMantenimiento

    Rol "1" --> "0..*" Usuario : asigna
    Socio "1" --> "0..*" Vehiculo : posee
    Vehiculo "1" --> "0..*" MantenimientoProgramado : tiene
    TipoMantenimiento "1" --> "0..*" MantenimientoProgramado : define
    Vehiculo "1" --> "0..*" HistorialMantenimiento : registra
    TipoMantenimiento "1" --> "0..*" HistorialMantenimiento : clasifica

    Vehiculo ..> EstadoVehiculo : status
    Socio ..> EstadoSocio : estado
    MantenimientoProgramado ..> EstadoMantenimiento : estado_alerta
    Usuario ..> RolUsuario : rol_nombre
```

> [!NOTE]
> Los atributos de `Vehiculo`, `MantenimientoProgramado` e `HistorialMantenimiento` incluyen campos derivados de `JOIN` (`socio_nombre`, `placa`, `tipo_nombre`, etc.) que no son columnas propias de su tabla.

---

## 4. UML de clases — Controladores, Repositorios y Servicios

```mermaid
classDiagram
    direction LR

    class BaseController {
        +respuesta_exito(datos, mensaje)$ Dict
        +respuesta_error(mensaje, datos)$ Dict
    }

    class AuthController {
        -Usuario _sesion
        +CLAVE_MAESTRA_EMERGENCIA str
        +login(username, contrasena)$ Tuple
        +logout()$
        +get_sesion_actual()$ Usuario
        +cambiar_contrasena(id_usuario, actual, nueva)$ Tuple
        +obtener_pregunta_recuperacion(username)$ Tuple
        +restablecer_por_pregunta(...)$ Tuple
        +restablecer_por_clave_maestra(...)$ Tuple
    }

    class UsuarioController {
        +listar_usuarios()$ List
        +obtener_usuario(id)$ Usuario
        +listar_roles()$ List
        +registrar_usuario(...)$ Tuple
        +actualizar_usuario(...)$ Tuple
        +restablecer_contrasena(id, nueva)$ Tuple
        +eliminar_usuario(id, logico)$ Tuple
    }

    class SocioController {
        +listar_socios()$ List
        +obtener_socio(id)$ Socio
        +registrar_socio(...)$ Tuple
        +reactivar_socio(...)$ Tuple
        +actualizar_socio(...)$ Tuple
        +eliminar_socio(id, logico)$ Tuple
    }

    class VehiculoController {
        +listar_vehiculos()$ List
        +obtener_vehiculo(id)$ Vehiculo
        +registrar_vehiculo(...)$ Tuple
        +reactivar_vehiculo(...)$ Tuple
        +actualizar_vehiculo(...)$ Tuple
        +actualizar_kilometraje(id, nuevo_km)$ Tuple
        +eliminar_vehiculo(id, logico)$ Tuple
    }

    class MantenimientoController {
        +listar_tipos()$ List
        +registrar_tipo(...)$ Tuple
        +actualizar_tipo(...)$ Tuple
        +eliminar_tipo(id, logico)$ Tuple
        +calcular_estado_alerta(item)$ Dict
        +listar_programaciones(...)$ List
        +programar_mantenimiento(...)$ Tuple
        +eliminar_programacion(id, logico)$ Tuple
        +registrar_servicio_realizado(...)$ Tuple
        +listar_historial(...)$ List
        +obtener_resumen_dashboard()$ Dict
    }

    class ReporteController {
        +normalizar_filtros(filtros)$ Dict
        +describir_filtros(filtros)$ str
        +obtener_catalogos_para_filtros()$ Dict
        +contar_registros(numero_reporte, filtros)$ Tuple
        +generar_reporte_1_flota_pdf(ruta, filtros)$ Tuple
        +generar_reporte_2_preventivo_pdf(ruta, filtros)$ Tuple
        +generar_reporte_3_historial_excel(ruta, filtros)$ Tuple
        +generar_reporte_4_socios_pdf(ruta, filtros)$ Tuple
        +generar_reporte_5_metricas_excel(ruta, filtros)$ Tuple
    }

    class FiltroInvalidoError {
        <<exception>>
    }

    class SeguridadService {
        +generar_salt()$ str
        +hashear_contrasena(contrasena, salt)$ str
        +verificar_contrasena(plana, salt, hash)$ bool
        +normalizar_texto_seguridad(texto)$ str
        +verificar_respuesta_seguridad(ingresada, guardada)$ bool
    }

    class UsuarioRepository
    class SocioRepository
    class VehiculoRepository
    class TipoMantenimientoRepository
    class MantenimientoRepository {
        +get_programaciones()$
        +get_programacion_by_id()$
        +upsert_programacion()$
        +delete_programacion()$
        +restore_programacion()$
        +add_historial()$
        +get_historial()$
        +get_talleres_registrados()$
    }

    BaseController <|-- AuthController
    BaseController <|-- UsuarioController
    BaseController <|-- SocioController
    BaseController <|-- VehiculoController
    BaseController <|-- MantenimientoController
    BaseController <|-- ReporteController
    ReporteController ..> FiltroInvalidoError : lanza

    AuthController ..> SeguridadService
    UsuarioController ..> SeguridadService
    AuthController ..> UsuarioRepository
    UsuarioController ..> UsuarioRepository
    SocioController ..> SocioRepository
    SocioController ..> VehiculoRepository
    VehiculoController ..> VehiculoRepository
    MantenimientoController ..> MantenimientoRepository
    MantenimientoController ..> VehiculoRepository
    MantenimientoController ..> TipoMantenimientoRepository
    ReporteController ..> MantenimientoController
    ReporteController ..> MantenimientoRepository
    ReporteController ..> VehiculoRepository
    ReporteController ..> SocioRepository
```

### Capa de servicios heredada (legacy)

```mermaid
classDiagram
    direction LR
    class AutenticacionService {
        +validar_credenciales(usuario, contrasena)$ bool
    }
    class SocioService
    class VehiculoService
    class TipoMantenimientoService
    class MantenimientoService {
        +calcular_estado_alerta(item)$
        +listar_programaciones()$
        +programar_mantenimiento()$
        +registrar_mantenimiento_realizado()$
        +listar_historial()$
        +obtener_resumen_dashboard()$
    }
    AutenticacionService ..> AuthController : delega
    SocioService ..> SocioRepository
    VehiculoService ..> VehiculoRepository
    TipoMantenimientoService ..> TipoMantenimientoRepository
    MantenimientoService ..> MantenimientoRepository
```

---

## 5. UML de clases — Vistas

```mermaid
classDiagram
    direction TB

    class MainWindow {
        +Usuario usuario_actual
        +dict vistas
        +dict botones_nav
        -_mostrar_pantalla_login()
        -_abrir_aplicacion(usuario)
        -_setup_layout()
        -_inicializar_vistas()
        +cambiar_vista(key)
        +cambiar_tema(nuevo_tema)
    }

    class LoginView
    class RecuperarPasswordModal
    class DashboardView
    class VehiculosView
    class SociosView
    class ProgramacionMantView
    class TiposMantView
    class HistorialMantView
    class ReportesView
    class ModalFiltrosReporte
    class UsuariosView

    MainWindow *-- LoginView : muestra al inicio
    LoginView ..> RecuperarPasswordModal : abre
    MainWindow *-- DashboardView
    MainWindow *-- VehiculosView
    MainWindow *-- SociosView
    MainWindow *-- ProgramacionMantView
    MainWindow *-- TiposMantView
    MainWindow *-- HistorialMantView
    MainWindow *-- ReportesView
    MainWindow *-- UsuariosView : solo Administrador
    ReportesView ..> ModalFiltrosReporte : abre

    LoginView ..> AuthController
    RecuperarPasswordModal ..> AuthController
    DashboardView ..> MantenimientoController
    VehiculosView ..> VehiculoController
    VehiculosView ..> SocioController
    SociosView ..> SocioController
    ProgramacionMantView ..> MantenimientoController
    ProgramacionMantView ..> VehiculoController
    TiposMantView ..> MantenimientoController
    HistorialMantView ..> MantenimientoController
    ReportesView ..> ReporteController
    ModalFiltrosReporte ..> ReporteController
    UsuariosView ..> UsuarioController
    UsuariosView ..> AuthController
```

---

## 6. UML de clases — Generación de reportes

```mermaid
classDiagram
    direction LR
    class ReporteController
    class PDFReportGenerator {
        +generar_reporte_flota(vehiculos, ruta, criterios)$
        +generar_reporte_preventivo(programaciones, ruta, criterios)$
        +generar_reporte_socios(socios, ruta, criterios)$
    }
    class ExcelReportGenerator {
        -_aplicar_estilos_base(ws, titulo, subtitulo, criterios)$
        -_autoajustar_columnas(ws)$
        +generar_reporte_historial_costos(historial, ruta, criterios)$
        +generar_reporte_metricas_talleres(historial, vehiculos, ruta, criterios)$
    }
    ReporteController ..> PDFReportGenerator : Reportes 1, 2 y 4 (PDF)
    ReporteController ..> ExcelReportGenerator : Reportes 3 y 5 (Excel)
```

| Reporte | Formato | Generador |
|---|---|---|
| 1. Ficha Técnica y Estado de Flota | PDF | `PDFReportGenerator.generar_reporte_flota` |
| 2. Plan Preventivo y Alertas | PDF | `PDFReportGenerator.generar_reporte_preventivo` |
| 3. Bitácora Histórica y Costos | Excel | `ExcelReportGenerator.generar_reporte_historial_costos` |
| 4. Directorio de Socios y Unidades | PDF | `PDFReportGenerator.generar_reporte_socios` |
| 5. Métricas por Taller | Excel | `ExcelReportGenerator.generar_reporte_metricas_talleres` |

---

## 7. Modelo Entidad-Relación (base de datos)

Definido en [`database/schema.sql`](../database/schema.sql): 7 tablas en 3FN, con `PRAGMA foreign_keys = ON`.

```mermaid
flowchart LR
    OPE(["Operador / Auditor"])
    MEC(["Mecanico"])
    ADM(["Administrador"])

    MEC -. "hereda permisos de" .-> OPE
    ADM -. "hereda permisos de" .-> MEC

    subgraph SIS ["Sistema de Mantenimiento Preventivo - Brisas del Palmar"]
        direction TB
        subgraph G1 ["Casos de uso del Operador (base de todos los roles)"]
            direction TB
            UC1(["Iniciar y cerrar sesion"])
            UC2(["Recuperar contrasena"])
            UC3(["Ver dashboard y KPIs"])
            UC4(["Consultar flota, socios,<br/>catalogo e historial"])
            UC5(["Generar reportes PDF / Excel"])
            UC6(["Cambiar tema visual"])
        end
        subgraph G2 ["Casos de uso adicionales del Mecanico"]
            direction TB
            UC7(["Programar mantenimiento"])
            UC8(["Registrar servicio realizado"])
            UC9(["Actualizar odometro"])
        end
        subgraph G3 ["Casos de uso exclusivos del Administrador"]
            direction TB
            UC10(["Crear, editar y dar de baja<br/>socios y vehiculos"])
            UC11(["Gestionar catalogo de rutinas"])
            UC12(["Gestionar usuarios y<br/>restablecer contrasenas"])
        end
    end

    OPE --> G1
    MEC --> G2
    ADM --> G3
```

> [!NOTE]
> Restricción compuesta: `UNIQUE(id_vehiculo, id_tipo)` en `mantenimiento_programado` (una programación por unidad y rutina). Existen 15 índices de búsqueda (`idx_*`) sobre `username`, `cedula`, `placa`, `numero_unidad`, `activo`, etc.

---

## 8. Casos de uso por rol

```mermaid
flowchart LR
    ADM(["🔑 Administrador"])
    MEC(["🔧 Mecánico"])
    OPE(["👁️ Operador / Auditor"])

    subgraph SIS ["Sistema Brisas del Palmar"]
        UC0(["Iniciar / cerrar sesión"])
        UC0b(["Recuperar contraseña"])
        UC1(["Ver dashboard y KPIs"])
        UC2(["Consultar flota, socios, catálogo e historial"])
        UC3(["Generar reportes PDF / Excel"])
        UC4(["Programar mantenimiento y registrar servicio realizado"])
        UC5(["Actualizar odómetro"])
        UC6(["Crear / editar / dar de baja socios y vehículos"])
        UC7(["Gestionar catálogo de rutinas"])
        UC8(["Gestionar usuarios y restablecer contraseñas"])
        UC9(["Cambiar tema visual"])
    end

    ADM --- UC0 & UC0b & UC1 & UC2 & UC3 & UC4 & UC5 & UC6 & UC7 & UC8 & UC9
    MEC --- UC0 & UC0b & UC1 & UC2 & UC3 & UC4 & UC5 & UC9
    OPE --- UC0 & UC0b & UC1 & UC2 & UC3 & UC9
```

| Capacidad | Administrador | Mecánico | Operador |
|---|:---:|:---:|:---:|
| Dashboard, consulta, reportes (`puede_generar_reportes`) | ✅ | ✅ | ✅ |
| Programar / registrar mantenimiento (`puede_gestionar_mantenimiento`) | ✅ | ✅ | ❌ |
| Modificar flota y socios (`puede_modificar_flota`) | ✅ | ❌ (solo odómetro) | ❌ |
| Eliminar / dar de baja (`puede_eliminar`) | ✅ | ❌ | ❌ |
| Gestionar usuarios (`puede_gestionar_usuarios`) | ✅ | ❌ | ❌ |

> [!NOTE]
> Los permisos se **definen** en `Usuario` (modelo) y se **aplican** en las vistas (habilitando/ocultando controles, y creando `UsuariosView` solo para el Administrador). Revisa `vehiculos_view.py`, `programacion_mant_view.py` y `tipos_mant_view.py` para el detalle fino del rol Mecánico.

---

## 9. Diagramas de secuencia

### 9.1 Inicio de sesión

```mermaid
sequenceDiagram
    actor U as Usuario
    participant LV as LoginView
    participant AC as AuthController
    participant UR as UsuarioRepository
    participant SS as SeguridadService
    participant MW as MainWindow

    U->>LV: usuario + contraseña (clic o Enter)
    LV->>AC: login(username, contrasena)
    AC->>UR: get_by_username(username)
    UR-->>AC: fila de usuario (hash, salt, rol)
    alt usuario no existe
        AC-->>LV: (False, None, "credenciales inválidas")
    else cuenta inactiva (activo = 0)
        AC-->>LV: (False, None, "cuenta inactiva")
    else existe y activo
        AC->>SS: verificar_contrasena(plana, salt, hash)
        SS-->>AC: compare_digest → True / False
        alt contraseña incorrecta
            AC-->>LV: (False, None, mensaje)
        else correcta
            AC-->>LV: (True, Usuario, "ok")
            LV->>MW: _abrir_aplicacion(usuario)
            MW->>MW: expandir a 1280x800, crear sidebar y vistas según rol
        end
    end
    LV-->>U: error en rojo o panel principal
```

### 9.2 Registrar mantenimiento realizado (transacción atómica)

```mermaid
sequenceDiagram
    actor U as Mecánico / Admin
    participant PV as ProgramacionMantView
    participant MC as MantenimientoController
    participant DB as get_db_transaction()
    participant MR as MantenimientoRepository
    participant VR as VehiculoRepository

    U->>PV: "✅ Registrar Mantenimiento Realizado"
    PV->>MC: registrar_servicio_realizado(vehiculo, tipo, fecha, km, costo, taller, desc)
    MC->>MC: validar fecha, km ≥ 0, costo ≥ 0
    MC->>DB: BEGIN IMMEDIATE
    MC->>MR: add_historial(..., conn)
    MC->>VR: get_by_id(vehiculo)
    opt km > kilometraje_actual
        MC->>VR: update_kilometraje(km, conn)
    end
    MC->>MC: programar_mantenimiento(fecha_ultimo, km_ultimo, conn)
    MC->>MR: upsert_programacion(próx. fecha y km, conn)
    alt todo correcto
        DB-->>MC: COMMIT
        MC-->>PV: (True, id_historial, mensaje)
        PV-->>U: tabla refrescada, semáforo 🟢 Al Día
    else cualquier excepción
        DB-->>MC: ROLLBACK
        MC-->>PV: (False, None, error)
        PV-->>U: mensaje de error
    end
```

### 9.3 Generar un reporte con filtros

```mermaid
sequenceDiagram
    actor U as Usuario
    participant RV as ReportesView
    participant MF as ModalFiltrosReporte
    participant RC as ReporteController
    participant REPO as Repositorios
    participant GEN as PDF / Excel Generator

    U->>RV: elige reporte
    RV->>MF: abre modal de filtros
    MF->>RC: obtener_catalogos_para_filtros()
    RC-->>MF: tipos, talleres, vehículos, socios
    U->>MF: fechas, tipo, taller, estado...
    MF->>RC: normalizar_filtros(filtros)
    alt filtros inválidos
        RC-->>MF: FiltroInvalidoError
        MF-->>U: mensaje de validación
    else válidos
        U->>RV: elige carpeta destino
        RV->>RC: generar_reporte_N_*(ruta, filtros)
        RC->>REPO: consultar datos filtrados
        REPO-->>RC: filas
        RC->>GEN: generar_reporte_*(datos, ruta, describir_filtros())
        GEN-->>RC: archivo .pdf / .xlsx
        RC-->>RV: respuesta de éxito (o "sin resultados")
        RV-->>U: confirmación
    end
```

### 9.4 Recuperación de contraseña

```mermaid
sequenceDiagram
    actor U as Usuario
    participant LV as LoginView
    participant RM as RecuperarPasswordModal
    participant AC as AuthController
    participant SS as SeguridadService
    participant UR as UsuarioRepository

    U->>LV: "¿Olvidaste tu contraseña?"
    LV->>RM: abrir modal
    alt Método 1: pregunta secreta
        RM->>AC: obtener_pregunta_recuperacion(username)
        AC-->>RM: pregunta
        U->>RM: respuesta + nueva contraseña + confirmación
        RM->>AC: restablecer_por_pregunta(...)
        AC->>SS: verificar_respuesta_seguridad (normalizada)
    else Método 2: clave maestra
        U->>RM: clave maestra + nueva contraseña
        RM->>AC: restablecer_por_clave_maestra(...)
        AC->>AC: comparar con BRISAS_MASTER_KEY
    end
    AC->>SS: generar_salt + hashear_contrasena
    AC->>UR: update_password(id, hash, salt)
    AC-->>RM: (True, mensaje)
    RM-->>LV: on_success_callback
```

---

## 10. Máquina de estados del semáforo preventivo

Implementada en `MantenimientoController.calcular_estado_alerta` (mismos umbrales en `MantenimientoService`). Se evalúan **km** y **días**; gana el estado más grave.

```mermaid
stateDiagram-v2
    [*] --> AlDia : programar_mantenimiento()
    AlDia : 🟢 Al Día
    AlDia : Δkm > 500 y Δdías > 10
    PorVencer : 🟡 Por Vencer
    PorVencer : Δkm ≤ 500 o Δdías ≤ 10
    Vencido : 🔴 Vencido
    Vencido : Δkm ≤ 0 o Δdías ≤ 0

    AlDia --> PorVencer : avanza odómetro / pasa el tiempo
    PorVencer --> Vencido : se alcanza o supera el límite
    AlDia --> Vencido : salto grande de odómetro
    PorVencer --> AlDia : registrar_servicio_realizado()
    Vencido --> AlDia : registrar_servicio_realizado()
```

---

## 11. Diagrama de actividad: arranque de la aplicación

```mermaid
flowchart TD
    A(["python main.py"]) --> B["sys.path ← raíz del proyecto"]
    B --> C["init_db()"]
    C --> C1["Crear carpeta data/ si no existe"]
    C1 --> C2["Migrar columnas activo / seguridad"]
    C2 --> C3["Ejecutar schema.sql"]
    C3 --> C4{"Faltan roles o tipos de mantenimiento<br/>o (fuera de test) socios / vehículos?"}
    C4 -- Sí --> C5["Ejecutar seeds.sql"]
    C4 -- No --> D
    C5 --> D{"¿Error en init_db?"}
    D -- Sí --> E["Mensaje crítico y sys.exit(1)"]
    D -- No --> F["MainWindow() 520x620"]
    F --> G["Mostrar LoginView"]
    G --> H{"¿Credenciales válidas?"}
    H -- No --> G
    H -- Sí --> I["Ventana 1280x800, sidebar y vistas según rol"]
    I --> J["Dashboard"]
    J --> K{"¿Cerrar sesión?"}
    K -- Sí --> G
    K -- No --> J
```

---

## 12. Mapa de navegación de la interfaz

```mermaid
flowchart LR
    LOGIN["LoginView"] -- "olvidé contraseña" --> REC["RecuperarPasswordModal"]
    REC --> LOGIN
    LOGIN -- "éxito" --> MW["MainWindow + Sidebar"]
    MW --> D["📊 Dashboard"]
    MW --> U["🚐 Flota y Unidades"]
    MW --> S["👥 Socios"]
    MW --> P["🛠️ Control Preventivo"]
    MW --> T["📋 Catálogo Rutinas"]
    MW --> H["📜 Bitácora Histórica"]
    MW --> R["📑 Reportes"]
    MW --> US["⚙️ Usuarios (solo Admin)"]
    D -- "Ir a Control Preventivo" --> P
    R --> MF["Modal de filtros"]
    MW -- "Cerrar sesión" --> LOGIN
```

---

## 13. Diagrama de despliegue

```mermaid
flowchart TB
    subgraph PC ["Computadora de escritorio (Linux / Windows / macOS)"]
        subgraph PY ["Intérprete Python 3.10+ (venv)"]
            APP["Aplicación: main.py + src/ + config/"]
            LIBS["customtkinter, pillow, reportlab, openpyxl"]
            TK["Tkinter / Tcl-Tk"]
            SQ["sqlite3 (librería estándar)"]
        end
        FS1[("data/mantenimiento.db")]
        FS2[("data/test_mantenimiento.db (solo pruebas)")]
        FS3["assets/ (logos)"]
        OUT["Carpeta destino: reportes .pdf / .xlsx"]
    end
    APP --> LIBS --> TK
    APP --> SQ --> FS1
    APP -. "pruebas" .-> FS2
    APP --> FS3
    APP --> OUT
```

> [!NOTE]
> No hay servidor ni red: es una aplicación monolítica local. El respaldo consiste en copiar `data/mantenimiento.db`.
