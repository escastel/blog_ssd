# Criterios de aceptación: Blog de robótica

Estos criterios concretan el PRD y el alcance de la primera versión. Cada criterio describe un resultado observable que puede comprobarse manualmente o mediante pruebas automatizadas.

## CA-01: Mostrar la portada

**Dado** que una persona visita la ruta raíz  
**Cuando** hay artículos publicados  
**Entonces** la portada muestra el nombre del blog y los artículos en orden descendente por fecha de publicación  
**Y** cada artículo incluye título, imagen, fecha y extracto  
**Y** el título o elemento del artículo enlaza a su página completa.

## CA-02: Mostrar un estado vacío

**Dado** que no hay artículos publicados  
**Cuando** una persona visita la portada  
**Entonces** se muestra un mensaje que informa de que todavía no hay artículos, en lugar de una lista vacía sin explicación.

## CA-03: Leer un artículo

**Dado** que existe un artículo publicado  
**Cuando** una persona abre su URL individual  
**Entonces** se muestran el título, la imagen, la fecha de publicación, la autoría y el contenido  
**Y** los párrafos y subtítulos del contenido se conservan como una estructura legible.

## CA-04: Gestionar una imagen de artículo

**Dado** que el editor crea o modifica un artículo  
**Cuando** guarda el artículo con su imagen  
**Entonces** esa imagen se muestra en la portada y en la página individual del artículo.

## CA-05: Responder a una URL de artículo inexistente

**Dado** que una persona solicita la URL de un artículo inexistente  
**Cuando** el sitio procesa la solicitud  
**Entonces** responde con el estado HTTP 404  
**Y** muestra una página de error propia, con un mensaje original y, si encaja con el diseño, humorístico.

## CA-06: Consultar «Sobre mí»

**Dado** que una persona visita la página «Sobre mí»  
**Cuando** se carga la página  
**Entonces** se identifica claramente la sección y se muestra la presentación vigente del autor  
**Y** la navegación principal ofrece un enlace descriptivo para llegar a ella.

## CA-07: Navegar por el sitio

**Dado** que una persona está en la portada, en «Sobre mí» o en un artículo  
**Cuando** utiliza los enlaces de navegación  
**Entonces** puede volver a la portada y acceder a «Sobre mí» desde la navegación principal  
**Y** desde una página de artículo puede volver a la portada  
**Y** estos recorridos funcionan sin JavaScript.

## CA-08: Crear y actualizar contenido como editor

**Dado** que el editor ha iniciado sesión y está autorizado en Django Admin  
**Cuando** crea o modifica un artículo o la presentación del autor  
**Entonces** puede guardar esos cambios desde el panel administrativo  
**Y** los cambios se reflejan en las páginas públicas correspondientes.

## CA-09: Retirar contenido y ocultar borradores

**Dado** que un artículo no está publicado o ha sido retirado  
**Cuando** una persona visita la portada o intenta acceder al contenido público  
**Entonces** el artículo no aparece ni se ofrece como contenido público.

## CA-10: Restringir la gestión editorial

**Dado** que una persona visitante no ha iniciado sesión con una cuenta autorizada  
**Cuando** intenta acceder a funciones de edición del panel administrativo  
**Entonces** no puede crear, modificar ni retirar contenido  
**Y** el sitio no ofrece un proceso público de registro de lectores.

## CA-11: Presentar contenido inicial editable

**Dado** que se entrega la primera versión  
**Cuando** una persona visita el blog  
**Entonces** encuentra contenido de ejemplo relacionado con robótica y una presentación inicial del autor  
**Y** el editor puede sustituir o retirar esos contenidos desde la gestión editorial.

## CA-12: Adaptarse a distintos tamaños de pantalla

**Dado** que una persona visita el sitio desde una pantalla pequeña o grande  
**Cuando** consulta la portada, un artículo o «Sobre mí»  
**Entonces** puede leer el contenido y utilizar la navegación sin desplazamiento horizontal innecesario ni pérdida de información.

## CA-13: Permitir navegación accesible

**Dado** que una persona navega por cualquiera de las páginas  
**Cuando** utiliza un teclado o tecnologías de asistencia  
**Entonces** puede identificar y activar los enlaces  
**Y** el contenido utiliza HTML semántico, encabezados coherentes y nombres de enlace descriptivos.

## CA-14: Renderizar las páginas de lectura en el servidor

**Dado** que una persona solicita una página pública informativa  
**Cuando** Django procesa la solicitud  
**Entonces** el servidor entrega el contenido de la página  
**Y** la lectura y la navegación básica no dependen de JavaScript.

## CA-15: Listar artículos mediante la API

**Dado** que existen artículos publicados y borradores
**Cuando** una persona solicita `GET /api/articulos/`
**Entonces** recibe HTTP 200 y una lista JSON de artículos publicados
**Y** cada elemento contiene `id`, `titulo`, `cuerpo` y `estado: "publicado"`
**Y** ningún borrador aparece en la respuesta.

## CA-16: Consultar un artículo mediante la API

**Dado** que existe un artículo publicado
**Cuando** una persona solicita `GET /api/articulos/{id}/`
**Entonces** recibe HTTP 200 con JSON que contiene `id`, `titulo`, `cuerpo` y `estado: "publicado"`
**Y** un identificador inexistente o correspondiente a un borrador responde HTTP 404.

## CA-17: Crear un borrador mediante la API

**Dado** que una persona editora activa presenta un token de Django válido
**Cuando** envía `POST /api/articulos/` con `titulo` y `cuerpo` válidos
**Entonces** se crea un artículo con `published=False` y responde HTTP 201
**Y** el JSON de respuesta contiene `id`, `titulo`, `cuerpo` y `estado: "borrador"`
**Y** el artículo no aparece en la web ni en los endpoints GET.

## CA-18: Proteger la creación de borradores

**Dado** que la persona no presenta un token válido o no tiene acceso editorial
**Cuando** intenta enviar `POST /api/articulos/`
**Entonces** la API responde HTTP 401 o 403 según corresponda
**Y** no se crea ningún artículo.

## CA-19: Validar datos de entrada de la API

**Dado** que una solicitud POST omite el título o el cuerpo, o proporciona valores vacíos o inválidos
**Cuando** se procesa la solicitud
**Entonces** la API responde con un error de validación JSON
**Y** no se crea ningún artículo.