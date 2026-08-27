from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from rest_framework.routers import DefaultRouter
from properties.views import PropertyViewSet, ProjectViewSet
from leads.views import LeadViewSet
from insights.views import InsightViewSet


def health_check(request):
    return JsonResponse({'status': 'ok'})

router = DefaultRouter()
router.register(r'properties', PropertyViewSet)
router.register(r'leads', LeadViewSet)
router.register(r'projects', ProjectViewSet)
router.register(r'insights', InsightViewSet, basename='insight')

urlpatterns = [
    path('health/', health_check, name='health-check'),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
