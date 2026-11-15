---
description: Cierra la épica actual y propone, revisadas por un experto en el stack, las iteraciones de la siguiente
argument-hint: "[número de la épica que cierra, opcional]"
---

Cierra la épica $ARGUMENTS (si no se indica, la de la iteración activa en `registro-pendientes.md`) y planifica la siguiente. El flujo completo está en la sección 4.4 de `_planificacion/README.md`: síguelo tal como está escrito ahí. Este comando agrega solo lo siguiente.

## 1. Lee antes de proponer

1. `AGENTS.md` completo, en especial «Stack y versiones» y «Estándares de calidad».
2. `README.md` (raíz) y, si el proyecto tiene interfaz, `DESIGN.md`.
3. `_planificacion/README.md`, `00_producto/registro-pendientes.md` (backlog) y `00_producto/decisiones.md`.
4. La definición de la épica que cierra, sus iteraciones y sus bitácoras.
5. La definición de la épica siguiente, las especificaciones relacionadas y, si existe, el contrato `docs/api/openapi.yaml`.

Si la épica todavía tiene iteraciones sin terminar, dilo y no la cierres.

## 2. Cierra la épica

Escribe la bitácora de cierre en la carpeta `bitacoras/` de la épica con la plantilla `_planificacion/plantillas/bitacora-cierre.md`: criterio de término comprobado con evidencia, hallazgos abiertos, decisiones del desarrollador y revisión al cierre. Aplica en el registro, en la misma pasada, lo que la revisión cambie.

## 3. Revisa como experto antes de proponer

Asume el rol de **desarrollador senior experto en el stack declarado en `AGENTS.md`** (por ejemplo, experto en Java y Spring Boot, en Python y Django o en Astro, según el proyecto). Antes de presentar las iteraciones, revisa cada una contra «Estándares de calidad» de `AGENTS.md`:

- Separación de responsabilidades y patrones de diseño adecuados al problema.
- Pruebas que corresponden al cambio y verificación medible en sus criterios.
- Seguridad: validación de entradas, manejo de secretos, permisos.
- Deuda técnica que arrastra la épica que cierra (bitácoras, hallazgos abiertos).
- **Sobreingeniería:** un patrón, una capa o una dependencia se proponen solo si resuelven un problema real del proyecto, en proporción a su nivel. Si algo sobra, quítalo.

Si una iteración necesita ajustes para cumplir los estándares, ajústala antes de proponerla.

## 4. Propón y espera aprobación

Presenta en el chat las iteraciones de la épica siguiente (número, nombre, objetivo en una línea, elementos del backlog que cubre y qué necesita cada una), todas dentro del tamaño máximo, y agrega una sección **«Revisión técnica del experto»** con lo que ajustaste y por qué. No generes ningún archivo de iteración hasta que el desarrollador apruebe.

Con la aprobación, sigue los pasos de generación y preparación de la sección 4.4 de `_planificacion/README.md`.
