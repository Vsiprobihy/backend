from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from djoser.views import UserViewSet
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from authentication.models import CustomUser
from authentication.serializers import (
    LoginSerializer,
    RegisterSerializer,
)
from swagger.authenticate import SwaggerDocs
from utils.custom_exceptions import (
    BadRequestError,
    ForbiddenError,
    NotFoundError,
    SuccessResponse,
    UnauthorizedError,
)


class RegisterView(APIView):
    serializer_class = RegisterSerializer

    @swagger_auto_schema(**SwaggerDocs.UserRegister.post)
    def post(self, request, *args, **kwargs) -> Response:
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()  # noqa: F841

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
            return SuccessResponse('Verify your account from email').get_response()
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

        if not user.isActive:
            raise ForbiddenError('User account is not active')

        refresh = RefreshToken.for_user(user)
        response = Response()
        response.data = {
            'accessToken': {
                'value': str(refresh.access_token),  # noqa
                'expires': settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds(),
            },
            'refreshToken': {
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
            user.isActive = True
            user.save()

            return SuccessResponse('Your account has been activated successfully').get_response()
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
            return SuccessResponse('A password reset email has been sent to the provided email address.').get_response()  # noqa: E501

        return response


class CustomResetPasswordConfirmView(UserViewSet):
    @swagger_auto_schema(**SwaggerDocs.CustomResetPasswordConfirmView.post)
    def reset_password_confirm(self, request, *args, **kwargs):
        response = super().reset_password_confirm(request, *args, **kwargs)

        if response.status_code == status.HTTP_204_NO_CONTENT:
            return SuccessResponse('Your password has been successfully changed.').get_response()

        return response

