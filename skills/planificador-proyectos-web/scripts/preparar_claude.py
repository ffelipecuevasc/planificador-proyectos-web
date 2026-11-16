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
grupos (comandos, Git, sistema, edición, lectura, web), sin reglas repetidas. Después hay
que revisar el resultado contra el proyecto real: los fragmentos son un punto de partida.

Si una regla de allow o ask queda anulada por una de deny (también cuando son idénticas), el
script se detiene sin escribir nada y muestra los conflictos.

Un proyecto que ya tiene .claude/ nunca se sobrescribe en silencio. Hay que elegir un modo:
    --simular     muestra las diferencias con lo que hay y no escribe nada.
    --actualizar  fusiona settings.json: conserva las claves ajenas (env, otros hooks,
                  additionalDirectories…), une las listas de permisos sin duplicados y agrega
                  los hooks que falten. Muestra la diferencia antes de escribir. Si el
                  settings.json actual no es JSON válido, se detiene sin tocar nada. Los demás
                  archivos (README, hooks, comandos, lista) solo se escriben si no existen: si
                  ya existen y difieren, se conservan y se informan.
    --reemplazar  escribe todo de nuevo, como en un proyecto sin .claude/. Úsalo solo con la
                  autorización explícita del desarrollador y después de un commit.
"""

import argparse
import difflib
import fnmatch
import json
import re
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
    """Reglas de allow o ask que una de deny anula, incluida la regla idéntica.

    El chequeo es aproximado: fnmatch no reproduce las reglas de permisos de Claude Code
    (en fnmatch, * también cruza /, ** no tiene semántica propia y los corchetes son clases
    de caracteres). Puede marcar de más, pero no deja pasar una regla idéntica.
    """
    def partes(regla):
        m = re.match(r"^(\w+)\((.*)\)$", regla)
        return (m.group(1), m.group(2)) if m else (None, None)

    salida = []
    for lista in ("allow", "ask"):
        for regla in permisos.get(lista, []):
            h1, valor = partes(regla)
            for negada in permisos.get("deny", []):
                h2, patron = partes(negada)
                if h1 and h1 == h2 and (regla == negada or fnmatch.fnmatchcase(valor, patron)):
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


def fusionar(actual: dict, generado: dict) -> dict:
    """settings.json actual + el generado: conserva todo lo ajeno y agrega lo que falta."""
    resultado = json.loads(json.dumps(actual))  # copia profunda
    resultado.setdefault("$schema", generado["$schema"])
    permisos = resultado.setdefault("permissions", {})
    permisos.setdefault("defaultMode", generado["permissions"]["defaultMode"])
    for lista in LISTAS:
        existentes = permisos.setdefault(lista, [])
        existentes.extend(r for r in generado["permissions"][lista] if r not in existentes)
    hooks = resultado.setdefault("hooks", {})
    for evento, entradas in generado["hooks"].items():
        actuales = hooks.setdefault(evento, [])
        registrados = {h.get("command") for e in actuales if isinstance(e, dict) for h in e.get("hooks", []) if isinstance(h, dict)}
        for entrada in entradas:
            if not all(h["command"] in registrados for h in entrada["hooks"]):
                actuales.append(entrada)
    return resultado


def diferencia(ruta: str, antes: str, despues: str) -> str:
    lineas = difflib.unified_diff(antes.splitlines(), despues.splitlines(),
                                  fromfile=f"{ruta} (actual)", tofile=f"{ruta} (propuesto)", lineterm="")
    return "\n".join(lineas)


def leer_texto(ruta: Path) -> str:
    return ruta.read_bytes().decode("utf-8", errors="replace").replace("\r\n", "\n")


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
    modo = ap.add_mutually_exclusive_group()
    modo.add_argument("--simular", action="store_true", help="Muestra las diferencias con el .claude/ actual y no escribe nada")
    modo.add_argument("--actualizar", action="store_true", help="Fusiona con el .claude/ actual sin borrar lo ajeno")
    modo.add_argument("--reemplazar", action="store_true", help="Sobrescribe el .claude/ actual (requiere autorización explícita)")
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

    # 1. Todo se arma en memoria; nada se escribe hasta decidir el modo.
    texto_lista = lista_documentos(componentes)
    archivos = {"hooks/documentos-permitidos.md": texto_lista}
    for hook in ("proteger-secretos.sh", "restringir-documentos.sh"):
        archivos[f"hooks/{hook}"] = leer_texto(PLANTILLA_CLAUDE / "hooks" / hook)
    for archivo, _, _, _, comp in COMANDOS:
        if comp is None or comp in componentes:
            archivos[f"commands/{archivo}"] = leer_texto(PLANTILLA_CLAUDE / "commands" / archivo)
    grupos, filas = combinar(args.stack, args.api_rest, texto_lista, args.dominio_produccion)
    texto_settings = escribir_settings(grupos)
    generado = json.loads(texto_settings)  # comprueba que el resultado sea JSON válido
    readme = (PLANTILLA_CLAUDE / "README.md").read_text(encoding="utf-8")
    archivos["README.md"] = (readme.replace("{{TABLA_ALLOW}}", tabla_reglas(filas["allow"]))
                                   .replace("{{TABLA_ASK}}", tabla_reglas(filas["ask"]))
                                   .replace("{{TABLA_DENY}}", tabla_reglas(filas["deny"]))
                                   .replace("{{TABLA_COMANDOS}}", tabla_comandos(componentes)))

    # 2. ¿Hay un .claude/ con contenido? Entonces hay que elegir modo.
    existentes = [r for r in [*archivos, "settings.json"] if (destino / r).exists()]
    if existentes and not (args.simular or args.actualizar or args.reemplazar):
        print(f"{destino} ya existe y tiene: {', '.join(sorted(existentes))}.", file=sys.stderr)
        print("No se escribió nada. Elige un modo: --simular (ver diferencias), --actualizar (fusionar sin borrar lo ajeno) "
              "o --reemplazar (sobrescribir, solo con autorización explícita).", file=sys.stderr)
        sys.exit(1)

    settings_final = generado
    if (args.actualizar or args.simular) and (destino / "settings.json").exists():
        try:
            actual = json.loads(leer_texto(destino / "settings.json"))
            if not isinstance(actual, dict):
                raise ValueError("no es un objeto JSON")
        except ValueError as e:
            print(f"ERROR: el settings.json actual no es JSON válido ({e}). No se escribió nada: corrígelo a mano y vuelve a ejecutar.", file=sys.stderr)
            sys.exit(1)
        settings_final = fusionar(actual, generado)
        texto_settings = json.dumps(settings_final, ensure_ascii=False, indent=2) + "\n"

    # 3. Conflictos: con el resultado final (en --actualizar incluye tus reglas propias).
    problemas = conflictos(settings_final.get("permissions", {}))
    if problemas:
        print("ERROR: reglas de allow o ask anuladas por deny. No se escribió nada:", file=sys.stderr)
        for pr in problemas:
            print(f"  - {pr}", file=sys.stderr)
        if args.actualizar or args.simular:
            print("Si alguna es una regla propia del proyecto, quítala o cámbiala en el settings.json actual y vuelve a "
                  "ejecutar; o usa --reemplazar si el desarrollador lo autoriza.", file=sys.stderr)
        if not args.simular:
            sys.exit(1)
    archivos["settings.json"] = texto_settings

    # 4. Qué se escribe y qué se conserva.
    escribir, conservados, iguales = {}, [], []
    for rel, contenido in archivos.items():
        ruta = destino / rel
        if not ruta.exists() or args.reemplazar or (rel == "settings.json" and not args.simular):
            if ruta.exists() and leer_texto(ruta) == contenido:
                iguales.append(rel)
            else:
                escribir[rel] = contenido
        elif leer_texto(ruta) == contenido:
            iguales.append(rel)
        else:
            conservados.append(rel)

    if args.simular or args.actualizar:
        for rel in [*escribir, *conservados]:
            ruta = destino / rel
            if ruta.exists():
                print(diferencia(f".claude/{rel}", leer_texto(ruta), archivos[rel]) or f"(sin cambios en .claude/{rel})")
                print()
    if args.simular:
        if problemas:
            print("Simulación: hay conflictos entre allow y deny (detalle arriba); --actualizar se detendría. No se escribió nada.")
            sys.exit(1)
        print(f"Simulación: se escribirían {len(escribir)} archivo(s) y se conservarían {len(conservados)}. No se escribió nada.")
        return

    for rel, contenido in escribir.items():
        ruta = destino / rel
        ruta.parent.mkdir(parents=True, exist_ok=True)
        ruta.write_bytes(contenido.encode("utf-8"))
        if rel.endswith(".sh"):
            ruta.chmod(0o755)

    agentes = args.proyecto / "AGENTS.md"
    tabla_en_agents = False
    if agentes.is_file():
        contenido = agentes.read_text(encoding="utf-8")
        if "{{TABLA_DOCUMENTOS_PERMITIDOS}}" in contenido:
            agentes.write_text(contenido.replace("{{TABLA_DOCUMENTOS_PERMITIDOS}}", tabla_documentos(texto_lista)), encoding="utf-8")
            tabla_en_agents = True

    total = sum(len(settings_final["permissions"].get(l, [])) for l in LISTAS)
    accion = "actualizada" if args.actualizar else "preparada"
    print(f".claude/ {accion} en {destino} ({total} reglas, {len(escribir)} archivo(s) escrito(s), componentes: {', '.join(sorted(componentes)) or 'ninguno'}).")
    for rel in conservados:
        print(f"CONSERVADO: .claude/{rel} ya existía y difiere de la versión de la skill; se dejó como estaba (la diferencia está arriba).")
    if tabla_en_agents:
        print("AGENTS.md: tabla de documentos permitidos insertada.")
    elif agentes.is_file():
        print("AVISO: AGENTS.md no tiene el marcador {{TABLA_DOCUMENTOS_PERMITIDOS}}; revisa que su tabla coincida con la lista.")


if __name__ == "__main__":
    main()
