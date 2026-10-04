# Kit de marca — Desarmalo

Extraído del código del monorepo (2 de octubre de 2026). **Todo valor está copiado del código y
lleva su archivo de origen.** Donde el código no tiene algo, lo dice; no se completó con
suposiciones.

## Qué hay

| Archivo | Contenido |
|---|---|
| [`tokens.css`](tokens.css) | Colores, tipografía, espaciado, radios, sombras. Mismos nombres `--ds-*` que la app |
| [`fonts/README.md`](fonts/README.md) | Barlow Condensed (600/700/800) y la fuente del sistema, con los archivos y dónde se usa cada peso |
| [`fonts/bootstrap-icons-subset.be244f7afc.woff2`](fonts/) | Subset de iconos que usa el sitio (el único archivo de fuente que está en el repo) |
| [`logo/logo-desarmalo-banner.png`](logo/logo-desarmalo-banner.png) | El logo real del sitio (PNG, 4,9 KB), bajado de la URL que usan el header y el footer |
| [`logo/desarmalo-mark-d.svg`](logo/desarmalo-mark-d.svg) | El cuadrado naranja con la "D", **reconstruido desde CSS** (ver § Logo) |
| [`logo/favicon.ico`](logo/favicon.ico) | Copia de `apps/web/public/favicon.ico` |
| [`textos.md`](textos.md) | Nombres de secciones y llamados a la acción, con su archivo |

## Lo que el pedido original busca y NO está en el código

Esto cambia las reglas de uso, así que va primero:

- **No hay degradado ámbar.** Ninguna hoja de estilos de `apps/web` ni `apps/admin` define un
  `linear-gradient`/`radial-gradient` de marca. La única mención es un comentario en
  `apps/admin/src/app/pages/login/login.component.scss:11` que dice lo contrario: "nada de
  imágenes ni gradientes vistosos". Los acentos son **planos**: naranja `#ff4200`, azul
  `#0155ab`, navy `#081828`. Tampoco hay ningún color ámbar de marca; lo más cercano es el
  color de advertencia `#b26a00`, que es de estado, no de marca.
- **No hay "contador de días".** Busqué `contador`, `días restantes`, `tranquil`, `paso a paso` en `web`
  y `admin`. Los únicos contadores reales: el de pendientes junto a "Publicaciones" en el menú del
  admin, la pastilla de cambios/pasos pendientes del formulario de publicar, "Paso N de 6" y
  "N resultados" en el listado. Lo más parecido a algo de días es el texto "Visible 12 meses"
  (`apps/web/src/app/pages/home/home.content.ts`).
- **No existe el texto "Tranquilo/a, vamos paso a paso".** La app no tiene ese tono; el más
  cercano está en el formulario de publicar (§ Tono de voz).
- **No hay un logo SVG** en el repo. El logo del sitio es un PNG que vive en Azure Storage, fuera
  del repo. El "cuadrado" existe sólo como estilos CSS en el login del admin.
- **No hay modo oscuro** ni tema alterno.

Si esas piezas (degradado, contador, tono "Tranquilo/a") vienen de otro producto o de un diseño
que aún no se implementó, hay que pasarme esa fuente: no las puedo derivar de este código.

## Color: roles y reglas

Fuente: `apps/web/src/styles/_tokens.scss`, `apps/web/STYLEGUIDE.md` § 2.

| Rol | Token | Valor |
|---|---|---|
| Fondo de página / sección clara | `--ds-color-bg` | `#f8f9fa` |
| Tarjeta, input | `--ds-color-white` | `#fff` |
| Texto | `--ds-color-text` | `#212529` |
| Texto secundario, metadatos | `--ds-color-muted` | `#6c757d` |
| Bordes | `--ds-color-border` | `#dee2e6` |
| **Acento / acción primaria** | `--ds-color-orange` | `#ff4200` (hover `#d63700`) |
| Enlaces, acción secundaria, precio | `--ds-color-blue` | `#0155ab` (hover `#01417f`) |
| Header, footer, hero | `--ds-color-navy` | `#081828` |
| Bandas CTA oscuras | `--ds-color-navy-2` | `#0f2236` |
| Éxito / error / advertencia | `--ds-color-success` / `-danger` / `-warning` | `#1e7d32` / `#c62828` / `#b26a00` (con fondo `-bg` al 12 %) |

