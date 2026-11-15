#!/bin/sh
# proteger-secretos.sh · Hook PreToolUse de Claude Code.
#
# Impide que el agente lea, busque o edite archivos con secretos (.env y sus variantes,
# .dev.vars, llaves privadas, certificados y archivos de credenciales), tanto con las
# herramientas de archivos como con comandos de Bash o PowerShell.
#
# - Escrito en shell POSIX, sin dependencias: corre con sh en macOS y Linux, y con Git Bash
#   en Windows (Git para Windows lo instala y Claude Code lo usa para los hooks).
# - Falla cerrado: si algo inesperado ocurre dentro del script, bloquea la acción.
# - Código 2 = bloquear (el mensaje de stderr le llega al agente). Código 0 = sin objeción.
# - Archivos de ejemplo que se versionan sin secretos y sí se pueden leer:
#   .env.example, .env.sample, .env.template, .env.dist.
#
# Límite: no ve qué archivos abre por dentro un programa (por ejemplo, un script de Python
# que carga .env). Esa parte la cubren las reglas de AGENTS.md y la revisión del desarrollador.

bloquear() {
  printf '%s\n' "Bloqueado por proteger-secretos.sh: $1. Los archivos con secretos no se leen, no se buscan ni se editan (AGENTS.md, «Límites de actuación»). Si necesitas un valor, usa un marcador PENDIENTE_DESARROLLADOR y pídeselo al desarrollador sin que lo pegue en el chat." >&2
  exit 2
}

# Valor de texto de un campo del JSON de entrada (sin jq).
campo() {
  printf '%s' "$entrada" |
    sed -n -E "s/.*\"$1\"[[:space:]]*:[[:space:]]*\"(([^\"\\\\]|\\\\.)*)\".*/\\1/p" |
    sed -e 's/\\"/"/g' -e 's#\\/#/#g' -e 's#\\\\#/#g'
}

# ¿El nombre corresponde a un archivo con secretos? El segundo argumento, «palabra», indica
# que viene de un comando: ahí no se usa *.env, que calzaría con código como process.env.
es_secreto() {
  nombre=$(printf '%s' "$1" | tr '\\' '/' | sed 's#.*/##' | tr 'A-Z' 'a-z')
  case "$nombre" in
    .env.example*|.env.sample*|.env.template*|.env.dist*) return 1 ;;
    .env|.env.*|.env\**|.envrc|.dev.vars) return 0 ;;
    *.env) [ "$2" = palabra ] && return 1; return 0 ;;
    *.pem|*.key|*.p12|*.pfx|*.jks|*.keystore) return 0 ;;
    id_rsa|id_rsa.*|id_ed25519|id_ed25519.*|id_ecdsa|id_ecdsa.*) return 0 ;;
    credentials.json|secrets.json|secrets.yml|secrets.yaml|secrets.toml|*.tfvars) return 0 ;;
  esac
  return 1
}

revisar_ruta() {
  [ -n "$1" ] || return 0
  if es_secreto "$1"; then bloquear "«$1» contiene o puede contener secretos"; fi
}

# Revisa cada palabra de un comando o de un patrón de búsqueda.
revisar_texto() {
  palabras=$(printf '%s' "$1" | tr "\"'=<>|;&()," '           ')
  for palabra in $palabras; do
    if es_secreto "$palabra" palabra; then bloquear "el comando o la búsqueda toca «$palabra»"; fi
  done
}

principal() {
  set -e
  set -f
  entrada=$(cat | tr '\r\n\t' '   ')
  herramienta=$(campo tool_name)
  case "$herramienta" in
    Read|Edit|Write|MultiEdit|NotebookEdit)
      revisar_ruta "$(campo file_path)"
      revisar_ruta "$(campo notebook_path)"
      ;;
    Grep|Glob)
      revisar_texto "$(campo path) $(campo glob)"
      [ "$herramienta" = "Glob" ] && revisar_texto "$(campo pattern)"
      ;;
    Bash|PowerShell)
      revisar_texto "$(campo command)"
      ;;
  esac
  exit 0
}

( principal )
estado=$?
case "$estado" in
  0|2) exit "$estado" ;;
  *)
    printf '%s\n' "Bloqueado por proteger-secretos.sh: el hook falló de forma inesperada (código $estado) y, por seguridad, bloqueó la acción. Avísale al desarrollador." >&2
    exit 2
    ;;
esac
