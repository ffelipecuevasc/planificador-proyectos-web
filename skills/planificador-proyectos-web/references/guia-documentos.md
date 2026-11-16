# Guía documento por documento

Qué lleva cada archivo, qué no lleva y por qué. Las plantillas correspondientes están en `assets/plantillas/`.

## Índice

1. AGENTS.md
2. DESIGN.md
3. README.md (raíz)
4. .claude/: permisos, hooks, comandos y README
5. _planificacion/README.md
6. 00_producto/producto.md
7. 00_producto/registro-pendientes.md
8. 00_producto/decisiones.md
9. Auditorías: auditoria-tecnica.md y auditorias/
10. Épicas: definicion-epica-XX.md
11. Iteraciones: iteracion-XX-YY-descripcion.md
12. Bitácoras y bitácora de cierre
13. Evidencia del desarrollador
14. Especificaciones: spec-funcionalidad.md
15. Contrato de la API: docs/api/openapi.yaml
16. Cambios y correcciones: qué documentos se tocan
17. Proyecto con código existente: épica 00 y auditoría inicial
18. Propuestas a documentos protegidos
19. Línea base de producción
20. Documentos permitidos
21. Plantillas internas: _planificacion/plantillas/
22. Migrar un proyecto con la estructura anterior

---

## 1. AGENTS.md

Es la entrada principal para cualquier agente de IA (Claude Code lo lee de forma nativa desde su versión 2.1.277; también Antigravity y Codex). No se genera `CLAUDE.md`.

Ojo con una trampa de Claude Code: si en la carpeta del proyecto o más arriba existe un `CLAUDE.md` o un `CLAUDE.local.md`, en el modo por defecto Claude Code lee ese archivo y **deja de cargar `AGENTS.md`**. Por eso `.claude/README.md` lo advierte, y quien necesite instrucciones personales debe importar las reglas del proyecto con una primera línea `@AGENTS.md` en su `CLAUDE.local.md`.

**Lleva, en este orden:**

1. **Contexto en 30 segundos**: cliente (o «proyecto propio»), objetivo, alcance, desarrollador responsable. Corto: el agente lo lee en cada sesión.
2. **Documentos protegidos**: `AGENTS.md`, `DESIGN.md`, `README.md`, `_planificacion/README.md`, `_planificacion/plantillas/` y `.claude/` no se editan. Si el agente cree que conviene cambiarlos, registra la propuesta en `propuestas-documentos-protegidos.md` (sección 18 de esta guía). Esto va arriba y explícito, porque un agente que «mejora» las reglas por su cuenta deja de seguirlas.
3. **Documentos permitidos**: la tabla que genera `scripts/preparar_claude.py` en el marcador `{{TABLA_DOCUMENTOS_PERMITIDOS}}` y la prohibición explícita de crear otros `.md` (registros de prompts, notas, borradores). `{{CARPETAS_DE_CONTENIDO}}` nombra las carpetas de contenido en `.md` que no son documentación (por ejemplo `src/content/` en Astro); si no hay, se borra el marcador. Detalle en la sección 20.
4. **Orden de lectura obligatorio**: `registro-pendientes.md` (backlog, qué está pendiente y cuál es la iteración activa), la iteración activa, su especificación y el contrato OpenAPI si los tiene, `decisiones.md`, `DESIGN.md`, `README.md` (raíz), `_planificacion/README.md` y el resto de `_planificacion/` según la tarea. Si algo está en conflicto, el agente se detiene y pregunta.
5. **Stack y versiones**, con las restricciones que no se deducen de los archivos (por ejemplo «no actualices TypeScript a la 7: rompe `astro check`»).
6. **Comandos**: aquí y solo aquí. El README raíz no lleva comandos.
7. **Límites de actuación** en tres grupos: prohibido, requiere consulta, permitido sin consulta. Coherentes con `.claude/settings.json` y los hooks. La regla de ramas sale de la convención acordada: por defecto, ramas por iteración (`{{REGLA_DE_RAMAS}}`: «Crear o cambiar de rama. Propón el nombre con el formato `iteracion/XX-YY-descripcion-corta`…»); solo si el desarrollador lo pide explícitamente, rama única `main` con etiqueta antes de cada despliegue, registrada como RDA.
8. **Reglas de contenido**: idioma, no inventar datos ni resultados, marcadores de pendientes.
9. **Reglas técnicas** del tipo de proyecto (ver `tipos-proyecto.md`).
10. **Estándares de calidad**: los generales de la plantilla (responsabilidad única, sin duplicación, validación y secretos, pruebas, sin sobreingeniería) y los del stack, desde la ficha de `stacks.md`. `{{STACK_EXPERTO}}` nombra el ecosistema del que el agente debe actuar como desarrollador senior.
11. **Flujo de trabajo por iteración**: leer, comprobar que la especificación esté aprobada, proponer rama (`{{PASO_DE_RAMA}}`: «Propón el nombre de la rama de la iteración y espera aprobación antes de crearla», o con rama única «Trabaja en `main`: el proyecto no usa ramas por iteración»), implementar con los estándares, verificar, escribir la bitácora con su revisión, actualizar el registro, entregar el resumen y el commit sugerido. Incluye la regla de autonomía de la sección 13 de esta guía y, como último paso, el cierre de la épica y la propuesta de la siguiente (sección 10).
12. **Cambios y correcciones**: el flujo corto de la sección 16 de esta guía.
13. **Definición de preparada y de terminado.** La **preparada** es la lista de chequeo antes de empezar una iteración: objetivo en una o dos frases, criterios verificables, especificación `Aprobada` si la tiene, dependencias terminadas, datos del cliente disponibles (o acuerdo de trabajar con el marcador) y tamaño dentro del máximo (sección 11 de esta guía). Si falla una condición, el agente no empieza y dice qué falta. La **de terminado** son tres a cinco condiciones que valen para todo trabajo (compilación si aplica, la aplicación se ejecuta, criterios comprobados con evidencia, documentos afectados al día, bitácora o línea de historial), más los comandos que el desarrollador declaró obligatorios. Aparte, en una lista separada, las verificaciones **recomendadas**: se escriben como recomendación y el agente no las presenta como requisito. No se confunde con los criterios de aceptación, que son de cada funcionalidad o iteración.
14. **Cuándo detenerse y preguntar**, incluido cuando una tarea introduce un factor que cambia la complejidad del proyecto o cuando haría falta un documento que no está en la lista.
15. **Convenciones de la API**, solo en backend y fullstack: reglas generales y dónde está el contrato, no el detalle de cada ruta. Va al final para que borrarla en un frontend no cambie los números que citan las demás secciones.

