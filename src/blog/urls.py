from django.urls import path

from . import api_views
from . import views

urlpatterns = [
    path(
        "api/articulos/",
        api_views.ArticleListCreateAPIView.as_view(),
        name="api-article-list",
    ),
    path(
        "api/articulos/<int:pk>/",
        api_views.ArticleDetailAPIView.as_view(),
        name="api-article-detail",
    ),
    path("", views.home, name="home"),
    path("sobre-mi/", views.about, name="about"),
    path("articulos/<slug:slug>/", views.article_detail, name="article-detail"),
]
