#!/usr/bin/env python3
"""
revisar_caption.py - revisa un caption de Instagram de Desarmalo.cl y muestra
exactamente lo que se ve en el feed antes del "... más".

Instagram muestra unos 125 caracteres del caption y esconde el resto detrás de
un toque. Casi todos los captions que fallan, fallan ahí. Este script imprime
esa ventana como una caja, tal como la lee alguien que va pasando, y después
revisa lo que vale la pena revisar, incluidas las reglas de marca de Desarmalo
(tuteo, nombre de la marca, sin datos inventados).

El corte de 125 es aproximado: cambia con el teléfono, el tamaño de letra y
los saltos de línea. Por eso conviene dejar margen. Se ajusta con --corte.

Adaptado de caption.py de instagram-agent-skill (MIT, (c) 2026 Jake
Schincariol). Ver ../TERCEROS.md.

Uso
  python3 revisar_caption.py caption.txt
  python3 revisar_caption.py caption.txt --palabras "repuestos usados,desarmaduría"
  python3 revisar_caption.py content/carruseles/pieza.md      # lee la sección "## Caption"
  python3 revisar_caption.py caption.txt --json
"""

import argparse
import json
import re
import sys
import textwrap

LIMITE = 2200            # Límite duro de Instagram para un caption.
CORTE = 125              # Más o menos donde el feed corta a "... más".
TOPE_HASHTAGS = 5        # Tope por post o reel desde el 18 dic 2025 (antes 30),
                         # anunciado por la cuenta @creators de Instagram.

HASHTAG_RE = re.compile(r"(?:^|\s)(#\w+)")
MENCION_RE = re.compile(r"(?:^|\s)(@[\w.]+)")
# URLs con ruta. "desarmalo.cl" a secas es el nombre de la marca y no cuenta.
LINK_RE = re.compile(r"https?://\S+|\bwww\.\S+|\b[\w-]+\.(?:cl|com|co|io|net|org|ai|app)/\S+",
                     re.IGNORECASE)
EMOJI_RE = re.compile(r"[\U0001F300-\U0001FAFF☀-➿←-⇿]")
CONCRETO_RE = re.compile(r"\$\s?\d|\b\d[\d.,]*\b|(?<!^)(?<![.!?¿¡] )\b[A-ZÁÉÍÓÚÑ][a-záéíóúñ]{2,}",
                         re.MULTILINE)

LLAMADOS = [
    (re.compile(r"(?i)\bcomenta(?:nos)? (?:la palabra |\")?[A-ZÁÉÍÓÚÑ0-9]{2,}\b"), "comentar una palabra"),
    (re.compile(r"(?i)\b(?:escr[ií]benos|m[aá]ndanos un (?:dm|mensaje)|h[aá]blanos)\b"), "escribirnos"),
    (re.compile(r"(?i)\bgu[aá]rd(?:a|alo|ala|a este)\b"), "guardar"),
    (re.compile(r"(?i)\bcomp[aá]rt(?:e|elo|ela)\b"), "compartir"),
    (re.compile(r"(?i)\bs[ií]gu?enos\b"), "seguirnos"),
    (re.compile(r"(?i)\b(?:link|enlace) en (?:la |nuestra )?bio\b"), "link en la bio"),
    (re.compile(r"(?i)\bdesliza\b"), "deslizar"),
    (re.compile(r"(?i)\bpubl[ií]ca(?:lo|la)?\b|\bpublica tu anuncio\b"), "publicar un anuncio"),
    (re.compile(r"(?i)\bb[uú]sca(?:lo|la)?\b"), "buscar en el sitio"),
    (re.compile(r"(?i)\bcu[eé]ntanos\b|\b¿(?:cu[aá]l|qu[eé]) (?:prefieres|eliges)\b"), "responder una pregunta"),
]

RELLENO = {"#viral", "#fyp", "#explore", "#explorepage", "#foryou", "#foryoupage",
           "#parati", "#trending", "#tendencia", "#instagood", "#love", "#follow",
           "#like4like", "#reels", "#reelsinstagram", "#viralreels", "#instadaily",
           "#chile"}

# Voseo: la marca tutea ("busca", no "buscá"). Lista corta de formas comunes.
VOSEO_RE = re.compile(
    r"(?i)\b(?:buscá|publicá|contactá|mirá|entrá|comprá|vendé|escribí|iniciá|ingresá|"
    r"revisá|probá|fijate|tenés|podés|querés|sabés|vos)\b")

