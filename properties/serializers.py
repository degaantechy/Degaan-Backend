from rest_framework import serializers
from .models import Property, Lead, Project


class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = [
            'id', 'project', 'address', 'location', 'price', 'size',
            'bedrooms', 'bathrooms', 'property_type', 'description',
            'features', 'status', 'images', 'created_date', 'updated_date'
        ]
        read_only_fields = ['id', 'created_date', 'updated_date']


class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = [
            'id', 'name', 'email', 'phone', 'interest_type',
            'property', 'message', 'status', 'source', 'created_date'
        ]
        read_only_fields = ['id', 'created_date', 'status', 'source']

    def create(self, validated_data):
        lead = Lead.objects.create(**validated_data)
        lead.send_confirmation_email()
        return lead


class ProjectSerializer(serializers.ModelSerializer):
    properties_count = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            'id', 'name', 'description', 'budget', 'cost_estimate',
            'timeline_start', 'timeline_end', 'units_total', 'units_sold',
            'status', 'structural_specs', 'certifications', 'progress_percentage',
            'properties_count', 'created_date', 'updated_date'
        ]
        read_only_fields = ['id', 'created_date', 'updated_date']

    def get_properties_count(self, obj):
        return obj.properties.count()
