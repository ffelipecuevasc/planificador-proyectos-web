#!/usr/bin/env python3
"""Arma la carpeta .claude/ de un proyecto: permisos, hooks, comandos, lista de documentos
permitidos y su README, todo desde una sola fuente para que no queden desalineados.

Uso:
    python preparar_claude.py --proyecto <dir> --stack astro-pnpm --nivel mediano
    python preparar_claude.py --proyecto <dir> --stack astro-pnpm:frontend --stack django:backend \
        --api-rest --nivel complejo --dominio-produccion app.ejemplo.cl
    python preparar_claude.py --listar

Qué escribe en <dir>/.claude/:
- settings.json: base.json más un fragmento por pieza del stack (assets/permisos/), la
  edición sin consulta de los documentos de _planificacion/ que permite la lista, el contrato
  docs/api/** si hay API REST, el bloqueo web de los dominios de producción y los dos hooks.
- hooks/: proteger-secretos.sh, restringir-documentos.sh y documentos-permitidos.md, esta
  última solo con los patrones de los componentes activos.
- commands/: siguiente-epica.md e iteracion.md siempre; auditar-epica.md si hay auditorías.
- README.md: la plantilla con las tablas «regla · por qué» generadas desde los fragmentos.

Además, si existe <dir>/AGENTS.md con {{TABLA_DOCUMENTOS_PERMITIDOS}}, reemplaza ese marcador
por la tabla de documentos permitidos.

Componentes según el nivel: especificaciones y auditorías desde nivel mediano. --auditoria
activa las auditorías en nivel pequeño (por ejemplo, un proyecto con código existente) y
--linea-base-produccion agrega el documento de línea base de producción.

`--stack nombre:carpeta` sirve para un monorrepo: las reglas de edición del fragmento se
aplican dentro de esa carpeta y se permite `cd carpeta`. El resultado conserva el orden de
grupos (comandos, Git, sistema, edición, lectura, web), sin reglas repetidas, y avisa si una
regla de allow o ask queda anulada por una de deny. Después hay que revisar el resultado
contra el proyecto real: los fragmentos son un punto de partida.
"""

import argparse
import fnmatch
import json
import re
import shutil
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
PERMISOS = SKILL / "assets" / "permisos"
PLANTILLA_CLAUDE = SKILL / "assets" / "plantillas" / "claude"
GRUPOS = ["comandos", "git", "sistema", "edicion", "lectura", "web"]
LISTAS = ["allow", "ask", "deny"]
NIVELES = ["pequeno", "mediano", "complejo"]

NOMBRE_GRUPO = {
    "comandos": "Comandos del proyecto",
    "git": "Git",
    "sistema": "Sistema y servicios",
    "edicion": "Edición",
    "lectura": "Lectura",
    "web": "Web",
}
NOMBRE_STACK = {
    "base": "",
    "astro-pnpm": "Astro",
    "django": "Django",
    "fastapi": "FastAPI",
    "spring": "Spring Boot",
    "quarkus": "Quarkus",
    "express-pnpm": "Express",
}

# Patrones de la lista que dependen de un componente del proceso.
COMPONENTE_DE_PATRON = {
    "_planificacion/20_especificaciones/spec-*.md": "especificaciones",
    "_planificacion/00_producto/auditoria-tecnica.md": "auditoria",
    "_planificacion/00_producto/auditorias/auditoria-*.md": "auditoria",
    "_planificacion/00_producto/linea-base-produccion.md": "linea_base",
}
# Documentos de _planificacion/ que nunca se editan sin consulta (están protegidos).
PROTEGIDOS_PLANIFICACION = {"_planificacion/README.md", "_planificacion/plantillas/*.md"}

COMANDOS = [
    ("siguiente-epica.md", "/siguiente-epica [XX]", "Cierra la épica con su bitácora de cierre, revisa como experto en el stack y propone las iteraciones de la siguiente.", "`_planificacion/README.md`, sección 4.4", None),
    ("iteracion.md", "/iteracion XX-YY", "Ejecuta una iteración completa: preparada, implementación, verificación medida, bitácora y registro.", "`AGENTS.md`, «Flujo de trabajo por iteración»", None),
    ("auditar-epica.md", "/auditar-epica XX", "Audita una épica antes de cerrarla, en una sesión nueva, y registra los hallazgos.", "`_planificacion/README.md`, sección 4.6", "auditoria"),
]