**No lleva:** historial, fechas, iteraciones ni RDA como justificación (es inmutable). Las excepciones a una regla se escriben como parte de la regla, con su razón técnica. Conviene que no pase de unas 220 líneas: es lo que el agente carga en cada sesión.

## 2. DESIGN.md

Fuente única de verdad del diseño. Solo en frontend y fullstack.

**Lleva:** concepto visual y principios; color (tokens, uso y tabla de contrastes medidos, con la regla práctica que sale de ella); tipografía y escala; espaciado, retícula y forma; componentes con sus reglas; botones; iconografía; imágenes; movimiento; implementación de los tokens en el stack; voz y textos.

**Reglas al escribirlo:**

- Valores concretos y medibles (hex, px, rem, ratios), no adjetivos. «Contraste suficiente» no le sirve a un agente; «6,09:1, usar en botones» sí.
- Cada excepción vive dentro de la regla a la que pertenece, con su razón técnica, sin fecha ni iteración. En vez de «Excepciones (iteración 04-04, decisiones del 2026-10-02): …», escribe en la sección de botones: «Los botones de la barra móvil llegan a los bordes de la pantalla: su anillo de foco se dibuja hacia adentro».
- Si el diseño no está definido, no lo inventes: propónlo en el chat, espera aprobación y recién entonces escríbelo. Lo que quede sin decidir va con `PENDIENTE_DESARROLLADOR` en su sección y se registra en `registro-pendientes.md`.
- Al optimizar un `DESIGN.md` existente: consolida, elimina rastros de tiempo, quita duplicados con `AGENTS.md` (las reglas técnicas generales van allá; las de diseño, aquí) y explica en el chat qué cambió.
- **Optimizar no es completar.** Las secciones de la plantilla que el documento original no cubría quedan con `PENDIENTE_DESARROLLADOR`, no con valores que parezcan razonables. Sugerencias, solo en el chat. Si un valor existente rompe una regla (contraste, objetivos táctiles), se escribe la restricción que lo neutraliza, se mide y documenta el problema en la tabla de contraste o en la auditoría, y el cambio de valor queda como decisión pendiente del desarrollador.
- Recorre al final el documento optimizado y compara cada valor concreto (hex, px, nombres de familias, librerías, umbrales) contra el original: todo valor nuevo que no venga del original, del desarrollador o de una norma citada sobra.
- **En nivel pequeño**, versión breve: concepto, color con su tabla de contraste, tipografía, componentes clave con sus reglas y voz. Las secciones que el proyecto no necesita (escala tipográfica detallada, movimiento, iconografía) se omiten en vez de quedar con `PENDIENTE_DESARROLLADOR`; si después hacen falta, el desarrollador las agrega.

## 3. README.md (raíz)

La vitrina del repositorio en GitHub. Sus lectores llegan sin contexto (personas que evalúan tu trabajo, colegas, estudiantes), así que se explica de forma conceptual y ordenada.

**Lleva:** qué es el proyecto y para quién; qué problema resuelve; secciones o funciones principales; stack con una frase por pieza explicando para qué sirve; arquitectura explicada en palabras; estructura del repositorio (se permite un árbol de carpetas en un bloque `text`, porque no es código ni comandos); cómo se despliega, en concepto; metodología de trabajo (backlog, épicas, iteraciones, especificaciones y contrato de la API si el proyecto los usa, RDA, bitácoras, agentes de IA y quién hace los commits); autoría y licencia (en un proyecto propio, sin cliente).

**No lleva:** código fuente, comandos (ni de instalación ni de uso), historial, fechas, iteraciones ni estados («aún no existe», «se publica en…»). Si un estudiante quiere ejecutar el proyecto, el README le dice en palabras qué necesita (por ejemplo «Node.js 24 y PNPM») y que los comandos están en `AGENTS.md`.

**Por qué**: un README con comandos se desactualiza en cuanto cambia el gestor de paquetes, y el que tiene fechas parece abandonado a los seis meses. El README conceptual dura lo que dura el proyecto.

## 4. .claude/: permisos, hooks, comandos y README

Toda la carpeta se prepara con `scripts/preparar_claude.py` (ver `stacks.md`, sección 6) y no a mano, para que los permisos, los hooks, la lista de documentos y su explicación salgan de una sola fuente. En el entregable queda:

