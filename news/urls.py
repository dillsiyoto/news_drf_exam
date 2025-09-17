from django.urls import path
from news.views import UpdateArticles, ArticlesList

urlpatterns = [
    path("articles/update/", UpdateArticles.as_view(), name="articles-update"),
    path("articles/", ArticlesList.as_view(), name="articles-list"),
]
