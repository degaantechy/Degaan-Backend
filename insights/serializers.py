from rest_framework import serializers

from .models import Insight


class InsightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Insight
        fields = [
            'id', 'slug', 'title_en', 'title_so', 'excerpt_en', 'excerpt_so',
            'content_en', 'content_so', 'category', 'author', 'cover_image_url',
            'is_featured', 'published_at', 'created_at', 'updated_at',
        ]
        read_only_fields = fields