- **`settings.json`**: JSON limpio, sin comentarios (JSON no los admite y el archivo dejaría de cargarse) y sin claves inventadas para comentar (generan advertencias de esquema). Tres bloques, `allow`, `ask` y `deny`, agrupados por tema en un orden fijo: comandos del proyecto, Git, sistema, edición, lectura, web. Los documentos protegidos van en `deny` de edición, no en `ask`, porque el desarrollador decidió que ningún agente los edite. La edición sin consulta de `_planificacion/` se limita a los patrones de la lista de documentos permitidos: un archivo con otro nombre hace que Claude Code pregunte. Incluye el registro de los dos hooks.
- **`hooks/proteger-secretos.sh`**: bloquea la lectura, búsqueda y edición de archivos con secretos, también desde Bash y PowerShell. `.env.example` y los demás archivos de ejemplo quedan legibles.
- **`hooks/restringir-documentos.sh`**: bloquea la creación de archivos `.md` fuera de la lista, en las zonas de documentación. No bloquea la edición de archivos que ya existen.
- **`hooks/documentos-permitidos.md`**: la lista cerrada (sección 20), solo con los patrones de los componentes activos.
- **`commands/`**: `/siguiente-epica` y `/iteracion` siempre, y `/auditar-epica` si el proyecto tiene auditorías. Son atajos cortos que remiten a los flujos de `_planificacion/README.md`: el flujo completo vive allá para que los agentes sin estos atajos hagan lo mismo. `/siguiente-epica` agrega la revisión de las iteraciones como desarrollador senior experto en el stack, contra los estándares de `AGENTS.md`.
- **`README.md`**: explica qué hay en la carpeta, cómo se resuelven las reglas (`deny` gana sobre `ask` y `ask` sobre `allow`; los hooks corren antes y su bloqueo vale en cualquier modo), una tabla «regla · por qué» por bloque generada desde las razones de los fragmentos, los hooks y su prueba rápida, los comandos y los límites de la protección. Es documentación del desarrollador: el agente no lo edita (está dentro de `.claude/`).

**Por qué hooks en shell POSIX:** ningún intérprete está garantizado en todas las máquinas (un proyecto Java puede no tener Python ni Node.js). `sh` existe en macOS y Linux, y en Windows Claude Code ejecuta los hooks con Git Bash, que viene con Git para Windows, una herramienta que el flujo de trabajo ya exige. Los hooks fallan cerrados: ante un error interno, bloquean. Si el proyecto tiene archivos de secretos con otro nombre, se agregan a `es_secreto()` del hook y a `deny` de lectura.

## 5. _planificacion/README.md

Guía de la carpeta, inmutable. Lleva: para qué sirve la carpeta, estructura, contenido de cada subcarpeta, convenciones (numeración, nombres en ASCII, documentos permitidos, estados, fechas, idioma, ramas, commits), los ciclos de trabajo (iteración, funcionalidad nueva, cambio o corrección, cierre de épica, propuestas a documentos protegidos y, si hay auditorías, auditoría de una épica), las reglas de mantenimiento de los documentos vivos (secciones 7 a 20 de esta guía) y una tabla que remite a las plantillas de `_planificacion/plantillas/` (sección 21). Las plantillas ya no se copian dentro de este archivo: así hay una sola fuente y el README se mantiene corto.

`{{CONVENCION_DE_RAMAS}}` se llena con la convención acordada: por defecto «`iteracion/XX-YY-descripcion-corta`, o `correccion/descripcion-corta` para una corrección fuera de iteración. Su creación requiere aprobación del desarrollador»; con rama única, «rama única `main`; el desarrollador crea una etiqueta anotada antes de cada despliegue».

Las reglas de mantenimiento van escritas aquí porque los agentes que trabajan en el proyecto no tienen esta skill: lo que no quede en el repositorio no lo van a seguir.

**Se escribe solo con los componentes activos.** Las secciones de la plantilla que dependen del nivel (especificaciones, auditorías, contrato de la API, línea base de producción) llevan un comentario `<!-- PLANTILLA: … -->`: si el componente no está activo, se borra la sección completa y se renumera; si lo está, se borra solo el comentario. Lo mismo para las líneas del árbol de la sección 1 y las filas de la tabla de plantillas. Un agente que lee reglas de componentes que el proyecto no usa intenta aplicarlas.

## 6. 00_producto/producto.md

Documento vivo que cambia poco. Lleva: datos del documento (cliente, desarrollador, documento base, última revisión), propósito, qué es, qué no es, público objetivo (tabla perfil · situación · qué necesita), condiciones de uso, idioma y tono, indicadores de éxito e hitos comprometidos. «Qué no es» es tan importante como «qué es»: es la sección que el agente consulta cuando una tarea huele a fuera de alcance.

## 7. 00_producto/registro-pendientes.md

Fuente única de verdad del trabajo pendiente: si discrepa con cualquier otro documento de planificación, prevalece. Lleva: encabezado con última actualización, iteración activa, próximo hito y flujo de ramas vigente (cada campo en una línea); estado de las épicas abiertas y sus iteraciones (tabla con enlace a las bitácoras); épicas cerradas; **backlog**; datos pendientes del cliente; decisiones por tomar; propuestas fuera de alcance; historial.

**Backlog:** una tabla ordenada por prioridad con las funcionalidades, mejoras, correcciones y trabajo técnico relevante que el proyecto ya comprometió. Columnas: prioridad (`Alta`, `Media`, `Baja`), elemento (una frase), tipo (`Funcionalidad`, `Mejora`, `Corrección`, `Técnico`), especificación (enlace, si tiene), iteración (si ya está asignada) y estado. No lleva IDs, historias de usuario, puntos ni estimaciones: si un proyecto complejo necesita dependencias entre elementos, se agrega una columna «Depende de» y nada más.

Para que no haya dos fuentes de verdad:

- El backlog dice **qué** falta y en qué orden; la tabla de estado dice **cómo va** cada iteración. Un elemento asignado a una iteración muestra su número, y al cerrar la iteración el agente actualiza en la misma pasada la fila de la iteración y las filas del backlog que cubrió.
- Los elementos terminados se quedan en el backlog con estado `Terminada`, al final de la tabla, hasta que su épica se cierra.
- «Propuestas fuera de alcance» es otra cosa: ideas que nadie comprometió, incluidos los documentos nuevos que un agente crea necesarios. Si el desarrollador (o el cliente) aprueba una, se mueve al backlog y se borra de las propuestas con una fila de historial.
- En nivel pequeño, el backlog puede ser una lista corta con prioridad y estado; las otras columnas se omiten.

