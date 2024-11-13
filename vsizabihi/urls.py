from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from vsizabihi.views import api_root_view


schema_view = get_schema_view(
    openapi.Info(
        title='API Documentation',
        default_version='v1',
        description='Посилання на OAuth - http://localhost:8000/api/auth/oauth/login/google-oauth2/',
        terms_of_service='https://www.google.com/policies/terms/',
        contact=openapi.Contact(email='support@example.com'),
        license=openapi.License(name='BSD License'),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', api_root_view, name='api-root'),
    path('api/admin/', admin.site.urls),
    path('api/auth/', include('authentication.urls')),
    path('api/user/', include('user_info.urls')),
    path(
        'swagger/',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui',
    ),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/organizer/', include('event.urls')),
    path('api/event/', include('public_events.urls')),
    path('api/calendar/', include('event_filters.urls')),
    path('api/upcoming-events/', include('mainpage.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
