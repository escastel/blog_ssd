# Incorporar API REST al blog Django

Actúa como desarrollador experto en Django y SDD.

Analiza el repositorio, especialmente `src/blog/`, `PRD.md` y `spec/`. **Actualiza primero las especificaciones y después implementa la API.**

1. **API:** utiliza Django REST Framework e incorpora:
   - `GET /api/articulos/`: listar artículos publicados.
   - `GET /api/articulos/{id}/`: consultar un artículo publicado.
   - `POST /api/articulos/`: crear un borrador.

2. **Contrato JSON:** el POST recibe `titulo` y `cuerpo`. La respuesta incluye `id`, `titulo`, `cuerpo` y `estado` (`publicado` o `borrador`).

3. **Modelo:** conserva `Article` y su campo `published`. El POST siempre guardará `published=False`. Completa automáticamente los demás campos obligatorios utilizando soluciones compatibles con el modelo existente.

4. **Seguridad:** los GET son públicos y excluyen borradores. El POST requiere un token del administrador de Django. No implementes nuevos sistemas de usuarios.

5. **Compatibilidad:** conserva la web, Django Admin y los artículos existentes. Evita modificar el modelo o crear migraciones salvo que sean imprescindibles.

6. **Verificación:** ejecuta las pruebas existentes y añade pruebas de API, permisos, validación y regresión. Actualiza el README con ejemplos `curl`.

No implementes FastAPI, agentes ni MCP. Resume los cambios y los resultados de las pruebas.