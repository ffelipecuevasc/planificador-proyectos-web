# Planificador de proyectos web

Una [skill](#14-glosario) para Claude que planifica y documenta proyectos web (sitios, APIs o aplicaciones completas) antes de pedirle a un agente de IA, como Claude Code, que los programe. Deja en tu repositorio lo que el agente necesita para construir bien: qué se construye, con qué reglas, en qué orden y qué se hizo.

Combina dos ideas, aplicadas en la medida que tu proyecto necesita:

- **Especificar antes de programar.** Antes de escribir código se deja por escrito qué debe hacer cada funcionalidad, y al terminar se comprueba que el resultado cumple lo escrito. Esta idea se conoce como *Spec-Driven Development* (SDD).
- **Avanzar en etapas cortas.** Una lista priorizada de lo que falta por hacer, etapas de trabajo con un objetivo claro y una revisión al cerrar cada una para decidir qué sigue. Son prácticas tomadas de Scrum, pero sin sus reuniones ni roles.

> ◆ **Qué no es.** No genera el código de tu proyecto ni te obliga a seguir una metodología formal. Es una herramienta de organización: el proceso solo se vuelve más exigente cuando el proyecto es más grande o más delicado.

---

## Índice

1. [El problema que resuelve](#1-el-problema-que-resuelve)
2. [Inicio rápido](#2-inicio-rápido)
3. [Requisitos](#3-requisitos)
4. [Instalación](#4-instalación)
5. [Uso](#5-uso)
6. [Cómo funciona](#6-cómo-funciona)
7. [Niveles de complejidad](#7-niveles-de-complejidad)
8. [Qué genera](#8-qué-genera)
9. [Trabajar con el agente después de generar](#9-trabajar-con-el-agente-después-de-generar)
10. [El validador](#10-el-validador)
11. [Personalizar la skill](#11-personalizar-la-skill)
12. [Para quienes ya conocen SDD o Scrum](#12-para-quienes-ya-conocen-sdd-o-scrum)
13. [Preguntas frecuentes](#13-preguntas-frecuentes)
14. [Glosario](#14-glosario)
15. [Estructura de este repositorio](#15-estructura-de-este-repositorio)
16. [Licencia y autoría](#16-licencia-y-autoría)

---

## 1. El problema que resuelve

Un agente de IA escribe código más rápido de lo que una persona alcanza a revisar. Si le pides «haz una página de contacto» en una frase, va a decidir por su cuenta todo lo que no dijiste: qué campos lleva el formulario, qué pasa si el envío falla, qué colores usa, si agrega una librería. A veces acierta y a veces no, y cuando abres una sesión nueva ya olvidó lo que habían acordado.

Esta skill ataca ese problema con documentos que viven en tu repositorio y que el agente lee al empezar cada sesión:

- **Reglas estables** (`AGENTS.md`, `DESIGN.md`): cómo se trabaja en este proyecto y qué no se puede hacer.
- **Intención explícita** (lista de pendientes, especificaciones, [criterios de aceptación](#14-glosario)): qué se va a construir y cómo se sabe que quedó bien.
- **Memoria del proyecto** (decisiones, bitácoras, historial): qué se decidió, qué se hizo y cómo se comprobó.

---

## 2. Inicio rápido

Si es tu primera vez, sigue estos pasos y vuelve al resto del documento cuando tengas el resultado en la mano.

1. **Instala la skill** en Claude siguiendo la [sección 4](#4-instalación). Toma un par de minutos.
2. **Abre un chat nuevo** y describe tu proyecto con tus palabras. Por ejemplo:

   > Quiero crear mi CV online con portafolio: un sitio estático en HTML y CSS, publicado en GitHub Pages. Tiene secciones sobre mí, proyectos y contacto. Ayúdame a planificarlo.

3. **Responde las preguntas.** Claude te hará preguntas cortas en bloques. Si no sabes alguna respuesta, dilo: quedará registrada como pendiente y no bloquea el resto.
4. **Confirma el nivel.** Claude te propondrá un nivel de complejidad (pequeño, mediano o complejo) y te explicará por qué. Puedes aceptarlo o cambiarlo.
5. **Descarga el resultado.** Recibirás un archivo `.zip`. Descomprímelo en la carpeta principal de tu proyecto, donde está (o estará) la carpeta `.git`.
6. **Empieza a construir** con el agente siguiendo la [sección 9](#9-trabajar-con-el-agente-después-de-generar).

---

## 3. Requisitos

| Para usarla en | Necesitas |
| :------------- | :-------- |
| Claude (web, escritorio o móvil) | Cualquier plan, incluido el gratuito, con la **ejecución de código activada**. En planes individuales se activa en *Settings → Capabilities*; en Team y Enterprise la activa la organización. |
| Claude Code | Un plan de pago (Pro, Max, Team o Enterprise) o acceso por API. |
| El validador | Python 3. Dentro de Claude ya está disponible; solo lo necesitas instalado en tu computador si quieres ejecutarlo a mano. No requiere librerías adicionales. |

Planes y menús verificados en octubre de 2026 en [support.claude.com](https://support.claude.com/en/articles/12512180-using-skills-with-claude) y [claude.com/pricing](https://claude.com/pricing). Estos productos cambian seguido: si algo no coincide, revisa esas páginas.

---

## 4. Instalación

### En Claude (claude.ai o la app)

1. Descarga [`planificador-proyectos-web.zip`](https://github.com/ffelipecuevasc/planificador-proyectos-web/releases/latest/download/planificador-proyectos-web.zip), que corresponde siempre a la última versión publicada en [Releases](https://github.com/ffelipecuevasc/planificador-proyectos-web/releases). Si no hay ninguna, descarga el repositorio y comprime la carpeta `skills/planificador-proyectos-web/` completa (la carpeta en sí, no solo los archivos que tiene dentro).
2. En Claude, ve a *Customize → Skills*.
3. Pulsa **+**, luego *Create skill* y *Upload a skill*.
4. Sube el `.zip`.

### En Claude Code

Tienes tres opciones:

- **Para todos tus proyectos:** copia la carpeta `skills/planificador-proyectos-web/` dentro de la carpeta `.claude/skills/` de tu usuario.
- **Solo para un proyecto:** cópiala a `.claude/skills/` dentro de ese proyecto.
- **Desde tu cuenta:** si ya la subiste en Claude y entras a Claude Code con la misma cuenta, se sincroniza sola (Claude Code v2.1.273 o posterior).

En macOS o Linux, desde la terminal:

```bash
git clone https://github.com/ffelipecuevasc/planificador-proyectos-web.git
mkdir -p ~/.claude/skills
cp -r planificador-proyectos-web/skills/planificador-proyectos-web ~/.claude/skills/
```

En Windows, desde PowerShell:

```powershell
git clone https://github.com/ffelipecuevasc/planificador-proyectos-web.git
New-Item -ItemType Directory -Force "$HOME\.claude\skills"
Copy-Item -Recurse planificador-proyectos-web\skills\planificador-proyectos-web "$HOME\.claude\skills\"
```

Para comprobar que quedó instalada, abre Claude Code y escribe `/planificador-proyectos-web`. Si la skill responde, está lista.

---

## 5. Uso

No necesitas nombrar la skill: Claude la usa sola cuando le pides planificar o documentar un proyecto web. En Claude Code también puedes llamarla directamente con `/planificador-proyectos-web`.

**Empezar un proyecto pequeño**

> Quiero crear mi CV online con portafolio: un sitio estático en HTML y CSS, publicado en GitHub Pages. Tiene secciones sobre mí, proyectos y contacto. Ayúdame a planificarlo.

**Empezar una API**

> Voy a construir una API REST en Node.js con Express y PostgreSQL para reservar horas en una peluquería. Hay inicio de sesión para el administrador. Planifiquemos el proyecto.

**Seguir trabajando en un proyecto que ya tiene la documentación**

Estos pedidos se hacen en Claude Code, porque el agente necesita leer y modificar los archivos de tu repositorio:

> Agrega al backlog la funcionalidad de cancelar una reserva y especifícala.

> El formulario de contacto envía el correo vacío cuando el nombre tiene tildes. Corrígelo.

> Ahora la API también la va a usar una app móvil de terceros. ¿Cambia el nivel del proyecto?

---

## 6. Cómo funciona

La skill trabaja de dos formas: cuando el proyecto es nuevo y cuando ya tiene la documentación.

### Proyecto nuevo

```text
Entrevista  ▸  Diagnóstico  ▸  Variante  ▸  Generación  ▸  Validación  ▸  Entrega
(preguntas     (pequeño,       (frontend,    (solo lo que   (revisión      (.zip en el chat,
 en bloques)    mediano o       backend o     el nivel        automática)    o archivos en el
                complejo)       fullstack)    necesita)                      repositorio)
```

1. **Entrevista.** Claude te pregunta en bloques cortos lo que necesita saber: tipo de proyecto, [stack](#14-glosario), dónde se va a publicar, qué incluye y qué lo vuelve más delicado (inicio de sesión, conexión con otros servicios, pagos, datos personales). Si adjuntas documentos, como una descripción del proyecto, un prototipo o un README antiguo, saca las respuestas de ahí en vez de preguntarte.
2. **Diagnóstico de complejidad.** Clasifica el proyecto como pequeño, mediano o complejo, te explica por qué y qué documentos va a crear. Tú confirmas o cambias el nivel. El diagnóstico es una propuesta, no una verdad absoluta.
3. **Variante por tipo.** Un proyecto con interfaz visual lleva `DESIGN.md`. Una API lleva sus propias convenciones y, si es REST, un [contrato OpenAPI](#14-glosario).
4. **Generación.** Crea solo los documentos que el nivel justifica, a partir de plantillas.
5. **Validación.** Un script revisa que la estructura y los nombres sean correctos y que no queden datos inventados ni partes de la plantilla sin completar. Más detalles en la [sección 10](#10-el-validador).
6. **Entrega.** En el chat recibes un `.zip` para descomprimir en la carpeta principal de tu proyecto. En Claude Code, los archivos se escriben directamente en el repositorio. En ambos casos recibes una explicación de por qué cada documento quedó como quedó y la lista de datos pendientes.

### Proyecto que ya tiene la documentación

Cuando el repositorio ya tiene `AGENTS.md` y la carpeta `_planificacion/`, la skill no vuelve a generar nada: trabaja sobre lo que existe.

- **Funcionalidad nueva:** se agrega a la lista de pendientes ▸ se especifica, si lo justifica ▸ se planifica una etapa de trabajo con sus tareas ▸ se programa ▸ se comprueba contra los criterios de aceptación.
- **Cambio o corrección:** se clasifica como *menor* o *significativo*. Es menor si la especificación sigue siendo correcta: no se toca y se corrige el código. Es significativo si cambia el comportamiento, la API o la arquitectura: primero se actualiza la especificación y después el código.
- **Nuevo diagnóstico:** si el proyecto creció o se simplificó (por ejemplo, ahora tiene inicio de sesión), la skill propone un nivel nuevo y tú decides.

---

## 7. Niveles de complejidad

El nivel decide cuánta documentación se genera. Un CV online no necesita lo mismo que una tienda con pagos.

| | Pequeño | Mediano | Complejo |
| :- | :------ | :------ | :------- |
| **Ejemplos** | Sitio informativo, CV online, landing | API con base de datos e inicio de sesión, app con varias funcionalidades | Varios tipos de usuario, pagos o datos sensibles, conexión con varios servicios |
| **Lista de pendientes** | Mínima | Priorizada | Priorizada, indicando qué depende de qué |
| **Especificaciones** | No: cada etapa lleva su objetivo y criterios | Para cada funcionalidad con reglas o lógica propia | Para cada funcionalidad, con escenarios y [casos borde](#14-glosario) |
| **Plan técnico** | Opcional | Cuando la etapa toca la arquitectura, los datos o la API | Siempre |
| **Contrato OpenAPI** (API REST) | Recomendado | Obligatorio | Obligatorio y detallado |
| **Auditoría técnica** | Solo si hay algo que revisar | Sí | Sí |
| **Comprobación obligatoria** | Que compile, que se ejecute y que cumpla los criterios de aceptación | Lo mismo, más pruebas de la API | Lo mismo |

Las demás pruebas (unitarias, E2E, cobertura, contract testing; ver el [glosario](#14-glosario)) se recomiendan según el riesgo del proyecto, pero nunca se imponen. Solo pasan a ser obligatorias si tú lo decides.

---

## 8. Qué genera

```text
<carpeta-principal-del-proyecto>/
├── AGENTS.md                     Reglas para cualquier agente de IA (lo primero que lee)
├── DESIGN.md                     Colores, tipografía y componentes (solo si hay interfaz)
├── README.md                     Presentación del proyecto para quien llega al repositorio
├── .claude/
│   ├── settings.json             Permisos de Claude Code: qué hace solo, qué consulta, qué tiene prohibido
│   └── README.md                 Explicación de cada permiso
├── docs/api/openapi.yaml         Contrato de la API REST (según el nivel)
└── _planificacion/
    ├── README.md                 Guía de la carpeta y de cómo se trabaja
    ├── 00_producto/
    │   ├── producto.md           Qué es el proyecto, para quién y qué NO es
    │   ├── registro-pendientes.md   Lista de pendientes y estado del trabajo
    │   ├── decisiones.md         Registro de Decisiones Arquitectónicas (RDA)
    │   └── auditoria-tecnica.md  Revisiones técnicas y hallazgos (según el nivel)
    ├── 10_epicas/                Bloques grandes de trabajo y sus etapas
    ├── 20_especificaciones/      Especificaciones por funcionalidad (desde nivel mediano)
    └── 99_bitacora/              Qué se hizo, cómo se comprobó y qué se aprendió
```

Los documentos son de dos tipos, con reglas distintas. En los archivos internos de la skill y en los mensajes del validador, los protegidos aparecen con el nombre técnico de *inmutables*.

| Tipo | Archivos | Quién los edita | Regla |
| :--- | :------- | :-------------- | :---- |
| **Protegidos** | `AGENTS.md`, `DESIGN.md`, `README.md`, `_planificacion/README.md` | Solo tú. El agente puede proponerte cambios, pero no aplicarlos | Describen cómo es el proyecto hoy: sin fechas ni historial |
| **Vivos** | Registro de pendientes, decisiones, auditorías, especificaciones, OpenAPI, épicas, etapas y bitácoras | El agente, siguiendo las reglas de `_planificacion/README.md` | Llevan fechas y estados. Cada dato se escribe en un solo lugar, para que no haya dos versiones distintas |

### Cómo se ve un criterio de aceptación

Los criterios de aceptación son la pieza central: es lo que el agente usa para saber si terminó. La diferencia entre uno vago y uno verificable es esta:

```text
○  Vago:         El formulario de contacto funciona correctamente.
●  Verificable:  Si el campo «Correo» está vacío y presiono «Enviar», el formulario
                 no se envía y aparece el mensaje «Ingresa tu correo» bajo el campo.
```

El segundo se puede comprobar con un sí o un no. El primero no, y el validador te avisará si encuentra criterios de ese tipo.

---

## 9. Trabajar con el agente después de generar

1. Descomprime el `.zip` en la carpeta principal de tu proyecto (o deja que Claude Code escriba los archivos) y haz el primer commit con el mensaje que te sugirió la skill.
2. Abre `_planificacion/00_producto/registro-pendientes.md` y revisa los datos marcados como `PENDIENTE_CLIENTE` (información que debe dar quien encarga el proyecto; si el proyecto es tuyo, eres tú) y `PENDIENTE_DESARROLLADOR` (decisiones técnicas que te tocan a ti). Resuelve los que bloquean la primera etapa.
3. Si la etapa incluye una especificación, léela. Si estás de acuerdo, cambia el campo **Estado**, al inicio del archivo, de `Borrador` a `Aprobada`. El agente no programa nada que siga en `Borrador`.
4. En `registro-pendientes.md`, marca la iteración como `En curso` (o pídele al agente que lo haga). Su nombre aparece en el campo **Iteración activa** al inicio de ese archivo.
5. Pídele al agente: «Ejecuta la iteración activa». El agente leerá el registro, la etapa y su especificación, programará, comprobará el resultado, escribirá la bitácora y dejará la etapa `En revisión`, con un mensaje de commit sugerido.
6. Revisa lo que hizo, haz tú el commit y marca la etapa como `Terminada`.

> ◆ **El agente nunca hace commits, push, merges ni despliegues.** Los permisos de `.claude/settings.json` se lo impiden, y `AGENTS.md` le explica por qué. Esos pasos siempre quedan en tus manos.

---

## 10. El validador

Es un script que revisa que la documentación esté completa y bien formada. La skill lo ejecuta sola antes de entregarte los archivos, pero también puedes usarlo tú cuando quieras revisar un proyecto.

Ejecútalo desde la carpeta donde clonaste este repositorio. Por ejemplo, para revisar un sitio pequeño que está en la carpeta `../mi-cv`:

```bash
python3 skills/planificador-proyectos-web/scripts/validar_documentacion.py ../mi-cv --tipo frontend --nivel pequeno
```

En Windows, usa `python` o `py` en lugar de `python3`.

| Opción | Valores posibles | ¿Obligatoria? |
| :----- | :--------------- | :------------ |
| Carpeta del proyecto | La ruta a tu proyecto, como `../mi-cv` | Sí |
| `--tipo` | `frontend`, `backend` o `fullstack` | Sí |
| `--nivel` | `pequeno`, `mediano` o `complejo` (sin tilde) | No. Si no lo indicas, usa `mediano` |
| `--api-rest` | Se agrega sin valor si el proyecto expone una API REST | No |
| `--zip` | Nombre de un archivo, como `salida.zip`, para empaquetar el resultado | No |

El validador entrega dos tipos de resultados:

- **Errores**, que impiden la entrega hasta que se corrijan: faltan archivos que el nivel exige; hay nombres con tildes o que no siguen la convención; `settings.json` está mal escrito o tiene reglas que se contradicen; quedaron partes de la plantilla sin completar; el `README.md` del proyecto incluye bloques de código o comandos (ese archivo es una presentación, no un manual técnico; solo se admite un bloque `text` para el árbol de carpetas); el registro no tiene lista de pendientes; hay etapas o especificaciones sin criterios de aceptación; una API REST de nivel mediano o complejo no tiene contrato; o hay datos pendientes que no quedaron registrados.
- **Avisos**, para que los revises uno por uno: fechas o referencias al pasado en los documentos protegidos, y criterios de aceptación vagos como «se ve bien» o «funciona correctamente».

---

## 11. Personalizar la skill

Durante la entrevista puedes cambiar las convenciones de cada proyecto: idioma y variante regional (por defecto, español latinoamericano neutro, con trato de tú), formato de los mensajes de commit, nombres de ramas, zona horaria y gestor de paquetes.

Si quieres que tus propias convenciones se usen siempre, edita la sección «Convenciones por defecto» de `SKILL.md`. Las plantillas de `assets/plantillas/` también puedes ajustarlas. Por ejemplo, los comandos de `settings.json` vienen escritos para PNPM; si usas npm o Yarn, cámbialos ahí.

---

## 12. Para quienes ya conocen SDD o Scrum

Esta sección resume qué se tomó de cada metodología y dónde quedó. No es necesaria para usar la skill.

| Práctica | Viene de | Dónde vive |
| :------- | :------- | :--------- |
| Especificación antes del código | SDD | `20_especificaciones/spec-*.md` (o los criterios de la etapa en nivel pequeño) |
| Plan técnico y tareas | SDD | Cada etapa, secciones «Plan técnico» y «Tareas» |
| Validación contra criterios verificables | SDD | Criterios de aceptación y bitácora con evidencia |
| Contrato de API como fuente de verdad | SDD | `docs/api/openapi.yaml`: cambia antes que el código |
| Contexto duradero para el agente | SDD | `AGENTS.md`, decisiones (RDA), `DESIGN.md` |
| Backlog priorizado | Scrum | Sección «Backlog» de `registro-pendientes.md` |
| Iteraciones con objetivo y entregables | Scrum | `10_epicas/`, sin duración fija |
| Revisión y aprendizaje al cerrar | Scrum (revisión y retrospectiva, simplificadas) | Sección «Revisión» de cada bitácora y «Revisión al cierre» de cada épica |
| Definición de terminado breve | Scrum | `AGENTS.md`, separada de los criterios de aceptación |

Se dejaron fuera a propósito: sprints de duración fija, Daily, Sprint Planning, retrospectivas formales, historias de usuario obligatorias, puntos y estimaciones, y los archivos separados `spec.md`, `plan.md` y `tasks.md` por funcionalidad. El plan y las tareas cambian en cada iteración, y la iteración ya es su lugar natural.

---

## 13. Preguntas frecuentes

**¿Tengo que saber Scrum para usar esta skill?**
No. Solo toma tres ideas: una lista de pendientes ordenada por prioridad, etapas de trabajo con un objetivo y una revisión al cerrar cada una. Sirve para trabajar solo o con agentes de IA, sin roles ni reuniones.

**¿Necesito OpenAPI?**
Solo si tu proyecto expone una API REST y su nivel es mediano o complejo. En nivel pequeño es una recomendación, y en un sitio sin API no aparece.

**¿Por qué `AGENTS.md` y no `CLAUDE.md`?**
`AGENTS.md` es un formato abierto que leen varios agentes (Claude Code, Codex, Antigravity, entre otros). Claude Code lo lee de forma nativa desde su versión 2.1.277.

> ◆ **Importante.** Si creas un `CLAUDE.md` o un `CLAUDE.local.md` en el proyecto, Claude Code deja de leer `AGENTS.md` en su modo por defecto. Si necesitas uno de esos archivos, escribe `@AGENTS.md` en su primera línea.

**¿El agente puede cambiar las reglas del proyecto?**
No. Los cuatro documentos protegidos solo los editas tú. El agente te entrega una propuesta con el texto actual, el texto nuevo y la razón del cambio.

**¿Qué pasa si el diagnóstico de complejidad está mal?**
Lo cambias. El diagnóstico es una propuesta y queda registrado como la primera decisión del proyecto (`RDA-001`). Si el proyecto cambia más adelante, se puede volver a diagnosticar.

**¿Funciona con otros agentes además de Claude Code?**
Los documentos que genera, sí: `AGENTS.md` y `_planificacion/` son archivos Markdown que cualquier agente puede leer. La skill en sí (la entrevista y la generación) está pensada para Claude.

**¿Qué hago si no entiendo un término?**
Revisa el [glosario](#14-glosario). Y si algo de la entrevista no te queda claro, pregúntale a Claude en el mismo chat: puede explicártelo antes de seguir.

---

## 14. Glosario

### Trabajo con IA

| Término | Qué significa |
| :------ | :------------ |
| **Agente de IA** | Una IA que no solo responde, sino que actúa: lee archivos, escribe código y ejecuta comandos en tu proyecto. Claude Code es un agente. |
| **Skill** | Un paquete de instrucciones y archivos que le enseña a Claude a hacer una tarea específica de una forma determinada. Esta skill le enseña a planificar proyectos web. |
| **Contexto** | La información que el agente tiene a la vista mientras trabaja. Es limitado, por eso conviene que los documentos sean breves y estén en el repositorio. |
| **Marcador de plantilla** | Un espacio por completar dentro de una plantilla, como `<nombre-del-proyecto>`. Si queda uno sin reemplazar, el validador lo detecta. |

### Organización del trabajo

| Término | Qué significa |
| :------ | :------------ |
| **Backlog** | La lista de todo lo que falta por hacer en el proyecto, ordenada por prioridad. Aquí vive en `registro-pendientes.md`. |
| **Épica** | Un bloque grande de trabajo que agrupa varias funcionalidades relacionadas. Por ejemplo, «Gestión de reservas». |
| **Iteración** | Una etapa corta de trabajo con un objetivo claro, como «Formulario de contacto funcionando». Al terminarla se revisa el resultado antes de pasar a la siguiente. |
| **Especificación** | Un documento que describe qué debe hacer una funcionalidad antes de programarla: cómo se comporta, qué reglas sigue y qué pasa cuando algo falla. |
| **Criterios de aceptación** | Condiciones concretas que se comprueban con un sí o un no para saber si una funcionalidad quedó bien. Ver el ejemplo de la [sección 8](#8-qué-genera). |
| **Casos borde** | Situaciones poco comunes que suelen romper el código: un campo vacío, un nombre con tildes, dos personas reservando la misma hora a la vez. |
| **Definición de terminado** | Una lista breve de condiciones que cualquier trabajo debe cumplir para darse por terminado. Por ejemplo, que el proyecto compile y que no queden errores en la consola. |
| **Bitácora** | Un registro de lo que se hizo en cada etapa, cómo se comprobó y qué se aprendió. |
| **RDA** | Registro de Decisiones Arquitectónicas. Un documento donde se anota cada decisión técnica importante y su motivo, para que nadie tenga que adivinar por qué algo se hizo así. |
| **Fuente única de verdad** | La regla de que cada dato se escribe en un solo lugar. Si el estado de una tarea aparece en dos archivos distintos, tarde o temprano uno quedará desactualizado. |
| **Trazabilidad** | Poder seguir el camino de una funcionalidad desde la idea hasta el código: en qué pendiente nació, qué especificación la describe y en qué bitácora se comprobó. |
| **SDD** | *Spec-Driven Development*, o desarrollo guiado por especificaciones. La idea de escribir qué se va a construir antes de construirlo. |
| **Scrum** | Una metodología ágil para organizar equipos de desarrollo. Esta skill toma solo algunas de sus prácticas. |

### Proyecto y repositorio

| Término | Qué significa |
| :------ | :------------ |
| **Stack** | El conjunto de tecnologías que usa un proyecto. Por ejemplo, React, Node.js y PostgreSQL. |
| **Hosting** | El servicio donde se publica tu proyecto para que otros puedan verlo, como GitHub Pages, Vercel o Netlify. |
| **API REST** | Una forma estándar de que dos programas se comuniquen por internet usando direcciones (URL) y métodos como `GET` o `POST`. |
| **Contrato OpenAPI** | Un archivo (`openapi.yaml`) que describe con precisión qué recibe y qué responde cada dirección de tu API. Sirve de acuerdo entre quien hace la API y quien la usa. |
| **Repositorio** | La carpeta de tu proyecto controlada por Git, con todo su historial de cambios. |
| **Carpeta principal del proyecto** | La carpeta de más arriba de tu repositorio, donde está la carpeta `.git`. También se le llama *raíz del repositorio*. |
| **Commit** | Un punto guardado en el historial de Git, con un mensaje que describe qué cambió. |
| **Push** | Enviar tus commits al repositorio remoto, por ejemplo a GitHub. |
| **Merge** | Unir los cambios de una rama con otra. |
| **Despliegue** | Publicar una versión del proyecto en su hosting para que quede disponible. |
| **Release** | Una versión publicada de un repositorio en GitHub, normalmente con archivos listos para descargar. |
| **Markdown** | El formato de texto simple que usan los archivos `.md`, como este README. |

### Pruebas

| Término | Qué significa |
| :------ | :------------ |
| **Prueba unitaria** | Código que comprueba automáticamente que una pieza pequeña (una función, por ejemplo) hace lo que debe. |
| **Prueba E2E** | Prueba de extremo a extremo (*end to end*): simula a una persona usando la aplicación completa, desde abrir la página hasta terminar una acción. |
| **Cobertura** | El porcentaje del código que las pruebas automáticas alcanzan a ejecutar. |
| **Contract testing** | Pruebas que comprueban que la API responde exactamente lo que dice su contrato OpenAPI. |

---

## 15. Estructura de este repositorio

```text
.
├── README.md                          Este archivo
├── LICENSE                            Licencia MIT
└── skills/
    └── planificador-proyectos-web/    La skill (esto es lo que se instala)
        ├── SKILL.md                   Instrucciones principales que lee Claude
        ├── references/
        │   ├── entrevista.md          Preguntas de la entrevista inicial
        │   ├── niveles-complejidad.md Diagnóstico y documentos por nivel
        │   ├── tipos-proyecto.md      Variantes frontend, backend y fullstack; contrato de API
        │   └── guia-documentos.md     Qué lleva cada documento y por qué
        ├── assets/plantillas/         Plantillas con la misma estructura que se entrega
        └── scripts/
            └── validar_documentacion.py
```

Este README está fuera de la carpeta de la skill a propósito: así no ocupa el contexto del agente ni se confunde con el `README.md` que la skill genera para cada proyecto.

---

## 16. Licencia y autoría

Creada por **Felipe Cuevas** ([felipecuevas.dev](https://felipecuevas.dev)). Publicada con licencia [MIT](LICENSE): puedes usarla, modificarla y compartirla, siempre que mantengas el aviso de copyright.
