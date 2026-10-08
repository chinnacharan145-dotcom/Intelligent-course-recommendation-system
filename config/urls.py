from django.contrib import admin
from django.urls import path, include, re_path
from django.shortcuts import render
from django.conf import settings
from django.conf.urls.static import static

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

def index_view(request):
    return render(request, 'index.html')

urlpatterns = [
    path('admin/', admin.site.urls),

    # OpenAPI 3 Schema & Swagger UI
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # API v1 Domain App Endpoints
    path('api/v1/auth/', include('apps.accounts.urls')),
    path('api/v1/', include('apps.academics.urls')),
    path('api/v1/students/', include('apps.students.urls')),
    path('api/v1/', include('apps.skills.urls')),
    path('api/v1/', include('apps.careers.urls')),
    path('api/v1/', include('apps.courses.urls')),
    path('api/v1/', include('apps.assessments.urls')),
    path('api/v1/', include('apps.recommendations.urls')),
    path('api/v1/', include('apps.learning.urls')),
    path('api/v1/', include('apps.roadmap.urls')),
    path('api/v1/', include('apps.notifications.urls')),
    path('api/v1/', include('apps.analytics.urls')),
    path('api/v1/', include('apps.ai_assistant.urls')),
    
    # Catch-all for single-page application routes
    re_path(r'^.*$', index_view, name='index'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
