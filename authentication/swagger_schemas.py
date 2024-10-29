from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from authentication.serializers import LoginSerializer, AdditionalProfileSerializer,  AdditionalProfileDetailSerializer

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

AdditionalProfileListViewGet = swagger_auto_schema(
    operation_description="Get a list of additional profiles",
    responses={200: AdditionalProfileSerializer(many=True)}
)

AdditionalProfileListViewPost = swagger_auto_schema(
    operation_description="Create an additional profile",
    request_body=AdditionalProfileSerializer,
    responses={201: AdditionalProfileSerializer}
)

AdditionalProfileDetailViewGet = swagger_auto_schema(
    operation_description="Get an additional profile",
    responses={200: AdditionalProfileDetailSerializer}
)

AdditionalProfileDetailViewPut = swagger_auto_schema(
    operation_description="Update an additional profile",
    request_body=AdditionalProfileDetailSerializer,
    responses={200: AdditionalProfileDetailSerializer}
)

AdditionalProfileDetailViewDelete = swagger_auto_schema(
    operation_description="Delete an additional profile",
    responses={204: "Profile deleted successfully"}
)