Reglas (del `STYLEGUIDE.md`, vigentes):

1. **Una sola acción primaria naranja por vista.** Azul para enlaces y acciones secundarias;
   navy sólo en header, footer y bandas oscuras.
2. **El naranja no es un rojo de alerta.** No mezclar tintes rojizos con él. Los estados reales
   (éxito/advertencia/error) usan sus propios tokens, y esos colores **no se usan como CTA**
   de producto.
3. **Nunca un hex suelto en un componente:** siempre `var(--ds-color-*)`. Si falta un color, se
   agrega primero al archivo de tokens.

### Contraste (calculado para este kit, WCAG 2.x)

| Par | Ratio | Consecuencia |
|---|---|---|
| Blanco sobre `#ff4200` | **3,48:1** | No pasa AA en texto normal |
| Blanco sobre `#d63700` (orange-hover) | 4,77:1 | Pasa AA |
| Blanco sobre `#0155ab` | 7,27:1 | OK |
| `#ff4200` sobre navy `#081828` | 5,15:1 | OK (eyebrows y acentos sobre fondo oscuro) |
| `#ff4200` sobre blanco | 3,48:1 | Sólo para texto grande/en negrita (eyebrow, "Ver todos") |
| `#6c757d` sobre blanco / sobre `#f8f9fa` | 4,69 / 4,45 | El segundo queda justo bajo AA |

Por eso el código **no pone texto blanco sobre `#ff4200` en las bandas grandes**: la cinta
"Publica tu anuncio" y el bloque naranja del home usan `--ds-color-orange-hover` como fondo
(`home-publish-band.component.scss`, `home-publish-block.component.scss`, con el comentario de
por qué). Los botones `.btn-ds-primary` sí usan `#ff4200` con texto blanco de 14–16 px en
negrita; si el botón es chico o es el único elemento de una banda, copia el criterio de la cinta.

## "Degradado ámbar" — qué usar en su lugar

No hay degradado. Para el mismo trabajo (destacar el llamado principal) el sitio usa **bandas
planas**: azul `#0155ab` bajo el hero (`.ds-band--blue`), naranja `#d63700` en el bloque de publicar,
navy `#0f2236` (`.ds-band--navy`) y el filete naranja de 4 px sobre el footer y las tarjetas
oscuras (`border-top: 4px solid var(--ds-color-orange)`). Si más adelante se aprueba un
degradado, debe nacer como token en `_tokens.scss` de las dos apps antes de usarse.

## Tipografía

Detalle en [`fonts/README.md`](fonts/README.md). Resumen: **Barlow Condensed** (600/700/800),
siempre en mayúsculas, para títulos, navegación, eyebrows y botones grandes; **fuente del
sistema** para todo el cuerpo.

## Tarjetas (publicaciones)

Fuente: `apps/web/src/styles/_card.scss` y `STYLEGUIDE.md` § "Anatomía de tarjeta".

- Fondo `--ds-color-white`, **sin borde ni sombra**: sólo un filete inferior de **3 px**
  `--ds-color-border` que en hover pasa a `--ds-color-orange` (`transition: border-color .2s`).
  Radio `--ds-radius` (2 px).
- Foto 3:2 (`aspect-ratio: 3 / 2`), `object-fit: cover`, zoom `scale(1.04)` en hover.
- Cinta sobre la foto: 12 px, 700, mayúsculas, blanco; arriba-izquierda navy (`--top`), abajo-izquierda
  azul (`--cat`) o naranja (`--orange`). Píldora "N fotos" abajo-derecha: `rgba(8,24,40,.72)`, radio pill.
- Cuerpo: eyebrow naranja 12 px/700/mayúsculas (`.06em`), título Barlow `25px` con `line-height: 1.02`
  a 2 líneas, metadatos 13 px muted.
