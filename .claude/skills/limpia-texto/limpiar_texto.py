#!/usr/bin/env python3
"""
limpiar_texto.py - saca las huellas de texto generado de un borrador en
español antes de que llegue a Karina.

Tres pasadas, en este orden:

  1. INVISIBLES   borra o normaliza caracteres que un teclado no produce:
                  espacios de ancho cero, guiones suaves, BOM, caracteres de
                  etiqueta, espacios duros. Sobreviven al copiar y pegar.
                  La unión de ancho cero se respeta dentro de emojis
                  compuestos (👨‍🔧), porque ahí es parte del emoji.
  2. TIPOGRAFÍA   raya -> coma, guion medio -> guion, comillas curvas ->
                  rectas, "…" -> "...", viñeta -> guion. No toca ¿ ni ¡.
  3. MULETILLAS   cambia las frases y palabras de muletillas.json por algo
                  simple o las borra, respetando mayúsculas y sin tocar links.

Las estructuras ("No es solo X, es Y", saludos, superlativos, muros de
hashtags) se REPORTAN, no se reescriben: cambiar la forma de una frase
requiere criterio.

Adaptado de humanize.py de instagram-agent-skill (MIT, (c) 2026 Jake
Schincariol). Ver ../TERCEROS.md.

Uso
  python3 limpiar_texto.py borrador.txt
  python3 limpiar_texto.py borrador.txt --reporte
  python3 limpiar_texto.py borrador.txt -o limpio.txt
  python3 limpiar_texto.py borrador.txt --json
"""

import argparse
import json
import os
import re
import sys
import unicodedata

AQUI = os.path.dirname(os.path.abspath(__file__))
LEXICO = os.path.join(AQUI, "muletillas.json")

URL_RE = re.compile(r"https?://\S+|www\.\S+|\S+@\S+\.\S+")
FRASE_RE = re.compile(r"[^.!?\n]+[.!?]*")
ZWJ = "‍"


def cargar_lexico(ruta=LEXICO):
    with open(ruta, encoding="utf-8") as fh:
        return json.load(fh)


def _cp(spec):
    """'U+200B' -> 0x200B;  'U+E0000-U+E007F' -> (inicio, fin)."""
    if "-" in spec:
        a, b = spec.split("-")
        return (int(a[2:], 16), int(b[2:], 16))
    return int(spec[2:], 16)


def proteger_urls(texto):
    """Cambia los links por marcadores para que ninguna pasada los reescriba."""
    guardadas = []

    def guardar(m):
        guardadas.append(m.group(0))
        return f"\x00URL{len(guardadas) - 1}\x00"

    return URL_RE.sub(guardar, texto), guardadas


def restaurar_urls(texto, guardadas):
    for i, url in enumerate(guardadas):
        texto = texto.replace(f"\x00URL{i}\x00", url)
    return texto


def _es_emoji(c):
    return unicodedata.category(c) == "So" or 0x1F000 <= ord(c) <= 0x1FAFF


def pasada_invisibles(texto, lex):
    # Protege la unión de ancho cero entre dos emojis (o emoji + selector de variación).
    texto = re.sub(r"(?<=[\U0001F000-\U0001FAFF☀-➿️])‍(?=[\U0001F000-\U0001FAFF☀-➿])",
                   "\x00ZWJ\x00", texto)
    hallazgos = []
    for e in lex["invisibles"]:
        cp = _cp(e["cp"])
        if isinstance(cp, tuple):
            patron = "[" + re.escape(chr(cp[0])) + "-" + re.escape(chr(cp[1])) + "]"
        else:
            patron = re.escape(chr(cp))
        n = len(re.findall(patron, texto))
        if n:
            hallazgos.append({"nombre": e["cp"] + " " + e["nombre"], "veces": n, "accion": e["accion"]})
            texto = re.sub(patron, "" if e["accion"] == "borrar" else " ", texto)
    # Cualquier otro carácter de formato (Cf) es invisible por definición.
    sueltos = [c for c in texto if unicodedata.category(c) == "Cf"]
    if sueltos:
        hallazgos.append({"nombre": "otros caracteres de formato invisibles",
                          "veces": len(sueltos), "accion": "borrar"})
        texto = "".join(c for c in texto if unicodedata.category(c) != "Cf")
    return texto.replace("\x00ZWJ\x00", ZWJ), hallazgos


