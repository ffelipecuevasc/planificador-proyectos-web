#!/usr/bin/env python3
"""Valida la documentación generada por la skill planificador-proyectos-web y,
opcionalmente, la empaqueta en un .zip listo para descomprimir en la raíz del repositorio.

Uso:
    python validar_documentacion.py <directorio> --tipo frontend|backend|fullstack
        [--nivel pequeno|mediano|complejo] [--api-rest] [--zip salida.zip]

El nivel (por defecto, mediano) decide qué archivos son obligatorios: auditorías,
especificaciones y el comando /auditar-epica desde nivel mediano (las auditorías también si
existe auditoria-tecnica.md); contrato OpenAPI desde nivel mediano si el proyecto expone una
API REST (--api-rest).

Errores (código de salida 1): archivos obligatorios faltantes (incluidos .claude/, sus hooks y
comandos, y las plantillas internas), la carpeta 99_bitacora/ de la estructura anterior,
nombres no ASCII o fuera de convención, archivos .md fuera de la lista de documentos
permitidos, settings.json inválido o sin hooks, hooks que no bloquean lo que deben en sus
pruebas, marcadores de plantilla sin rellenar, DESIGN.md en un backend, registro sin backlog,
iteraciones o especificaciones sin criterios de aceptación.
Advertencias: posibles rastros de tiempo en los documentos inmutables, criterios vagos,
iteraciones con más de 8 tareas, una épica 00 mal formada, épicas sin carpeta bitacoras/,
secciones clave de AGENTS.md ausentes y marcadores PENDIENTE_ que conviene revisar. El zip
solo se genera si no hay errores.
"""

import argparse
import fnmatch
import json
import os
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

INMUTABLES = ["AGENTS.md", "DESIGN.md", "README.md", "_planificacion/README.md"]

LISTA_DOCUMENTOS = ".claude/hooks/documentos-permitidos.md"

OBLIGATORIOS = [
    "AGENTS.md",
    "README.md",
    ".claude/settings.json",
    ".claude/README.md",
    ".claude/hooks/proteger-secretos.sh",
    ".claude/hooks/restringir-documentos.sh",
    LISTA_DOCUMENTOS,
    ".claude/commands/siguiente-epica.md",
    ".claude/commands/iteracion.md",
    "_planificacion/README.md",
    "_planificacion/plantillas/iteracion.md",
    "_planificacion/plantillas/definicion-epica.md",
    "_planificacion/plantillas/bitacora.md",
    "_planificacion/plantillas/bitacora-cierre.md",
    "_planificacion/plantillas/rda.md",
    "_planificacion/plantillas/propuestas-documentos-protegidos.md",
    "_planificacion/00_producto/producto.md",
    "_planificacion/00_producto/registro-pendientes.md",
    "_planificacion/00_producto/decisiones.md",
]

# Obligatorios que dependen del nivel de proceso o de un componente activo.
DESDE_MEDIANO = ["_planificacion/00_producto/auditoria-tecnica.md", "_planificacion/plantillas/especificacion.md"]
CON_AUDITORIAS = [".claude/commands/auditar-epica.md", "_planificacion/plantillas/auditoria.md"]
PROTEGIDOS_EN_DENY = ["Edit(/_planificacion/plantillas/**)", "Edit(/.claude/**)"]
CARPETAS_IGNORADAS = {".git", "node_modules", ".venv", "venv", "dist", "build", "target", ".astro", "__pycache__"}
NIVELES = ["pequeno", "mediano", "complejo"]
OPENAPI = ["docs/api/openapi.yaml", "docs/api/openapi.yml", "docs/api/openapi.json"]

# Criterios que no se pueden comprobar con una medición o un comando.
VAGOS = re.compile(
    r"se ve bien|funciona bien|funciona correctamente|de forma adecuada|adecuadamente|intuitiv|amigable|como corresponde",
    re.I,
)