# La marca es "Desarmalo.cl" con D mayúscula. En minúscula sólo vale como URL.
MARCA_MINUSCULA_RE = re.compile(r"(?<![\w/.@#])desarmalo(?!\.cl)\b")


def extraer_caption(texto):
    """Si es una pieza de content/ (.md con frontmatter), toma sólo "## Caption"."""
    if not texto.lstrip().startswith("---"):
        return texto
    m = re.search(r"(?ms)^##\s*Caption\s*\n(.*?)(?=^##\s|\Z)", texto)
    if not m:
        sys.exit("La pieza no tiene una sección '## Caption'.")
    return m.group(1)


def ventana_visible(texto, corte):
    """Lo que muestra el feed. Instagram corta a mitad de palabra, así que esto también."""
    plano = texto.strip()
    return plano if len(plano) <= corte else plano[:corte]


def dibujar_caja(ventana, cortado, out=sys.stdout, ancho=52):
    print("\n  LO QUE SE VE EN EL FEED", file=out)
    print("  +" + "-" * (ancho + 2) + "+", file=out)
    lineas = []
    for crudo in ventana.split("\n"):
        lineas.extend(textwrap.wrap(crudo, ancho) or [""])
    for linea in lineas[:8]:
        print(f"  | {linea:<{ancho}} |", file=out)
    cola = "... más" if cortado else "(cabe entero)"
    print("  +" + "-" * (ancho + 2 - len(cola) - 2) + f" {cola} " + "+", file=out)


def analizar(texto, corte=CORTE, palabras=None):
    limpio = texto.strip()
    chars = len(limpio)
    lineas = limpio.split("\n")
    primera = lineas[0].strip() if lineas else ""
    tags = HASHTAG_RE.findall(limpio)
    menciones = MENCION_RE.findall(limpio)
    links = LINK_RE.findall(limpio)
    emoji = EMOJI_RE.findall(limpio)
    ventana = ventana_visible(limpio, corte)
    cortado = chars > corte
    llamados = [nombre for patron, nombre in LLAMADOS if patron.search(limpio)]
    relleno = [t for t in tags if t.lower() in RELLENO]
    palabras = [p.strip() for p in (palabras or []) if p.strip()]

    revisiones = []

    def add(nombre, estado, detalle):
        revisiones.append({"revision": nombre, "estado": estado, "detalle": detalle})

    add("LARGO", "FALLA" if chars > LIMITE else "OK",
        f"{chars} / {LIMITE} caracteres" + (f", {chars - LIMITE} de más" if chars > LIMITE else ""))

    if not primera:
        add("PRIMERA LÍNEA", "FALLA", "el caption parte con una línea en blanco")
    elif primera.startswith(("#", "@")):
        add("PRIMERA LÍNEA", "FALLA", "parte con un hashtag o una mención, y ese es el lugar más valioso")
    elif len(primera) > corte:
        add("PRIMERA LÍNEA", "OJO",
            f"{len(primera)} caracteres, se corta en {corte} a mitad de idea. "
            "Sirve si el corte deja intriga, no si corta una frase a medias")
    else:
        add("PRIMERA LÍNEA", "OK", f"{len(primera)} caracteres, se ve entera")

    n_concretos = len(CONCRETO_RE.findall(ventana))
    add("GANCHO CONCRETO", "OK" if n_concretos else "OJO",
        f"{n_concretos} número(s) o nombre(s) antes del corte"
        + ("" if n_concretos else ": nada concreto antes del toque"))

    if len(tags) > TOPE_HASHTAGS:
        add("HASHTAGS", "FALLA", f"{len(tags)} hashtags, sobre el tope de {TOPE_HASHTAGS} de Instagram. "
                                 "Deja los más específicos")
    elif relleno:
        add("HASHTAGS", "OJO", f"{len(tags)} hashtags, {len(relleno)} genéricos "
                               f"({', '.join(relleno[:3])}). No describen nada")
    else:
        add("HASHTAGS", "OK", f"{len(tags)} hashtag(s)" + (f": {' '.join(tags)}" if tags else ""))

    if tags and any(re.search(r"(?:^|\s)" + re.escape(t) + r"\b", ventana) for t in tags):
        add("UBICACIÓN TAGS", "OJO", "hay un hashtag dentro de la parte visible; gasta espacio del feed")
    else:
        add("UBICACIÓN TAGS", "OK", "sin hashtags antes del corte")

    add("LINKS", "OJO" if links else "OK",
        f"{len(links)} link(s) con ruta en el caption, y en Instagram no se pueden tocar. "
        "Mejor la bio o el primer comentario" if links else "sin links muertos")

    if len(llamados) == 1:
        add("UN LLAMADO", "OK", f"un llamado a la acción: {llamados[0]}")
    elif not llamados:
        add("UN LLAMADO", "OJO", "no hay llamado a la acción. Decide para qué es este post")
    else:
        add("UN LLAMADO", "OJO", f"{len(llamados)} llamados ({', '.join(llamados)}). "
                                 "Dos llamados valen lo mismo que ninguno")

    densidad = len(emoji) * 100 / max(chars, 1)
    add("EMOJIS", "OJO" if densidad > 4 else "OK",
        f"{len(emoji)} emoji(s), {densidad:.1f} cada 100 caracteres"
        + (": se lee como adorno" if densidad > 4 else ""))

    voseo = sorted(set(m.lower() for m in VOSEO_RE.findall(limpio)))
    add("TUTEO", "FALLA" if voseo else "OK",
        f"voseo encontrado: {', '.join(voseo)}. La marca tutea" if voseo else "sin voseo")

    sin_link = LINK_RE.sub(" ", limpio)
    minuscula = MARCA_MINUSCULA_RE.findall(sin_link)
    add("MARCA", "OJO" if minuscula else "OK",
        "aparece 'desarmalo' en minúscula fuera de un link. Se escribe Desarmalo.cl"
        if minuscula else "nombre de marca bien escrito")

    llaves = re.findall(r"\{\{[^}]+\}\}", limpio)
    add("DATOS PENDIENTES", "FALLA" if llaves else "OK",
        f"{len(llaves)} dato(s) por completar: {', '.join(llaves[:3])}" if llaves
        else "sin {{marcadores}} pendientes")

    if palabras:
        bajo = limpio.lower()
        hay = [p for p in palabras if p.lower() in bajo]
        faltan = [p for p in palabras if p.lower() not in bajo]
        en_ventana = [p for p in hay if p.lower() in ventana.lower()]
        estado = "OK" if not faltan else ("OJO" if hay else "FALLA")
        add("BÚSQUEDA", estado,
            f"{len(hay)}/{len(palabras)} presentes"
            + (f", {len(en_ventana)} antes del corte" if hay else "")
            + (f". Faltan: {', '.join(faltan)}" if faltan else ""))

    fallas = sum(1 for r in revisiones if r["estado"] == "FALLA")
    ojos = sum(1 for r in revisiones if r["estado"] == "OJO")
    veredicto = "CORREGIR" if fallas else ("REVISAR" if ojos else "LISTO")

    return {
        "caracteres": chars, "limite": LIMITE, "corte": corte,
        "visible": ventana, "cortado": cortado,
        "hashtags": tags, "menciones": menciones, "links": links,
        "emojis": len(emoji), "llamados": llamados,
        "revisiones": revisiones, "veredicto": veredicto,
    }


