# PRD: Blog de robótica

## 1. Resumen

Crear un blog de robótica sencillo, claro y adaptable a móviles y ordenadores. Las personas visitantes podrán consultar los artículos recientes, leer cada artículo completo y conocer al autor en una sección «Sobre mí». El sitio se implementará con Django.

## 2. Objetivo y contexto

El producto busca compartir artículos sobre robótica en una experiencia centrada en la lectura. La navegación debe ser sencilla y el contenido debe poder actualizarse sin modificar manualmente las plantillas del sitio.

## 3. Usuarios

- **Visitante:** persona interesada en leer artículos de robótica y conocer al autor.
- **Editor del sitio:** persona responsable de añadir y actualizar los artículos y la presentación del autor.

No habrá cuentas públicas ni registro de lectores. Para mantener el contenido se contempla el panel administrativo estándar de Django, reservado al editor del sitio.

## 4. Alcance del producto

### Incluido

1. Portada con el nombre del blog y una lista de artículos recientes.
2. Página individual para cada artículo.
3. Página «Sobre mí» con una presentación breve del autor.
4. Navegación visible entre la portada y «Sobre mí».
5. Diseño adaptable, legible y accesible, con prioridad en el contenido.
6. Contenido inicial de ejemplo que pueda sustituirse.
7. Gestión básica del contenido mediante el panel administrativo de Django.
8. API REST para consultar artículos publicados y crear borradores con autorización del editor.

### Excluido

- Cuentas o perfiles para lectores.
- Comentarios.
- Suscripciones o boletines.
- Buscador.
- Flujos editoriales avanzados, como revisión, programación de publicaciones o múltiples roles.
- Funciones de interacción social.

## 5. Requisitos funcionales

### RF-01: Mostrar la portada

La portada debe mostrar el nombre del blog y una lista de artículos recientes publicados, ordenados del más nuevo al más antiguo. Cada elemento debe incluir título, fecha y un extracto, y enlazar al artículo completo.

**Criterios de aceptación**

- Al visitar la ruta raíz, se muestra la portada.
- Los artículos publicados aparecen en orden cronológico descendente.
- Cada artículo de la lista permite abrir su página individual.
- Si todavía no hay artículos publicados, se muestra un mensaje informativo en lugar de una lista vacía sin contexto.

### RF-02: Leer un artículo

Cada artículo debe tener una página propia que muestre título, fecha de publicación, autoría y contenido. El texto debe admitir párrafos y subtítulos para facilitar la lectura.

**Criterios de aceptación**

- La página muestra todos los datos disponibles del artículo.
- El contenido mantiene una estructura legible y conserva sus párrafos y subtítulos.
- Una ruta de artículo inexistente devuelve una página de no encontrado (HTTP 404).

### RF-03: Consultar «Sobre mí»

La sección «Sobre mí» debe presentar brevemente al autor y ser accesible desde la navegación principal.

**Criterios de aceptación**

- Existe una página identificable como «Sobre mí».
- La navegación principal incluye un enlace a dicha página.
- El contenido inicial de presentación puede sustituirse por el del autor.

### RF-04: Navegar por el sitio

Las páginas deben ofrecer navegación sencilla entre la portada y «Sobre mí». Desde un artículo se debe poder volver a la portada.

**Criterios de aceptación**

- Los enlaces principales funcionan desde las páginas del sitio.
- Los enlaces tienen nombres claros y comprensibles.
- No se requiere JavaScript para la navegación básica.

### RF-05: Gestionar contenido

El editor podrá crear, editar y retirar artículos y actualizar el texto de «Sobre mí» a través del panel administrativo estándar de Django.

**Criterios de aceptación**

- El panel administrativo permite gestionar los artículos y la presentación del autor.
- Los artículos no publicados no aparecen en las páginas públicas.
- No se ofrece un proceso de registro público.

### RF-06: Consultar artículos mediante la API

La API REST ofrecerá `GET /api/articulos/` para listar artículos publicados y `GET /api/articulos/{id}/` para consultar un artículo publicado. Ambos endpoints serán públicos y nunca expondrán borradores.

**Criterios de aceptación**

- La lista y el detalle devuelven JSON con `id`, `titulo`, `cuerpo` y `estado`.
- `estado` será `publicado` para los artículos expuestos; un borrador no será accesible por API y el detalle responderá HTTP 404.