def pasada_tipografia(texto, lex):
    hallazgos = []
    for e in lex["tipografia"]:
        ch = e["de"]
        n = texto.count(ch)
        if not n:
            continue
        hallazgos.append({"nombre": f"{ch} {e['nombre']}", "veces": n, "a": e["a"].strip() or "(espacio)"})
        if ch == "—":
            texto = re.sub(r"\s*—\s*", ", ", texto)
        elif ch == "–":
            texto = re.sub(r"\s*–\s*(?=\d)", "-", texto)    # 5–10 -> 5-10
            texto = re.sub(r"\s+–\s+", ", ", texto)          # usado como raya
            texto = texto.replace("–", "-")
        else:
            texto = texto.replace(ch, e["a"])
    texto = re.sub(r",\s*([,.;:!?])", r"\1", texto)
    texto = re.sub(r"(?m)^\s*,\s*", "", texto)
    texto = re.sub(r",\s*\n", "\n", texto)
    return texto, hallazgos


def _igualar_mayusculas(original, cambio):
    if not cambio:
        return cambio
    if original.isupper() and len(original) > 1:
        return cambio.upper()
    if original[0].isupper():
        return cambio[0].upper() + cambio[1:]
    return cambio


def pasada_muletillas(texto, lex):
    """Cambia frases y palabras. Las más largas primero, para que las frases ganen."""
    hallazgos = []
    entradas = sorted(lex["frases"] + lex["palabras"], key=lambda e: len(e["buscar"]), reverse=True)
    for e in entradas:
        buscar = e["buscar"]
        inicio = r"\b" if buscar[0].isalnum() else ""
        fin = r"\b" if buscar[-1].isalnum() else ""
        patron = re.compile(inicio + re.escape(buscar).replace(r"\ ", r"\s+") + fin, re.IGNORECASE)
        encontrados = patron.findall(texto)
        if not encontrados:
            continue
        hallazgos.append({"buscar": buscar, "cambiar": e["cambiar"] or "(borrado)",
                          "veces": len(encontrados), "familia": e["familia"]})
        texto = patron.sub(lambda m: _igualar_mayusculas(m.group(0), e["cambiar"]), texto)
    # Limpieza después de borrar: puntuación huérfana, espacios dobles, líneas vacías.
    texto = re.sub(r"[ \t]{2,}", " ", texto)
    texto = re.sub(r"(?m)^[ \t]*(?:[,.;:]+[ \t]*)+", "", texto)
    texto = re.sub(r"(?m)^[ \t](?=\S)", "", texto)
    texto = re.sub(r"[ \t]+([,.;:!?])", r"\1", texto)
    texto = re.sub(r",\s*([,.;:!?])", r"\1", texto)
    texto = texto.replace("...", "\x00SUSP\x00")
    texto = re.sub(r"\.\s*\.+", ".", texto)
    texto = re.sub(r"([!?])\s*\.", r"\1", texto)
    texto = texto.replace("\x00SUSP\x00", "...")
    texto = re.sub(r"([!?.])[ \t]*,[ \t]*", r"\1 ", texto)   # "Hola! , hoy" -> "Hola! hoy"
    texto = re.sub(r"([¿¡])\s+", r"\1", texto)
    texto = re.sub(r"(?m)^[ \t]+$", "", texto)
    texto = re.sub(r"\n{3,}", "\n\n", texto)
    return texto, hallazgos


def revisar_estructuras(texto, lex):
    marcas = []
    for s in lex["estructuras"]:
        try:
            patron = re.compile(s["regex"], re.MULTILINE)
        except re.error:
            continue
        encontrados = patron.findall(texto)
        if encontrados:
            marcas.append({"nombre": s["nombre"], "veces": len(encontrados), "arreglo": s["arreglo"]})
    largos = [len(f.split()) for f in FRASE_RE.findall(texto) if len(f.split()) > 2]
    if len(largos) >= 4:
        media = sum(largos) / len(largos)
        var = sum((n - media) ** 2 for n in largos) / len(largos)
        cv = (var ** 0.5) / media if media else 0
        if cv < 0.35:
            marcas.append({"nombre": f"Frases todas del mismo largo (variación {cv:.2f})",
                           "veces": len(largos),
                           "arreglo": "Corta una frase en dos y deja otra más larga. Lo parejo suena a máquina."})
    return marcas