# Rastros de tiempo que no deben aparecer en los documentos inmutables.
RASTROS = [
    (r"\b20\d{2}-\d{2}-\d{2}\b", "fecha"),
    (r"\biteraci[oó]n(es)?\s+\d{2}-\d{2}\b", "número de iteración"),
    (r"\b[ée]pica\s+\d{1,2}\b", "número de épica"),
    (r"\bRDA-\d{3}\b", "referencia a una RDA"),
    (r"\bAUD-\d{2}-\d{3}\b", "referencia a un hallazgo"),
    (r"\ba[uú]n no existe\b", "estado temporal"),
    (r"\bse (crea|creará|publica|publicará|agrega|agregará) en\b", "estado temporal"),
    (r"\b(por ahora|hasta ahora|a partir de ahora|antes era|ya no)\b", "estado temporal"),
    (r"\b(registro|historial) de cambios\b", "registro de cambios"),
    (r"\bchangelog\b", "registro de cambios"),
]

MARCADOR_PLANTILLA = re.compile(r"\{\{[A-Z0-9_]+\}\}|PLANTILLA:")
EXTENSIONES_CON_MARCADORES = ("*.md", "*.yaml", "*.yml", "*.json")

# Archivos que solo explican cómo usar los marcadores: sus menciones no son datos pendientes.
SIN_PENDIENTES_REALES = {
    "AGENTS.md",
    "_planificacion/README.md",
    ".claude/README.md",
    LISTA_DOCUMENTOS,
    "_planificacion/00_producto/registro-pendientes.md",
}
PREFIJOS_SIN_PENDIENTES = ("_planificacion/plantillas/", ".claude/commands/")

# Líneas que nombran el marcador como regla o criterio, no como dato faltante.
EXPLICATIVA = re.compile(
    r"marcador|mientras falten|se usa `PENDIENTE|usa `PENDIENTE|sin `PENDIENTE|ning[uú]n[^|]*`PENDIENTE|no (tiene|tenga|quede)[^|]*`PENDIENTE|queda alguno",
    re.I,
)


def seccion(texto: str, nombre: str):
    """Devuelve el texto de la sección «## N. Nombre» (por nombre, no por número)."""
    m = re.search(rf"^## (?:\d+\.\s*)?{re.escape(nombre)}.*?(?=^## |\Z)", texto, flags=re.S | re.M)
    return m.group(0) if m else None


def filas_de_seccion(texto: str, nombre: str) -> int:
    """Cuenta las filas con datos de la tabla de una sección del registro."""
    m = seccion(texto, nombre)
    if not m:
        return 0
    filas = [l for l in m.splitlines() if l.startswith("|")]
    datos = [l for l in filas[2:] if not re.match(r"^\|\s*—\s*\|", l)]
    return len(datos)


def revisar_registro(raiz: Path, pendientes: dict, errores: list, avisos: list):
    """Todo marcador real debe tener dónde estar registrado en registro-pendientes.md."""
    registro = raiz / "_planificacion/00_producto/registro-pendientes.md"
    if not pendientes or not registro.is_file():
        return
    texto = registro.read_text(encoding="utf-8")
    secciones = {"CLIENTE": "Datos pendientes del cliente", "DESARROLLADOR": "Decisiones por tomar"}
    for tipo, archivos in sorted(pendientes.items()):
        nombre = secciones[tipo]
        lista = ", ".join(sorted(archivos))
        if filas_de_seccion(texto, nombre) == 0:
            errores.append(f"Hay PENDIENTE_{tipo} en {lista}, pero la sección «{nombre}» de registro-pendientes.md está vacía.")
        else:
            avisos.append(f"PENDIENTE_{tipo} en {lista}: comprueba que cada uno tenga su fila en «{nombre}».")


def conflictos_de_permisos(permisos: dict) -> list:
    """Reglas de allow o ask que nunca se aplican porque una de deny las cubre."""
    def partes(regla):
        m = re.match(r"^(\w+)\((.*)\)$", regla)
        return (m.group(1), m.group(2)) if m else (None, None)

    conflictos = []
    for lista in ("allow", "ask"):
        for regla in permisos.get(lista, []):
            herramienta, valor = partes(regla)
            for negada in permisos.get("deny", []):
                h2, patron = partes(negada)
                if herramienta and herramienta == h2 and regla != negada and fnmatch.fnmatchcase(valor, patron):
                    conflictos.append(f"settings.json: «{regla}» en {lista} queda anulada por «{negada}» en deny.")
    return conflictos


