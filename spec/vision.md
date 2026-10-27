# Visión del producto: Blog de robótica

## Visión

Ofrecer un espacio digital sencillo, accesible y adaptable donde las personas interesadas en la robótica puedan descubrir y leer artículos con comodidad, y conocer a quien los escribe. El sitio debe permitir que su editor mantenga el contenido actualizado sin tener que modificar las plantillas.

## Usuarios principales

- **Visitantes:** personas interesadas en la robótica que quieren consultar artículos recientes, leerlos completos y conocer al autor.
- **Editor del sitio:** persona responsable de gestionar los artículos y actualizar la presentación del autor mediante el panel administrativo de Django.

## Propuesta de valor

- Facilitar el descubrimiento de artículos recientes y el acceso a cada texto completo.
- Ofrecer una experiencia de lectura clara en móviles y ordenadores, con contenido estructurado y navegación comprensible.
- Dar al editor una forma sencilla de mantener los contenidos desde Django Admin, sin editar manualmente las plantillas.

## Principios del producto

1. **Contenido primero:** la interfaz debe ayudar a leer, con tipografía, contraste y espaciado adecuados.
2. **Sencillez:** las páginas y los enlaces deben ser claros y previsibles; la navegación básica no dependerá de JavaScript.
3. **Accesibilidad y adaptación:** el sitio debe usar estructura semántica y funcionar con teclado y en pantallas pequeñas y grandes.
4. **Edición práctica:** el contenido debe poder actualizarse desde Django Admin, con acceso reservado a usuarios autorizados.
5. **Robustez:** las rutas de artículos inexistentes deben responder con una página 404 adecuada.

## Indicadores de éxito

- Una persona visitante puede encontrar un artículo en la portada, abrirlo y leerlo completo.
- La sección «Sobre mí» se encuentra desde la navegación principal.
- La experiencia mantiene su legibilidad y navegación en móvil y escritorio, sin desplazamiento horizontal innecesario.
- El editor puede actualizar artículos y la presentación del autor sin modificar las plantillas.
