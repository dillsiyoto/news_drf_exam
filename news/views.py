import requests
from django.conf import settings
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from drf_yasg.utils import swagger_auto_schema

from news.models import Article
from news.serializers import ArticleSerializer


class UpdateArticles(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={
            200: "новости обновлены или взяты из кэша",
            400: "ошибка NewsAPI",
            401: "не авторизован"
        },
    )
    def post(self, request):
        cached_data = cache.get("news_update")
        if cached_data:
            return Response({"message": "из кэша", "articles": cached_data})

        url = "https://newsapi.org/v2/top-headlines"
        params = {
            "country": "us",
            "apiKey": settings.NEWSAPI_KEY
        }
        response = requests.get(url, params=params)
        data = response.json()

        if data.get("status") != "ok":
            return Response({"error": "ошибка NewsAPI", "details": data}, status=400)

        new_articles = []
        for item in data.get("articles", []):
            article_obj, created = Article.objects.get_or_create(
                url=item["url"],
                defaults={
                    "source_id": item.get("source", {}).get("id"),
                    "source_name": item.get("source", {}).get("name"),
                    "author": item.get("author"),
                    "title": item.get("title"),
                    "description": item.get("description"),
                    "url_to_image": item.get("urlToImage"),
                    "published_at": item.get("publishedAt"),
                    "content": item.get("content"),
                },
            )
            if created:
                new_articles.append(article_obj)

        cache.set("news_update", [article_obj.title for article_obj in new_articles], 
                  timeout=60 * 30)

        return Response({
            "message": "новости обновлены",
            "new_articles": [article_obj.title for article_obj in new_articles],
        })
    

class ArticlesList(APIView):
    @swagger_auto_schema(
        responses={
            200: "успешно",
            400: "ошибка валидации"
        },
    )
    def get(self, request):
        cache_key = f"articles:{request.GET.urlencode()}"
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)

        articles_qs = Article.objects.all()

        if request.GET.get("fresh") == "true":
            last_day = timezone.now() - timedelta(days=1)
            articles_qs = articles_qs.filter(published_at__gte=last_day)

        title_filter = request.GET.get("title_contains")
        if title_filter:
            articles_qs = articles_qs.filter(title__icontains=title_filter)

        serializer = ArticleSerializer(articles_qs, many=True)
        data = serializer.data

        cache.set(cache_key, data, timeout=60 * 10)

        return Response(data)