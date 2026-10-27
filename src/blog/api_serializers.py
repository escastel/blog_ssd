from io import BytesIO

from django.core.files.base import ContentFile
from django.utils import timezone
from django.utils.text import slugify
from rest_framework import serializers
from PIL import Image

from .models import Article


class ArticleSerializer(serializers.ModelSerializer):
    titulo = serializers.CharField(source="title", read_only=True)
    cuerpo = serializers.CharField(source="content", read_only=True)
    estado = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ("id", "titulo", "cuerpo", "estado")

    def get_estado(self, article):
        return "publicado" if article.published else "borrador"


class ArticleDraftSerializer(serializers.Serializer):
    titulo = serializers.CharField(source="title", max_length=200)
    cuerpo = serializers.CharField(source="content", trim_whitespace=True)

    def create(self, validated_data):
        title = validated_data["title"]
        content = validated_data["content"]
        author = self.context["request"].user
        image_buffer = BytesIO()
        Image.new("RGB", (960, 600), color="#e5e7eb").save(
            image_buffer,
            format="PNG",
        )
        author_name = author.get_full_name() or author.get_username()

        return Article.objects.create(
            title=title,
            slug=self._unique_slug(title),
            image=ContentFile(image_buffer.getvalue(), name="api-placeholder.png"),
            publication_date=timezone.now(),
            excerpt=content[:400],
            content=content,
            author=author_name[:150],
            published=False,
        )

    @staticmethod
    def _unique_slug(title):
        base_slug = slugify(title)[:220] or "borrador"
        slug = base_slug
        suffix = 2
        while Article.objects.filter(slug=slug).exists():
            suffix_text = f"-{suffix}"
            slug = f"{base_slug[:220 - len(suffix_text)]}{suffix_text}"
            suffix += 1
        return slug
