from rest_framework import filters, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import Property, Project
from .serializers import PropertySerializer, ProjectSerializer


class PublicReadAdminWriteMixin:
    def get_permissions(self):
        if self.action in ('list', 'retrieve', 'featured', 'similar', 'properties'):
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]


class PropertyViewSet(PublicReadAdminWriteMixin, viewsets.ModelViewSet):
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
class ProjectViewSet(PublicReadAdminWriteMixin, viewsets.ModelViewSet):
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