HOOKS = {
    "PreToolUse": [
        {
            "matcher": "Read|Edit|Write|MultiEdit|NotebookEdit|Grep|Glob|Bash|PowerShell",
            "hooks": [{"type": "command", "command": 'sh "$CLAUDE_PROJECT_DIR/.claude/hooks/proteger-secretos.sh"', "timeout": 15}],
        },
        {
            "matcher": "Edit|Write|MultiEdit|NotebookEdit|Bash|PowerShell",
            "hooks": [{"type": "command", "command": 'sh "$CLAUDE_PROJECT_DIR/.claude/hooks/restringir-documentos.sh"', "timeout": 15}],
        },
    ]
}


def cargar(nombre: str) -> dict:
    ruta = PERMISOS / f"{nombre}.json"
    if not ruta.is_file():
        disponibles = ", ".join(sorted(p.stem for p in PERMISOS.glob("*.json") if p.stem != "base"))
        sys.exit(f"No existe el fragmento «{nombre}». Disponibles: {disponibles}")
    return json.loads(ruta.read_text(encoding="utf-8"))


def con_carpeta(regla: str, carpeta: str) -> str:
    """Edit(/src/**) -> Edit(/frontend/src/**); Read(./x) -> Read(./frontend/x)."""
    m = re.match(r"^(Edit|Read)\((\.?/)(.*)\)$", regla)
    if not m:
        return regla
    herramienta, raiz, resto = m.groups()
    return f"{herramienta}({raiz}{carpeta.strip('/')}/{resto})"


def conflictos(permisos: dict) -> list:
    def partes(regla):
        m = re.match(r"^(\w+)\((.*)\)$", regla)
        return (m.group(1), m.group(2)) if m else (None, None)

    salida = []
    for lista in ("allow", "ask"):
        for regla in permisos[lista]:
            h1, valor = partes(regla)
            for negada in permisos["deny"]:
                h2, patron = partes(negada)
                if h1 and h1 == h2 and regla != negada and fnmatch.fnmatchcase(valor, patron):
                    salida.append(f"«{regla}» en {lista} queda anulada por «{negada}» en deny.")
    return salida


def lista_documentos(componentes: set) -> str:
    """documentos-permitidos.md sin los patrones de componentes inactivos."""
    texto = (PLANTILLA_CLAUDE / "hooks" / "documentos-permitidos.md").read_text(encoding="utf-8")
    lineas = []
    for linea in texto.splitlines():
        m = re.match(r"^- `([^`]+)`", linea)
        if m and COMPONENTE_DE_PATRON.get(m.group(1), None) not in (None, *componentes):
            continue
        lineas.append(linea)
    return "\n".join(lineas) + "\n"


def patrones(texto_lista: str) -> list:
    """Pares (subsección, patrón) de la sección «## Patrones»."""
    salida, dentro, sub = [], False, ""
    for linea in texto_lista.splitlines():
        if linea.startswith("## "):
            dentro = linea.startswith("## Patrones")
            continue
        if dentro and linea.startswith("### "):
            sub = linea[4:].strip()
        m = re.match(r"^- `([^`]+)`", linea)
        if dentro and m:
            salida.append((sub, m.group(1)))
    return salida


