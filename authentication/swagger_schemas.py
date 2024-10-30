from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from authentication.serializers import LoginSerializer, AdditionalProfileSerializer,  AdditionalProfileDetailSerializer, UserAvatarUploadSerializer

SwaggerLoginSchema = swagger_auto_schema(
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

SwaggerAdditionalProfileListViewGet = swagger_auto_schema(
    tags=['Additional Profile'],
    operation_description="Get a list of additional profiles",
    responses={200: AdditionalProfileSerializer(many=True)}
)

SwaggerAdditionalProfileListViewPost = swagger_auto_schema(
    tags=['Additional Profile'],
    operation_description="Create an additional profile",
    request_body=AdditionalProfileSerializer,
    responses={201: AdditionalProfileSerializer}
)

SwaggerAdditionalProfileDetailViewGet = swagger_auto_schema(
    tags=['Additional Profile'],
    operation_description="Get an additional profile",
    responses={200: AdditionalProfileDetailSerializer}
)

SwaggerAdditionalProfileDetailViewPut = swagger_auto_schema(
    tags=['Additional Profile'],
    operation_description="Update an additional profile",
    request_body=AdditionalProfileDetailSerializer,
    responses={200: AdditionalProfileDetailSerializer}
)

SwaggerAdditionalProfileDetailViewDelete = swagger_auto_schema(
    tags=['Additional Profile'],
    operation_description="Delete an additional profile",
    responses={204: "Profile deleted successfully"}
)

SwaggerUserAvatarUploadViewPut = swagger_auto_schema(
        tags=['User Management'],
        request_body=UserAvatarUploadSerializer,
        responses={200: 'Avatar uploaded successfully.', 400: 'Bad Request - Invalid image file.'},
        operation_description="Upload user avatar using PUT method."
    )

SwaggerUserAvatarUploadViewPatch = swagger_auto_schema(
        tags=['User Management'],
        request_body=UserAvatarUploadSerializer,
        responses={200: 'Avatar uploaded successfully.', 400: 'Bad Request - Invalid image file.'},
        operation_description="Upload user avatar using PATCH method."
    )
