# Textos clave de la app

Copiados literalmente del código (ortografía incluida; ver § Observaciones al final). Ruta de
archivo relativa a `apps/web/src/app/` salvo donde se indica `admin`.

## Nombre y descripciones de marca

| Texto | Archivo |
|---|---|
| `Desarmalo.cl` (sitio) · `Desarmalo · Admin` (título del panel) | `apps/web/src/index.html` · `apps/admin/src/index.html` |
| Título de página: **Desarmalo.cl Desarmaduria, piezas y repuestos para tu joyita.** | `apps/web/src/index.html:5` |
| Descripción: *Marketplace chileno de repuestos usados de desarmadurías y autos chocados en venta. Busca por marca, año y ciudad, y contacta directo al vendedor.* | `apps/web/src/index.html:14` |
| Organización: *Portal de compra y venta de piezas de vehículos en desarme y autos chocados en Chile.* | `apps/web/src/index.html:58` |
| Eyebrow del hero: **El marketplace de repuestos N°1 de Chile.** | `shared/components/home-subheader/home-subheader.component.html` |
| Footer: *El portal Nº1 en compra y venta de piezas de desarme y vehículos chocados en Chile. Recicla, reutiliza y ahorra.* | `shared/components/footer/footer.component.html` |
| Panel: **Panel de administración** — *Modera publicaciones nuevas, gestiona usuarios y revisa la actividad del sitio en un solo lugar.* | `apps/admin/src/app/pages/login/login.component.html` |

## Navegación y nombres de sección

**Header** (`shared/components/header/header.component.html`): Publicaciones · Desarmaduría ·
Chocados en venta · botón **Publica tu anuncio** · **Acceder** (avatar con la inicial si hay sesión).

**Menú lateral** (`shared/components/sidenav/sidenav.component.html`): Inicio · Publicaciones ·
Desarmaduría · Chocados en venta · Categorias · *Tu cuenta* → Configurar tu cuenta · Mis publicaciones ·
Cerrar Sesión · (sin sesión) Crea tu cuenta · botón **Publica tu anuncio**.

**Footer**: Contáctanos (contacto@desarmalo.cl · Sobre nosotros · Contacto) · Legal (Términos y condiciones ·
Políticas de privacidad) · Síguenos (Instagram · Facebook).

**Categorías** (únicas dos, `pages/categories`, `home.content.ts`):

| Categoría | Descripción |
|---|---|
| **Desarmaduría** | Vehículos completos y piezas originales para desarme. |
| **Chocados en venta** | Autos siniestrados con precio publicado, listos para reparar. |

**Secciones del home** (`pages/home/home.component.html`): *Últimos publicados* (con "Ver todos") ·
segmentos *Todos / Desarmaduría / Chocados en venta* · *Busca por marca* (con "Todas las marcas") ·
**Compra seguro** · *Encuentra repuestos y vehículos en desarme en un solo lugar*.

**Panel del admin** (`apps/admin`, `shell.component.html`/`event-label.ts`): Inicio · Publicaciones ·
Usuarios · Eventos; buscador de comandos ⌘K.

## Hero del home

- **H1:** El repuesto que buscas está en algún **desarme** *(la palabra "desarme" va en naranja)*
- Subtítulo: Desarmadurías y particulares de todo Chile. Compara y contacta directo al vendedor.
- Placeholder del buscador: `Ej: Citroen C4, motor Kia Rio, faros Sail…`
- Pasos: **Busca** por marca, modelo o pieza · **Compara** fotos, precio y ubicación · **Contacta** directo por WhatsApp

Fuente: `shared/components/home-subheader/home-subheader.component.html`.

## Llamados a la acción (CTA)

### Publicar (el CTA principal, en naranja)

| Dónde | Texto | Archivo |
|---|---|---|
| Header, menú lateral | **Publica tu anuncio** | `header.component.html`, `sidenav.component.html` |
| Cinta azul bajo el hero | ¿Tienes repuestos o un auto para desarme? — *Publicar es gratis por lanzamiento · sin comisiones* — botón **Publica tu anuncio** | `pages/home/home.content.ts` (`PUBLISH_CTA`) |
| Bloque naranja del home | Eyebrow *Vender · Gratis por lanzamiento* · título **Publica tu anuncio** · *Tu publicación visible 1 año, sin comisiones por venta. Publicar toma 2 minutos.* · botón **Publicar gratis** · *Antes ~~$4.990/año~~* | `home.content.ts` |
| Beneficios | Visible 12 meses · Hasta 6 fotos · Contacto por WhatsApp | `home.content.ts` (`PUBLISH_CHECKS`) |
| Barra fija móvil | **Buscar** · **Publica gratis** | `home-mobile-actions.component.html` |
| Sin publicaciones propias | **Crear mi primera publicación** | `pages/user/user-posts/user-posts.component.html` |

### Buscar y explorar

**Buscar** · **Ver todas las publicaciones** · **Ver todos** · **Todas las marcas** · **Ver publicaciones** ·
**Reiniciar la búsqueda** · **Limpiar filtros** · **Reintentar** · **Ver otras publicaciones** · **Ir al inicio**.
Filtros: Ciudad · Marca · Año · Tipo de vehículo · Combustible · Transmisión
(`shared/components/filter-post-list`, `STYLEGUIDE.md`).

### Contactar al vendedor (`pages/posts/post-detail/post-detail.component.html`)

