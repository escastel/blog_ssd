from django.shortcuts import get_object_or_404, render

from .models import AboutPage, Article


def home(request):
    articles = Article.objects.filter(published=True)
    return render(request, "blog/home.html", {"articles": articles})


def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug, published=True)
    return render(request, "blog/article_detail.html", {"article": article})


def about(request):
    page = get_object_or_404(AboutPage, pk=1)
    return render(request, "blog/about.html", {"page": page})


def page_not_found(request, exception):
    return render(request, "404.html", status=404)