- Pie: borde superior 1 px `--ds-color-border`; **precio en azul**, 26 px, peso 800; CTA a la derecha
  en naranja, 14 px, 700.
- Avatar del vendedor: círculo 24 px, azul (persona) o navy (empresa).
- Mecánica obligatoria: el enlace va **dentro del título** con `stretched-link`; ningún ancestro del
  enlace lleva `overflow: hidden` (recortaría el área clicable).
- **En el admin las tarjetas son otra cosa** (`apps/admin/src/styles/_base.scss`, `.card`): fondo
  blanco, borde de 1 px `--ds-color-border`, radio 6 px, padding 24 px. No mezclar los dos estilos.

## Botones

Fuente: `apps/web/src/styles/_base.scss:57-92`, `_bootstrap-bridge.scss`.

| Clase | Fondo | Cuándo |
|---|---|---|
| `.btn-ds-primary` | naranja `#ff4200` → hover `#d63700` | **La** acción de la vista: "Publica tu anuncio", "Buscar", "Iniciar sesión" |
| `.btn-ds-secondary` | azul `#0155ab` → hover `#01417f` | "Ver todas las publicaciones", "Reintentar", "Editar" |
| `.btn-ds-light` | blanco, texto navy | Sobre fondo naranja/azul/navy ("Publicar gratis") |
| `.btn-primary` / `.btn-outline-primary` (Bootstrap) | retematizados en azul de marca | Formularios del detalle y la cuenta |

- Radio `--ds-radius` (2 px en web). El tamaño lo da `.btn` de Bootstrap; las bandas CTA grandes suben
  a Barlow 800, mayúsculas, `letter-spacing: .04em`, 19–20 px.
- Admin (`apps/admin/src/styles/_base.scss`): alto mínimo **44 px** (objetivo táctil), radio 6 px, 14 px/600.
  Primario = azul (`.btn--primary`), no naranja. Peligro/éxito con `--ds-color-danger`/`-success`.
- Botón de WhatsApp: verde `#25d366` con texto blanco, **sólo** en el contacto del detalle. Contraste
  blanco/verde = 1,98:1: es una excepción heredada de la marca de WhatsApp, no un patrón a copiar.
- Chips (`.ds-chip`): pill, borde 1 px; activo = fondo azul y texto blanco.

## Contadores

No existe un contador de días (ver arriba). Los contadores que sí tiene el producto:

- **Cambios / pasos pendientes** del formulario de publicar (`post-side-panel`): pastilla **naranja**
  al editar (cuenta cambios) y **navy** al crear (cuenta pasos pendientes) — `STYLEGUIDE.md` § Formulario por bloques.
- **Paso N de 6** en el stepper (`post-stepper.component.html:20,26`).
- **Pendientes** junto a "Publicaciones" en el menú del admin (`AdminStatsService`, `apps/admin/CLAUDE.md`).
- **Resultados** en el listado: "Publicaciones · N resultados".

## Espaciado, radios y sombras

- Escala de espaciado: 4 · 8 · 12 · 16 · 24 · 32 · 48 · 64 px (`--ds-space-1…8`).
- Radios: **2 px** en el sitio público (cuadrado, casi sin curva: es parte del carácter), **6 px** en el admin,
  `999px` sólo para chips y píldoras.
- Sombras: `--ds-shadow-1` (sutil) y `--ds-shadow-2` (buscador del hero, bloque naranja, modales), ambas
  con base navy `rgb(8 24 40)`, nunca negro puro.
- Altura del header: 72 px escritorio / 60 px móvil. Breakpoint de "móvil": **768 px** (en el admin, 640 px
  para tablas y 799 px para el login).

## Header, footer y hero

- Header navy, logo a la izquierda (36 px de alto, 30 px en móvil), navegación en Barlow 600 mayúsculas
  17 px; el ítem activo = pill `rgba(255,255,255,.1)` con texto naranja. CTA naranja "Publica tu anuncio".
- Footer navy con **filete superior naranja de 4 px**, texto `--ds-color-on-dark-muted`, enlaces blancos
  que pasan a naranja en hover.