def restaurar_mayusculas(original, texto):
    """Al borrar una apertura, la palabra siguiente queda en minúscula. Se arregla
    sólo si quien escribió usa mayúscula al inicio de frase."""
    inicios = re.findall(r"(?:^|[.!?]\s+|\n)\s*[¿¡]?([A-Za-zÁÉÍÓÚÑáéíóúñ])", original)
    if not inicios or sum(1 for c in inicios if c.isupper()) * 2 < len(inicios):
        return texto
    return re.sub(r"(?:^|(?<=[^.]\. )|(?<=[!?] )|(?<=[.!?]\n)|(?<=\n))(\s*[¿¡]?)([a-záéíóúñ])",
                  lambda m: m.group(1) + m.group(2).upper(), texto)


def limpiar(texto, lex):
    original = texto
    texto, urls = proteger_urls(texto)
    texto, inv = pasada_invisibles(texto, lex)
    texto, tipo = pasada_tipografia(texto, lex)
    texto, mul = pasada_muletillas(texto, lex)
    texto = restaurar_mayusculas(original, texto)
    texto = restaurar_urls(texto, urls)
    return texto.strip() + "\n", {
        "invisibles": inv,
        "tipografia": tipo,
        "muletillas": mul,
        "estructuras": revisar_estructuras(texto, lex),
    }


def mostrar_reporte(r, out=sys.stderr):
    def titulo(t):
        print(f"\n{t}\n" + "-" * len(t), file=out)

    total = sum(h["veces"] for k in ("invisibles", "tipografia", "muletillas") for h in r[k])
    titulo("REPORTE DE LIMPIEZA")
    print(f"{total} cambios automáticos, {len(r['estructuras'])} estructuras marcadas para reescribir", file=out)
    if r["invisibles"]:
        titulo("1. CARACTERES INVISIBLES")
        for h in r["invisibles"]:
            print(f"  {h['veces']:>3}x  {h['nombre']}  -> {h['accion']}", file=out)
    if r["tipografia"]:
        titulo("2. TIPOGRAFÍA")
        for h in r["tipografia"]:
            print(f"  {h['veces']:>3}x  {h['nombre']}  -> {h['a']}", file=out)
    if r["muletillas"]:
        titulo("3. MULETILLAS")
        for h in r["muletillas"]:
            print(f"  {h['veces']:>3}x  {h['buscar']}  -> {h['cambiar']}   [{h['familia']}]", file=out)
    if r["estructuras"]:
        titulo("4. ESTRUCTURAS (no se arreglan solas, hay que reescribirlas)")
        for h in r["estructuras"]:
            print(f"  {h['veces']:>3}x  {h['nombre']}\n        {h['arreglo']}", file=out)
    if not any(r.values()):
        titulo("LIMPIO")
        print("  Nada que sacar.", file=out)
    print("", file=out)


def main():
    ap = argparse.ArgumentParser(description="Limpia un borrador en español antes de mostrarlo.")
    ap.add_argument("entrada", nargs="?", default="-", help="archivo, o - para stdin")
    ap.add_argument("-o", "--salida", help="escribe el texto limpio aquí en vez de la pantalla")
    ap.add_argument("--reporte", action="store_true", help="muestra qué cambió (por stderr)")
    ap.add_argument("--json", action="store_true", help="devuelve {texto, reporte} en JSON")
    ap.add_argument("--lexico", default=LEXICO, help="ruta a muletillas.json")
    args = ap.parse_args()

    crudo = sys.stdin.read() if args.entrada == "-" else open(args.entrada, encoding="utf-8").read()
    lex = cargar_lexico(args.lexico)
    limpio, reporte = limpiar(crudo, lex)

    if args.json:
        print(json.dumps({"texto": limpio, "reporte": reporte}, indent=2, ensure_ascii=False))
        return
    if args.salida:
        with open(args.salida, "w", encoding="utf-8") as fh:
            fh.write(limpio)
        print(f"escrito en {args.salida}", file=sys.stderr)
    else:
        sys.stdout.write(limpio)
    if args.reporte:
        mostrar_reporte(reporte)


if __name__ == "__main__":
    main()
