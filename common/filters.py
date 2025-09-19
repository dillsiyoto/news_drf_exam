from typing import Any

from django.utils import timezone
from datetime import timedelta
from rest_framework.filters import BaseFilterBackend
from rest_framework.request import Request
from django.db.models import Q, QuerySet


class FreshFilter(BaseFilterBackend):
    def filter_queryset(self, request: Request, queryset: QuerySet, view: Any) -> QuerySet:
        if request.GET.get("fresh") == "true":
            last_day = timezone.now() - timedelta(days=1)
            queryset = queryset.filter(published_at__gte=last_day)
        return queryset


class SearchFilter(BaseFilterBackend):
    def filter_queryset(self, request: Request, queryset: QuerySet, view: Any) -> QuerySet:
        search_fields: list = getattr(view, "search_fields", [])
        search_value = request.GET.get("search")
        if not search_value:
            return queryset
        
        query = Q()
        for field in search_fields:
            query |= Q(**{f"{field}__icontains": search_value})
            
        return queryset.filter(query)
