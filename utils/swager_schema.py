from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions


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
