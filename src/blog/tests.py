from datetime import timedelta
from io import BytesIO
import json
import tempfile

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from PIL import Image
from rest_framework.authtoken.models import Token

from .models import AboutPage, Article


def make_test_image(name="robot.png"):
    image_content = BytesIO()
    Image.new("RGB", (8, 8), color="teal").save(image_content, format="PNG")
    return SimpleUploadedFile(
        name,
        image_content.getvalue(),
        content_type="image/png",
    )


class BlogPageTests(TestCase):
    def setUp(self):
        temporary_media = tempfile.TemporaryDirectory()
        self.addCleanup(temporary_media.cleanup)
        self.enterContext(override_settings(MEDIA_ROOT=temporary_media.name))
        AboutPage.objects.update_or_create(
            pk=1,
            defaults={"content": "Presentación de prueba del autor."},
        )

    def create_article(self, **overrides):
        article_data = {
            "title": "Robótica educativa",
            "slug": "robotica-educativa",
            "image": make_test_image(),
            "publication_date": timezone.now(),
            "excerpt": "Un extracto sobre robótica.",
            "content": "## Primeros pasos\n\nContenido del artículo.",
            "author": "Ada",
            "published": True,
        }
        article_data.update(overrides)
        return Article.objects.create(**article_data)

    def test_home_lists_published_articles_newest_first_with_image_and_link(self):
        older = self.create_article(
            title="Primeros pasos",
            slug="primeros-pasos",
            publication_date=timezone.now() - timedelta(days=2),
        )
        newer = self.create_article(
            title="Robots actuales",
            slug="robots-actuales",
            publication_date=timezone.now() - timedelta(days=1),
        )
        draft = self.create_article(
            title="Borrador secreto",
            slug="borrador-secreto",
            published=False,
        )

        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Blog de robótica")
        self.assertEqual(list(response.context["articles"]), [newer, older])
        self.assertContains(response, newer.image.url)
        self.assertContains(response, 'alt="Robots actuales"')
        self.assertContains(response, reverse("article-detail", args=[newer.slug]))
        self.assertNotContains(response, draft.title)

    def test_home_shows_informative_empty_state_when_there_are_no_published_articles(self):
        self.create_article(published=False)

        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Todavía no hay artículos publicados")
        self.assertNotContains(response, "article-grid")
        self.assertNotContains(response, "Robótica educativa")

    def test_article_detail_shows_metadata_image_and_safe_structured_content(self):
        article = self.create_article(
            content="## El primer movimiento\n\nUn párrafo.\n\n<script>alert('x')</script>"
        )

        response = self.client.get(article.get_absolute_url())

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, article.title)
        self.assertContains(response, article.image.url)
        self.assertContains(response, article.author)
        self.assertContains(response, '<h2>El primer movimiento</h2>', html=True)
        self.assertContains(response, "<p>Un párrafo.</p>", html=True)
        self.assertNotContains(response, "<script>alert")

    def test_unpublished_article_is_not_publicly_accessible(self):
        article = self.create_article(published=False)

        with override_settings(DEBUG=False):
            response = self.client.get(article.get_absolute_url())

        self.assertEqual(response.status_code, 404)
        self.assertContains(response, "Este robot se ha perdido", status_code=404)

    def test_unknown_article_uses_custom_not_found_page(self):
        with override_settings(DEBUG=False):
            response = self.client.get("/articulos/no-existe/")

        self.assertEqual(response.status_code, 404)
        self.assertContains(response, "Este robot se ha perdido", status_code=404)
        self.assertContains(response, reverse("home"), status_code=404)

    def test_about_page_is_editable_and_has_main_navigation(self):
        response = self.client.get(reverse("about"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<h1 id=\"page-title\">Sobre mí</h1>", html=True)
        self.assertContains(response, "Presentación de prueba del autor.")
        self.assertContains(response, reverse("home"))
        self.assertContains(response, reverse("about"))

    def test_navigation_is_available_from_home_and_article(self):
        article = self.create_article()

        for url in (reverse("home"), article.get_absolute_url()):
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertContains(response, 'aria-label="Navegación principal"')
                self.assertContains(response, reverse("about"))
                self.assertContains(response, reverse("home"))


class ArticleApiTests(TestCase):
    def setUp(self):
        temporary_media = tempfile.TemporaryDirectory()
        self.addCleanup(temporary_media.cleanup)
        self.enterContext(override_settings(MEDIA_ROOT=temporary_media.name))
        user_model = get_user_model()
        self.admin = user_model.objects.create_superuser(
            username="api-editor",
            email="api-editor@example.com",
            password="Strong-test-password-123!",
        )
        self.admin_token = Token.objects.create(user=self.admin)
        self.reader = user_model.objects.create_user(
            username="api-reader",
            password="Strong-test-password-123!",
        )
        self.reader_token = Token.objects.create(user=self.reader)

    def create_article(self, **overrides):
        article_data = {
            "title": "Artículo publicado",
            "slug": "articulo-publicado",
            "image": make_test_image(),
            "publication_date": timezone.now(),
            "excerpt": "Extracto.",
            "content": "Contenido completo.",
            "author": "Ada",
            "published": True,
        }
        article_data.update(overrides)
        return Article.objects.create(**article_data)

    def test_public_list_and_detail_return_only_published_articles(self):
        published = self.create_article()
        draft = self.create_article(
            title="Borrador privado",
            slug="borrador-privado",
            published=False,
        )

        list_response = self.client.get("/api/articulos/")
        detail_response = self.client.get(f"/api/articulos/{published.pk}/")

        self.assertEqual(list_response.status_code, 200)
        self.assertEqual(
            list_response.json(),
            [
                {
                    "id": published.pk,
                    "titulo": published.title,
                    "cuerpo": published.content,
                    "estado": "publicado",
                }
            ],
        )
        self.assertEqual(detail_response.status_code, 200)
        self.assertEqual(
            detail_response.json(),
            {
                "id": published.pk,
                "titulo": published.title,
                "cuerpo": published.content,
                "estado": "publicado",
            },
        )
        self.assertEqual(self.client.get(f"/api/articulos/{draft.pk}/").status_code, 404)
        self.assertEqual(self.client.get("/api/articulos/999999/").status_code, 404)

    def test_draft_creation_requires_an_admin_token(self):
        payload = {"titulo": "Nuevo artículo", "cuerpo": "Contenido nuevo."}

        missing_token = self.client.post(
            "/api/articulos/",
            data=json.dumps(payload),
            content_type="application/json",
        )
        invalid_token = self.client.post(
            "/api/articulos/",
            data=json.dumps(payload),
            content_type="application/json",
            HTTP_AUTHORIZATION="Token invalid",
        )
        non_admin_token = self.client.post(
            "/api/articulos/",
            data=json.dumps(payload),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Token {self.reader_token.key}",
        )

        self.assertEqual(missing_token.status_code, 401)
        self.assertEqual(invalid_token.status_code, 401)
        self.assertEqual(non_admin_token.status_code, 403)
        self.assertEqual(Article.objects.count(), 0)

    def test_admin_can_create_a_complete_unpublished_article(self):
        payload = {
            "titulo": "Robótica educativa",
            "cuerpo": "A" * 450,
            "published": True,
        }
        response = self.client.post(
            "/api/articulos/",
            data=json.dumps(payload),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Token {self.admin_token.key}",
        )

        self.assertEqual(response.status_code, 201)
        article = Article.objects.get(pk=response.json()["id"])
        self.assertEqual(
            response.json(),
            {
                "id": article.pk,
                "titulo": payload["titulo"],
                "cuerpo": payload["cuerpo"],
                "estado": "borrador",
            },
        )
        self.assertFalse(article.published)
        self.assertEqual(article.slug, "robotica-educativa")
        self.assertEqual(article.content, payload["cuerpo"])
        self.assertEqual(article.excerpt, payload["cuerpo"][:400])
        self.assertEqual(article.author, self.admin.username)
        self.assertIsNotNone(article.publication_date)
        self.assertTrue(article.image.storage.exists(article.image.name))
        self.assertEqual(self.client.get("/api/articulos/").json(), [])
        self.assertEqual(self.client.get(f"/api/articulos/{article.pk}/").status_code, 404)
        self.assertNotContains(self.client.get("/"), article.title)

    def test_draft_creation_generates_a_unique_slug(self):
        self.create_article(
            title="Robótica educativa",
            slug="robotica-educativa",
        )
        response = self.client.post(
            "/api/articulos/",
            data=json.dumps({"titulo": "Robótica educativa", "cuerpo": "Borrador."}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Token {self.admin_token.key}",
        )

        self.assertEqual(response.status_code, 201)
        article = Article.objects.get(pk=response.json()["id"])
        self.assertEqual(article.slug, "robotica-educativa-2")

    def test_draft_creation_validates_required_fields_and_title_length(self):
        invalid_payloads = (
            {},
            {"titulo": "", "cuerpo": "Contenido."},
            {"titulo": "Título", "cuerpo": "   "},
            {"titulo": "T" * 201, "cuerpo": "Contenido."},
        )

        for payload in invalid_payloads:
            with self.subTest(payload=payload):
                response = self.client.post(
                    "/api/articulos/",
                    data=json.dumps(payload),
                    content_type="application/json",
                    HTTP_AUTHORIZATION=f"Token {self.admin_token.key}",
                )

                self.assertEqual(response.status_code, 400)
                self.assertIsInstance(response.json(), dict)
                self.assertEqual(Article.objects.count(), 0)


class EditorialAdminTests(TestCase):
    def setUp(self):
        temporary_media = tempfile.TemporaryDirectory()
        self.addCleanup(temporary_media.cleanup)
        self.enterContext(override_settings(MEDIA_ROOT=temporary_media.name))
        from django.contrib.auth import get_user_model

        self.user = get_user_model().objects.create_superuser(
            username="editor",
            email="editor@example.com",
            password="secure-test-password",
        )
        AboutPage.objects.get_or_create(pk=1, defaults={"content": "Texto inicial."})

    def test_anonymous_visitors_cannot_access_editorial_admin(self):
        response = self.client.get(reverse("admin:blog_article_add"))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("admin:login"), response.url)
        self.assertEqual(self.client.get("/registro/").status_code, 404)

    def test_editor_can_create_and_update_an_article_with_its_image(self):
        self.client.force_login(self.user)
        add_url = reverse("admin:blog_article_add")
        response = self.client.post(
            add_url,
            {
                "title": "Brazo robótico",
                "slug": "brazo-robotico",
                "image": make_test_image("brazo.png"),
                "publication_date_0": timezone.localtime().strftime("%d/%m/%Y"),
                "publication_date_1": timezone.localtime().strftime("%H:%M:%S"),
                "excerpt": "Un brazo aprende a manipular objetos.",
                "content": "## Precisión\n\nContenido del artículo.",
                "author": "Ada",
                "published": "on",
                "_save": "Guardar",
            },
        )

        self.assertEqual(response.status_code, 302)
        article = Article.objects.get(slug="brazo-robotico")
        self.assertTrue(article.image.storage.exists(article.image.name))
        self.assertContains(
            self.client.get(reverse("home")),
            article.image.url,
        )

        change_url = reverse("admin:blog_article_change", args=[article.pk])
        response = self.client.post(
            change_url,
            {
                "title": "Brazo robótico actualizado",
                "slug": article.slug,
                "publication_date_0": timezone.localtime(
                    article.publication_date
                ).strftime("%d/%m/%Y"),
                "publication_date_1": timezone.localtime(
                    article.publication_date
                ).strftime("%H:%M:%S"),
                "excerpt": article.excerpt,
                "content": article.content,
                "author": article.author,
                "published": "on",
                "_save": "Guardar",
            },
        )

        self.assertEqual(response.status_code, 302)
        article.refresh_from_db()
        self.assertEqual(article.title, "Brazo robótico actualizado")
        self.assertContains(
            self.client.get(article.get_absolute_url()),
            article.image.url,
        )

    def test_editor_can_update_about_page_and_changes_are_public(self):
        self.client.force_login(self.user)
        about_page = AboutPage.objects.get(pk=1)
        response = self.client.post(
            reverse("admin:blog_aboutpage_change", args=[about_page.pk]),
            {"content": "Una presentación actualizada del autor.", "_save": "Guardar"},
        )

        self.assertEqual(response.status_code, 302)
        about_page.refresh_from_db()
        self.assertEqual(about_page.content, "Una presentación actualizada del autor.")
        self.assertContains(
            self.client.get(reverse("about")),
            about_page.content,
        )

    def test_editor_can_unpublish_an_article_and_it_disappears_from_public_pages(self):
        article = Article.objects.create(
            title="Artículo visible",
            slug="articulo-visible",
            image=make_test_image(),
            publication_date=timezone.now(),
            excerpt="Extracto visible.",
            content="Contenido.",
            author="Ada",
            published=True,
        )
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("admin:blog_article_change", args=[article.pk]),
            {
                "title": article.title,
                "slug": article.slug,
                "publication_date_0": timezone.localtime(
                    article.publication_date
                ).strftime("%d/%m/%Y"),
                "publication_date_1": timezone.localtime(
                    article.publication_date
                ).strftime("%H:%M:%S"),
                "excerpt": article.excerpt,
                "content": article.content,
                "author": article.author,
                "_save": "Guardar",
            },
        )

        self.assertEqual(response.status_code, 302)
        article.refresh_from_db()
        self.assertFalse(article.published)
        self.assertNotContains(self.client.get(reverse("home")), article.title)


class DemoContentCommandTests(TestCase):
    def test_demo_command_creates_editable_profile_and_three_articles(self):
        temporary_media = tempfile.TemporaryDirectory()
        self.addCleanup(temporary_media.cleanup)
        with override_settings(MEDIA_ROOT=temporary_media.name):
            from django.core.management import call_command

            call_command("load_demo_content", verbosity=0)

            self.assertEqual(Article.objects.filter(published=True).count(), 3)
            self.assertEqual(AboutPage.objects.count(), 1)
            self.assertEqual(Article.objects.filter(image="").count(), 0)
            for article in Article.objects.filter(published=True):
                self.assertTrue(article.image.storage.exists(article.image.name))
