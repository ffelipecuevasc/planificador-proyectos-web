# .claude · Permisos y protecciones de Claude Code

Esta carpeta define qué puede hacer Claude Code en el repositorio sin preguntar, qué debe consultar antes, qué tiene prohibido y qué bloquean los hooks. Este README explica cada grupo de reglas y por qué existe. Ningún agente edita esta carpeta: la mantiene el desarrollador.

---

## 1. Qué hay en esta carpeta

| Archivo | Para qué sirve |
| :------ | :------------- |
| `settings.json` | Permisos (`allow`, `ask`, `deny`) y registro de los hooks. |
| `README.md` | Esta explicación. |
| `commands/` | Atajos de Claude Code (sección 7). Remiten a los flujos de `_planificacion/README.md`, que siguen todos los agentes. |
| `hooks/proteger-secretos.sh` | Bloquea la lectura, búsqueda y edición de archivos con secretos. |
| `hooks/restringir-documentos.sh` | Bloquea la creación de archivos `.md` que no están en la lista de documentos permitidos. |
| `hooks/documentos-permitidos.md` | Lista cerrada de documentos: la usan el hook, `settings.json` y `AGENTS.md`. |

## 2. Cómo se resuelven las reglas

- Claude Code evalúa primero `deny`, luego `ask` y al final `allow`. La primera lista que calza decide, sin importar qué regla es más específica: una regla de `allow` nunca abre una excepción dentro de una de `ask` o `deny`.
- Lo que no calza con ninguna regla queda en el comportamiento del modo de permisos activo (en el modo por defecto, Claude Code pregunta).
- Las rutas que empiezan con `/` se leen desde la raíz del proyecto; `*` cubre un nivel de carpeta y `**` cualquier profundidad. `Bash(comando *)` calza con el comando y cualquier argumento.
- Los hooks se ejecutan **antes** de los permisos y su bloqueo vale incluso en los modos que aprueban todo.
- `settings.local.json`, si existe, es personal: no se versiona y no debe usarse para relajar las reglas de `deny`.
- Si en la carpeta del proyecto o más arriba existe un `CLAUDE.md` o un `CLAUDE.local.md`, Claude Code lee ese archivo y deja de cargar `AGENTS.md`. Quien necesite instrucciones personales debe empezar su `CLAUDE.local.md` con la línea `@AGENTS.md`.

## 3. `allow` · Sin consulta

{{TABLA_ALLOW}}

## 4. `ask` · Requiere consulta

{{TABLA_ASK}}

## 5. `deny` · Prohibido

{{TABLA_DENY}}

## 6. Hooks

Los dos hooks son scripts de shell POSIX sin dependencias. Corren con `sh` en macOS y Linux, y con Git Bash en Windows (Git para Windows lo instala y Claude Code lo usa para ejecutar los hooks). Responden con código 2 para bloquear, y el motivo le llega al agente; con código 0 no objetan nada. **Fallan cerrados:** si algo inesperado ocurre dentro del script, bloquean la acción.

| Hook | Qué revisa | Qué bloquea |
| :--- | :--------- | :---------- |
| `proteger-secretos.sh` | Herramientas de lectura, edición y búsqueda, y comandos de Bash o PowerShell | Cualquier acceso a `.env` y sus variantes, `.dev.vars`, llaves privadas, certificados y archivos de credenciales. `.env.example`, `.env.sample`, `.env.template` y `.env.dist` se pueden leer porque se versionan sin secretos. |
| `restringir-documentos.sh` | La herramienta de escritura y los comandos que escriben archivos | La **creación** de un `.md` en las zonas de documentación que no calza con ningún patrón de `documentos-permitidos.md`. Editar un archivo que ya existe siempre se permite. |

**Prueba rápida** desde la raíz del repositorio (en Windows, desde Git Bash). La primera debe responder `2` y la segunda `0`:

```bash
printf '%s' '{"tool_name":"Read","tool_input":{"file_path":".env"}}' | sh .claude/hooks/proteger-secretos.sh; echo $?
printf '%s' '{"tool_name":"Read","tool_input":{"file_path":".env.example"}}' | sh .claude/hooks/proteger-secretos.sh; echo $?
```

**Aprobar un documento nuevo:** agrega su patrón a `hooks/documentos-permitidos.md` y a la tabla «Documentos permitidos» de `AGENTS.md`. Si el documento vive en `_planificacion/` y quieres que el agente lo edite sin consulta, agrega también su regla `Edit(...)` en `allow`.

## 7. Comandos

{{TABLA_COMANDOS}}

## 8. Límites de la protección

- **Las reglas `Read` y `Edit` solo gobiernan las herramientas de archivos de Claude Code.** No cubren un programa que abre el archivo por dentro (un script de Python, un servidor de desarrollo que carga `.env`). El hook revisa el texto de los comandos, pero no puede ver qué hace un programa al ejecutarse.
- **Búsquedas recursivas.** Un `grep -r` desde la raíz puede recorrer `.env` sin nombrarlo. Por eso `.env` y sus variantes deben estar en `.gitignore`: la herramienta de búsqueda de Claude Code respeta ese archivo, y el agente excluye los secretos en sus búsquedas.
- **Sin shell, sin hooks.** Si la máquina no tiene `sh` ni Git Bash, los hooks no se ejecutan y solo quedan los permisos de `settings.json`. Con Git para Windows instalado, que el flujo de trabajo ya exige, esto no ocurre.
- **Sin sandbox en Windows nativo.** El sandbox de Claude Code, que limitaría a nivel de sistema los archivos que leen los comandos, no existe en Windows nativo: ahí las barreras son los permisos, los hooks y la revisión del desarrollador.
- **Otros agentes.** Codex, Antigravity u otros no leen esta carpeta. Para ellos valen las reglas de `AGENTS.md`, y el comando `/auditar-epica` detecta después los documentos que no debieran existir.