### RF-07: Crear borradores mediante la API

`POST /api/articulos/` aceptará `titulo` y `cuerpo` en JSON y creará un artículo no publicado. La operación requerirá un token de un usuario activo con acceso administrativo de Django.

**Criterios de aceptación**

- Una solicitud sin credenciales válidas o de un usuario que no sea editor autorizado no crea artículos.
- Una solicitud válida devuelve HTTP 201 y JSON con `id`, `titulo`, `cuerpo` y `estado: "borrador"`.
- Los campos obligatorios restantes del modelo se completan en el servidor, sin permitir publicar el artículo desde la API.
- Los datos ausentes o inválidos responden con errores de validación JSON y no crean artículos.

## 6. Requisitos de contenido y datos

### Artículo

Cada artículo tendrá, como mínimo:

- Título.
- Identificador legible para la URL (slug).
- Contenido.
- Autoría.
- Fecha de publicación.
- Estado de publicación.

Los artículos publicados se mostrarán en la portada. Los borradores solo estarán disponibles para el editor autenticado mediante el panel administrativo.

### Presentación del autor

La sección «Sobre mí» tendrá un texto breve editable. Para la primera versión puede existir una única presentación del sitio.

### Contenido inicial

La entrega incluirá contenido de ejemplo relacionado con robótica. Este contenido deberá poder sustituirse o eliminarse desde la gestión de contenido.

## 7. Requisitos no funcionales

- **Adaptabilidad:** las páginas deben poder utilizarse en pantallas pequeñas y grandes sin desplazamiento horizontal innecesario.
- **Legibilidad:** tipografía, contraste, espaciado y longitud de línea deben favorecer la lectura prolongada.
- **Accesibilidad:** usar HTML semántico, estructura de encabezados coherente, enlaces descriptivos y controles utilizables con teclado.
- **Rendimiento:** las páginas informativas deben renderizarse en el servidor con Django y evitar dependencias de JavaScript innecesarias.
- **Robustez:** las rutas inválidas de artículos deben mostrar una respuesta 404 adecuada.
- **Seguridad:** el panel administrativo no debe exponer operaciones de edición a visitantes anónimos; se deben seguir las prácticas de seguridad de Django para producción.

## 8. Propuesta técnica

- **Backend y renderizado:** Django, con vistas y plantillas del servidor.
- **Persistencia:** modelos Django y migraciones para artículos y presentación del autor.
- **Gestión editorial:** Django Admin, restringido a usuarios autorizados.
- **API:** Django REST Framework; autenticación por token para crear borradores y lectura pública de artículos publicados.
- **Interfaz:** plantillas HTML semánticas y CSS adaptable; JavaScript solo si una necesidad concreta lo justifica.
- **Base de datos:** SQLite para desarrollo inicial. La elección de base de datos para producción queda pendiente de las necesidades de despliegue.

La estructura exacta de aplicaciones, versiones de Django y configuración de despliegue se decidirán durante la implementación.

## 9. Rutas propuestas

- `/` — portada y artículos recientes.
- `/sobre-mi/` — presentación del autor.
- `/articulos/<slug>/` — detalle de un artículo.
- `/api/articulos/` — listado público de artículos publicados; `POST` crea un borrador y requiere token administrativo.
- `/api/articulos/<id>/` — detalle público de un artículo publicado.
- `/admin/` — panel administrativo de Django, con acceso restringido.

## 10. Métricas de éxito

- Un visitante puede llegar desde la portada al artículo elegido y leerlo completo.
- Un visitante puede encontrar y consultar la sección «Sobre mí».
- Las páginas se pueden utilizar en móvil y escritorio sin perder contenido o navegación.
- El editor puede actualizar los artículos y la presentación sin editar las plantillas.

## 11. Supuestos y decisiones pendientes

- El tema del contenido es la robótica, de acuerdo con el briefing.
- El sitio tendrá un editor y una presentación principal del autor en su primera versión.
- El idioma inicial del sitio será el español.
- El dominio, identidad visual, contenido definitivo y entorno de despliegue todavía no están definidos.
- La selección de base de datos para producción dependerá del entorno donde se publique el sitio.