def sin_codigo(texto: str) -> str:
    """Quita bloques de código y código en línea: ahí van ejemplos de formato, no rastros."""
    texto = re.sub(r"```.*?```", "", texto, flags=re.S)
    return re.sub(r"`[^`\n]*`", "", texto)


def revisar_criterios(rel: str, texto: str, errores: list, avisos: list, minimo: str):
    """Una iteración o especificación debe tener criterios de aceptación, y conviene que no sean vagos."""
    criterios = seccion(texto, "Criterios de aceptación")
    if criterios is None:
        errores.append(f"{rel} no tiene la sección «Criterios de aceptación».")
        return
    lineas = [l for l in criterios.splitlines()[1:] if re.match(minimo, l.strip())]
    if not lineas:
        errores.append(f"{rel}: la sección «Criterios de aceptación» no tiene ningún criterio.")
    for l in lineas:
        m = VAGOS.search(l)
        if m:
            avisos.append(f"{rel}: criterio posiblemente vago («{m.group(0)}»); un criterio se comprueba con una medición o un comando.")


MAX_TAREAS = 8


def revisar_tamano(rel: str, texto: str, avisos: list):
    """Tamaño máximo de una iteración: 8 tareas. Si se pasa, conviene partirla."""
    tareas = seccion(texto, "Tareas")
    if tareas is None:
        return
    n = len([l for l in tareas.splitlines()[1:] if re.match(r"^\d+\.\s", l.strip())])
    if n > MAX_TAREAS:
        avisos.append(f"{rel}: tiene {n} tareas (máximo {MAX_TAREAS}); conviene partir la iteración.")


def revisar_linea_base(ep: Path, avisos: list):
    """La épica 00 registra lo que ya existía: Terminada, sin iteraciones ni bitácoras."""
    definicion = ep / "definicion-epica-00.md"
    if definicion.is_file() and not re.search(r"^- \*\*Estado:\*\* Terminada", definicion.read_text(encoding="utf-8"), flags=re.M):
        avisos.append(f"{ep.name}: la épica de línea base debe estar «Terminada».")
    if list(ep.glob("iteracion-*.md")):
        avisos.append(f"{ep.name}: la épica de línea base no lleva iteraciones.")
    if (ep / "bitacoras").exists():
        avisos.append(f"{ep.name}: la épica de línea base no lleva carpeta de bitácoras.")


def leer_lista(raiz: Path):
    """Zonas y patrones de .claude/hooks/documentos-permitidos.md."""
    zonas, patrones, seccion_actual = [], [], ""
    archivo = raiz / LISTA_DOCUMENTOS
    if not archivo.is_file():
        return None, None
    for linea in archivo.read_text(encoding="utf-8").splitlines():
        if linea.startswith("## "):
            seccion_actual = linea[3:]
            continue
        m = re.match(r"^- `([^`]+)`", linea)
        if not m:
            continue
        valor = m.group(1).strip()
        while valor.startswith("./"):
            valor = valor[2:]
        if seccion_actual.startswith("Zonas"):
            zonas.append(valor.rstrip("/"))
        elif seccion_actual.startswith("Patrones"):
            patrones.append(valor)
    return zonas, patrones


def calza(rel: str, patron: str) -> bool:
    """Mismo criterio que el hook: * dentro de un nivel de carpeta."""
    return rel.count("/") == patron.count("/") and fnmatch.fnmatchcase(rel, patron)


def archivos(raiz: Path, patron: str):
    for f in raiz.rglob(patron):
        partes = f.relative_to(raiz).parts
        if not any(p in CARPETAS_IGNORADAS for p in partes[:-1]):
            yield f


