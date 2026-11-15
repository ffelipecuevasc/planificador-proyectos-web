#!/bin/sh
# restringir-documentos.sh · Hook PreToolUse de Claude Code.
#
# Impide que el agente cree archivos Markdown que no están en la lista cerrada de
# .claude/hooks/documentos-permitidos.md (por ejemplo, un registro de prompts o notas de
# sesión dentro de la carpeta de bitácoras).
#
# - Solo actúa en las zonas de documentación que declara la lista (la raíz, _planificacion/,
#   docs/ y .claude/). El contenido del sitio, como src/content/, queda fuera.
# - Solo bloquea la creación de archivos nuevos: editar uno que ya existe siempre se permite.
# - Revisa la herramienta de escritura y los comandos de Bash o PowerShell que escriben
#   archivos (redirecciones, tee, Out-File, Set-Content, New-Item, cp, mv, touch…).
# - Escrito en shell POSIX, sin dependencias. Falla cerrado: si algo inesperado ocurre, o si
#   falta la lista, bloquea la creación.
# - Código 2 = bloquear (el mensaje de stderr le llega al agente). Código 0 = sin objeción.

LISTA_REL=".claude/hooks/documentos-permitidos.md"

bloquear() {
  printf '%s\n' "Bloqueado por restringir-documentos.sh: $1. Solo se pueden crear los documentos de $LISTA_REL (AGENTS.md, sección «Documentos permitidos»). No guardes prompts, notas de sesión, borradores ni resúmenes en archivos nuevos. Si crees que falta un documento, propónlo en «Propuestas fuera de alcance» de _planificacion/00_producto/registro-pendientes.md." >&2
  exit 2
}

campo() {
  printf '%s' "$entrada" |
    sed -n -E "s/.*\"$1\"[[:space:]]*:[[:space:]]*\"(([^\"\\\\]|\\\\.)*)\".*/\\1/p" |
    sed -e 's/\\"/"/g' -e 's#\\/#/#g' -e 's#\\\\#/#g'
}

# Ruta con «/», sin «./» inicial y con la unidad de Windows en forma /c/… para comparar.
normalizar() {
  r=$(printf '%s' "$1" | tr '\\' '/')
  case "$r" in
    [A-Za-z]:/*)
      unidad=$(printf '%s' "$r" | cut -c1 | tr 'A-Z' 'a-z')
      r="/$unidad/$(printf '%s' "$r" | cut -c4-)"
      ;;
  esac
  while :; do
    case "$r" in
      ./*) r=${r#./} ;;
      *) break ;;
    esac
  done
  printf '%s' "${r%/}"
}

# Elementos de lista («- `ruta`») de una sección «## …» de la lista.
elementos() {
  awk -v sec="$1" '
    /^## / { dentro = (index($0, "## " sec) == 1); next }
    dentro && /^- `/ { l = $0; sub(/^- `/, "", l); sub(/`.*/, "", l); print l }
  ' "$lista"
}

barras() {
  printf '%s' "$1" | tr -cd '/' | wc -c | tr -d ' '
}

revisar() {
  [ -n "$1" ] || return 0
  case "$1" in
    *.[mM][dD]) ;;
    *) return 0 ;;
  esac
  ruta=$(normalizar "$1")
  case "$ruta" in
    /*)
      case "$ruta" in
        "$raiz"/*) rel=${ruta#"$raiz"/} ;;
        *) return 0 ;;
      esac
      ;;
    *) rel=$ruta ;;
  esac
  [ -e "$raiz/$rel" ] && return 0
  [ -f "$lista" ] || bloquear "no existe $LISTA_REL, así que no se puede comprobar «$rel»"

  en_zona=no
  for zona in $(elementos "Zonas"); do
    zona=$(normalizar "$zona")
    case "$zona" in
      .|"")
        case "$rel" in */*) ;; *) en_zona=si ;; esac
        ;;
      *)
        case "$rel" in "$zona"/*) en_zona=si ;; esac
        ;;
    esac
  done
  [ "$en_zona" = si ] || return 0

  nivel=$(barras "$rel")
  for patron in $(elementos "Patrones"); do
    patron=$(normalizar "$patron")
    [ "$(barras "$patron")" = "$nivel" ] || continue
    # shellcheck disable=SC2254
    case "$rel" in $patron) return 0 ;; esac
  done
  bloquear "«$rel» no es un documento permitido"
}

# Rutas .md que un comando podría escribir. Solo se revisan si el comando escribe archivos.
destinos() {
  case "$1" in
    *'>'*|*tee\ *|*Out-File*|*Set-Content*|*Add-Content*|*New-Item*|*touch\ *|*cp\ *|*mv\ *|*copy\ *|*move\ *|*Copy-Item*|*Move-Item*|*ren\ *|*Rename-Item*) ;;
    *) return 0 ;;
  esac
  for palabra in $(printf '%s' "$1" | tr "\"'=<>|;&(),{}" '             '); do
    case "$palabra" in *.[mM][dD]) printf '%s\n' "$palabra" ;; esac
  done
}

principal() {
  set -e
  set -f
  entrada=$(cat | tr '\r\n\t' '   ')
  herramienta=$(campo tool_name)
  raiz=$(normalizar "${CLAUDE_PROJECT_DIR:-$(pwd)}")
  lista="$raiz/$LISTA_REL"
  case "$herramienta" in
    Write|Edit|MultiEdit|NotebookEdit)
      revisar "$(campo file_path)"
      revisar "$(campo notebook_path)"
      ;;
    Bash|PowerShell)
      for destino in $(destinos "$(campo command)"); do
        revisar "$destino"
      done
      ;;
  esac
  exit 0
}

( principal )
estado=$?
case "$estado" in
  0|2) exit "$estado" ;;
  *)
    printf '%s\n' "Bloqueado por restringir-documentos.sh: el hook falló de forma inesperada (código $estado) y, por seguridad, bloqueó la acción. Avísale al desarrollador." >&2
    exit 2
    ;;
esac
