from django.contrib import admin

from .models import AboutPage, Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "publication_date", "published")
    list_filter = ("published", "publication_date")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "excerpt", "content", "author")


@admin.register(AboutPage)
class AboutPageAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not AboutPage.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False
