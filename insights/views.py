from django.utils import timezone
from rest_framework import filters, permissions, viewsets

from .models import Insight
from .serializers import InsightSerializer


class InsightViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = InsightSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = [
        'title_en', 'title_so', 'excerpt_en', 'excerpt_so',
        'content_en', 'content_so', 'author',
    ]
    ordering_fields = ['published_at', 'created_at']
    ordering = ['-published_at']

    def get_queryset(self):
        queryset = Insight.objects.filter(
            is_published=True,
            published_at__isnull=False,
            published_at__lte=timezone.now(),
        )

        category = self.request.query_params.get('category')
        featured = self.request.query_params.get('featured')

        if category:
            queryset = queryset.filter(category=category)
        if featured and featured.lower() in ('1', 'true', 'yes'):
            queryset = queryset.filter(is_featured=True)

        return queryset
