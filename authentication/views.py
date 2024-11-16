
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.storage import default_storage
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from djoser.views import UserViewSet
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from authentication.models import AdditionalProfile, CustomUser
from authentication.serializers import (
    AdditionalProfileDetailSerializer,
    AdditionalProfileSerializer,
    LoginSerializer,
    RegisterSerializer,
    UserAvatarUploadSerializer,
    UserProfileSerializer,
)
from swager.authenticate import SwaggerDocs
from utils.custom_exceptions import (
    BadRequestError,
    ForbiddenError,
    NotFoundError,
    SuccessResponseCustom,
    UnauthorizedError,
)


class RegisterView(APIView):
    serializer_class = RegisterSerializer

    @swagger_auto_schema(**SwaggerDocs.UserRegister.post)
    def post(self, request, *args, **kwargs) -> Response:
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()

            # if user and user.pk is not None:
            #     uid = urlsafe_base64_encode(force_bytes(user.pk))
            #     token = default_token_generator.make_token(user)
            #
            #     send_activation_email(
            #         user=user,
            #         uid=uid,
            #         token=token,
            #         site_name='vsiprobihy',
            #         domain='127.0.0.1:8000'
            #     )
            #
            return SuccessResponseCustom('Verify your account from email').get_response()
        else:
            raise BadRequestError('Failed to create user')


class LoginView(APIView):
    serializer_class = LoginSerializer

    @swagger_auto_schema(**SwaggerDocs.UserLogin.post)
    def post(self, request, *args, **kwargs) -> Response:
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email, password=password)

        if user is None:
            raise UnauthorizedError('Invalid credentials')

        if not user.is_active:
            raise ForbiddenError('User account is not active')

        refresh = RefreshToken.for_user(user)
        response = Response()
        response.data = {
            'access_token': {
                'value': str(refresh.access_token),
                'expires': settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds(),
            },
            'refresh_token': {
                'value': str(refresh),
                'expires': settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds(),
            },
        }

        return response


class ActivateUserEmailView(APIView):

    @swagger_auto_schema(**SwaggerDocs.ActivateUserEmailView.get)
    def get(self, request, uid, token):

        uid = force_str(urlsafe_base64_decode(uid))
        user = CustomUser.objects.get(pk=uid)

        if user is None:
            return NotFoundError('User does not exist')

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()

            return SuccessResponseCustom('Your account has been activated successfully').get_response()
        else:
            return BadRequestError().get_response()


class CustomResetPasswordView(UserViewSet):
    @swagger_auto_schema(**SwaggerDocs.CustomResetPasswordView.post)
    def reset_password(self, request, *args, **kwargs):
        email = request.data.get('email')
        if not email:
            return BadRequestError('Email field is required.').get_response()

        if not CustomUser.objects.filter(email=email).exists():
            return NotFoundError('Email not found in the database.').get_response()

        response = super().reset_password(request, *args, **kwargs)

        if response.status_code == status.HTTP_204_NO_CONTENT:
            return SuccessResponseCustom('A password reset email has been sent to the provided email address.').get_response()

        return response


class CustomResetPasswordConfirmView(UserViewSet):
    @swagger_auto_schema(**SwaggerDocs.CustomResetPasswordConfirmView.post)
    def reset_password_confirm(self, request, *args, **kwargs):
        response = super().reset_password_confirm(request, *args, **kwargs)

        if response.status_code == status.HTTP_204_NO_CONTENT:
            return SuccessResponseCustom('Your password has been successfully changed.').get_response()

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
            try:
                if default_storage.exists(old_avatar_path):
                    default_storage.delete(old_avatar_path)
            except ObjectDoesNotExist:
                pass

        serializer.save(avatar=self.request.data.get('avatar'))


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
    def get(self, request, _id):
        try:
            profile = request.user.additional_profiles.get(id=_id)
            serializer = AdditionalProfileDetailSerializer(profile)
            return Response(serializer.data)
        except AdditionalProfile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(**SwaggerDocs.AdditionalProfileDetail.put)
    def put(self, request, _id):
        try:
            profile = request.user.additional_profiles.get(id=_id)
            serializer = AdditionalProfileDetailSerializer(profile, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except AdditionalProfile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(**SwaggerDocs.AdditionalProfileDetail.delete)
    def delete(self, request, _id):
        try:
            profile = request.user.additional_profiles.get(id=_id)
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
