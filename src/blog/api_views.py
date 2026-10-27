from django.shortcuts import get_object_or_404
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from .api_serializers import ArticleDraftSerializer, ArticleSerializer
from .models import Article


class ArticleListCreateAPIView(APIView):
    http_method_names = ["get", "post", "head", "options"]

    def get_authenticators(self):
        if self.request.method == "POST":
            return [TokenAuthentication()]
        return []

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAdminUser()]
        return [AllowAny()]

    def get(self, request):
        articles = Article.objects.filter(published=True)
        return Response(ArticleSerializer(articles, many=True).data)

    def post(self, request):
        serializer = ArticleDraftSerializer(
            data=request.data,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        article = serializer.save()
        return Response(ArticleSerializer(article).data, status=201)


class ArticleDetailAPIView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    http_method_names = ["get", "head", "options"]

    def get(self, request, pk):
        article = get_object_or_404(Article, pk=pk, published=True)
        return Response(ArticleSerializer(article).data)