def mostrar(a, out=sys.stdout):
    cab = (f"REVISIÓN DE CAPTION  ·  {a['caracteres']} / {a['limite']} car.  ·  "
           f"{len(a['hashtags'])} hashtags  ·  {len(a['llamados'])} llamado(s)")
    print("\n" + cab, file=out)
    print("=" * max(len(cab), 62), file=out)
    dibujar_caja(a["visible"], a["cortado"], out=out)
    print("", file=out)
    for r in a["revisiones"]:
        print(f"  {r['estado']:<5} {r['revision']:<17} {r['detalle']}", file=out)
    print("-" * max(len(cab), 62), file=out)
    print(f"  VEREDICTO  {a['veredicto']}\n", file=out)


def main():
    ap = argparse.ArgumentParser(description="Revisa un caption de Instagram de Desarmalo.cl.")
    ap.add_argument("entrada", nargs="?", default="-",
                    help="archivo con el caption, una pieza .md de content/, o - para stdin")
    ap.add_argument("--corte", type=int, default=CORTE,
                    help=f"caracteres visibles antes de '... más' (por defecto {CORTE})")
    ap.add_argument("--palabras", default="", help="términos de búsqueda separados por coma")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    crudo = sys.stdin.read() if args.entrada == "-" else open(args.entrada, encoding="utf-8").read()
    a = analizar(extraer_caption(crudo), corte=args.corte, palabras=args.palabras.split(","))
    if args.json:
        print(json.dumps(a, indent=2, ensure_ascii=False))
    else:
        mostrar(a)
    sys.exit(0 if a["veredicto"] == "LISTO" else 1)


if __name__ == "__main__":
    main()
