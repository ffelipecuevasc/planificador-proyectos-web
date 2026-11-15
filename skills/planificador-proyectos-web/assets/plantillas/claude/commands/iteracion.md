---
description: Ejecuta una iteración completa siguiendo AGENTS.md, con verificación medida, bitácora y registro al día
argument-hint: "XX-YY"
---

Ejecuta la iteración $ARGUMENTS. Si no se indica número, usa la iteración activa de `_planificacion/00_producto/registro-pendientes.md`. El flujo completo está en la sección «Flujo de trabajo por iteración» de `AGENTS.md` y en la sección 4.1 de `_planificacion/README.md`: síguelo tal como está escrito ahí. Este comando es un recordatorio de los pasos que no se pueden saltar.

1. **Lee** en el orden de `AGENTS.md` («Orden de lectura obligatorio»): el registro, el archivo de la iteración, su especificación y el contrato de la API si los tiene, las RDA relacionadas y las bitácoras anteriores de la misma épica.
2. **Comprueba la definición de preparada** de `AGENTS.md`. Si algo falla, no empieces: di qué falta y propón cómo resolverlo.
3. **Marca la iteración `En curso`** en el registro y, si el proyecto trabaja con ramas, propón el nombre de la rama y espera aprobación.
4. **Implementa** solo lo de los criterios de aceptación, aplicando «Estándares de calidad» de `AGENTS.md` como lo haría un desarrollador senior experto en el stack del proyecto, sin sobreingeniería. Lo que esté fuera de alcance va como propuesta al registro.
5. **Verifica** según la definición de terminado: cada criterio que marques lleva el comando o la medición y su resultado. Si un dato solo lo puede obtener el desarrollador y ya lo intentaste por todos los medios, completa la sección «Evidencia del desarrollador» de la iteración.
6. **Escribe la bitácora** en la carpeta `bitacoras/` de la épica con `_planificacion/plantillas/bitacora.md`, incluida su revisión. No crees ningún otro archivo `.md` (sección «Documentos permitidos» de `AGENTS.md`).
7. **Actualiza el registro** en la misma pasada: estado de la iteración, filas del backlog que cubrió y una línea de historial con enlace a la bitácora.
8. **Deja la iteración `En revisión`** y entrega el resumen con los archivos modificados y el commit sugerido, con el formato y el largo de `AGENTS.md`.
9. Si era la **última iteración de su épica**, sigue con el cierre y la propuesta de la siguiente (`/siguiente-epica`).