**Contactar por WhatsApp** (en móvil: **Contactar**) · **Contacta al Vendedor** (formulario: Nombre Apellido ·
Correo Electrónico · Teléfono (Opcional) · Mensaje · *Acepto los* Términos y condiciones / Políticas de privacidad) ·
**Enviar Mensaje** · **Editar publicación** (si es el dueño) · Copiar enlace · Compartir · Favoritos (botón decorativo, sin acción hoy).

### Cuenta

- Login: **Iniciar sesión** · "Correo Electrónico" · "Contraseña" · "Recordar mi usuario" ·
  *¿No tienes una cuenta? Regístrate* · *Olvidé mi contraseña* (`pages/auth/login`).
- Registro: **Crear cuenta** · botón **Registrarse** · éxito: *Sólo un paso más, {nombre}* → **Volver al inicio**
  (`pages/auth/register`).
- Recuperar: **Recuperar contraseña** · *Revisa tu correo* (`pages/auth/recover-password`).
- Perfil: **Mi perfil** · *Datos de contacto* · *Seguridad* · **Guardar cambios** (`pages/user/user-profile`).

### Mis publicaciones (`pages/user/user-posts/user-posts.component.html`)

**Mis publicaciones** · estados *Pendiente de revisión / Aprobada / Rechazada* · *Pausada / Pausada por el
administrador* · acciones **Editar · Pausar · Reactivar · Borrar** ("Sí, borrar" / "Cancelar").

### Formulario de publicar — "paso a paso"

(`pages/posts/post-form/post-form.blocks.ts`, `post-form.component.html`, `post-side-panel`, `post-stepper`)

- Seis bloques, en este orden: **1 Fotos · 2 Datos del vehículo · 3 Tipo de publicación · 4 Datos técnicos
  (opcional) · 5 Ubicación · 6 Descripción.**
- Subtítulo: *Seis pasos cortos. Completa cada uno y presiona Listo para pasar al siguiente.*
- Botones: **Listo, siguiente paso** · **Listo** · **Cancelar** · **Publicar** · **Guardar cambios** ·
  **Deshacer** · **Descartar todo**. Indicador: *Paso N de 6* (móvil: "Paso N de 6 · {nombre}" + "Ir a paso").
- Aviso: *Al guardar, la publicación vuelve a revisión.*
- Etiquetas de campo (`FIELD_LABELS`): Nombre de la publicación · Marca · Modelo · Año · Tipo de vehículo ·
  Combustible · Transmisión · Tipo de publicación · Motor · Chasis · Ciudad · Comuna · Precio · Descripción.

### Demanda sin resultados (`shared/components/demand-form/demand-form.component.html`)

*¿No encontraste la pieza?* — *Déjanos tu email o WhatsApp y el repuesto que buscas, te avisamos cuando se
publique.* — **Avísame** — éxito: *¡Listo! Te avisamos cuando se publique.*
Validaciones: *Cuéntanos qué buscas (al menos 2 caracteres).* · *Ingresa un email válido.* ·
*Ingresa tu WhatsApp: 9 dígitos, empezando con 9.*

### Contacto (`pages/contact/contact.component.html`)

**Contacto** · *Nombre completo · Correo electrónico · Asunto · Mensaje* · éxito **¡Mensaje enviado!** ·
*Otras formas de contacto*.

## Mensajes del sistema

| Situación | Texto | Archivo |
|---|---|---|
| Listado vacío | No encontramos publicaciones con esos filtros | `post-list.component.html:65` |
| Página inexistente | **No encontramos esta página** | `pages/not-found/not-found.component.html` |
| Publicación inexistente/pausada | **Esta publicación ya no está disponible** | `post-detail.component.html:4` |
| Resultado con búsqueda | *Resultados para {búsqueda}* · "Publicaciones · N resultado(s)" | `post-list.component.ts`, `.html` |
| Título del listado sin filtros | **Repuestos usados y autos en desarme** | `post-list.component.ts` (`heading`) |
| Seguridad | Para evitar estafas, recomendamos comprar los repuestos personalmente y no transferir dinero por adelantado. — *Equipo Desarmalo.cl* | `home.content.ts` (`SAFETY_NOTICE`) |
| Sesión expirada (admin) | Tu sesión expiró. ~~Iniciá~~ sesión de nuevo. | `apps/admin/.../login.component.html:24` |

## Páginas informativas

- **Sobre Desarmalo.cl**: Nuestros fundadores · Misión y visión · Nuestros logros y metas (Posicionamiento digital ·
  Crecimiento constante · Expansión nacional) · **¿Cómo funciona Desarmalo.cl?** (1 *Registra tu vehículo* ·
  2 *Especifica las piezas disponibles* · 3 *Recibe contactos directos*) · ¿Por qué elegirnos?
  (`pages/about-us/about-us.component.html`).
- **Términos y condiciones** · **Políticas de privacidad** (`pages/terms`, `pages/policies`).

## Observaciones

- El admin tiene un voseo ("Iniciá") que contradice la regla de tuteo del proyecto; está marcado con ~~tachado~~
  arriba y debería corregirse en el código.
- Hay inconsistencias de capitalización/ortografía en el código, copiadas tal cual: "Categorias" (sin tilde) en el
  menú lateral, "Desarmaduria" (sin tilde) en el título de la tarjeta de `categories.component.html`, "Cerrar
  Sesión" y "Correo Electrónico" con mayúscula en la segunda palabra.
- El texto "Publica tu anuncio" es contrato con los tests (el CTA mantiene ese texto exacto; ver
  `apps/web/STYLEGUIDE.md` § Header/footer): no renombrarlo sin actualizar `apps/web/e2e`.