**Historial corto:** una fila por cambio, una sola línea, con el enlace a la bitácora que tiene el detalle. Ejemplo: `| 2026-10-06 | Iteración 05-04 en revisión. [Bitácora](../10_epicas/epica-05-publicacion/bitacoras/bitacora-05-04.md) |`. El detalle (mediciones, decisiones, salvedades) va en la bitácora; repetirlo aquí deja un historial de cientos de líneas que nadie lee.

**Contra el crecimiento.** En los proyectos reales del autor de la skill, el registro llegó a superar los 100 KB y cada agente lo leía completo en cada sesión. Por eso:

- Al cerrar una épica, sus filas de la tabla de estado y sus elementos terminados del backlog pasan a `registro-archivo.md` (se crea la primera vez, con un encabezado y las mismas tablas), y la épica queda en «Épicas cerradas» con una fila y el enlace a su bitácora de cierre.
- Cuando el historial pasa de 50 filas, las más antiguas también pasan a `registro-archivo.md`.
- Lo archivado no se edita ni se vuelve a leer en el trabajo diario.

**Reversiones:** nada se borra. Si un cambio anterior queda sin efecto, se agrega una fila nueva que lo dice («La fila del 2026-09-30 que da por terminada la Épica 02 queda sin efecto: …»).

## 8. 00_producto/decisiones.md

Registro de Decisiones Arquitectónicas (RDA): tabla índice (número, título, estado) y una sección por RDA con fecha, estado, contexto, decisión, alternativas consideradas y consecuencias.

- Numeración correlativa sin huecos (`RDA-001`, `RDA-002`…).
- Una RDA aceptada no se contradice: se reemplaza con una nueva que la declare «Reemplazada por RDA-XXX» (o «Reemplazada parcialmente»), y la antigua recibe una línea que remite a la nueva.
- Las actualizaciones de una RDA van como párrafos «**Actualización AAAA-MM-DD:** …» al final de la RDA, breves. Si una RDA acumula más de dos o tres actualizaciones de fondo, conviene una RDA nueva que la reemplace: es más fácil de leer que una cadena de parches.
- Al inicio del proyecto, `RDA-001 · Nivel de proceso` registra el diagnóstico de complejidad acordado: nivel, factores que lo justifican, componentes activos y los que quedaron fuera a propósito. Después, registra como RDA las decisiones estructurales ya tomadas en la entrevista (stack, hosting, fuente de datos, estructura de páginas o de la API), con el estado que corresponda.

## 9. Auditorías: auditoria-tecnica.md y auditorias/

`00_producto/auditoria-tecnica.md` es el **índice**: reglas, tabla de auditorías (número, fecha, título, alcance y enlace) y la tabla de **todos los hallazgos** con su estado. Cada auditoría completa vive en `00_producto/auditorias/auditoria-NN.md`, con la plantilla `auditoria.md`, y no se edita después de entregada. Así, un archivo acumulativo de decenas de kilobytes no se lee completo para saber qué hallazgos siguen abiertos.

- **Numeración**: antes de agregar una auditoría, busca el último número del índice y suma uno. IDs con el formato `AUD-NN-MMM` (número de auditoría y correlativo del hallazgo). Nunca se reutiliza un número.
- **Estado**: se actualiza solo en la tabla del índice. Un hallazgo se marca «Resuelto en XX-YY» o «Resuelto en RDA-XXX», con la evidencia mínima («medido en…»). «Riesgo aceptado» solo si el desarrollador lo aceptó y consta dónde.
- **Severidad**: Alta (bloquea la publicación o afecta al usuario o al negocio), Media (afecta calidad o rendimiento), Baja (mejora).
- **Contenido de cada auditoría**: tabla de metadatos (fecha, auditor, commit auditado, alcance, método y limitaciones), veredicto, qué se implementó bien, verificaciones técnicas con su comando o medición, trazabilidad del plan a la implementación (en la auditoría de una épica), conformidad con `DESIGN.md` y `AGENTS.md` (incluidos los documentos fuera de la lista), hallazgos nuevos y cierre de hallazgos anteriores.
- **Auditoría de una épica**: desde nivel mediano, antes de cerrar cada épica, con `/auditar-epica` en una sesión nueva. Compara cada criterio marcado como cumplido con lo que realmente existe; en los proyectos del autor de la skill, así se encontró deuda técnica en iteraciones que estaban marcadas como cumplidas.
- Al inicio del proyecto, si hay insumos que auditar (prototipo, propuesta, sitio anterior, o código existente según la sección 17), genera la Auditoría 01 y su fila en el índice. Si no los hay, el índice nace solo con el encabezado, las reglas y las tablas vacías, y la carpeta `auditorias/` no se crea hasta la primera auditoría.
- **En nivel pequeño**, el índice no se genera salvo que haya insumos que auditar. Si más adelante se hace una auditoría, se crean el índice y el archivo con sus plantillas.

## 10. Épicas: definicion-epica-XX.md

Carpeta `10_epicas/epica-XX-<nombre-corto>/`, con la plantilla `definicion-epica.md`. La definición lleva: estado, objetivo, alcance, fuera de alcance, tabla de iteraciones (número y nombre), decisiones de la épica (o «Ninguna»), reglas comunes de la épica si las hay, criterio de término verificable (qué se mide para darla por terminada) y un enlace a su bitácora de cierre.

La revisión al cierre ya no se escribe en la definición: vive solo en la **bitácora de cierre** (sección 12), para que haya una sola fuente. La definición solo la enlaza.

