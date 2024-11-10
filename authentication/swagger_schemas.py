from drf_yasg import openapi
from authentication.serializers import (
    LoginSerializer,
    AdditionalProfileSerializer,
    AdditionalProfileDetailSerializer,
    UserAvatarUploadSerializer,
    UserProfileSerializer,
)


class SwaggerDocs:

    class UserAuth:

        post = {
            "operation_description": "Login with JWT token",
            "request_body": LoginSerializer,
            "responses": {
                200: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "refresh": openapi.Schema(
                            type=openapi.TYPE_STRING, description="JWT Refresh Token"
                        ),
                        "access": openapi.Schema(
                            type=openapi.TYPE_STRING, description="JWT Access Token"
                        ),
                    },
                    required=["refresh", "access"],
                ),
                400: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "detail": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Invalid request parameters or data.",
                        )
                    },
                    required=["detail"],
                ),
                401: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "detail": openapi.Schema(
                            type=openapi.TYPE_STRING, description="Invalid credentials."
                        )
                    },
                    required=["detail"],
                ),
                500: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "detail": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="An unexpected error occurred on the server.",
                        )
                    },
                    required=["detail"],
                ),
            },
        }

    class AdditionalProfileList:

        get = {
            "tags": ["Additional Profile"],
            "operation_description": "Get a list of additional profiles",
            "responses": {
                200: AdditionalProfileSerializer(many=True),
                400: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "detail": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Invalid request parameters or data.",
                        )
                    },
                    required=["detail"],
                ),
                401: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "detail": openapi.Schema(
                            type=openapi.TYPE_STRING, description="Invalid credentials."
                        )
                    },
                    required=["detail"],
                ),
                403: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "detail": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Insufficient permissions to access this resource.",
                        )
                    },
                    required=["detail"],
                ),
                500: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "detail": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="An unexpected error occurred on the server.",
                        )
                    },
                    required=["detail"],
                ),
            },
        }

        post = {
            "tags": ["Additional Profile"],
            "operation_description": "Create an additional profile",
            "request_body": AdditionalProfileSerializer,
            "responses": {
                201: AdditionalProfileSerializer,
                400: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "detail": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Invalid request parameters or data.",
                        )
                    },
                    required=["detail"],
                ),
                401: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "detail": openapi.Schema(
                            type=openapi.TYPE_STRING, description="Invalid credentials."
                        )
                    },
                    required=["detail"],
                ),
                403: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "detail": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Insufficient permissions to create this resource.",
                        )
                    },
                    required=["detail"],
                ),
                500: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "detail": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="An unexpected error occurred on the server.",
                        )
                    },
                    required=["detail"],
                ),
            },
        }

    class AdditionalProfileDetail:

        get = {
            "tags": ["Additional Profile"],
            "operation_description": "Get an additional profile",
            "responses": {
                200: AdditionalProfileDetailSerializer,
                400: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "detail": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Invalid request parameters or data.",
                        )
                    },
                    required=["detail"],
                ),
                401: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "detail": openapi.Schema(
                            type=openapi.TYPE_STRING, description="Invalid credentials."
                        )
                    },
                    required=["detail"],
                ),
                403: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "detail": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Insufficient permissions to access this resource.",
                        )
                    },
                    required=["detail"],
                ),
                404: openapi.Response(description="Profile not found"),
                500: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "detail": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="An unexpected error occurred on the server.",
                        )
                    },
                    required=["detail"],
                ),
            },
        }

        put = {
            "tags": ["Additional Profile"],
            "operation_description": "Update an additional profile",
            "request_body": AdditionalProfileDetailSerializer,
            "responses": {
                200: AdditionalProfileDetailSerializer,
                400: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "detail": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Invalid request parameters or data.",
                        )
                    },
                    required=["detail"],
                ),
                401: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "detail": openapi.Schema(
                            type=openapi.TYPE_STRING, description="Invalid credentials."
                        )
                    },
                    required=["detail"],
                ),
                403: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "detail": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Insufficient permissions to update this resource.",
                        )
                    },
                    required=["detail"],
                ),
                404: openapi.Response(description="Profile not found"),
                500: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "detail": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="An unexpected error occurred on the server.",
                        )
                    },
                    required=["detail"],
                ),
            },
        }

        delete = {
            "tags": ["Additional Profile"],
            "operation_description": "Delete an additional profile",
            "responses": {
                204: openapi.Response(description="Profile deleted successfully"),
                400: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "detail": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Invalid request parameters or data.",
                        )
                    },
                    required=["detail"],
                ),
                401: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "detail": openapi.Schema(
                            type=openapi.TYPE_STRING, description="Invalid credentials."
                        )
                    },
                    required=["detail"],
                ),
                403: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "detail": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Insufficient permissions to delete this resource.",
                        )
                    },
                    required=["detail"],
                ),
                404: openapi.Response(description="Profile not found"),
                500: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "detail": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="An unexpected error occurred on the server.",
                        )
                    },
                    required=["detail"],
                ),
            },
        }

    class UserAvatarUpload:

        put = {
            "tags": ["User Management"],
            "request_body": UserAvatarUploadSerializer,
            "responses": {
                200: openapi.Response(description="Avatar uploaded successfully."),
                400: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "detail": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Invalid image file or bad request parameters.",
                        )
                    },
                    required=["detail"],
                ),
                401: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "detail": openapi.Schema(
                            type=openapi.TYPE_STRING, description="Invalid credentials."
                        )
                    },
                    required=["detail"],
                ),
                415: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "avatar": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_STRING,
                                description="Upload a valid image. The file you uploaded was either not an image or a corrupted image.",
                            ),
                        )
                    },
                    required=["avatar"],
                ),
                500: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "detail": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="An unexpected error occurred on the server.",
                        )
                    },
                    required=["detail"],
                ),
            },
            "operation_description": "Upload user avatar using PUT method.",
        }

        patch = {
            "tags": ["User Management"],
            "request_body": UserAvatarUploadSerializer,
            "responses": {
                200: openapi.Response(description="Avatar uploaded successfully."),
                400: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "detail": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Invalid image file or bad request parameters.",
                        )
                    },
                    required=["detail"],
                ),
                401: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "detail": openapi.Schema(
                            type=openapi.TYPE_STRING, description="Invalid credentials."
                        )
                    },
                    required=["detail"],
                ),
                415: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "avatar": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_STRING,
                                description="Upload a valid image. The file you uploaded was either not an image or a corrupted image.",
                            ),
                        )
                    },
                    required=["avatar"],
                ),
                500: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "detail": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="An unexpected error occurred on the server.",
                        )
                    },
                    required=["detail"],
                ),
            },
            "operation_description": "Upload user avatar using PATCH method.",
        }

    class Profile:

        get = {
            "tags": ["Profile"],
            "responses": {
                200: UserProfileSerializer,
                400: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "detail": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Invalid request parameters or data.",
                        )
                    },
                    required=["detail"],
                ),
                401: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "detail": openapi.Schema(
                            type=openapi.TYPE_STRING, description="Invalid credentials."
                        )
                    },
                    required=["detail"],
                ),
                403: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "detail": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Insufficient permissions to access this resource.",
                        )
                    },
                    required=["detail"],
                ),
                404: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "detail": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="The requested resource does not exist.",
                        )
                    },
                    required=["detail"],
                ),
                500: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "detail": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="An unexpected error occurred on the server.",
                        )
                    },
                    required=["detail"],
                ),
            },
            "operation_description": "Get user profile data",
        }

        put = {
            "tags": ["Profile"],
            "request_body": UserProfileSerializer,
            "responses": {
                200: UserProfileSerializer,
                400: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "detail": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Invalid request parameters or data.",
                        )
                    },
                    required=["detail"],
                ),
                401: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "detail": openapi.Schema(
                            type=openapi.TYPE_STRING, description="Invalid credentials."
                        )
                    },
                    required=["detail"],
                ),
                403: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "detail": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Insufficient permissions to update this resource.",
                        )
                    },
                    required=["detail"],
                ),
                404: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "detail": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="The resource to update does not exist.",
                        )
                    },
                    required=["detail"],
                ),
                500: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "detail": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="An unexpected error occurred on the server.",
                        )
                    },
                    required=["detail"],
                ),
            },
            "operation_description": "Update user profile data",
        }

        patch = {
            "tags": ["Profile"],
            "request_body": UserProfileSerializer,
            "responses": {
                200: UserProfileSerializer,
                400: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "detail": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Invalid request parameters or data.",
                        )
                    },
                    required=["detail"],
                ),
                401: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "detail": openapi.Schema(
                            type=openapi.TYPE_STRING, description="Invalid credentials."
                        )
                    },
                    required=["detail"],
                ),
                403: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "detail": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Insufficient permissions to partially update this resource.",
                        )
                    },
                    required=["detail"],
                ),
                404: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "detail": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="The resource to partially update does not exist.",
                        )
                    },
                    required=["detail"],
                ),
                500: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "detail": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="An unexpected error occurred on the server.",
                        )
                    },
                    required=["detail"],
                ),
            },
            "operation_description": "Partial update of user profile data",
        }
