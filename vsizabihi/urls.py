from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from utils.swagger_schema import schema_view
from vsizabihi.views import api_root_view


urlpatterns = [
    path('', api_root_view, name='api-root'),
    path('api/admin/', admin.site.urls),
    path('api/custom-admin/', include('custom_admin.urls')),
    path('api/authentication/', include('authentication.urls')),
    # path('api/user/', include('user.urls')),
    path('api/organization/', include('organization.urls')),
    path('api/organization/', include('event.urls')),
    path('api/public-event/', include('public_event.urls')),
    path(
        'swagger/',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui',
    ),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
