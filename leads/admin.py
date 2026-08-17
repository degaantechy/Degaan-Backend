from django.contrib import admin

from .models import Lead


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'email', 'phone', 'interest_type',
        'status', 'source', 'created_date',
    ]
    list_filter = ['status', 'interest_type', 'source', 'created_date']
    search_fields = ['name', 'email', 'phone', 'message']
    readonly_fields = ['created_date', 'updated_date', 'source']

    fieldsets = (
        ('Contact Info', {'fields': ('name', 'email', 'phone')}),
        ('Inquiry Details', {
            'fields': ('interest_type', 'property', 'message', 'status'),
        }),
        ('Tracking', {
            'fields': ('source', 'created_date', 'updated_date'),
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
