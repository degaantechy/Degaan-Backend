from django.contrib import admin

from .models import Lead


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'phone', 'interest_type', 'project_slug', 'service',
        'budget_range', 'status', 'source', 'created_date',
    ]
    list_filter = [
        'status', 'interest_type', 'service', 'source',
        'utm_source', 'utm_campaign', 'created_date',
    ]
    search_fields = [
        'name', 'email', 'phone', 'message', 'project_slug',
        'service', 'source_page', 'utm_source', 'utm_campaign',
    ]
    readonly_fields = ['created_date', 'updated_date', 'source']

    fieldsets = (
        ('Contact Info', {'fields': ('name', 'email', 'phone', 'preferred_contact')}),
        ('Inquiry Details', {
            'fields': (
                'interest_type', 'property', 'project_slug', 'service',
                'unit_type', 'budget_range', 'message', 'status',
            ),
        }),
        ('Attribution', {
            'fields': (
                'source', 'source_page', 'utm_source', 'utm_medium',
                'utm_campaign', 'created_date', 'updated_date',
            ),
            'classes': ('collapse',),
        }),
    )

    actions = ['mark_contacted', 'mark_qualified', 'mark_converted']

    @admin.action(description='Mark selected leads as contacted')
    def mark_contacted(self, request, queryset):
        queryset.update(status='contacted')

    @admin.action(description='Mark selected leads as qualified')
    def mark_qualified(self, request, queryset):
        queryset.update(status='qualified')

    @admin.action(description='Mark selected leads as converted')
    def mark_converted(self, request, queryset):
        queryset.update(status='converted')