**Cierre de épica y planificación de la siguiente.** Al arrancar se detallan solo las iteraciones de la primera épica; las de cada épica siguiente se generan **todas juntas** al cerrar la anterior, para no planificar iteración por iteración. Es el último paso de la última iteración de la épica (y el desarrollador puede pedirlo en cualquier momento con «planifica la siguiente épica» o `/siguiente-epica`):

1. Bitácora de cierre de la épica que termina.
2. Lectura de `AGENTS.md`, `README.md`, `DESIGN.md`, la épica siguiente, el backlog, las especificaciones y las RDA.
3. Revisión de cada iteración como desarrollador senior experto en el stack, contra los «Estándares de calidad» de `AGENTS.md`, incluido el freno a la sobreingeniería.
4. Propuesta en el chat de las iteraciones de la épica siguiente: número, nombre, objetivo en una línea, elementos del backlog que cubre y qué necesita cada una, más la «Revisión técnica del experto». Toda iteración respeta el tamaño máximo (sección 11).
5. Si la épica siguiente ya tenía iteraciones detalladas, no se rehacen: se proponen ajustes solo si la revisión al cierre cambió algo.
6. Con la aprobación del desarrollador, se generan de una vez todos los archivos de iteración y se actualizan la tabla de la épica, el registro (con el archivado de la sección 7) y el backlog.
7. Cada iteración generada se revisa contra la definición de preparada; lo que falte por causas externas se registra como pendiente.

Como los agentes que trabajan en el repositorio no tienen esta skill, el flujo queda escrito en `_planificacion/README.md` (sección 4.4), resumido en el paso final del flujo por iteración de `AGENTS.md` y con el atajo `.claude/commands/siguiente-epica.md` para Claude Code.

## 11. Iteraciones: iteracion-XX-YY-descripcion.md

Nombre con descripción corta en ASCII: `iteracion-01-01-andamiaje.md`, con la plantilla `iteracion.md`. Una unidad de trabajo acotada, sin duración fija: puede ser una sesión, un hito o un bloque funcional, mientras se pueda revisar de una vez.

**Tamaño máximo:** un solo objetivo, un resultado que el desarrollador revisa en unos 30 minutos y **8 tareas como máximo** (las del agente; las «Tareas del desarrollador» van aparte). Si una iteración se pasa, se parte antes de escribirla en detalle, cada parte con su objetivo y sus criterios. No es una estimación (el backlog sigue sin puntos): es la regla para cortar el trabajo en trozos que un agente termina y una persona revisa de una vez. El validador avisa si una iteración tiene más de 8 tareas.

**Nace preparada:** al escribir una iteración, revísala contra la definición de preparada de `AGENTS.md` (sección 1 de esta guía, punto 13). Lo que falte por causas externas se registra como pendiente y queda anotado en la iteración.

**Lleva siempre:** épica, estado, rama sugerida (o «Rama: main» con rama única), dependencias, especificación y criterios que implementa (si tiene), RDA relacionadas, hallazgos que cierra, objetivo, alcance y entregables, tareas, criterios de aceptación verificables (casillas), fuera de alcance y datos requeridos, en dos partes: del cliente y del desarrollador.

**Secciones opcionales**, que se usan cuando aplican y se borran cuando no (salieron de las secciones que más se repetían en las iteraciones reales del autor de la skill):

- **Cambio de esquema** y **Respaldo previo al despliegue**, en la cabecera: solo en proyectos con base de datos en producción.
- **Punto de partida**: en proyectos con código existente, lo que hay hoy y que el agente debe verificar leyendo el código antes de escribir.
- **Contenido aprobado (copiar tal cual)**: textos, datos o imágenes aprobados que se publican literalmente. Una auditoría puede comprobarlos contra lo publicado.
- **Decisiones del desarrollador** ya tomadas que condicionan la implementación.
- **Plan técnico**: cómo se aborda la solución dentro de la arquitectura y las convenciones del proyecto: componentes o módulos que se tocan, cambios en el modelo de datos o en el contrato de la API, estándares de calidad que aplican y riesgos. Se escribe cuando la iteración toca arquitectura, datos, API o integraciones (desde nivel mediano) o siempre (nivel complejo).
- **Tareas del desarrollador**: lo que solo él puede hacer, planificado desde el inicio (configurar un servicio externo, probar en un teléfono).
- **Riesgos** y **Despliegue** (pasos, verificación después de publicar y cómo se revierte).
- **Evidencia del desarrollador**: la agrega el agente durante la ejecución, solo si hace falta (sección 13).

Reglas de escritura:

- **Objetivo:** una o dos frases sobre lo que la iteración deja funcionando. Es lo que se revisa al cerrar.
- **Alcance y entregables:** qué existe al terminar (una página publicada, un endpoint respondiendo, un componente en el sistema de diseño). Sirve para revisar el resultado sin leer el código.
- **Tareas:** concretas, ordenadas y ejecutables por un agente sin preguntar qué significan. En nivel complejo, cada tarea que depende de otra lo dice.
- **Criterios de aceptación:** si la iteración implementa una especificación, se citan sus criterios (`CA-01`, `CA-02`) en vez de copiarlos, y se agregan solo los técnicos propios de la iteración. Si no hay especificación, la iteración trae sus propios criterios, breves.

Un buen criterio de aceptación se puede comprobar con una medición o un comando: «`pnpm build` termina sin errores» sí; «el diseño se ve bien» no. Si hay que medir en producción, el criterio dice qué se mide y dónde.

## 12. Bitácoras y bitácora de cierre

Viven **dentro de la épica**, en `10_epicas/epica-XX-<nombre>/bitacoras/`, para que todo lo de una épica quede junto. La carpeta de la primera épica nace con un `.gitkeep`.

