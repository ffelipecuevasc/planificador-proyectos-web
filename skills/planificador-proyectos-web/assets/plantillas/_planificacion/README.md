# _planificacion · Guía de la documentación del proyecto

Esta carpeta contiene todo lo que un agente de IA o una persona necesita para saber **qué se construye, por qué, en qué orden y qué se hizo**. No contiene código ni se publica.

> Si este archivo discrepa con `00_producto/registro-pendientes.md` sobre el estado del trabajo, prevalece el registro. Sobre las reglas de la carpeta, prevalece este archivo.

<!-- PLANTILLA: este archivo se escribe solo con los componentes activos del proyecto. Las secciones marcadas con un comentario PLANTILLA se borran completas si su componente no está activo (y se renumeran las que siguen dentro del mismo grupo; las secciones condicionales están al final de cada grupo para que los números que citan otros documentos no cambien); si está activo, se borra solo el comentario. Quita también del árbol de la sección 1 y de la tabla de la sección 6 lo que el proyecto no usa. Borra también este comentario. -->

---

## 1. Estructura

```text
_planificacion/
├── README.md                              Esta guía y sus reglas
├── plantillas/                            Plantillas de los documentos que se repiten
├── 00_producto/
│   ├── producto.md                        Qué es el producto, para quién y qué no es
│   ├── registro-pendientes.md             Backlog y fuente única de verdad del trabajo pendiente
│   ├── registro-archivo.md                Filas antiguas del registro (épicas cerradas, historial)
│   ├── decisiones.md                      Registro de Decisiones Arquitectónicas (RDA)
│   ├── propuestas-documentos-protegidos.md   Cambios propuestos a los documentos protegidos
│   ├── auditoria-tecnica.md               Índice de auditorías y estado de los hallazgos
│   ├── auditorias/
│   │   └── auditoria-NN.md                Cada auditoría completa
│   └── linea-base-produccion.md           Cifras reales de producción, si el proyecto ya está publicado
├── 10_epicas/
│   └── epica-XX-nombre/
│       ├── definicion-epica-XX.md
│       ├── iteracion-XX-YY-descripcion.md
│       └── bitacoras/
│           ├── bitacora-XX-YY.md
│           ├── bitacora-XX-YY-sufijo.md   Bitácoras adicionales de la misma iteración
│           └── bitacora-XX-cierre.md      Cierre de la épica
└── 20_especificaciones/
    └── spec-funcionalidad.md              Comportamiento esperado de cada funcionalidad
```

`registro-archivo.md`, `propuestas-documentos-protegidos.md` y `linea-base-produccion.md` se crean recién cuando hacen falta, con su plantilla.

## 2. Contenido de cada carpeta

### 2.1 `00_producto/`

Documentos vivos que describen el producto completo.

1. **`producto.md`:** propósito, qué es, qué no es, público, idioma y tono, indicadores de éxito e hitos. Cambia poco; se consulta ante dudas de alcance.
2. **`registro-pendientes.md`:** estado de las épicas abiertas y sus iteraciones, épicas cerradas, backlog priorizado, datos pendientes del cliente, decisiones por tomar, propuestas fuera de alcance e historial. Es lo primero que se lee y lo último que se actualiza en cada trabajo.
3. **`registro-archivo.md`:** las filas que salen del registro para que no crezca sin control (sección 5.2). No se edita lo archivado.
4. **`decisiones.md`:** cada decisión técnica relevante como RDA numerada. `RDA-001` registra el nivel de proceso del proyecto.
5. **`propuestas-documentos-protegidos.md`:** los cambios que los agentes proponen a los documentos protegidos y su estado (sección 4.5).

### 2.2 `10_epicas/`

Una subcarpeta por épica, con nombre descriptivo en ASCII (`epica-01-fundacion/`). Cada una contiene su definición, sus iteraciones y la carpeta `bitacoras/` con las bitácoras de sus iteraciones y la de cierre. Todo lo de una épica queda junto.

Si el proyecto ya tenía código cuando se adoptó esta documentación, existe `epica-00-linea-base/`: describe lo que ya estaba construido, está `Terminada` y no lleva iteraciones ni carpeta de bitácoras. No se modifica; sirve de punto de partida para el backlog y la primera auditoría.

### 2.3 `plantillas/`

Las plantillas de los documentos que se crean durante el proyecto (sección 6). Son protegidas, como este archivo: ningún agente las edita, y un documento nuevo siempre parte de su plantilla.