def revisar_documentos(raiz: Path, errores: list):
    """Capa 4: todo .md de las zonas de documentación debe calzar con la lista."""
    zonas, patrones = leer_lista(raiz)
    if zonas is None:
        return
    if not patrones:
        errores.append(f"{LISTA_DOCUMENTOS} no tiene patrones en la sección «Patrones».")
        return
    for f in archivos(raiz, "*.md"):
        rel = f.relative_to(raiz).as_posix()
        en_zona = any((z == "" and "/" not in rel) or (z and rel.startswith(z + "/")) for z in zonas)
        if en_zona and not any(calza(rel, p) for p in patrones):
            errores.append(f"{rel} no está en la lista de documentos permitidos: elimínalo o apruébalo agregando su patrón a {LISTA_DOCUMENTOS} y a AGENTS.md.")


def aprobado_explicitamente(raiz: Path, rel: str) -> bool:
    """Un archivo histórico que la lista nombra sin comodines (por ejemplo, tras una migración)."""
    _, patrones = leer_lista(raiz)
    return bool(patrones) and rel in [p for p in patrones if "*" not in p]


PRUEBAS_DE_HOOKS = [
    ("proteger-secretos.sh", {"tool_name": "Read", "tool_input": {"file_path": ".env"}}, 2),
    ("proteger-secretos.sh", {"tool_name": "Read", "tool_input": {"file_path": ".env.example"}}, 0),
    ("proteger-secretos.sh", {"tool_name": "Bash", "tool_input": {"command": "cat .env.production | grep KEY"}}, 2),
    ("proteger-secretos.sh", {"tool_name": "PowerShell", "tool_input": {"command": "Get-Content .env"}}, 2),
    ("proteger-secretos.sh", {"tool_name": "Bash", "tool_input": {"command": "grep -rn process.env src"}}, 0),
    ("restringir-documentos.sh", {"tool_name": "Write", "tool_input": {"file_path": "{EPICA}/bitacoras/zz-prueba-del-validador.md", "content": "x"}}, 2),
    ("restringir-documentos.sh", {"tool_name": "Write", "tool_input": {"file_path": "{EPICA}/bitacoras/bitacora-99-99-zz-prueba-del-validador.md", "content": "x"}}, 0),
    ("restringir-documentos.sh", {"tool_name": "Bash", "tool_input": {"command": "echo x > _planificacion/zz-prueba-del-validador.md"}}, 2),
    ("restringir-documentos.sh", {"tool_name": "Write", "tool_input": {"file_path": "src/content/blog/entrada.md", "content": "x"}}, 0),
]


def probar_hooks(raiz: Path, errores: list, avisos: list):
    """Ejecuta los hooks con casos conocidos: deben bloquear (2) o dejar pasar (0)."""
    sh = shutil.which("sh")
    if not sh:
        avisos.append("No hay `sh` en esta máquina: no se pudieron probar los hooks. Pruébalos con la «Prueba rápida» de .claude/README.md.")
        return
    epicas = sorted(p for p in (raiz / "_planificacion/10_epicas").glob("epica-[0-9][0-9]-*") if p.is_dir() and not p.name.startswith("epica-00"))
    epica = (epicas[0] if epicas else raiz / "_planificacion/10_epicas/epica-01-prueba").relative_to(raiz).as_posix()
    entorno = dict(os.environ, CLAUDE_PROJECT_DIR=str(raiz))
    for hook, caso, esperado in PRUEBAS_DE_HOOKS:
        script = raiz / ".claude/hooks" / hook
        if not script.is_file():
            continue
        entrada = json.dumps(caso, ensure_ascii=False).replace("{EPICA}", epica)
        try:
            r = subprocess.run([sh, str(script)], input=entrada.encode("utf-8"), capture_output=True, env=entorno, cwd=raiz, timeout=20)
            codigo = r.returncode
        except (OSError, subprocess.TimeoutExpired) as e:
            errores.append(f"No se pudo ejecutar {hook}: {e}")
            continue
        if codigo != esperado:
            accion = "bloquear" if esperado == 2 else "dejar pasar"
            objetivo = (caso["tool_input"].get("file_path") or caso["tool_input"].get("command")).replace("{EPICA}", epica)
            errores.append(f"{hook} debía {accion} {caso['tool_name']} «{objetivo}» y respondió con código {codigo}.")


