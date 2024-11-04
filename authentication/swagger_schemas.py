from drf_yasg import openapi
from authentication.serializers import (
    LoginSerializer, AdditionalProfileSerializer, 
    AdditionalProfileDetailSerializer, UserAvatarUploadSerializer, 
    UserProfileSerializer
)

class SwaggerDocs:

    class UserAuth:

        post = {
            'operation_description': 'Login with JWT token',
            'request_body': LoginSerializer,
            'responses': {
                200: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'refresh': openapi.Schema(type=openapi.TYPE_STRING, description='JWT Refresh Token'),
                        'access': openapi.Schema(type=openapi.TYPE_STRING, description='JWT Access Token'),
                    },
                    required=['refresh', 'access'],
                )
            }
        }

    class AdditionalProfileList:

        get = {
            'tags': ['Additional Profile'],
            'operation_description': 'Get a list of additional profiles',
            'responses': {200: AdditionalProfileSerializer(many=True)},
        }

        post = {
            'tags': ['Additional Profile'],
            'operation_description': 'Create an additional profile',
            'request_body': AdditionalProfileSerializer,
            'responses': {201: AdditionalProfileSerializer},
        }

    class AdditionalProfileDetail:

        get = {
            'tags': ['Additional Profile'],
            'operation_description': 'Get an additional profile',
            'responses': {200: AdditionalProfileDetailSerializer},
        }

        put = {
            'tags': ['Additional Profile'],
            'operation_description': 'Update an additional profile',
            'request_body': AdditionalProfileDetailSerializer,
            'responses': {200: AdditionalProfileDetailSerializer},
        }

        delete = {
            'tags': ['Additional Profile'],
            'operation_description': 'Delete an additional profile',
            'responses': {204: 'Profile deleted successfully'},
        }

    class UserAvatarUpload:

        put = {
            'tags': ['User Management'],
            'request_body': UserAvatarUploadSerializer,
            'responses': {
                200: 'Avatar uploaded successfully.', 
                400: 'Bad Request - Invalid image file.'
            },
            'operation_description': 'Upload user avatar using PUT method.',
        }

        patch = {
            'tags': ['User Management'],
            'request_body': UserAvatarUploadSerializer,
            'responses': {
                200: 'Avatar uploaded successfully.', 
                400: 'Bad Request - Invalid image file.'
            },
            'operation_description': 'Upload user avatar using PATCH method.',
        }

    class Profile:

        get = {
            'tags': ['Profile'],
            'responses': {200: UserProfileSerializer},
            'operation_description': 'Get user profile data',
        }
        put = {
            'tags': ['Profile'],
            'request_body': UserProfileSerializer,
            'responses': {200: UserProfileSerializer},
            'operation_description': 'Update user profile data',
        }
        patch = {
            'tags': ['Profile'],
            'request_body': UserProfileSerializer,
            'responses': {200: UserProfileSerializer},
            'operation_description': 'Partial update of user profile data',
        }
