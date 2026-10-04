# Tipografías

Fuente de todo: `apps/web/src/styles/_tokens.scss:33-34` (tokens), `apps/web/src/styles/_fonts.scss`
(`@font-face`), `apps/web/angular.json:45-49` (copia de los archivos al build),
`apps/web/src/index.html:26-27` (preload).

## Barlow Condensed — display (títulos, navegación, eyebrows, botones grandes)

| Peso | Archivo que carga la app | Dónde se usa (según el código) |
|---|---|---|
| 600 | `/fonts/barlow-condensed/barlow-condensed-latin-600-normal.woff2` | Navegación del header (`.ds-header__link`, `header.component.scss`) |
| 700 | `/fonts/barlow-condensed/barlow-condensed-latin-700-normal.woff2` | `h2` de sección (`.ds-section-head h2`), `.ds-eyebrow`; también `h1`–`h4` del admin (`apps/admin/src/styles/_base.scss`) |
| 800 | `/fonts/barlow-condensed/barlow-condensed-latin-800-normal.woff2` | `.ds-display` (h1 del hero, bandas CTA, títulos de tarjetas de categoría), wordmark |

- Subset **latin**, `font-style: normal`, `font-display: swap`.
- Siempre en **MAYÚSCULAS** (`text-transform: uppercase`) y `line-height: .95` cuando es
  titular (`.ds-display`, `apps/web/src/styles/_base.scss:4-9`). Los títulos de tarjeta usan
  `line-height: 1.02` (`_card.scss:102-108`).
- `letter-spacing`: eyebrow `.12em` (`_base.scss:15`), navegación `.04em` (`header.component.scss`),
  eyebrow de tarjeta `.06em` (`_card.scss:99`).
- Pila completa: `'Barlow Condensed', 'Arial Narrow', Arial, sans-serif`.

## Cuerpo — fuente del sistema (no se aloja nada)

`system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', 'Noto Sans', sans-serif`
(`--ds-font-display`/`--ds-font-body` en `_tokens.scss`). No hay un peso o tamaño de cuerpo
fijado en un token: lo da Bootstrap 5.2.3 (base `1rem`).

## Archivos de fuente: NO están en el repositorio

Barlow Condensed llega por `@fontsource/barlow-condensed@^5.3.0` (`apps/web/package.json:31`) y
`angular.json` copia en el build sólo `barlow-condensed-latin-{600,700,800}-normal.woff2` desde
`node_modules/@fontsource/barlow-condensed/files`. En este checkout no hay `node_modules`, así
que **no copié los `.woff2` de Barlow**; no los inventé ni los bajé de otro lado.

Para traerlos a `brand/fonts/`:

```bash
npm install --prefix apps/web
cp apps/web/node_modules/@fontsource/barlow-condensed/files/barlow-condensed-latin-{600,700,800}-normal.woff2 brand/fonts/
```

(Licencia: SIL Open Font License 1.1, según el paquete de Fontsource.)

## Sí está en el repo: el subset de iconos

`bootstrap-icons-subset.be244f7afc.woff2` — copia de
`apps/web/src/assets/fonts/bootstrap-icons-subset.be244f7afc.woff2`. Es un subset de
`bootstrap-icons` con sólo los glifos que usa el sitio (61 según `apps/web/CLAUDE.md`). Los
codepoints son los originales de Bootstrap Icons, así que las clases `bi-*` salen de
`apps/web/src/styles/_icons.scss` (generado; no está copiado acá). Sirve de referencia; para
iconos nuevos hay que correr `npm run icons:subset --prefix apps/web`, no editar este archivo.