<!-- PLANTILLA: la sección 2.4 va si el proyecto tiene auditoria-tecnica.md. -->

### 2.4 Auditorías

`00_producto/auditoria-tecnica.md` es el índice: lista las auditorías y lleva la tabla de hallazgos con su estado. Cada auditoría completa vive en `00_producto/auditorias/auditoria-NN.md`.

<!-- PLANTILLA: la sección 2.5 va solo si el proyecto usa especificaciones (nivel mediano o complejo). -->

### 2.5 `20_especificaciones/`

Una especificación por funcionalidad que tiene lógica, reglas de negocio, varios caminos posibles o endpoints de API. Describe cómo debe comportarse el producto, no cuándo se construyó: varias iteraciones pueden implementar o cambiar la misma especificación.

<!-- PLANTILLA: la sección 2.6 va solo si el proyecto expone una API REST con contrato OpenAPI. -->

### 2.6 Fuera de esta carpeta: `docs/api/openapi.yaml`

El contrato técnico de la API REST: endpoints, métodos, parámetros, modelos de solicitud y respuesta, códigos HTTP, errores y seguridad. Vive fuera de `_planificacion/` porque también lo usan herramientas. Las especificaciones lo citan por `operationId` y no copian sus esquemas.

## 3. Convenciones

- **Numeración:** épicas `01`–`99`; iteraciones `XX-YY`, donde `XX` es la épica e `YY` el correlativo.
- **Nombres de archivo y carpeta:** minúsculas, guiones y solo caracteres ASCII, sin tildes ni ñ (`epica-02-sistema-diseno/`). El contenido sí lleva tildes y ñ.
- **Documentos permitidos:** solo existen los archivos `.md` de `.claude/hooks/documentos-permitidos.md` (sección 5.1).
- **Iteraciones:** `iteracion-XX-YY-descripcion-corta.md`.
- **Tamaño máximo de una iteración:** un solo objetivo, un resultado que el desarrollador revisa en unos 30 minutos y **8 tareas como máximo**. Una iteración que se pasa se parte en dos o más antes de empezar, cada una con su propio objetivo y sus criterios.
- **Detalle de las iteraciones:** al arrancar el proyecto se escriben en detalle solo las iteraciones de la primera épica; las de las demás épicas quedan nombradas en la tabla de su definición. Las iteraciones de cada épica siguiente se generan todas juntas al cerrar la anterior (sección 4.4).
- **Especificaciones:** `spec-nombre-de-la-funcionalidad.md`. Criterios de aceptación con ID corto (`CA-01`), que las iteraciones citan.
- **Bitácoras:** en `10_epicas/epica-XX-nombre/bitacoras/`. `bitacora-XX-YY.md` para la primera de la iteración; las siguientes llevan un sufijo descriptivo (`bitacora-XX-YY-correccion.md`, `bitacora-XX-YY-produccion.md`) y, si el sufijo se repite, un número (`bitacora-XX-YY-ajustes-2.md`). La de cierre es `bitacora-XX-cierre.md`. La fecha va dentro del archivo, no en el nombre.
- **Estados de trabajo:** `Pendiente`, `En curso`, `Bloqueada`, `En revisión`, `Terminada`, `Descartada`.
- **Estados de una especificación:** `Borrador`, `Aprobada`, `Vigente`, `Reemplazada`.
- **Fechas:** formato ISO `AAAA-MM-DD`, {{ZONA_HORARIA}}.
- **Idioma:** {{IDIOMA_Y_VARIANTE}} en toda la documentación.
- **Ramas:** {{CONVENCION_DE_RAMAS}}
- **Commits:** `Épica N - Iteración NN-NN: descripción`, `Épica N - Cierre: descripción` al cerrar una épica, o `Corrección: descripción` fuera de iteración; una línea de máximo 200 caracteres. Los hace solo el desarrollador.
- **Marcadores de datos faltantes:** `PENDIENTE_CLIENTE` (datos del negocio) y `PENDIENTE_DESARROLLADOR` (decisiones técnicas o de diseño). Todo marcador se registra en `registro-pendientes.md`.

## 4. Ciclos de trabajo

### 4.1 Una iteración

Una iteración es una unidad de trabajo que se puede revisar de una vez: una sesión, un hito o un bloque funcional. No tiene duración fija. En Claude Code, el atajo es `/iteracion XX-YY`.

