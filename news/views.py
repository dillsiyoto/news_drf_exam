import requests
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from news.models import Article
from news.serializers import ArticleSerializer
from common.filters import FreshFilter, SearchFilter


class UpdateArticles(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        responses={
            200: "новости обновлены или взяты из кэша",
            400: "ошибка NewsAPI",
            401: "не авторизован"
        },
    )
    @method_decorator(cache_page(60 * 30))
    def post(self, request):
        url = "https://newsapi.org/v2/top-headlines"
        params = {"country": "us", "apiKey": settings.NEWSAPI_KEY}
        response = requests.get(url, params=params)
        data = response.json()

        if response.status_code != 200 or data.get("status") != "ok":
            return Response({"error": "ошибка NewsAPI", "details": data}, status=400)

        new_articles = []
        for item in data.get("articles", []):
            article = Article(
                source_id=item.get("source", {}).get("id"),
                source_name=item.get("source", {}).get("name"),
                author=item.get("author"),
                title=item.get("title"),
                description=item.get("description"),
                url=item.get("url"),
                url_to_image=item.get("urlToImage"),
                published_at=item.get("publishedAt"),
                content=item.get("content"),
            )
            new_articles.append(article)

        Article.objects.bulk_create(new_articles, ignore_conflicts=True)

        all_articles = Article.objects.all()
        serializer = ArticleSerializer(all_articles, many=True)

        return Response({
            "message": "новости обновлены",
            "articles": serializer.data,
        })


class ArticlesList(APIView):
    permission_classes = [AllowAny] 
    filter_backends = [FreshFilter, SearchFilter]
    search_fields = ["title"] 
    @swagger_auto_schema(
        responses={
            200: "новости обновлены или взяты из кэша",
        },
    )
    @method_decorator(cache_page(60 * 10))
    def get(self, request, *args, **kwargs):
        queryset = Article.objects.all()

        for backend in self.filter_backends:
            queryset = backend().filter_queryset(request, queryset, self)

        serializer = ArticleSerializer(queryset, many=True)

        return Response({"message": "успешно", "articles": serializer.data})