- La primera bitácora de una iteración: `bitacora-01-01.md`, con la plantilla `bitacora.md`.
- Las siguientes de la misma iteración llevan un sufijo descriptivo en ASCII: `bitacora-01-01-correccion.md`, `bitacora-01-01-ajustes.md`, `bitacora-01-01-produccion.md`. Si se repite el sufijo, se numera: `bitacora-01-01-ajustes-2.md`.
- La fecha va dentro del archivo, no en el nombre.
- Se escribe al terminar y no se edita después de entregada: las correcciones van en una bitácora nueva.
- Registra mediciones reales. «Verificado» sin decir cómo no cuenta.
- **Secciones opcionales**: migraciones (solo con cambios de esquema), diferencias entre lo planificado y lo encontrado, lo que no se pudo verificar, revisión manual del desarrollador y despliegue. Se usan cuando aplican y se borran cuando no.
- **Breve**: entre 60 y 150 líneas como referencia. Las salidas largas de comandos no se pegan; se resume la medición que importa. En los proyectos del autor de la skill hubo bitácoras de 40 a 90 KB que nadie volvía a leer.
- Termina con una sección **«Revisión»** de dos a cuatro líneas: el resultado frente al objetivo, qué se aprendió y qué cambia para lo que sigue (una fila nueva en el backlog, una especificación que ajustar, una iteración que reordenar). Es la parte útil de una retrospectiva, sin la ceremonia. Si la revisión cambia algo, el agente lo aplica en el registro en la misma pasada.
- En nivel pequeño, la bitácora puede ser breve: resumen, verificación con evidencia, criterios y una o dos líneas de revisión.

**Bitácora de cierre** (`bitacora-XX-cierre.md`, plantilla `bitacora-cierre.md`): se escribe al cerrar la épica y es la única fuente de la revisión al cierre. Lleva resumen, tabla de iteraciones con sus bitácoras, criterio de término comprobado con evidencia, hallazgos abiertos y qué se decidió con cada uno, decisiones del desarrollador registradas, revisión al cierre, resumen de la propuesta de la épica siguiente y commit sugerido (`Épica N - Cierre: descripción`). En los tres proyectos recientes del autor de la skill este archivo apareció por su cuenta, cada vez con otro nombre: la plantilla fija el nombre y el contenido.

## 13. Evidencia del desarrollador

**Por defecto, una iteración se ejecuta completa.** El agente resuelve todo por su cuenta.

Se le piden datos al desarrollador **solo** cuando el trabajo exige contrastar lo que el agente hace en local con datos de producción **y** el agente, después de intentarlo por todos los medios a su alcance (comandos permitidos, herramientas web, documentación pública, registros del proyecto), no logra obtenerlos. Recién entonces:

1. Termina y registra todo lo que sí pudo hacer, en la bitácora de la iteración.
2. Completa la sección **«Evidencia del desarrollador»** del archivo de la iteración: fecha y hora de las pruebas, commit desplegado, qué intentó para obtener cada dato y por qué no pudo, qué dato necesita, para qué criterio y los pasos exactos para conseguirlo en el menor tiempo posible.
3. Deja la iteración «En revisión» y avisa al desarrollador.
4. Cuando el desarrollador responde en esa sección, el agente consolida en una bitácora nueva con sufijo (`bitacora-XX-YY-produccion.md`).

No se crean archivos de evidencia aparte: la iteración ya tiene dónde explicar cómo se cumplió cada criterio, y un archivo más por pedido es trabajo administrativo sin valor. Pedir evidencia es la excepción, no un paso del proceso, y la tabla «Qué intentó el agente» es obligatoria: sin ella el pedido no es válido.

## 14. Especificaciones: spec-funcionalidad.md

Carpeta `_planificacion/20_especificaciones/`, desde nivel mediano. Una especificación por funcionalidad que la justifique (criterios en `niveles-complejidad.md`, sección 4), con nombre en ASCII: `spec-reserva-de-horas.md`.

**Por qué una carpeta propia y no dentro de la épica:** la especificación describe cómo se comporta el producto, no cuándo se construyó. Una funcionalidad la tocan varias iteraciones de épicas distintas a lo largo del proyecto; si la especificación viviera en la carpeta de la épica donde nació, los cambios posteriores quedarían repartidos. Las iteraciones (lo temporal) apuntan a la especificación (lo vigente). Tampoco se separan `spec.md`, `plan.md` y `tasks.md` por funcionalidad, como hacen otras herramientas de SDD: el plan técnico y las tareas cambian en cada iteración, y la iteración ya es su lugar natural.

**Lleva, según la necesidad** (lo mínimo son problema, comportamiento y criterios; el resto se borra si no aporta):

1. **Estado** (`Borrador`, `Aprobada`, `Vigente`, `Reemplazada`), última revisión e iteraciones que la implementan.
2. **Problema o necesidad** que resuelve, en dos o tres líneas.
3. **Comportamiento esperado**, descrito desde quien usa la funcionalidad.
4. **Requisitos funcionales**, numerados.
5. **Reglas de negocio**, numeradas: cálculos, validaciones, estados, permisos.
6. **Escenarios** relevantes en formato Dado / Cuando / Entonces: el camino principal y los casos borde que cambian el resultado. No todos los imaginables.
7. **Criterios de aceptación** verificables, con ID corto (`CA-01`, `CA-02`) para que las iteraciones los citen.
8. **Restricciones o consideraciones técnicas** que el plan debe respetar.
9. **Contrato de API**, solo si expone o consume endpoints: las operaciones del OpenAPI por su `operationId`, sin copiar esquemas.
10. **Fuera de alcance.**
11. **Preguntas abiertas**, con sus marcadores de pendiente.

**Reglas:**

