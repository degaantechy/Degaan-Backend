from django.contrib import admin
from .models import Property, Lead, Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'status', 'budget', 'units_total', 'progress_percentage', 'created_date']
    list_filter = ['status', 'created_date']
    search_fields = ['name', 'description']
    readonly_fields = ['created_date', 'updated_date']

    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'description', 'status')
        }),
        ('Budget & Timeline', {
            'fields': ('budget', 'cost_estimate', 'timeline_start', 'timeline_end')
        }),
        ('Units', {
            'fields': ('units_total', 'units_sold', 'progress_percentage')
        }),
        ('Technical Specs', {
            'fields': ('structural_specs', 'certifications')
        }),
        ('Timestamps', {
            'fields': ('created_date', 'updated_date'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ['address', 'location', 'price', 'property_type', 'status', 'bedrooms', 'created_date']
    list_filter = ['status', 'property_type', 'created_date']
    search_fields = ['address', 'location', 'description']
    readonly_fields = ['created_date', 'updated_date']

    fieldsets = (
        ('Basic Info', {
            'fields': ('address', 'location', 'property_type', 'project', 'status')
        }),
        ('Pricing & Size', {
            'fields': ('price', 'size')
        }),
        ('Rooms', {
            'fields': ('bedrooms', 'bathrooms')
        }),
        ('Description', {
            'fields': ('description', 'features')
        }),
        ('Images', {
            'fields': ('images',),
            'description': 'Enter image URLs as JSON list: ["url1", "url2"]'
        }),
        ('Timestamps', {
            'fields': ('created_date', 'updated_date'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'interest_type', 'status', 'source', 'created_date']
    list_filter = ['status', 'interest_type', 'source', 'created_date']
    search_fields = ['name', 'email', 'phone', 'message']
    readonly_fields = ['created_date', 'updated_date', 'source']

    fieldsets = (
        ('Contact Info', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Inquiry Details', {
            'fields': ('interest_type', 'property', 'message', 'status')
        }),
        ('Tracking', {
            'fields': ('source', 'created_date', 'updated_date'),
            'classes': ('collapse',)
        }),
    )

    actions = ['mark_contacted', 'mark_qualified', 'mark_converted']

    def mark_contacted(self, request, queryset):
        queryset.update(status='contacted')
    mark_contacted.short_description = "Mark selected leads as contacted"

    def mark_qualified(self, request, queryset):
        queryset.update(status='qualified')
    mark_qualified.short_description = "Mark selected leads as qualified"

    def mark_converted(self, request, queryset):
        queryset.update(status='converted')
    mark_converted.short_description = "Mark selected leads as converted"
