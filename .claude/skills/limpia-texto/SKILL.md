---
name: limpia-texto
description: >-
  Saca las huellas de texto generado de un borrador en español (rayas,
  caracteres invisibles, muletillas, frases de plantilla) y marca lo que hay
  que reescribir. Úsala antes de mostrarle a Karina cualquier caption, guion,
  comentario, respuesta o DM de Desarmalo.cl, o cuando un texto "suena a IA".
---

# limpia-texto

```bash
python3 .claude/skills/limpia-texto/limpiar_texto.py borrador.txt --reporte
python3 .claude/skills/limpia-texto/limpiar_texto.py borrador.txt -o limpio.txt
```

Corre sin internet ni dependencias y lee `muletillas.json`, que se edita a
mano: si una palabra que la marca usa a propósito sale cambiada, sácala de ahí.

## Qué arregla solo

1. **Caracteres invisibles.** Espacios de ancho cero, guiones suaves, BOM,
   caracteres de etiqueta y espacios duros. Respeta los emojis compuestos
   (👨‍🔧), que usan uno de esos caracteres por dentro.
2. **Tipografía.** Raya a coma, guion medio a guion, comillas curvas a rectas,
   "…" a "...". No toca ¿ ni ¡.
3. **Muletillas.** "En el mundo actual", "es importante destacar que", "sin
   lugar a dudas", "deja de hacer scroll", "síguenos para más", "crucial",
   "potenciar" y otras más. Las cambia por algo simple o las borra, respetando
   mayúsculas y sin tocar los links.

No tiene reemplazos que choquen con el mundo automotriz: "potencia",
"elevar" o "corre a" quedan fuera a propósito.

## Qué marca para reescribir

"No es solo X, es Y", "No solo X sino también Y", "No se trata de X, se
trata de Y", "Imagina un mundo...", el saludo de apertura, tres palabras
gritadas seguidas, listas con tres o más emojis como viñetas, muros de
hashtags, superlativos sin respaldo ("los mejores", "N°1"), adjetivos
inflados ("increíble", "espectacular") y frases todas del mismo largo.

Esos casos no se arreglan con una regla, así que los reescribes tú. Un
superlativo sólo se queda si hay un dato que lo respalde (ver
`brand/voz-y-tono.md`: sin promesas que no podamos cumplir).

## El ciclo

1. Corre `limpiar_texto.py --reporte` sobre el borrador.
2. Reescribe cada estructura marcada.
3. Vuelve a correrlo hasta que no queden marcas que no puedas justificar.
4. Si es un caption, sigue con `/caption-ig`.

Es una revisión local con reglas simples, no un detector de IA, y no promete
que un texto pase por humano. Lo que sí hace es sacar lo que delata una
plantilla.

Adaptado de `ig-human` de instagram-agent-skill (MIT). Ver `../TERCEROS.md`.