- Nace en `Borrador`. El agente puede redactarla y proponerla, pero una funcionalidad con especificación no se implementa hasta que el desarrollador la marca `Aprobada`. Cuando la implementación cumple todos sus criterios, pasa a `Vigente`.
- Es un documento vivo: describe el comportamiento actual. Si un cambio altera el comportamiento, la especificación se actualiza **antes** de implementar y vuelve a `Aprobada` cuando el desarrollador revisa el cambio. No lleva tabla de historial: la trazabilidad está en las bitácoras y en el registro.
- Si una funcionalidad se rehace de raíz, la especificación antigua pasa a `Reemplazada` con un enlace a la nueva.

## 15. Contrato de la API: docs/api/openapi.yaml

Solo en backend y fullstack con API REST, obligatorio desde nivel mediano (detalle en `tipos-proyecto.md`, «Contrato de una API REST»). Es la única excepción a «todo en Markdown» junto con `settings.json`.

- Vive en el repositorio fuera de `_planificacion/` porque lo usan herramientas (generadores de tipos, visores, pruebas) y no solo personas.
- Es un documento vivo: el agente lo edita, siempre **antes** que el código de la ruta.
- Al arrancar el proyecto, nace con `info`, `servers`, esquemas de seguridad, el formato de error común y los endpoints ya especificados. Lo que no se sabe se marca con `PENDIENTE_DESARROLLADOR` en la descripción de la operación y se registra en el registro.

## 16. Cambios y correcciones: qué documentos se tocan

El flujo completo queda escrito en `_planificacion/README.md` (sección 4.3) y resumido en `AGENTS.md`. Lo importante para generar esos textos:

| Clase de cambio | Ejemplos | Documentos que se actualizan antes de implementar | Registro al terminar |
| :-------------- | :------- | :------------------------------------------------ | :------------------- |
| **Menor** | Un error en que el código no cumple lo especificado, un texto, un ajuste visual dentro de lo que define `DESIGN.md` | Ninguno | Fila en el backlog (tipo `Corrección`) y una línea de historial. Bitácora breve solo si hubo mediciones o decisiones que conviene conservar |
| **Significativo** | Cambia el comportamiento esperado, una regla de negocio, el contrato de la API, el modelo de datos o la arquitectura | La especificación, el OpenAPI o una RDA, según lo afectado. Si afecta un documento inmutable, propuesta al desarrollador | Iteración con plan y tareas, y bitácora completa |

La pregunta que decide la clase es: **¿después del cambio, la especificación (o el contrato, o la RDA) sigue describiendo bien el sistema?** Si sí, es menor. Si no, es significativo. Ante la duda, el agente pregunta.

Una corrección menor no necesita un archivo de iteración. Si pertenece a la iteración activa, se hace dentro de ella; si no, se trabaja como corrección fuera de iteración, con su rama y su formato de commit.

## 17. Proyecto con código existente: épica 00 y auditoría inicial
18. Propuestas a documentos protegidos
19. Línea base de producción
20. Documentos permitidos
21. Plantillas internas: _planificacion/plantillas/
22. Migrar un proyecto con la estructura anterior

Cuando el proyecto ya tiene código pero no esta documentación, el arranque parte por analizar el código (`proyecto-existente.md`). Además de los documentos de siempre, se generan:

- **`10_epicas/epica-00-linea-base/definicion-epica-00.md`**, desde `assets/linea-base/`: lo que ya existe, con su estado observado o verificado, dónde está en el código y el stack detectado con el archivo del que se dedujo. Nace `Terminada`, no lleva iteraciones ni bitácoras (tampoco carpeta `bitacoras/`) y no se edita después.
- **Auditoría 01** en `auditorias/auditoria-01.md`, con su fila en el índice `auditoria-tecnica.md`, con la revisión inicial del código, aunque el nivel sea pequeño.
- **RDA de las decisiones previas** (stack, hosting, base de datos), en estado `Aceptada`, sin inventar alternativas ni razones que nadie dejó escritas.
- **Backlog** con lo que está a medio hacer y los hallazgos Altos y Medios, además de lo que salga de la entrevista.

Las épicas planificadas empiezan en la 01. La tabla de estado del registro lleva una primera fila para la línea base.

## 18. Propuestas a documentos protegidos

`00_producto/propuestas-documentos-protegidos.md`, con la plantilla del mismo nombre. Se crea con la primera propuesta del proyecto, no al arrancar.

- Es la **única fuente vigente** de propuestas: las bitácoras y las revisiones al cierre la enlazan, no la repiten. En un proyecto del autor de la skill, las propuestas llegaron a estar repartidas entre varias bitácoras y versiones sucesivas, y aplicarlas exigía adivinar cuál valía.
- Lleva una sección «Cómo aplicarlas», una tabla de estado (`P-001`, documento y sección, origen, fecha y estado: `Pendiente`, `Aplicada AAAA-MM-DD` o `Descartada AAAA-MM-DD`) y un bloque por propuesta con documento, sección, por qué, el texto actual **copiado literalmente** y el texto propuesto.
- El agente nunca aplica una propuesta. Si el texto actual cambió antes de aplicarla, la propuesta se rehace.

## 19. Línea base de producción

`00_producto/linea-base-produccion.md`, con su plantilla, solo cuando el proyecto ya está en producción y el trabajo que viene es corregir u optimizar (activado con `--linea-base-produccion`).

- Cifras reales (tiempos, tamaños, volúmenes, errores) con fecha de medición y fuente; **nunca datos personales**, solo conteos, tamaños, fechas y estados.
- Lo que no se pudo medir va con su marcador de pendiente y su fila en el registro; no se estima.
- Toda corrección u optimización que promete una mejora medible se compara contra estas cifras. Una cifra nueva se agrega con su fecha; la anterior no se borra.

## 20. Documentos permitidos

