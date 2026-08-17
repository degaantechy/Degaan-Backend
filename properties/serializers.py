from rest_framework import serializers
from .models import Property, Project


class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = [
            'id', 'project', 'address', 'location', 'price', 'size',
            'bedrooms', 'bathrooms', 'property_type', 'description',
            'features', 'status', 'images', 'created_date', 'updated_date'
        ]
        read_only_fields = ['id', 'created_date', 'updated_date']
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