1. El desarrollador marca la iteración como `En curso` en `registro-pendientes.md` (o pide al agente que lo haga).
2. El agente lee `AGENTS.md`, el registro, la iteración, su especificación, el contrato si toca la API y las RDA relacionadas.
3. El agente comprueba la **definición de preparada** de `AGENTS.md`: objetivo claro, criterios verificables, especificación `Aprobada` si la tiene, dependencias terminadas, datos del cliente disponibles y tamaño dentro del máximo. Si algo falla, no empieza: avisa qué falta y propone cómo resolverlo (pedir la aprobación, registrar el dato pendiente, partir la iteración).
4. El agente ejecuta **la iteración completa**: sigue el plan técnico y las tareas aplicando los estándares de calidad de `AGENTS.md`, implementa, verifica según la definición de terminado, incluso contra producción si tiene cómo, y escribe la bitácora con su revisión en la carpeta `bitacoras/` de la épica.
5. Solo si no pudo obtener un dato de producción después de intentarlo por todos los medios, completa la sección «Evidencia del desarrollador» de la iteración (sección 5.5).
6. El agente actualiza el registro (estado, backlog, historial) y, si corresponde, la especificación (a `Vigente` cuando se cumplen todos sus criterios), las RDA y las auditorías.
7. El agente deja la iteración en `En revisión` y propone el mensaje de commit.
8. Si es la última iteración de su épica, el agente sigue con el cierre de la épica y la propuesta de la siguiente (sección 4.4), en la misma entrega.
9. El desarrollador revisa, hace commit y push, y marca la iteración como `Terminada`.

### 4.2 Una funcionalidad nueva

1. Se agrega al backlog con su prioridad.
2. Cuando se acerca su turno, si la funcionalidad lo justifica, el agente redacta su especificación en `Borrador` y, si expone endpoints, los agrega al contrato. Si no lo justifica, basta con el objetivo y los criterios de la iteración.
3. El desarrollador aprueba la especificación (`Aprobada`).
4. Se crea la iteración que la implementa, con plan técnico, tareas y los criterios que cita.
5. Se sigue el ciclo de la sección 4.1.

### 4.3 Un cambio o una corrección

1. **Entender** el pedido. Si es un error, reproducirlo antes de corregirlo.
2. **Identificar** las funcionalidades, componentes y documentos afectados.
3. **Clasificar** con una pregunta: ¿después del cambio, la especificación, el contrato y las RDA siguen describiendo bien el sistema?
   - **Menor (sí):** el código no cumplía lo especificado, un texto, un ajuste dentro de `DESIGN.md`. No se toca la especificación. Fila de tipo `Corrección` en el backlog, implementación, verificación contra los criterios existentes y una línea de historial. Bitácora breve solo si hubo mediciones o decisiones que conviene conservar.
   - **Significativo (no):** cambia el comportamiento esperado, una regla de negocio, el contrato, el modelo de datos o la arquitectura. Primero se actualiza la especificación (vuelve a `Borrador` hasta que el desarrollador la aprueba) o el contrato, o se propone una RDA; si afecta un documento protegido, se registra la propuesta (sección 4.5). Después se trabaja como una iteración, con plan, tareas y bitácora.
   - **Ante la duda,** se pregunta antes de tocar el código.
4. **Actualizar** solo los documentos afectados.
5. **Implementar, verificar y registrar.** Una corrección que no pertenece a la iteración activa usa la rama `correccion/descripcion-corta` (si el proyecto trabaja con ramas) y el commit `Corrección: descripción`.

### 4.4 Cierre de una épica y planificación de la siguiente

Se activa en dos casos: como paso final de la última iteración de una épica, o cuando el desarrollador lo pide («planifica la siguiente épica», o el comando `/siguiente-epica` en Claude Code). Si la épica todavía tiene iteraciones sin terminar, el agente lo dice y no la cierra.

