from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .emails import send_lead_notification_email
from .models import Lead
from .serializers import LeadSerializer


class LeadViewSet(viewsets.ModelViewSet):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'interest_type', 'source']
    ordering_fields = ['created_date', 'status']
    ordering = ['-created_date']

    def get_permissions(self):
        permission_classes = (
            [permissions.AllowAny]
            if self.action == 'create'
            else [permissions.IsAdminUser]
        )
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        lead = serializer.save()
        send_lead_notification_email(lead)

    @action(detail=False, methods=['post'])
    def bulk_status_update(self, request):
        lead_ids = request.data.get('lead_ids', [])
        new_status = request.data.get('status')
        valid_statuses = {choice[0] for choice in Lead.STATUS_CHOICES}

        if not isinstance(lead_ids, list) or not lead_ids:
            return Response(
                {'error': 'lead_ids must be a non-empty list'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if new_status not in valid_statuses:
            return Response(
                {'error': 'A valid status is required'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        updated = Lead.objects.filter(id__in=lead_ids).update(status=new_status)
        return Response({'updated': updated})

    @action(detail=False, methods=['get'])
    def stats(self, request):
        total = Lead.objects.count()
        new = Lead.objects.filter(status='new').count()
        contacted = Lead.objects.filter(status='contacted').count()
        converted = Lead.objects.filter(status='converted').count()

        return Response({
            'total': total,
            'new': new,
            'contacted': contacted,
            'converted': converted,
            'conversion_rate': (converted / total * 100) if total else 0,
        })
