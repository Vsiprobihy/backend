from drf_yasg.utils import swagger_auto_schema
from django.core.files.storage import default_storage
from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from authentication.swagger_schemas import SwaggerDocs

from authentication.serializers import RegisterSerializer, LoginSerializer, UserProfileSerializer, UserAvatarUploadSerializer, AdditionalProfileSerializer, AdditionalProfileDetailSerializer
from authentication.models import CustomUser, AdditionalProfile
from utils.custom_exceptions import InvalidCredentialsError


class RegisterView(generics.CreateAPIView):
    """
    API view for user registration.

    This view allows new users to register and generates access and refresh tokens
    upon successful registration.

    Methods:
        Handles POST requests to register a new user.

    """

    serializer_class = RegisterSerializer

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
        serializer = UserProfileSerializer(user, context={'request': request})
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


class UserAvatarUploadView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserAvatarUploadSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(**SwaggerDocs.UserAvatarUpload.put)
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)


    @swagger_auto_schema(**SwaggerDocs.UserAvatarUpload.patch)
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    def get_object(self):
        return self.request.user

    def perform_update(self, serializer):
        user = self.get_object()
        
        if user.avatar:
            old_avatar_path = user.avatar.path
            if default_storage.exists(old_avatar_path):
                default_storage.delete(old_avatar_path)
        serializer.save(avatar=self.request.data.get('avatar'))

class LoginView(APIView):
    """
    API view for user login.

    Allows users to authenticate using their email and password, and returns
    access and refresh tokens upon successful login.

    Methods:
        Handles POST requests to authenticate and issue JWT tokens.
    """

    serializer_class = LoginSerializer

    @swagger_auto_schema(**SwaggerDocs.UserAuth.post)
    def post(self, request, *args, **kwargs) -> Response:
        """
        Authenticate user and return JWT tokens.

        Validates user credentials and, if successful, returns access and refresh
        tokens. Raises an error if authentication fails.

        Args:
            request (Request): The request object with login credentials.

        Returns:
            Response: A response containing access and refresh tokens.

        Raises:
            InvalidCredentialsError: If the authentication fails.
        """
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(email=email, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            response = Response()

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
        raise InvalidCredentialsError


class AdditionalProfileListView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(**SwaggerDocs.AdditionalProfileList.get)
    def get(self, request):
        profiles = request.user.additional_profiles.all()
        serializer = AdditionalProfileSerializer(profiles, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(**SwaggerDocs.AdditionalProfileList.post)
    def post(self, request):
        serializer = AdditionalProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdditionalProfileDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(**SwaggerDocs.AdditionalProfileDetail.get)
    def get(self, request, profile_id):
        try:
            profile = request.user.additional_profiles.get(id=profile_id)
            serializer = AdditionalProfileDetailSerializer(profile)
            return Response(serializer.data)
        except AdditionalProfile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(**SwaggerDocs.AdditionalProfileDetail.put)
    def put(self, request, profile_id):
        try:
            profile = request.user.additional_profiles.get(id=profile_id)
            serializer = AdditionalProfileDetailSerializer(profile, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except AdditionalProfile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(**SwaggerDocs.AdditionalProfileDetail.delete)
    def delete(self, request, profile_id):
        try:
            profile = request.user.additional_profiles.get(id=profile_id)
            profile.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except AdditionalProfile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

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