1. **Bitácora de cierre.** El agente escribe `bitacoras/bitacora-XX-cierre.md` con la plantilla `plantillas/bitacora-cierre.md`: criterio de término comprobado con evidencia, hallazgos abiertos, decisiones del desarrollador y revisión al cierre (resultado, qué se aprendió y qué cambia en el backlog o en las épicas siguientes). En la definición de la épica solo enlaza ese archivo. Si la revisión cambia algo, lo aplica en el registro en la misma pasada; si justifica cambiar un documento protegido, registra la propuesta (sección 4.5).
2. **Lectura.** Lee `AGENTS.md`, `README.md`, `DESIGN.md` si existe, la definición de la épica siguiente, el backlog, las especificaciones relacionadas y las RDA vigentes.
3. **Revisión como experto.** Antes de proponer, revisa cada iteración como un desarrollador senior experto en el stack de `AGENTS.md`, contra sus «Estándares de calidad»: responsabilidades y patrones adecuados, pruebas, seguridad, deuda técnica heredada y **sin sobreingeniería** (un patrón, una capa o una dependencia solo si resuelven un problema real del proyecto).
4. **Propuesta.** Presenta en el chat las iteraciones de la épica siguiente: número, nombre y objetivo en una línea, elementos del backlog que cubre y qué especificación o dato del cliente necesita cada una, más una sección «Revisión técnica del experto» con lo que ajustó y por qué. Toda iteración respeta el tamaño máximo (sección 3); la que no cabe ya viene partida en la propuesta.
5. **Iteraciones que ya existen.** Si la épica siguiente ya tiene iteraciones escritas en detalle, no se rehacen: el agente las revisa contra la revisión al cierre y propone ajustes solo si algo cambió. Si nada cambió, lo dice.
6. **Aprobación.** El agente espera la aprobación del desarrollador. Si este ajusta la lista, el agente la corrige.
7. **Generación.** Con la aprobación, el agente genera de una vez todos los archivos de iteración de la épica siguiente con `plantillas/iteracion.md`, y en la misma pasada actualiza la tabla de iteraciones de la definición de la épica, el registro (las filas de la épica cerrada pasan a `registro-archivo.md` y la épica queda en «Épicas cerradas»; las iteraciones nuevas entran a la tabla de estado y al backlog) y una línea de historial.
8. **Preparación.** El agente revisa cada iteración generada contra la definición de preparada de `AGENTS.md`. Lo que falta por causas externas (una especificación por aprobar, un dato del cliente) se registra en «Decisiones por tomar» o «Datos pendientes del cliente», y la iteración queda `Pendiente` hasta que se resuelva.

Si no hay épica siguiente, el agente revisa el backlog: si quedan elementos comprometidos, propone una épica nueva con su definición; si no, lo dice para que el desarrollador cierre el proyecto o lo pase a mantenimiento.

### 4.5 Una propuesta de cambio a un documento protegido

Los documentos protegidos (`AGENTS.md`, `DESIGN.md`, `README.md`, este archivo, `plantillas/` y `.claude/`) no los edita ningún agente.

1. Si el archivo no existe, el agente crea `00_producto/propuestas-documentos-protegidos.md` con su plantilla.
2. Agrega la propuesta con el siguiente número (`P-001`, `P-002`…): documento, sección, por qué, el texto actual copiado literalmente y el texto propuesto, y su fila `Pendiente` en la tabla de estado.
3. Avisa al desarrollador en la entrega. Las bitácoras enlazan la propuesta; no la repiten.
4. El desarrollador la aplica o la descarta y cambia su estado con la fecha.

<!-- PLANTILLA: la sección 4.6 va si el proyecto tiene auditoria-tecnica.md. -->

### 4.6 Auditoría de una épica

Antes de cerrar una épica (o cuando el desarrollador lo pide, con `/auditar-epica` en Claude Code), conviene una auditoría hecha en una sesión nueva, sin el contexto de quien construyó la épica.

1. El auditor lee las fuentes de verdad (iteraciones, bitácoras, RDA, especificaciones, `AGENTS.md`, `DESIGN.md`) y **comprueba con mediciones reales**, no con lo que dicen las bitácoras, cada criterio marcado como cumplido.
2. Revisa los estándares de calidad, la deuda técnica, la conformidad con `DESIGN.md` y `AGENTS.md`, y los archivos `.md` que no estén en la lista de documentos permitidos.
3. Escribe `00_producto/auditorias/auditoria-NN.md` con `plantillas/auditoria.md` y agrega sus hallazgos al índice de `auditoria-tecnica.md`.
4. No corrige nada durante la auditoría. Los hallazgos Altos y Medios entran al backlog y el desarrollador decide qué se corrige antes del cierre.

## 5. Reglas de mantenimiento

### 5.1 Documentos permitidos

