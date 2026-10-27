from django.db import models
from django.urls import reverse


class Article(models.Model):
    title = models.CharField("título", max_length=200)
    slug = models.SlugField("URL", max_length=220, unique=True)
    image = models.ImageField("imagen", upload_to="articles/")
    publication_date = models.DateTimeField("fecha de publicación")
    excerpt = models.TextField("extracto", max_length=400)
    content = models.TextField("contenido")
    author = models.CharField("autoría", max_length=150)
    published = models.BooleanField("publicado", default=False)

    class Meta:
        ordering = ("-publication_date", "-pk")
        verbose_name = "artículo"
        verbose_name_plural = "artículos"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("article-detail", kwargs={"slug": self.slug})


class AboutPage(models.Model):
    content = models.TextField("presentación")

    class Meta:
        verbose_name = "presentación del autor"
        verbose_name_plural = "presentación del autor"

    def __str__(self):
        return "Sobre mí"
