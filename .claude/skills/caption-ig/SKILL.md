---
name: caption-ig
description: >-
  Escribe y revisa el caption de Instagram de una pieza de Desarmalo.cl: la
  primera línea que sobrevive al corte de "... más", el cuerpo, un solo llamado
  a la acción, los términos de búsqueda y hasta 5 hashtags. Úsala cuando haya
  que escribir o revisar un caption, o antes de pasar una pieza a revisión.
---

# caption-ig

En esta carpeta hay un script que corre sin internet ni dependencias:

```bash
python3 .claude/skills/caption-ig/revisar_caption.py caption.txt
python3 .claude/skills/caption-ig/revisar_caption.py content/carruseles/pieza.md --palabras "repuestos usados,desarmaduría"
```

Si le pasas una pieza `.md` de `content/`, revisa sólo la sección `## Caption`.
Muestra los primeros ~125 caracteres tal como se ven en el feed, en una caja,
y después las revisiones. Lee la caja antes que todo lo demás.

## Primero decide qué trabajo hace el caption

**A: el video ya enganchó.** En un reel, el gancho está en los primeros dos
segundos del video. El caption no compite con eso: da contexto, el llamado y
las palabras que la gente busca.

**B: el caption es el contenido.** En una imagen o un carrusel, la primera
línea es el gancho: concreta, corta, y si se corta, que sea en un punto que
deje intriga y no a mitad de frase.

## La forma

```
Línea 1    ~125 caracteres visibles. A: el llamado. B: el gancho.
           Nunca un saludo, un hashtag ni un emoji como primer carácter.
Cuerpo     párrafos cortos con una línea en blanco entre cada uno.
           Aquí van los términos de búsqueda, escritos como frase normal.
Llamado    uno solo: comentar una palabra, guardar, buscar en el sitio o publicar.
Hashtags   hasta 5, específicos, en la última línea. O ninguno.
```

## Reglas de Desarmalo

- **Hasta 5 hashtags.** Instagram bajó el tope de 30 a 5 el 18 de diciembre de
  2025. Los genéricos (`#viral`, `#fyp`, `#parati`) no describen nada.
- **Términos de búsqueda en el texto.** Instagram lee el caption. "Repuestos
  usados en Santiago" como frase vale más que `#RepuestosUsados`.
- **Un solo llamado.** Dos llamados valen lo mismo que ninguno.
- **Sin links con ruta en el caption**, porque no se pueden tocar. Usa "link en
  la bio" o el primer comentario. `desarmalo.cl` a secas sí se puede nombrar.
- **Tuteo, nunca voseo.** "Busca", no "buscá". El script lo revisa.
- **La marca es Desarmalo.cl**, con D mayúscula. En minúscula sólo como URL.
- **No inventar datos de producto, precios ni stock.** Si falta un dato, va
  como `{{dato}}` y el script lo marca hasta que alguien lo complete.
- **Sigue `brand/voz-y-tono.md` y usa los textos de `brand/textos.md`** (CTA
  "Publica tu anuncio", el aviso de seguridad, etc.) tal cual.

## El ciclo

1. Decide A o B y dilo.
2. Escribe el borrador.
3. Pásalo por `/limpia-texto`.
4. Corre `revisar_caption.py` con 2 o 3 términos de búsqueda. Arregla cada
   FALLA y decide cada OJO en voz alta, no en silencio.
5. Deja el caption en la sección `## Caption` de la pieza en `content/`, con
   `estado: revision`, y entrega este resumen:

```
CAPTION LISTO
trabajo:    B, el carrusel lleva el gancho en la primera línea
visible:    118 de 125 caracteres antes del corte
llamado:    uno, buscar en desarmalo.cl
hashtags:   4
búsqueda:   "chocados en venta" en la línea 1, "desarmaduría" en la línea 3
revisión:   LISTO
```

Nada se publica ni se programa en Metricool sin `estado: aprobado` y el visto
bueno de Karina.

Adaptado de `ig-caption` de instagram-agent-skill (MIT). Ver `../TERCEROS.md`.