- Hero navy: eyebrow naranja, h1 Barlow 800 con **una palabra en naranja** ("desarme"), subtítulo muted,
  buscador con `--ds-shadow-2`.

## Tono de voz

Fuente: `CLAUDE.md` § Convenciones y los textos de `textos.md`.

- **Español neutro, tuteo. Nunca voseo.** "Publica tu anuncio", "tu publicación", "puedes", "espera". Nunca
  "publicá", "podés", "vos". Aplica a UI, errores y correos.
- Directo y cercano, en imperativo corto: "Busca · Compara · Contacta". Tutea sin ser informal en exceso:
  la jerga aparece con medida ("piezas y repuestos para tu joyita", `index.html`).
- **Explica el siguiente paso, no culpa.** Errores y vacíos siempre traen salida: "No encontramos
  publicaciones con esos filtros" + botón "Reiniciar la búsqueda"; si falla el envío del contacto, se
  muestra el correo directo.
- **Lo más cercano a "vamos paso a paso"** (formulario de publicar): "Seis pasos cortos. Completa cada
  uno y presiona Listo para pasar al siguiente.", botón **"Listo, siguiente paso"**, "Publicar toma 2 minutos".
  Confirmaciones breves y positivas: "¡Listo! Te avisamos cuando se publique.", "¡Mensaje enviado!".
- Datos concretos antes que adjetivos: "Visible 12 meses · Hasta 6 fotos · Contacto por WhatsApp",
  "sin comisiones".
- Seguridad dicha sin dramatismo: "Para evitar estafas, recomendamos comprar los repuestos personalmente…".
- Marca en texto: **"Desarmalo.cl"** en el sitio público y los correos; "Desarmalo" sin ".cl" en el panel
  ("DESARMALO · ADMIN"). Los títulos de interfaz van en mayúsculas por CSS (Barlow), no escritos en mayúsculas.

## Logo

- **Real:** `logo/logo-desarmalo-banner.png` — 390×50 en el HTML del header/footer
  (`header.component.html`, `footer.component.html`). Trae el texto en un tono **claro** (sobre blanco sólo se ve el punto naranja) sobre
  transparente: está pensado para fondo **navy** (el header y el footer son navy). Sobre blanco no se ve el texto.
  Origen: `https://desarmalodevstorage.blob.core.windows.net/desarmalo/logo-desarmalo-banner.png`
  (también es el `logo` del JSON-LD de `index.html` y `DEFAULT_OG_IMAGE` de `seo.service.ts`).
  Tamaño de uso: 36 px de alto en el header (30 px en móvil), 160 px de ancho en el footer.
- **Wordmark en texto** (menú lateral, `sidenav.component.html:6-8` y `.scss`): `Desarmalo` + `.` + `cl` en
  Barlow 800 de 19 px, color navy, con el **punto naranja**. Es la misma idea del PNG: el punto es el acento.
- **Cuadrado "D"** (login del admin): 32×32, fondo `#ff4200`, radio 6 px, "D" blanca Barlow 800 de 16 px, seguido
  de "DESARMALO" en Barlow 800 de 18 px. `logo/desarmalo-mark-d.svg` lo reproduce con esos valores; es una
  **reconstrucción**, no un archivo oficial, y la "D" depende de tener la fuente instalada.
- Favicon: `logo/favicon.ico` (el mismo en web y admin).

## Inconsistencias que encontré (no las propago en el kit)

- `apps/web/STYLEGUIDE.md` dice que Bootstrap llega por CDN y que `_bootstrap.scss` es "fase siguiente"
  (§ 1 y § 9); `apps/web/CLAUDE.md` y el código dicen que ya se compila desde npm. La paleta y los tokens del
  `STYLEGUIDE.md` sí coinciden con `_tokens.scss`.
- `apps/admin/src/app/pages/login/login.component.html:24` dice "**Iniciá** sesión de nuevo": voseo, contra la
  regla del proyecto. Debería ser "Inicia sesión de nuevo".
- Los dos `_tokens.scss` están duplicados a mano (lo dice el propio admin): si cambia la paleta hay que tocar
  los dos archivos.