def validar(raiz: Path, tipo: str, nivel: str = "mediano", api_rest: bool = False):
    errores, avisos = [], []

    obligatorios = list(OBLIGATORIOS)
    con_auditorias = nivel != "pequeno" or (raiz / "_planificacion/00_producto/auditoria-tecnica.md").is_file()
    if nivel != "pequeno":
        obligatorios += DESDE_MEDIANO
    if con_auditorias:
        obligatorios += [c for c in CON_AUDITORIAS if c not in obligatorios]
    if tipo in ("frontend", "fullstack"):
        obligatorios.append("DESIGN.md")
    for rel in obligatorios:
        if not (raiz / rel).is_file():
            errores.append(f"Falta el archivo obligatorio: {rel}")

    if tipo == "backend" and (raiz / "DESIGN.md").exists():
        errores.append("Un proyecto backend no lleva DESIGN.md: sus convenciones van en AGENTS.md.")

    if not (raiz / "_planificacion/10_epicas").is_dir():
        errores.append("Falta la carpeta: _planificacion/10_epicas/")
    if (raiz / "_planificacion/99_bitacora").exists():
        errores.append("Existe _planificacion/99_bitacora/ (estructura anterior): las bitácoras van en la carpeta bitacoras/ de cada épica. Migra según la guía, sección 22.")

    epicas = sorted(p for p in (raiz / "_planificacion/10_epicas").glob("epica-*") if p.is_dir())
    if not epicas:
        errores.append("No hay ninguna carpeta de épica en _planificacion/10_epicas/.")
    for ep in epicas:
        m = re.match(r"epica-(\d{2})-[a-z0-9-]+$", ep.name)
        if not m:
            errores.append(f"Nombre de épica fuera de convención: {ep.name} (se espera epica-NN-nombre)")
            continue
        nn = m.group(1)
        if not (ep / f"definicion-epica-{nn}.md").is_file():
            errores.append(f"Falta {ep.name}/definicion-epica-{nn}.md")
        for f in sorted(ep.iterdir()):
            rel = f.relative_to(raiz).as_posix()
            if f.is_dir():
                if f.name != "bitacoras":
                    errores.append(f"Carpeta fuera de convención: {rel} (una épica solo lleva la carpeta bitacoras/)")
                continue
            if f.name.startswith("definicion-") or f.name == ".gitkeep":
                continue
            if not re.match(rf"iteracion-{nn}-\d{{2}}-[a-z0-9-]+\.md$", f.name):
                if not aprobado_explicitamente(raiz, rel):
                    errores.append(f"Nombre fuera de convención: {rel}")
                continue
            texto_it = f.read_text(encoding="utf-8")
            revisar_criterios(f"{ep.name}/{f.name}", texto_it, errores, avisos, r"^- \[[ xX]\]")
            revisar_tamano(f"{ep.name}/{f.name}", texto_it, avisos)
        if nn == "00":
            revisar_linea_base(ep, avisos)
            continue
        bitacoras = ep / "bitacoras"
        if not bitacoras.is_dir():
            avisos.append(f"Falta la carpeta {ep.name}/bitacoras/ (créala con un .gitkeep).")
            continue
        for f in sorted(bitacoras.iterdir()):
            rel = f.relative_to(raiz).as_posix()
            if f.name == ".gitkeep":
                continue
            if f.is_dir() or not re.match(rf"bitacora-{nn}-(\d{{2}}(-[a-z0-9-]+)?|cierre)\.md$", f.name):
                if not aprobado_explicitamente(raiz, rel):
                    errores.append(f"Nombre de bitácora fuera de convención: {rel} (bitacora-{nn}-YY.md, bitacora-{nn}-YY-sufijo.md o bitacora-{nn}-cierre.md)")

    auditorias = raiz / "_planificacion/00_producto/auditorias"
    if auditorias.is_dir():
        for f in sorted(auditorias.iterdir()):
            if f.name != ".gitkeep" and not re.match(r"auditoria-\d{2}\.md$", f.name):
                errores.append(f"Nombre de auditoría fuera de convención: {f.relative_to(raiz).as_posix()} (auditoria-NN.md)")

    specs_dir = raiz / "_planificacion/20_especificaciones"
    if nivel != "pequeno" and not specs_dir.is_dir():
        errores.append("Falta la carpeta: _planificacion/20_especificaciones/ (desde nivel mediano; puede nacer con un .gitkeep).")
    if specs_dir.is_dir():
        specs = sorted(specs_dir.glob("*.md"))
        if nivel == "pequeno" and specs:
            avisos.append("Hay especificaciones en un proyecto de nivel pequeño: si son varias, conviene revisar el nivel de proceso.")
        for f in specs:
            rel = f.relative_to(raiz).as_posix()
            if not re.match(r"spec-[a-z0-9-]+\.md$", f.name):
                errores.append(f"Nombre de especificación fuera de convención: {rel} (se espera spec-nombre.md)")
                continue
            texto = f.read_text(encoding="utf-8")
            if not re.search(r"^- \*\*Estado:\*\* (Borrador|Aprobada|Vigente|Reemplazada)", texto, flags=re.M):
                avisos.append(f"{rel}: no declara un estado válido (Borrador, Aprobada, Vigente o Reemplazada).")
            revisar_criterios(rel, texto, errores, avisos, r"^- (\*\*)?CA-\d{2}|^- \[[ xX]\]")

    if api_rest:
        contrato = next((raiz / c for c in OPENAPI if (raiz / c).is_file()), None)
        if contrato is None:
            if nivel == "pequeno":
                avisos.append("API REST sin contrato docs/api/openapi.yaml: en nivel pequeño es recomendado, no obligatorio.")
            else:
                errores.append("Falta el contrato de la API: docs/api/openapi.yaml (obligatorio desde nivel mediano con --api-rest).")
        else:
            texto = contrato.read_text(encoding="utf-8")
            if not re.search(r'^\s*"?openapi"?\s*:\s*"?3\.', texto, flags=re.M):
                errores.append(f"{contrato.relative_to(raiz).as_posix()} no declara una versión OpenAPI 3.x.")
            if not re.search(r'^\s*"?paths"?\s*:', texto, flags=re.M):
                errores.append(f"{contrato.relative_to(raiz).as_posix()} no tiene la sección «paths».")

    revisar_documentos(raiz, errores)
    probar_hooks(raiz, errores, avisos)

    for p in archivos(raiz, "*"):
        rel = p.relative_to(raiz).as_posix()
        if not rel.isascii():
            errores.append(f"Nombre con caracteres no ASCII (tildes o ñ): {rel}")

    ajustes = raiz / ".claude/settings.json"
    if ajustes.is_file():
        try:
            datos = json.loads(ajustes.read_text(encoding="utf-8"))
            permisos = datos.get("permissions", {})
            for lista in ("allow", "ask", "deny"):
                if lista not in permisos:
                    errores.append(f"settings.json no tiene la lista permissions.{lista}")
            deny = permisos.get("deny", [])
            for doc in INMUTABLES:
                if f"Edit(/{doc})" not in deny:
                    errores.append(f"settings.json no deniega la edición de {doc}")
            for regla in PROTEGIDOS_EN_DENY:
                if regla not in deny:
                    errores.append(f"settings.json no tiene {regla} en deny.")
            errores.extend(conflictos_de_permisos(permisos))
            comandos_hooks = json.dumps(datos.get("hooks", {}).get("PreToolUse", []))
            for hook in ("proteger-secretos.sh", "restringir-documentos.sh"):
                if hook not in comandos_hooks:
                    errores.append(f"settings.json no registra el hook {hook} en PreToolUse.")
        except json.JSONDecodeError as e:
            errores.append(f"settings.json no es JSON válido: {e}")

    for patron in EXTENSIONES_CON_MARCADORES:
        for f in archivos(raiz, patron):
            texto = f.read_text(encoding="utf-8")
            rel = f.relative_to(raiz).as_posix()
            for m in MARCADOR_PLANTILLA.finditer(texto):
                errores.append(f"Marcador de plantilla sin rellenar en {rel}: {m.group(0)}")

    agentes = raiz / "AGENTS.md"
    if agentes.is_file() and "definición de preparada" not in agentes.read_text(encoding="utf-8").lower():
        avisos.append("AGENTS.md no tiene la «Definición de preparada»: sin ella, el agente empieza iteraciones que no están listas.")
    if agentes.is_file():
        texto_agentes = agentes.read_text(encoding="utf-8")
        for nombre in ("Documentos permitidos", "Estándares de calidad"):
            if seccion(texto_agentes, nombre) is None:
                avisos.append(f"AGENTS.md no tiene la sección «{nombre}».")

    registro = raiz / "_planificacion/00_producto/registro-pendientes.md"
    if registro.is_file() and seccion(registro.read_text(encoding="utf-8"), "Backlog") is None:
        errores.append("registro-pendientes.md no tiene la sección «Backlog».")

    pendientes = {}
    for f in list(archivos(raiz, "*.md")) + list(archivos(raiz, "*.yaml")) + list(archivos(raiz, "*.yml")):
        texto = f.read_text(encoding="utf-8")
        rel = f.relative_to(raiz).as_posix()
        if rel in SIN_PENDIENTES_REALES or rel.startswith(PREFIJOS_SIN_PENDIENTES):
            continue
        for linea in texto.splitlines():
            if EXPLICATIVA.search(linea):
                continue
            for m in re.finditer(r"PENDIENTE_(CLIENTE|DESARROLLADOR)", linea):
                pendientes.setdefault(m.group(1), set()).add(rel)

    revisar_registro(raiz, pendientes, errores, avisos)

    for doc in INMUTABLES:
        f = raiz / doc
        if not f.is_file():
            continue
        lineas = sin_codigo(f.read_text(encoding="utf-8")).splitlines()
        for i, linea in enumerate(lineas, 1):
            for patron, tipo_rastro in RASTROS:
                for m in re.finditer(patron, linea, flags=re.I):
                    avisos.append(f"{doc}, línea ~{i}: posible {tipo_rastro} en un documento inmutable: «{m.group(0)}»")

    if (raiz / "README.md").is_file():
        texto = (raiz / "README.md").read_text(encoding="utf-8")
        for bloque in re.findall(r"```(\w*)", texto)[::2]:
            if bloque not in ("text", ""):
                errores.append(f"README.md tiene un bloque de código «{bloque}»: el README raíz no lleva código ni comandos (solo se admite «text» para el árbol de carpetas).")

    return errores, avisos


