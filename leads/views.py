from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend

from .models import Property, Lead, Project
from .serializers import PropertySerializer, LeadSerializer, ProjectSerializer
from .emails import send_lead_notification_email


class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'property_type', 'project']
    search_fields = ['address', 'location', 'description']
    ordering_fields = ['price', 'created_date', 'bedrooms']
    ordering = ['-created_date']

    def get_queryset(self):
        queryset = Property.objects.all()

        # Price range filter
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')

        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        # Bedrooms filter
        min_bedrooms = self.request.query_params.get('min_bedrooms')
        if min_bedrooms:
            queryset = queryset.filter(bedrooms__gte=min_bedrooms)

        return queryset

    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured properties"""
        properties = Property.objects.filter(status='available')[:6]
        serializer = self.get_serializer(properties, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def similar(self, request, pk=None):
        """Get similar properties"""
        property = self.get_object()
        similar = Property.objects.filter(
            property_type=property.property_type,
            status='available'
        ).exclude(id=property.id)[:4]
        serializer = self.get_serializer(similar, many=True)
        return Response(serializer.data)


class LeadViewSet(viewsets.ModelViewSet):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'interest_type', 'source']
    ordering = ['-created_date']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Send notification email
        lead = serializer.instance
        send_lead_notification_email(lead)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def bulk_status_update(self, request):
        """Update status for multiple leads"""
        lead_ids = request.data.get('lead_ids', [])
        new_status = request.data.get('status')

        if not lead_ids or not new_status:
            return Response(
                {'error': 'lead_ids and status are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        Lead.objects.filter(id__in=lead_ids).update(status=new_status)
        return Response({'success': f'Updated {len(lead_ids)} leads'})

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get lead statistics"""
        total = Lead.objects.count()
        new = Lead.objects.filter(status='new').count()
        contacted = Lead.objects.filter(status='contacted').count()
        converted = Lead.objects.filter(status='converted').count()

        return Response({
            'total': total,
            'new': new,
            'contacted': contacted,
            'converted': converted,
            'conversion_rate': (converted / total * 100) if total > 0 else 0
        })


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status']
    search_fields = ['name', 'description']

    @action(detail=True, methods=['get'])
    def properties(self, request, pk=None):
        """Get all properties for a project"""
        project = self.get_object()
        properties = project.properties.all()
        serializer = PropertySerializer(properties, many=True)
        return Response(serializer.data)
