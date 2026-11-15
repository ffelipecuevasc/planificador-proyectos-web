---
description: Audita una épica antes de cerrarla, comprobando que lo marcado como cumplido realmente lo esté
argument-hint: "XX"
---

Audita la épica $ARGUMENTS (si no se indica, la de la iteración activa en `registro-pendientes.md`). El flujo completo está en la sección 4.6 de `_planificacion/README.md`: síguelo tal como está escrito ahí.

Conviene ejecutar este comando en una sesión nueva, sin el contexto de quien construyó la épica: así la revisión no se apoya en lo que el agente ya cree que hizo.

1. **Lee** `AGENTS.md`, `DESIGN.md` si existe, la definición de la épica, cada iteración con sus criterios, todas sus bitácoras, las RDA relacionadas, las especificaciones y el contrato de la API si los tiene, y `00_producto/auditoria-tecnica.md` para saber el último número de auditoría y los hallazgos abiertos.
2. **Comprueba con mediciones reales**, no con lo que dicen las bitácoras: ejecuta los comandos de verificación de `AGENTS.md`, recorre el código que tocó cada iteración y compara cada criterio marcado como cumplido con lo que realmente existe.
3. **Revisa como un desarrollador senior experto en el stack** del proyecto: «Estándares de calidad» de `AGENTS.md`, deuda técnica declarada o escondida, y conformidad con `DESIGN.md` y `AGENTS.md`.
4. **Revisa los documentos:** busca en las zonas de documentación archivos `.md` que no estén en `.claude/hooks/documentos-permitidos.md` y repórtalos como hallazgo; no los borres.
5. **Escribe la auditoría** en `00_producto/auditorias/auditoria-NN.md` con la plantilla `_planificacion/plantillas/auditoria.md` (NN = último número usado más uno) y agrega sus hallazgos al índice de `auditoria-tecnica.md`.
6. **No corrijas nada** durante la auditoría. Los hallazgos Altos y Medios entran al backlog, y el desarrollador decide qué se corrige antes del cierre.
