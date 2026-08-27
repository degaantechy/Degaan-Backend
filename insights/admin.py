from django.contrib import admin

from .models import Insight


@admin.register(Insight)
class InsightAdmin(admin.ModelAdmin):
    list_display = [
        'title_en', 'category', 'author', 'is_published',
        'is_featured', 'published_at', 'updated_at',
    ]
    list_filter = ['is_published', 'is_featured', 'category', 'published_at']
    search_fields = ['title_en', 'title_so', 'excerpt_en', 'excerpt_so', 'author']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'published_at'
    actions = ['publish_selected', 'unpublish_selected']

    fieldsets = (
        ('Publishing', {
            'fields': (
                'category', 'author', 'cover_image_url', 'is_featured',
                'is_published', 'published_at', 'slug',
            ),
        }),
        ('English content', {
            'fields': ('title_en', 'excerpt_en', 'content_en'),
        }),
        ('Somali content', {
            'fields': ('title_so', 'excerpt_so', 'content_so'),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    @admin.action(description='Publish selected insights')
    def publish_selected(self, request, queryset):
        for insight in queryset:
            insight.is_published = True
            insight.save()

    @admin.action(description='Unpublish selected insights')
    def unpublish_selected(self, request, queryset):
        queryset.update(is_published=False)
