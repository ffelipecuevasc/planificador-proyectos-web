# Documentos permitidos

Lista cerrada de los archivos Markdown que pueden existir en las zonas de documentación del proyecto. Es la fuente única de esta regla:

- `restringir-documentos.sh` la lee en cada escritura y bloquea los `.md` nuevos que no calzan con ningún patrón.
- `settings.json` permite editar sin consulta solo estos patrones dentro de `_planificacion/`.
- La tabla «Documentos permitidos» de `AGENTS.md` resume esta lista.

Ningún agente edita este archivo. Para aprobar un documento nuevo, el desarrollador agrega su patrón aquí y en la tabla de `AGENTS.md`.

## Cómo se leen los patrones

- Las rutas son relativas a la raíz del repositorio y usan `/`.
- `*` reemplaza cualquier texto dentro de un mismo nivel de carpeta: `epica-*/` calza con `epica-01-fundacion/`, pero no con dos carpetas.
- Solo cuentan las líneas de lista que empiezan con una ruta entre acentos graves.

## Zonas de documentación

Fuera de estas carpetas (por ejemplo, el contenido del sitio en `src/content/`) la regla no se aplica.

- `./` (solo la raíz, sin subcarpetas)
- `_planificacion/`
- `docs/`
- `.claude/`

## Patrones

### Raíz

- `AGENTS.md`
- `DESIGN.md`
- `README.md`

### .claude/

- `.claude/README.md`
- `.claude/commands/*.md`
- `.claude/hooks/documentos-permitidos.md`

### _planificacion/

- `_planificacion/README.md`
- `_planificacion/plantillas/*.md`
- `_planificacion/00_producto/producto.md`
- `_planificacion/00_producto/registro-pendientes.md`
- `_planificacion/00_producto/registro-archivo.md`
- `_planificacion/00_producto/decisiones.md`
- `_planificacion/00_producto/propuestas-documentos-protegidos.md`
- `_planificacion/00_producto/auditoria-tecnica.md`
- `_planificacion/00_producto/auditorias/auditoria-*.md`
- `_planificacion/00_producto/linea-base-produccion.md`
- `_planificacion/10_epicas/epica-*/definicion-epica-*.md`
- `_planificacion/10_epicas/epica-*/iteracion-*.md`
- `_planificacion/10_epicas/epica-*/bitacoras/bitacora-*.md`
- `_planificacion/20_especificaciones/spec-*.md`
