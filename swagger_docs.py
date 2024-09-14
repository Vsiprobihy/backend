from drf_yasg import openapi
from authentication.serializers import RegisterSerializer, UserProfileSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class SwaggerDocs:
    class Register:
        post = {
            'request_body': RegisterSerializer,
            'responses': {
                201: openapi.Response('User registered successfully'),
                400: 'Bad request'
            },
            'operation_description': "User Registration Endpoint.",
        }

    class Profile:
        get = {
            'responses': {200: UserProfileSerializer},
            'operation_description': "Get user profile data",
        }
        put = {
            'request_body': UserProfileSerializer,
            'responses': {200: UserProfileSerializer},
            'operation_description': "Update user profile data",
        }

        patch = {
            'request_body': UserProfileSerializer,
            'responses': {200: UserProfileSerializer},
            'operation_description': "Partial update of user profile data",
        }

    class Token:
        post = {
            'request_body': TokenObtainPairSerializer,
            'responses': {
                200: openapi.Response('Token Response', TokenObtainPairSerializer),
            },
            'operation_description': "Login with JWT token",
        }

