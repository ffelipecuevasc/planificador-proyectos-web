# Iteración XX-YY · Nombre

- **Épica:** XX · Nombre
- **Estado:** Pendiente
- **Rama sugerida:** iteracion/XX-YY-descripcion-corta
- **Depende de:** XX-YY o —
- **Especificación:** spec-funcionalidad.md (CA-01, CA-02) o —
- **RDA relacionadas:** RDA-XXX o —
- **Hallazgos que cierra:** AUD-NN-MMM o —
- **Cambio de esquema:** no | sí: qué tablas o campos, y si se puede revertir
- **Respaldo previo al despliegue:** no aplica | qué se respalda y dónde, antes de desplegar

> Las dos últimas líneas van solo en un proyecto con base de datos en producción; si no, bórralas. Con rama única `main`, la línea de rama dice «Rama: main».

## Objetivo

Una o dos frases: qué deja funcionando la iteración.

## Punto de partida

> Opcional, en un proyecto con código existente: lo que hay hoy en el código y que la iteración debe verificar leyendo los archivos antes de escribir. Si no aplica, borra la sección.

- …

## Alcance y entregables

- …

## Contenido aprobado (copiar tal cual)

> Opcional, cuando la iteración publica textos, datos o imágenes aprobados por el cliente o el desarrollador: se copian literalmente, sin reescribirlos. Si no aplica, borra la sección.

- …

## Decisiones del desarrollador

> Opcional: decisiones ya tomadas que condicionan cómo se implementa (con su fecha). Si no hay, borra la sección.

- …

## Plan técnico

> Va si la iteración toca arquitectura, datos, API o integraciones (desde nivel mediano) y siempre en nivel complejo; si no, borra la sección.

Componentes que se tocan, cambios en el modelo de datos o en el contrato, decisiones de implementación, estándares de calidad de `AGENTS.md` que aplican (patrones, pruebas, seguridad) y riesgos.

## Tareas

1. …

## Tareas del desarrollador

> Opcional: lo que solo puede hacer el desarrollador (configurar un servicio externo, probar en un teléfono, entregar un acceso), planificado desde el inicio. Si no hay, borra la sección.

1. …

## Criterios de aceptación

- [ ] CA-01 de la especificación (se cita, no se copia)
- [ ] … (criterio técnico propio, verificable con una medición o un comando)

## Riesgos

> Opcional: qué puede salir mal y cómo se detecta o se mitiga. Si no hay riesgos relevantes, borra la sección.

- …

## Despliegue

> Opcional, si la iteración se publica en producción: pasos, verificación después de publicar y cómo se revierte. Si no aplica, borra la sección.

- …

## Fuera de alcance

- …

## Datos requeridos

### Del cliente

- … o «Ninguno»

### Del desarrollador

- … o «Ninguno»

## Evidencia del desarrollador

> Solo si el agente, después de intentarlo por todos los medios, no pudo obtener un dato que exige un criterio (un panel de un servicio externo, una medición en un dispositivo real). La agrega el agente durante la iteración y la responde el desarrollador. Si no hace falta, borra la sección.

- **Fecha y hora de las pruebas:** AAAA-MM-DD HH:MM
- **Commit desplegado:** hash corto o —

### Qué intentó el agente

| Dato | Qué intentó | Por qué no pudo |
| :--- | :---------- | :-------------- |
| … | … | … |

### Qué necesita del desarrollador

1. **Dato:** … · **Para qué criterio:** … · **Cómo obtenerlo:** pasos exactos.
   - **Respuesta:**
