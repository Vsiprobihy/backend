from drf_yasg.utils import swagger_auto_schema
from django.conf import settings
from rest_framework import status, generics, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg import openapi

from swagger_docs import SwaggerDocs
from .serializers import RegisterSerializer, UserProfileSerializer


class RegisterView(generics.CreateAPIView):
    """
    API view for user registration.

    This view allows new users to register and generates access and refresh tokens
    upon successful registration.

    """

    serializer_class = RegisterSerializer

    @swagger_auto_schema(**SwaggerDocs.Register.post)
    def create(self, request, *args, **kwargs) -> Response:
        """
        Register a new user and return tokens.

        Args:
            request (Request): The request object with user data.

        Returns:
            Response: A response containing access and refresh tokens.

        Raises:
            ValidationError: If validation fails.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        if user is not None:
            refresh = RefreshToken.for_user(user)
            response = Response(status=status.HTTP_201_CREATED)

            response.data = {
                "access_token": {
                    "value": str(refresh.access_token),
                    "expires": settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds(),
                },
                "refresh_token": {
                    "value": str(refresh),
                    "expires": settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds(),
                },
            }

            return response

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(**SwaggerDocs.Profile.get)
    def get(self, request):
        user = request.user
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)

    @swagger_auto_schema(**SwaggerDocs.Profile.put)
    def put(self, request):
        user = request.user
        serializer = UserProfileSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(**SwaggerDocs.Profile.patch)
    def patch(self, request):
        user = request.user
        serializer = UserProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    @swagger_auto_schema(
        operation_description="Login with JWT token",
        request_body=TokenObtainPairSerializer,
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
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

# class AdminOnlyView(APIView):
#     permission_classes = [IsAuthenticated, IsAdmin]

#     def get(self, request):
#         return Response({"message": "Only for admins"})

# class OrganizerOnlyView(APIView):
#     permission_classes = [IsAuthenticated, IsOrganizer]

#     def get(self, request):
#         return Response({"message": "Only for organizers"})

# class PublicView(APIView):
#     permission_classes = []

#     def get(self, request):
#         return Response({"message": "This is a public endpoint, accessible by anyone."})
