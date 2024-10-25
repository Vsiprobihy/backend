from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from authentication.serializers import LoginSerializer

LoginSchema = swagger_auto_schema(
    operation_description="Login with JWT token",
    request_body=LoginSerializer,
    responses={
        200: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'refresh': openapi.Schema(type=openapi.TYPE_STRING, description='JWT Refresh Token'),
                'access': openapi.Schema(type=openapi.TYPE_STRING, description='JWT Access Token'),
            },
            required=['refresh', 'access'],
        )
    }
)