def combinar(stacks: list, api_rest: bool, texto_lista: str, dominios: list):
    """Devuelve (grupos, filas) donde filas alimenta las tablas del README."""
    grupos = {lista: {g: [] for g in GRUPOS} for lista in LISTAS}
    filas = {lista: [] for lista in LISTAS}

    def agregar(nombre: str, carpeta: str = ""):
        fragmento = cargar(nombre)
        razones = fragmento.get("razones", {})
        for lista in LISTAS:
            for grupo in GRUPOS:
                reglas = fragmento.get(lista, {}).get(grupo, [])
                if not reglas:
                    continue
                nuevas = []
                for regla in reglas:
                    regla = con_carpeta(regla, carpeta) if carpeta else regla
                    if regla not in grupos[lista][grupo]:
                        grupos[lista][grupo].append(regla)
                        nuevas.append(regla)
                etiqueta = NOMBRE_GRUPO[grupo]
                stack = NOMBRE_STACK.get(nombre, nombre)
                if stack:
                    etiqueta += f" ({stack}{' · ' + carpeta.strip('/') + '/' if carpeta else ''})"
                filas[lista].append((grupo, etiqueta, nuevas, razones.get(lista, {}).get(grupo, "")))

    agregar("base")
    carpetas = []
    for item in stacks:
        nombre, _, carpeta = item.partition(":")
        agregar(nombre, carpeta)
        if carpeta:
            regla = f"Bash(cd {carpeta.strip('/')})"
            if regla not in grupos["allow"]["sistema"]:
                grupos["allow"]["sistema"].append(regla)
                carpetas.append(regla)
    if carpetas:
        filas["allow"].append(("sistema", "Sistema (monorrepo)", carpetas, "Entrar a la carpeta de cada parte del monorrepo para ejecutar sus comandos."))

    editables = [f"Edit(/{p})" for _, p in patrones(texto_lista)
                 if p.startswith("_planificacion/") and p not in PROTEGIDOS_PLANIFICACION]
    grupos["allow"]["edicion"].extend(editables)
    filas["allow"].append(("edicion", "Edición (documentos de planificación)", editables,
                           "Solo los documentos vivos de `hooks/documentos-permitidos.md`. Un archivo con otro nombre no se crea en silencio: Claude Code pregunta, y además el hook `restringir-documentos.sh` lo bloquea."))
    if api_rest:
        grupos["allow"]["edicion"].append("Edit(/docs/api/**)")
        filas["allow"].append(("edicion", "Edición (contrato de la API)", ["Edit(/docs/api/**)"],
                               "El contrato OpenAPI es un documento vivo y cambia antes que el código."))
    if dominios:
        reglas = [f"WebFetch(domain:{d})" for d in dominios]
        grupos["deny"]["web"].extend(reglas)
        filas["deny"].append(("web", "Web (producción)", reglas,
                              "El sitio o el panel de producción no se consulta desde el agente: puede tener rutas que modifican datos con una simple visita."))
    for lista in LISTAS:
        filas[lista].sort(key=lambda f: GRUPOS.index(f[0]))
    return grupos, filas


def escribir_settings(grupos: dict) -> str:
    """JSON válido con una línea en blanco entre grupos de permisos, seguido de los hooks."""
    lineas = ["{", '  "$schema": "https://json.schemastore.org/claude-code-settings.json",',
              '  "permissions": {', '    "defaultMode": "default",']
    for i, lista in enumerate(LISTAS):
        reglas = [(g, r) for g in GRUPOS for r in grupos[lista][g]]
        lineas.append(f'    "{lista}": [')
        for j, (grupo, regla) in enumerate(reglas):
            if j > 0 and reglas[j - 1][0] != grupo:
                lineas.append("")
            coma = "," if j < len(reglas) - 1 else ""
            lineas.append(f"      {json.dumps(regla, ensure_ascii=False)}{coma}")
        lineas.append("    ]" + ("," if i < len(LISTAS) - 1 else ""))
    lineas.append("  },")
    hooks = json.dumps(HOOKS, ensure_ascii=False, indent=2).splitlines()
    lineas.append('  "hooks": ' + hooks[0])
    lineas += ["  " + l for l in hooks[1:]]
    lineas += ["}", ""]
    return "\n".join(lineas)


def tabla_reglas(filas: list) -> str:
    salida = ["| Grupo | Reglas | Por qué |", "| :---- | :----- | :------ |"]
    for _, etiqueta, reglas, razon in filas:
        if reglas:
            salida.append(f"| {etiqueta} | {', '.join(f'`{r}`' for r in reglas)} | {razon} |")
    return "\n".join(salida)


def tabla_comandos(componentes: set) -> str:
    salida = ["| Comando | Qué hace | Flujo completo |", "| :------ | :------- | :------------- |"]
    for _, uso, que, flujo, comp in COMANDOS:
        if comp is None or comp in componentes:
            salida.append(f"| `{uso}` | {que} | {flujo} |")
    return "\n".join(salida)


