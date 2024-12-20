from drf_yasg import openapi

from authentication.serializers import (
    AdditionalProfileDetailSerializer,
    AdditionalProfileSerializer,
    LoginSerializer,
    RegisterSerializer,
    UserProfileSerializer,
)


class SwaggerDocs:

    class UserRegister:
        post = {
            'tags': ['Authentication'],
            'operation_description': 'Register user with email and password',
            'request_body': RegisterSerializer,
            'responses': {
                200: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_STRING, description='Verify your account from email'
                        )
                    },
                    required=['detail'],
                ),
                400: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_STRING, description='Password must contain at least 1 uppercase letter.'
                        )
                    },
                    required=['detail'],
                ),
                500: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='An unexpected error occurred on the server',
                        )
                    },
                    required=['detail'],
                ),
            },
        }

    class UserLogin:
        post = {
            'tags': ['Authentication'],
            'operation_description': 'Login with JWT token',
            'request_body': LoginSerializer,
            'responses': {
                200: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'access_token': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'value': openapi.Schema(
                                    type=openapi.TYPE_STRING, description='JWT Access Token'
                                ),
                                'expires': openapi.Schema(
                                    type=openapi.TYPE_INTEGER, description='Expiration time of the access token in seconds'  # noqa: E501
                                ),
                            },
                            required=['value', 'expires'],
                        ),
                        'refresh_token': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'value': openapi.Schema(
                                    type=openapi.TYPE_STRING, description='JWT Refresh Token'
                                ),
                                'expires': openapi.Schema(
                                    type=openapi.TYPE_INTEGER, description='Expiration time of the refresh token in seconds'  # noqa: E501
                                ),
                            },
                            required=['value', 'expires'],
                        ),
                    },
                    required=['access_token', 'refresh_token'],
                ),
                400: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='Invalid request parameters or data.',
                        )
                    },
                    required=['detail'],
                ),
                401: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_STRING, description='Invalid credentials.'
                        )
                    },
                    required=['detail'],
                ),
                500: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='An unexpected error occurred on the server.',
                        )
                    },
                    required=['detail'],
                ),
            },
        }

    class CustomResetPasswordView:
        post = {
            'tags': ['Authentication'],
            'operation_description': 'Request a password reset email.',
            'request_body': openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'email': openapi.Schema(
                        type=openapi.TYPE_STRING, description='User email address'
                    ),
                },
                required=['email'],
            ),
            'responses': {
                200: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='A password reset email has been sent to the provided email address.'
                        ),
                    },
                    required=['detail'],
                ),
                400: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_STRING, description='Email field is required or invalid.'
                        )
                    },
                    required=['detail'],
                ),
                404: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_STRING, description='Email not found in the database.'
                        )
                    },
                    required=['detail'],
                ),
                500: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='An unexpected error occurred on the server.',
                        )
                    },
                    required=['detail'],
                ),
            },
        }

    class CustomResetPasswordConfirmView:
        post = {
            'tags': ['Authentication'],
            'operation_description': 'Confirm and reset the user password.',
            'request_body': openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'uid': openapi.Schema(
                        type=openapi.TYPE_STRING, description='User ID from the password reset link'
                    ),
                    'token': openapi.Schema(
                        type=openapi.TYPE_STRING, description='Password reset token'
                    ),
                    'new_password': openapi.Schema(
                        type=openapi.TYPE_STRING, description='New password for the user'
                    ),
                },
                required=['uid', 'token', 'new_password'],
            ),
            'responses': {
                200: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='Your password has been successfully changed.',
                        )
                    },
                    required=['detail'],
                ),
                400: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_STRING, description='Invalid token or password.'
                        )
                    },
                    required=['detail'],
                ),
                404: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_STRING, description='User not found or invalid request.'
                        )
                    },
                    required=['detail'],
                ),
                500: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='An unexpected error occurred on the server.',
                        )
                    },
                    required=['detail'],
                ),
            },
        }

    class ActivateUserEmailView:
        get = {
            'tags': ['Authentication'],
            'operation_description': 'Activate user by email',
            'manual_parameters': [
                openapi.Parameter(
                    'uid', openapi.IN_PATH, description="User's unique identifier", type=openapi.TYPE_STRING,
                    required=True
                ),
                openapi.Parameter(
                    'token', openapi.IN_PATH, description='Activation token for the user', type=openapi.TYPE_STRING,
                    required=True
                ),
            ]
            ,
            'responses': {
                200: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_STRING, description='Your account has been activated successfully'
                        )
                    },
                    required=['detail'],
                ),
                400: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_STRING, description='Bad request'
                        )
                    },
                    required=['detail'],
                ),
                404: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_STRING, description='User does not exist'
                        )
                    },
                    required=['detail'],
                ),
                500: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='An unexpected error occurred on the server',
                        )
                    },
                    required=['detail'],
                ),
            },
        }

    class AdditionalProfileList:
        get = {
            'tags': ['Additional Profile'],
            'operation_description': 'Get a list of additional profiles',
            'responses': {
                200: AdditionalProfileSerializer(many=True),
                400: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='Invalid request parameters or data.',
                        )
                    },
                    required=['detail'],
                ),
                401: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_STRING, description='Invalid credentials.'
                        )
                    },
                    required=['detail'],
                ),
                403: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='Insufficient permissions to access this resource.',
                        )
                    },
                    required=['detail'],
                ),
                500: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='An unexpected error occurred on the server.',
                        )
                    },
                    required=['detail'],
                ),
            },
        }

        post = {
            'tags': ['Additional Profile'],
            'operation_description': 'Create an additional profile',
            'request_body': AdditionalProfileSerializer,
            'responses': {
                201: AdditionalProfileSerializer,
                400: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='Invalid request parameters or data.',
                        )
                    },
                    required=['detail'],
                ),
                401: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_STRING, description='Invalid credentials.'
                        )
                    },
                    required=['detail'],
                ),
                403: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='Insufficient permissions to create this resource.',
                        )
                    },
                    required=['detail'],
                ),
                500: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='An unexpected error occurred on the server.',
                        )
                    },
                    required=['detail'],
                ),
            },
        }

    class AdditionalProfileDetail:
        get = {
            'tags': ['Additional Profile'],
            'operation_description': 'Get an additional profile',
            'responses': {
                200: AdditionalProfileDetailSerializer,
                400: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='Invalid request parameters or data.',
                        )
                    },
                    required=['detail'],
                ),
                401: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_STRING, description='Invalid credentials.'
                        )
                    },
                    required=['detail'],
                ),
                403: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='Insufficient permissions to access this resource.',
                        )
                    },
                    required=['detail'],
                ),
                404: openapi.Response(description='Profile not found'),
                500: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='An unexpected error occurred on the server.',
                        )
                    },
                    required=['detail'],
                ),
            },
        }

        put = {
            'tags': ['Additional Profile'],
            'operation_description': 'Update an additional profile',
            'request_body': AdditionalProfileDetailSerializer,
            'responses': {
                200: AdditionalProfileDetailSerializer,
                400: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='Invalid request parameters or data.',
                        )
                    },
                    required=['detail'],
                ),
                401: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_STRING, description='Invalid credentials.'
                        )
                    },
                    required=['detail'],
                ),
                403: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='Insufficient permissions to update this resource.',
                        )
                    },
                    required=['detail'],
                ),
                404: openapi.Response(description='Profile not found'),
                500: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='An unexpected error occurred on the server.',
                        )
                    },
                    required=['detail'],
                ),
            },
        }

        delete = {
            'tags': ['Additional Profile'],
            'operation_description': 'Delete an additional profile',
            'responses': {
                204: openapi.Response(description='Profile deleted successfully'),
                400: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='Invalid request parameters or data.',
                        )
                    },
                    required=['detail'],
                ),
                401: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_STRING, description='Invalid credentials.'
                        )
                    },
                    required=['detail'],
                ),
                403: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='Insufficient permissions to delete this resource.',
                        )
                    },
                    required=['detail'],
                ),
                404: openapi.Response(description='Profile not found'),
                500: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='An unexpected error occurred on the server.',
                        )
                    },
                    required=['detail'],
                ),
            },
        }

    class Profile:
        get = {
            'tags': ['Profile'],
            'responses': {
                200: UserProfileSerializer,
                400: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='Invalid request parameters or data.',
                        )
                    },
                    required=['detail'],
                ),
                401: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_STRING, description='Invalid credentials.'
                        )
                    },
                    required=['detail'],
                ),
                403: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='Insufficient permissions to access this resource.',
                        )
                    },
                    required=['detail'],
                ),
                404: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='The requested resource does not exist.',
                        )
                    },
                    required=['detail'],
                ),
                500: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='An unexpected error occurred on the server.',
                        )
                    },
                    required=['detail'],
                ),
            },
            'operation_description': 'Get user profile data',
        }

        put = {
            'tags': ['Profile'],
            'request_body': UserProfileSerializer,
            'responses': {
                200: UserProfileSerializer,
                400: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='Invalid request parameters or data.',
                        )
                    },
                    required=['detail'],
                ),
                401: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_STRING, description='Invalid credentials.'
                        )
                    },
                    required=['detail'],
                ),
                403: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='Insufficient permissions to update this resource.',
                        )
                    },
                    required=['detail'],
                ),
                404: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='The resource to update does not exist.',
                        )
                    },
                    required=['detail'],
                ),
                500: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='An unexpected error occurred on the server.',
                        )
                    },
                    required=['detail'],
                ),
            },
            'operation_description': 'Update user profile data',
        }

        patch = {
            'tags': ['Profile'],
            'request_body': UserProfileSerializer,
            'responses': {
                200: UserProfileSerializer,
                400: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='Invalid request parameters or data.',
                        )
                    },
                    required=['detail'],
                ),
                401: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_STRING, description='Invalid credentials.'
                        )
                    },
                    required=['detail'],
                ),
                403: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='Insufficient permissions to partially update this resource.',
                        )
                    },
                    required=['detail'],
                ),
                404: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='The resource to partially update does not exist.',
                        )
                    },
                    required=['detail'],
                ),
                500: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='An unexpected error occurred on the server.',
                        )
                    },
                    required=['detail'],
                ),
            },
            'operation_description': 'Partial update of user profile data',
        }
