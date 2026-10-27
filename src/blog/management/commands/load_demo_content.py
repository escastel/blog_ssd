from io import BytesIO
from datetime import timedelta

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand
from django.utils import timezone

from PIL import Image, ImageDraw

from blog.models import AboutPage, Article


DEMO_ARTICLES = (
    {
        "title": "Robots que aprenden a caminar",
        "slug": "robots-que-aprenden-a-caminar",
        "excerpt": "Cómo equilibrio, sensores y práctica ayudan a un robot a dar sus primeros pasos.",
        "author": "Marina Torres",
        "days_ago": 1,
        "color": (8, 126, 139),
        "content": (
            "## El reto del equilibrio\n\n"
            "Caminar parece sencillo, pero cada paso exige coordinar sensores, motores "
            "y cambios de peso. Un robot debe reaccionar cuando el suelo o su postura "
            "no son exactamente los esperados.\n\n"
            "## Aprender con cada paso\n\n"
            "Los prototipos actuales combinan modelos de movimiento con práctica "
            "repetida. Al medir sus resultados, ajustan la fuerza y la posición de "
            "sus articulaciones."
        ),
    },
    {
        "title": "Sensores para explorar el entorno",
        "slug": "sensores-para-explorar-el-entorno",
        "excerpt": "Cámaras, distancia y tacto: las señales que permiten orientarse a las máquinas.",
        "author": "Marina Torres",
        "days_ago": 4,
        "color": (54, 94, 153),
        "content": (
            "## Ver más allá de una cámara\n\n"
            "Un robot móvil puede combinar cámaras con sensores de distancia para "
            "detectar obstáculos y estimar cuánto espacio tiene a su alrededor.\n\n"
            "## De la señal a una decisión\n\n"
            "La información de cada sensor se transforma en un mapa útil para "
            "planificar movimientos seguros y llegar al destino."
        ),
    },
    {
        "title": "Un brazo robótico en el taller",
        "slug": "un-brazo-robotico-en-el-taller",
        "excerpt": "Qué hace falta para que un brazo mecánico manipule piezas con precisión.",
        "author": "Marina Torres",
        "days_ago": 8,
        "color": (173, 104, 54),
        "content": (
            "## Articulaciones coordinadas\n\n"
            "Cada articulación aporta un movimiento. El controlador coordina todas "
            "para colocar la herramienta en el punto deseado.\n\n"
            "## Precisión y seguridad\n\n"
            "En un taller, el brazo debe repetir movimientos con precisión y "
            "detenerse cuando una persona u objeto entra en su zona de trabajo."
        ),
    },
)


def make_demo_image(title, color):
    image = Image.new("RGB", (960, 600), color)
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((345, 110, 615, 390), radius=60, fill=(232, 242, 240))
    draw.ellipse((395, 175, 445, 225), fill=(23, 43, 58))
    draw.ellipse((515, 175, 565, 225), fill=(23, 43, 58))
    draw.rounded_rectangle((430, 270, 530, 300), radius=12, fill=color)
    draw.line((480, 110, 480, 55), fill=(232, 242, 240), width=14)
    draw.ellipse((458, 30, 502, 74), fill=(232, 242, 240))
    draw.text((70, 470), title, fill=(255, 255, 255), stroke_width=1)
    output = BytesIO()
    image.save(output, format="PNG")
    return output.getvalue()


class Command(BaseCommand):
    help = "Crea una presentación del autor y artículos de ejemplo editables."

    def handle(self, *args, **options):
        AboutPage.objects.get_or_create(
            pk=1,
            defaults={
                "content": (
                    "¡Hola! Soy Marina, divulgadora y entusiasta de la robótica. "
                    "En este espacio comparto ideas para entender cómo se diseñan "
                    "las máquinas que nos ayudan a explorar, aprender y construir."
                )
            },
        )

        created_count = 0
        for item in DEMO_ARTICLES:
            if Article.objects.filter(slug=item["slug"]).exists():
                continue

            image_name = f"articles/demo-{item['slug']}.png"
            if not default_storage.exists(image_name):
                image_name = default_storage.save(
                    image_name,
                    ContentFile(make_demo_image(item["title"], item["color"])),
                )

            Article.objects.create(
                title=item["title"],
                slug=item["slug"],
                image=image_name,
                publication_date=timezone.now() - timedelta(days=item["days_ago"]),
                excerpt=item["excerpt"],
                content=item["content"],
                author=item["author"],
                published=True,
            )
            created_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Contenido de ejemplo listo; {created_count} artículos nuevos."
            )
        )