def tabla_documentos(texto_lista: str) -> str:
    grupos = {}
    for sub, patron in patrones(texto_lista):
        grupos.setdefault(sub, []).append(f"`{patron}`")
    salida = ["| Zona | Documentos permitidos |", "| :--- | :-------------------- |"]
    for sub, pats in grupos.items():
        salida.append(f"| {sub} | {' · '.join(pats)} |")
    return "\n".join(salida)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--proyecto", type=Path, help="Raíz del proyecto donde se escribe .claude/")
    ap.add_argument("--stack", action="append", default=[], help="Fragmento, opcionalmente con carpeta: nombre[:carpeta]")
    ap.add_argument("--nivel", choices=NIVELES, default="mediano", help="Nivel de proceso acordado (por defecto, mediano)")
    ap.add_argument("--api-rest", action="store_true", help="Permite editar docs/api/**")
    ap.add_argument("--auditoria", action="store_true", help="Activa las auditorías aunque el nivel sea pequeño")
    ap.add_argument("--linea-base-produccion", action="store_true", help="Agrega el documento de línea base de producción")
    ap.add_argument("--dominio-produccion", action="append", default=[], help="Dominio de producción que el agente no consulta")
    ap.add_argument("--listar", action="store_true", help="Muestra los fragmentos disponibles")
    args = ap.parse_args()

    if args.listar:
        for p in sorted(PERMISOS.glob("*.json")):
            print(f"{p.stem:14} {json.loads(p.read_text(encoding='utf-8')).get('descripcion', '')}")
        return
    if not args.stack or not args.proyecto:
        ap.error("indica al menos un --stack y el --proyecto")

    componentes = set()
    if args.nivel != "pequeno":
        componentes |= {"especificaciones", "auditoria"}
    if args.auditoria:
        componentes.add("auditoria")
    if args.linea_base_produccion:
        componentes.add("linea_base")

    destino = args.proyecto / ".claude"
    (destino / "hooks").mkdir(parents=True, exist_ok=True)
    (destino / "commands").mkdir(parents=True, exist_ok=True)

    texto_lista = lista_documentos(componentes)
    (destino / "hooks" / "documentos-permitidos.md").write_text(texto_lista, encoding="utf-8")
    for hook in ("proteger-secretos.sh", "restringir-documentos.sh"):
        datos = (PLANTILLA_CLAUDE / "hooks" / hook).read_bytes().replace(b"\r\n", b"\n")
        (destino / "hooks" / hook).write_bytes(datos)
        (destino / "hooks" / hook).chmod(0o755)
    for archivo, _, _, _, comp in COMANDOS:
        if comp is None or comp in componentes:
            shutil.copyfile(PLANTILLA_CLAUDE / "commands" / archivo, destino / "commands" / archivo)

    grupos, filas = combinar(args.stack, args.api_rest, texto_lista, args.dominio_produccion)
    texto = escribir_settings(grupos)
    datos = json.loads(texto)  # comprueba que el resultado sea JSON válido
    (destino / "settings.json").write_text(texto, encoding="utf-8")

    readme = (PLANTILLA_CLAUDE / "README.md").read_text(encoding="utf-8")
    readme = (readme.replace("{{TABLA_ALLOW}}", tabla_reglas(filas["allow"]))
                    .replace("{{TABLA_ASK}}", tabla_reglas(filas["ask"]))
                    .replace("{{TABLA_DENY}}", tabla_reglas(filas["deny"]))
                    .replace("{{TABLA_COMANDOS}}", tabla_comandos(componentes)))
    (destino / "README.md").write_text(readme, encoding="utf-8")

    agentes = args.proyecto / "AGENTS.md"
    tabla_en_agents = False
    if agentes.is_file():
        contenido = agentes.read_text(encoding="utf-8")
        if "{{TABLA_DOCUMENTOS_PERMITIDOS}}" in contenido:
            agentes.write_text(contenido.replace("{{TABLA_DOCUMENTOS_PERMITIDOS}}", tabla_documentos(texto_lista)), encoding="utf-8")
            tabla_en_agents = True

    total = sum(len(datos["permissions"][l]) for l in LISTAS)
    print(f".claude/ preparada en {destino} ({total} reglas, 2 hooks, componentes: {', '.join(sorted(componentes)) or 'ninguno'}).")
    if tabla_en_agents:
        print("AGENTS.md: tabla de documentos permitidos insertada.")
    elif agentes.is_file():
        print("AVISO: AGENTS.md no tiene el marcador {{TABLA_DOCUMENTOS_PERMITIDOS}}; revisa que su tabla coincida con la lista.")
    for p in conflictos(datos["permissions"]):
        print(f"AVISO: {p}")


if __name__ == "__main__":
    main()