La lista cerrada de archivos `.md` que pueden existir en las zonas de documentación (la raíz, `_planificacion/`, `docs/` y `.claude/`). Existe porque, en un proyecto del autor de la skill, el agente empezó a crear archivos con otros nombres dentro de la carpeta de bitácoras, por ejemplo un registro de los prompts que ejecutaba.

**Una sola fuente**: `.claude/hooks/documentos-permitidos.md`, con un patrón por línea (`*` reemplaza texto dentro de un nivel de carpeta). `scripts/preparar_claude.py` la escribe solo con los componentes activos y, desde ella, genera las reglas de edición de `settings.json` y la tabla de `AGENTS.md`.

**Cuatro capas**, de la más general a la más estricta:

1. **`AGENTS.md`**: la tabla y la prohibición escrita. Es la única capa que leen todos los agentes.
2. **`settings.json`**: la edición sin consulta se limita a los patrones; un nombre distinto hace que Claude Code pregunte.
3. **`restringir-documentos.sh`**: bloquea la creación de un `.md` nuevo fuera de la lista, también con redirecciones y comandos que escriben archivos.
4. **Detección**: el validador de la skill y `/auditar-epica` reportan los `.md` que no calzan con la lista.

Las carpetas de contenido del sitio en `.md` (por ejemplo `src/content/` en Astro) quedan fuera porque no son zonas de documentación; `AGENTS.md` las nombra. Para aprobar un documento nuevo, el desarrollador agrega su patrón a la lista y a la tabla de `AGENTS.md` (y, si vive en `_planificacion/` y debe editarse sin consulta, su regla `Edit(...)`).

## 21. Plantillas internas: _planificacion/plantillas/

Las plantillas de los documentos que se repiten viven en el proyecto, en `_planificacion/plantillas/`, y se copian desde `assets/plantillas/_planificacion/plantillas/`. Son la fuente única: `_planificacion/README.md` solo las enumera en una tabla.

| Plantilla | Se copia | Se usa para |
| :-------- | :------- | :---------- |
| `iteracion.md`, `definicion-epica.md`, `bitacora.md`, `bitacora-cierre.md`, `rda.md`, `propuestas-documentos-protegidos.md` | Siempre | Iteraciones, épicas, bitácoras, cierres, RDA y la primera propuesta |
| `auditoria.md` | Si hay auditorías | Cada auditoría |
| `especificacion.md` | Si hay especificaciones | Cada especificación |
| `linea-base-produccion.md` | Si se activó la línea base | El documento de línea base |

- **Están protegidas** como los documentos inmutables: `deny` de edición en `settings.json` y ningún agente las edita.
- Usan marcadores genéricos (`XX-YY`, `AAAA-MM-DD`, `…`), no `{{…}}`, porque se entregan tal cual.
- Las notas en bloque de cita (`>`) explican cuándo usar cada sección opcional y se borran al escribir el documento. Al copiarlas a un proyecto, borra las secciones opcionales que el proyecto nunca usará (por ejemplo «Contenido aprobado» en un backend sin interfaz, o «Migraciones» y los campos de esquema y respaldo sin base de datos).
- La skill también escribe con ellas los documentos iniciales: la definición de cada épica y las iteraciones de la primera, y las especificaciones de las primeras iteraciones.

## 22. Migrar un proyecto con la estructura anterior

Un proyecto documentado con una versión anterior de esta skill tiene las bitácoras en `_planificacion/99_bitacora/<epica>/`, puede tener archivos `evidencia-XX-YY.md` y no tiene la lista de documentos permitidos, las plantillas internas ni los hooks. En modo evolución, si el desarrollador acepta migrarlo (propónlo una vez, no lo impongas):

1. **Bitácoras:** mueve cada `99_bitacora/epica-XX-nombre/` a `10_epicas/epica-XX-nombre/bitacoras/` con `git mv` (pide aprobación: mover archivos requiere consulta) y borra `99_bitacora/` cuando quede vacía. Si una bitácora tiene un nombre fuera de convención, se conserva tal cual y se registra en la migración; no se renombra lo histórico.
2. **Enlaces:** actualiza las rutas a las bitácoras en `registro-pendientes.md` y en los documentos vivos que las citen. Los documentos inmutables que las citen van como propuesta.
3. **Evidencias:** los archivos `evidencia-XX-YY.md` ya respondidos se dejan como están (son históricos) y se agrega su patrón a la lista; los pedidos nuevos usan la sección de la iteración.
4. **.claude/:** el proyecto ya tiene esa carpeta, así que ejecuta `scripts/preparar_claude.py` con `--simular`, muestra las diferencias y aplica con `--actualizar` (conserva los permisos y hooks propios del proyecto). Un `settings.json` de la versión anterior suele traer `Edit(/.env.*)` y `Read(./.env.*)` en `deny`: la versión actual enumera las variantes de `.env` para que `.env.example` se pueda leer y editar con consulta, así que el script se detiene por conflicto; propón quitar esas dos reglas. Los archivos que el script informa como «CONSERVADO» (el README y los comandos anteriores) se reemplazan borrándolos, con aprobación del desarrollador, y ejecutando `--actualizar` otra vez, que los crea. Revisa la lista generada contra los archivos que ya existen: los documentos históricos que se conservan se agregan a la lista con su patrón, para que el validador no los marque.
5. **Plantillas y registro:** copia `_planificacion/plantillas/`, y aplica el archivado del registro (sección 7) si ya es grande.
6. **Documentos inmutables:** entrega la propuesta de cambios para `AGENTS.md` (documentos permitidos, estándares de calidad, nuevas rutas) y `_planificacion/README.md` (estructura, ciclos y tabla de plantillas), con la versión completa del archivo para que el desarrollador la aplique de una vez.
7. **Registro:** una RDA «Migración a la estructura de documentación vigente» y una línea de historial. Valida con `scripts/validar_documentacion.py` al terminar.
