from rest_framework import serializers

from .models import Lead


class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = [
            'id', 'name', 'email', 'phone', 'interest_type',
            'property', 'message', 'status', 'source',
            'project_slug', 'service', 'source_page',
            'utm_source', 'utm_medium', 'utm_campaign',
            'budget_range', 'preferred_contact', 'unit_type',
            'created_date', 'updated_date',
        ]
        read_only_fields = [
            'id', 'status', 'source', 'created_date', 'updated_date',
        ]