- Solo existen los archivos `.md` de `.claude/hooks/documentos-permitidos.md`, resumidos en la sección «Documentos permitidos» de `AGENTS.md`. Ningún agente crea otro: ni registros de prompts, ni notas de sesión, ni borradores, ni resúmenes.
- Si un agente cree que falta un documento, lo propone en «Propuestas fuera de alcance» del registro. Para aprobarlo, el desarrollador agrega su patrón a la lista y a `AGENTS.md`.
- Un documento nuevo siempre parte de su plantilla de `plantillas/`.

### 5.2 Registro de pendientes y backlog

- El backlog dice **qué** falta y en qué orden; la tabla de estado dice **cómo va** cada iteración. Un elemento asignado a una iteración muestra su número, y al cerrar la iteración se actualizan en la misma pasada su fila y las del backlog que cubrió.
- Los elementos del backlog no llevan IDs, puntos ni estimaciones. Los terminados se quedan al final de la tabla con estado `Terminada` hasta que su épica se cierra.
- Una propuesta fuera de alcance que se aprueba se mueve al backlog, con una fila de historial.
- El historial lleva **una fila por cambio y una sola línea**, con enlace a la bitácora que tiene el detalle. Las mediciones, decisiones y salvedades van en la bitácora, no en el historial.
- Cada campo del encabezado ocupa una sola línea.
- Nada se borra. Si un cambio anterior queda sin efecto, se agrega una fila nueva que lo dice.
- La tabla de estado enlaza todas las bitácoras de cada iteración.
- **Para que no crezca sin control:** al cerrar una épica, sus filas de la tabla de estado y sus elementos terminados del backlog pasan a `registro-archivo.md` (creado con un encabezado y las mismas tablas), y la épica queda resumida en «Épicas cerradas». Cuando el historial pasa de 50 filas, las más antiguas también pasan al archivo. Lo archivado no se edita.

### 5.3 Decisiones (RDA)

- Numeración correlativa: `RDA-001`, `RDA-002`… Antes de crear una, revisa el último número usado.
- Una RDA aceptada no se contradice: se reemplaza con una nueva que la declare «Reemplazada por RDA-XXX» (o «Reemplazada parcialmente»), y la antigua recibe una línea que remite a la nueva.
- Las actualizaciones van al final de la RDA como «**Actualización AAAA-MM-DD:** …», breves. Si una RDA acumula varias actualizaciones de fondo, se reemplaza con una nueva.
- La tabla índice del inicio del archivo se mantiene al día.
- Un cambio de nivel de proceso se registra como una RDA nueva que reemplaza a `RDA-001` (o a la que la haya reemplazado).

### 5.4 Bitácoras

- Se escriben al terminar cada tramo de trabajo, con `plantillas/bitacora.md`, en la carpeta `bitacoras/` de la épica.
- No se editan después de entregadas: las correcciones van en una bitácora nueva con sufijo.
- Registran mediciones reales. «Verificado» sin decir cómo y dónde no cuenta.
- Una casilla de criterio se marca solo si se midió.
- Las secciones opcionales de la plantilla (migraciones, diferencias con lo planificado, lo que no se pudo verificar, revisión manual, despliegue) se usan cuando aplican y se borran cuando no.
- Terminan con una revisión breve: resultado frente al objetivo, qué se aprendió y qué cambia para lo que sigue. Si cambia algo (el backlog, una especificación, el orden de las iteraciones), se aplica en la misma pasada.
- Son breves: las salidas largas de comandos no se pegan, se resume la medición que importa.

### 5.5 Evidencia del desarrollador

**Por defecto, una iteración se ejecuta completa.** El agente resuelve todo por su cuenta, incluidas las verificaciones en producción que pueda hacer con las herramientas que tiene permitidas.

Pedir datos al desarrollador es **la excepción**, porque cada pedido le suma trabajo. Solo corresponde cuando se cumplen las dos condiciones:

1. El trabajo exige contrastar lo hecho en local con información de producción (un panel de un servicio externo, una medición en un dispositivo real, una cuenta a la que el agente no tiene acceso).
2. El agente intentó obtener esa información por todos los medios a su alcance y no pudo.

En ese caso, el agente:

1. Termina y registra en la bitácora todo lo que sí pudo hacer.
2. Completa la sección **«Evidencia del desarrollador»** del archivo de la iteración: fecha y hora de las pruebas, commit desplegado, **qué intentó y por qué no pudo** (sin eso el pedido no es válido), qué dato necesita, para qué criterio y los pasos exactos para obtenerlo con el menor esfuerzo.
3. Deja la iteración en `En revisión` y avisa.
4. Cuando el desarrollador responde en esa sección, consolida en una bitácora nueva (`bitacora-XX-YY-produccion.md`).

