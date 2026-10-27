# Alcance del producto: Blog de robótica

## Objetivo

Definir qué incluye la primera versión del blog de robótica y qué queda fuera. El producto ofrecerá una experiencia de lectura sencilla, adaptable y accesible, con gestión básica de contenido.

## Incluido en la primera versión

- **Portada:** muestra el nombre del blog y los artículos publicados más recientes, ordenados del más nuevo al más antiguo. Cada artículo presenta título, imagen, fecha y extracto, y enlaza al texto completo. Si no hay artículos publicados, se muestra un mensaje informativo.
- **Artículos:** cada artículo tiene una página propia con título, imagen, fecha de publicación, autoría y contenido estructurado en párrafos y subtítulos. Las rutas inexistentes muestran una respuesta 404 original (y a ser posible, graciosa).
- **Sobre mí:** página con una presentación breve y editable del autor, accesible desde la navegación principal.
- **Navegación:** enlaces claros entre la portada y «Sobre mí», y una forma de volver a la portada desde un artículo. La navegación básica funciona sin JavaScript.
- **Diseño y accesibilidad:** interfaz legible y adaptable a móviles y ordenadores, con HTML semántico, encabezados coherentes, enlaces descriptivos y uso mediante teclado.
- **Contenido inicial:** artículos de ejemplo sobre robótica y una presentación inicial del autor, sustituibles o eliminables.
- **Gestión editorial:** Django Admin permite al editor autorizado crear, editar y retirar artículos, y actualizar la presentación del autor. Los artículos no publicados no aparecen en las páginas públicas.
- **API REST:** `GET /api/articulos/` lista artículos publicados y `GET /api/articulos/<id>/` consulta uno por identificador. `POST /api/articulos/` permite a un editor autorizado, mediante token de Django, crear borradores enviando título y cuerpo. La API no ofrece publicación ni acceso a borradores.

## Excluido

- Cuentas, perfiles o registro para lectores.
- Comentarios.
- Suscripciones o boletines.
- Buscador.
- Flujos editoriales avanzados, como revisión, programación de publicaciones o múltiples roles.
- Funciones de interacción social.
- Registro público, autenticación propia de la API o publicación de artículos mediante API.

## Límites y supuestos

- El idioma inicial será el español y la temática, la robótica.
- La primera versión contempla un editor y una única presentación principal del autor.
- El contenido definitivo, la identidad visual, el dominio y el entorno de despliegue están por definir.
- SQLite se utilizará para el desarrollo inicial; la base de datos de producción dependerá del entorno de despliegue.