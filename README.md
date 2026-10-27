# Blog de robótica

Proyecto para crear un blog en español dedicado a la robótica, pensado para que sus visitantes descubran artículos recientes, los lean con comodidad y conozcan al autor.

## Descripción

El sitio ofrecerá una portada con los artículos publicados, una página para leer cada artículo completo y una sección «Sobre mí». La experiencia priorizará el contenido: navegación sencilla, diseño adaptable a móviles y ordenadores, y una estructura accesible y legible.

El editor podrá mantener los artículos y la presentación del autor desde el panel administrativo estándar de Django, sin modificar manualmente las plantillas. El contenido inicial será de ejemplo y podrá sustituirse o retirarse.

## Funcionalidades previstas

- Listado de artículos publicados en orden cronológico, con título, imagen, fecha y extracto.
- Página individual de cada artículo con su contenido y datos de publicación.
- Página «Sobre mí», editable y accesible desde la navegación principal.
- Navegación básica que funciona sin JavaScript.
- Página 404 propia para artículos inexistentes.
- Gestión de artículos y de la presentación del autor mediante Django Admin, restringida a usuarios autorizados.
- API REST para consultar artículos publicados y crear borradores con un token de administrador.

## Tecnologías previstas

- Python 3.12 y Django 5.2 LTS para el backend y el renderizado de páginas en el servidor.
- Django REST Framework y tokens de autenticación de Django para la API.
- Modelos y migraciones Django para persistir los contenidos.
- Plantillas HTML semánticas y CSS adaptable.
- SQLite para el desarrollo inicial; la base de datos de producción se decidirá según el entorno de despliegue.
- Código Django, dependencias y `manage.py` organizados en `src/`; la documentación y la configuración general del repositorio permanecen en la raíz.

## Puesta en marcha

Activa el entorno virtual, instala las dependencias y prepara la base de datos:

```bash
source .venv/bin/activate
python -m pip install -r src/requirements.txt
python src/manage.py migrate
python src/manage.py load_demo_content
python src/manage.py runserver
```

El servidor de desarrollo estará disponible en <http://127.0.0.1:8000/>.

El panel administrativo se encuentra en <http://127.0.0.1:8000/admin/>; para crear un usuario administrador, ejecuta:

```bash
python src/manage.py createsuperuser
```

No hay un usuario ni una clave predeterminados para el panel. Inicia sesión con las credenciales del superusuario que hayas creado.

En producción, configura `PYTHONPATH=src`, `DJANGO_SECRET_KEY`, `DJANGO_ALLOWED_HOSTS` y `DJANGO_DEBUG=False`, y despliega detrás de HTTPS. No reutilices la clave de desarrollo.

## API REST

La API devuelve JSON con `id`, `titulo`, `cuerpo` y `estado`. Los endpoints de lectura son públicos y solo incluyen artículos publicados:

```bash
curl http://127.0.0.1:8000/api/articulos/
curl http://127.0.0.1:8000/api/articulos/1/
```

Para crear un borrador, genera un token para el usuario editor existente:

```bash
python src/manage.py drf_create_token nombre_de_usuario
```

Envía el token en el encabezado `Authorization`. El cuerpo requiere `titulo` y `cuerpo`; el artículo siempre se guarda como borrador:

En Bash o Git Bash, carga el token desde `.env` con `source`. El fichero debe
contener una asignación como `export BLOG_API_TOKEN="TU_TOKEN"`:

```bash
source .env
curl -X POST http://127.0.0.1:8000/api/articulos/ \
  -H "Authorization: Token $BLOG_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"titulo":"Robótica educativa","cuerpo":"Contenido del borrador."}'
```

En PowerShell, asigna el token directamente a una variable y utiliza
`Invoke-RestMethod` para enviar JSON sin problemas de comillas:

```powershell
$token = "TU_TOKEN"

$body = @{
  titulo = "Robótica educativa"
  cuerpo = "Contenido del borrador."
} | ConvertTo-Json

Invoke-RestMethod `
  -Uri http://127.0.0.1:8000/api/articulos/ `
  -Method Post `
  -Headers @{ Authorization = "Token $token" } `
  -ContentType "application/json" `
  -Body $body
```

La cuenta debe tener acceso administrativo (`is_staff`). No compartas ni publiques el token.

## Fuera del alcance inicial

No se contemplan cuentas para lectores, comentarios, suscripciones, buscador, interacción social ni flujos editoriales avanzados.

## Documentación

- [Briefing](./briefing.md)
- [Requisitos del producto (PRD)](./PRD.md)
- [Visión del producto](./spec/vision.md)
- [Alcance](./spec/scope.md)
- [Criterios de aceptación](./spec/acceptance_criteria.md)

> El proyecto Django y la aplicación `blog` están en `src/`. `load_demo_content` añade artículos de ejemplo y genera imágenes localmente para que puedan editarse o retirarse desde Django Admin.