No se crean archivos de evidencia aparte.

<!-- PLANTILLA: la sección 5.6 va si el proyecto tiene auditoria-tecnica.md. -->

### 5.6 Auditorías

- Cada auditoría completa vive en `00_producto/auditorias/auditoria-NN.md` y no se edita después de entregada.
- **Antes de agregar una auditoría, busca el último número del índice de `auditoria-tecnica.md` y suma uno.** Los IDs de hallazgo tienen el formato `AUD-NN-MMM` (auditoría y correlativo) y nunca se reutilizan.
- El estado de los hallazgos se actualiza solo en la tabla del índice. Un hallazgo se cierra indicando dónde: «Resuelto en XX-YY» o «Resuelto en RDA-XXX», con la evidencia mínima. «Riesgo aceptado» solo si el desarrollador lo aceptó y consta dónde.
- Severidad: Alta (bloquea la publicación o afecta al usuario o al negocio), Media (afecta calidad o rendimiento), Baja (mejora).

<!-- PLANTILLA: la sección 5.7 va solo si el proyecto usa especificaciones. -->

### 5.7 Especificaciones

- Nacen en `Borrador`. El agente puede redactarlas; el desarrollador las aprueba. Nada se implementa desde una especificación en `Borrador`.
- Pasan a `Vigente` cuando la implementación cumple todos sus criterios, y vuelven a `Borrador` si un cambio significativo las modifica.
- Describen el comportamiento actual, sin tabla de historial: la trazabilidad está en las bitácoras y en el registro.
- Las secciones que no aportan se borran. Lo mínimo es problema, comportamiento esperado y criterios de aceptación.
- Una funcionalidad rehecha de raíz deja la especificación antigua en `Reemplazada`, con enlace a la nueva.

<!-- PLANTILLA: la sección 5.8 va solo si el proyecto expone una API REST con contrato OpenAPI. -->

### 5.8 Contrato de la API

- El contrato cambia antes que el código. Si una tarea cambia una ruta, primero se actualiza `docs/api/openapi.yaml` y después se implementa.
- Cada endpoint nuevo o modificado se ejercita contra sus criterios con peticiones reproducibles: el caso exitoso, al menos un error de validación y el acceso sin autorización si la ruta está protegida. La bitácora registra cuáles se ejecutaron y su resultado.
- Si el contrato y el código no coinciden, el agente se detiene y pregunta cuál de los dos está bien.

<!-- PLANTILLA: la sección 5.9 va solo si el proyecto usa la línea base de producción. -->

### 5.9 Línea base de producción

- Toda corrección u optimización que promete una mejora medible se compara contra las cifras de `00_producto/linea-base-produccion.md`.
- Cada cifra lleva fecha y fuente, y nunca datos personales. Una cifra nueva se agrega con su fecha; la anterior no se borra.

## 6. Plantillas

Todo documento que se repite parte de su plantilla en `plantillas/`. Las notas en bloque de cita (`>`) de cada plantilla explican cuándo usar una sección opcional y se borran al escribir el documento.

| Plantilla | Para qué | Dónde se guarda |
| :-------- | :------- | :-------------- |
| `iteracion.md` | Una iteración | `10_epicas/epica-XX-nombre/iteracion-XX-YY-descripcion.md` |
| `definicion-epica.md` | Una épica nueva | `10_epicas/epica-XX-nombre/definicion-epica-XX.md` |
| `bitacora.md` | Lo que pasó en un tramo de trabajo | `10_epicas/epica-XX-nombre/bitacoras/bitacora-XX-YY.md` |
| `bitacora-cierre.md` | El cierre de una épica | `10_epicas/epica-XX-nombre/bitacoras/bitacora-XX-cierre.md` |
| `rda.md` | Una decisión técnica | Al final de `00_producto/decisiones.md` |
| `propuestas-documentos-protegidos.md` | El archivo de propuestas, al crear la primera | `00_producto/propuestas-documentos-protegidos.md` |
| `auditoria.md` | Una auditoría | `00_producto/auditorias/auditoria-NN.md` |
| `especificacion.md` | El comportamiento esperado de una funcionalidad | `20_especificaciones/spec-funcionalidad.md` |
| `linea-base-produccion.md` | Las cifras de producción | `00_producto/linea-base-produccion.md` |
