# 🖼️ Imágenes de los Diagramas

Versiones listas para tesis de los diagramas de [`../DIAGRAMAS.md`](../DIAGRAMAS.md): fondo blanco, paleta azul corporativa sobria y tipografía Helvetica/Arial.

- **`.png`**: alta resolución (escala 4x), para Word / Google Docs / LaTeX.
- **`.svg`**: vectorial, para escalar sin pérdida (se puede importar en Word, LibreOffice o Inkscape, o convertir a PDF).

| Figura | Archivo | Descripción |
|---|---|---|
| 1 | `01-mvc` | Patrón MVC |
| 2 | `02-arquitectura-capas` | Arquitectura en capas |
| 3 | `03-uml-clases-modelos` | UML de clases: modelos de dominio |
| 4 | `04a-uml-clases-controladores` | UML de clases: controladores, repositorios y servicio de seguridad |
| 5 | `04b-uml-clases-servicios-legacy` | UML de clases: servicios heredados |
| 6 | `05-uml-clases-vistas` | UML de clases: vistas |
| 7 | `06-uml-clases-reportes` | UML de clases: generación de reportes |
| 8 | `07-modelo-entidad-relacion` | Modelo entidad-relación |
| 9 | `08-casos-de-uso` | Casos de uso por rol |
| 10 | `09-secuencia-login` | Secuencia: inicio de sesión |
| 11 | `10-secuencia-registrar-mantenimiento` | Secuencia: registrar mantenimiento |
| 12 | `11-secuencia-generar-reporte` | Secuencia: generar reporte |
| 13 | `12-secuencia-recuperar-password` | Secuencia: recuperar contraseña |
| 14 | `13-estados-semaforo` | Estados del semáforo |
| 15 | `14-actividad-arranque` | Actividad: arranque |
| 16 | `15-navegacion-interfaz` | Navegación de la interfaz |
| 17 | `16-despliegue` | Despliegue |

> [!NOTE]
> Si modificas `DIAGRAMAS.md`, regenera las imágenes con [`@mermaid-js/mermaid-cli`](https://github.com/mermaid-js/mermaid-cli) (`mmdc -i diagrama.mmd -o diagrama.png -b white -s 4`).