def empaquetar(raiz: Path, salida: Path):
    salida.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(salida, "w", zipfile.ZIP_DEFLATED) as z:
        for p in sorted(raiz.rglob("*")):
            if p.is_file():
                z.write(p, p.relative_to(raiz).as_posix())
    return salida


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("directorio", type=Path)
    ap.add_argument("--tipo", required=True, choices=["frontend", "backend", "fullstack"])
    ap.add_argument("--nivel", choices=NIVELES, default="mediano", help="Nivel de proceso acordado (por defecto, mediano)")
    ap.add_argument("--api-rest", action="store_true", help="El proyecto expone una API REST")
    ap.add_argument("--zip", type=Path, help="Ruta del .zip a generar si no hay errores")
    args = ap.parse_args()

    raiz = args.directorio.resolve()
    if not raiz.is_dir():
        print(f"No existe el directorio: {raiz}")
        sys.exit(2)

    errores, avisos = validar(raiz, args.tipo, args.nivel, args.api_rest)
    for e in errores:
        print(f"ERROR: {e}")
    for a in avisos:
        print(f"AVISO: {a}")
    print(f"\n{len(errores)} error(es), {len(avisos)} aviso(s).")

    if errores:
        sys.exit(1)
    if args.zip:
        print(f"Zip generado: {empaquetar(raiz, args.zip.resolve())}")


if __name__ == "__main__":
    main()
