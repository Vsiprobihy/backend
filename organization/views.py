from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.models import CustomUser
from authentication.permissions import IsOrganizer
from organization.models import Organization, Organizer
from organization.serializers import OrganizationSerializer
from swagger.organization import SwaggerDocs
from utils.custom_exceptions import ForbiddenError, NotFoundError, SuccessResponse, UnauthorizedError


User = get_user_model()


class OrganizationListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOrganizer]

    @swagger_auto_schema(**SwaggerDocs.Organization.get)
    def get(self, request):
        if request.user.is_authenticated:
            organization = Organization.objects.filter(organizerOrganization__user=request.user)
            serializer = OrganizationSerializer(organization, many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response([], status=status.HTTP_200_OK)

    @swagger_auto_schema(**SwaggerDocs.Organization.post)
    def post(self, request):
        serializer = OrganizationSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            organization = serializer.save()
            Organizer.objects.create(
                user=request.user,
                organization=organization,
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrganizationDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOrganizer]

    @swagger_auto_schema(**SwaggerDocs.Organization.get)
    def get(self, request, organization_id):
        if request.user.is_authenticated:
            organization = Organization.objects.filter(organizerOrganization__user=request.user, pk=organization_id).first()  # noqa: E501
            if organization:
                serializer = OrganizationSerializer(organization, context={'request': request})
                return Response(serializer.data, status=status.HTTP_200_OK)
            return ForbiddenError('You dont have permission to this action').get_response()
        return UnauthorizedError('Unauthorized').get_response()

    @swagger_auto_schema(**SwaggerDocs.Organization.put)
    def put(self, request, organization_id):
        organization = Organization.objects.filter(organizerOrganization__user=request.user, pk=organization_id).first()  # noqa: E501
        if not organization:
            return ForbiddenError('You dont have permission to this action').get_response()

        serializer = OrganizationSerializer(organization, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(**SwaggerDocs.Organization.patch)
    def patch(self, request, organization_id):
        organization = Organization.objects.filter(organizerOrganization__user=request.user, pk=organization_id).first()  # noqa: E501
        if not organization:
            return ForbiddenError('You dont have permission to this action').get_response()

        serializer = OrganizationSerializer(organization, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(**SwaggerDocs.Organization.delete)
    def delete(self, request, organization_id):
        event = Organization.objects.filter(organizerOrganization__user=request.user, pk=organization_id).first()
        if event:
            event.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return ForbiddenError('You dont have permission to this action').get_response()


class InviteOrganizerView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOrganizer]

    @swagger_auto_schema(**SwaggerDocs.Organization.post)
    def post(self, request, organization_id):
        email = request.data.get('email')
        message = request.data.get('message', '')  # noqa: F841

        user = User.objects.filter(email=email).first()
        if not user:
            return NotFoundError('User with this email not found').get_response()

        organization = Organization.objects.filter(pk=organization_id).first()
        if not organization:
            return NotFoundError('User with this email not found').get_response()

        is_organizer = Organizer.objects.filter(
            organization=organization, user=request.user, role=CustomUser.ORGANIZER
        ).exists()
        if not is_organizer:
            return ForbiddenError('You are not the organizer of this organization').get_response()

        Organizer.objects.create(
            user=user, organization=organization, role=CustomUser.ORGANIZER
        )

        return SuccessResponse('Organizer invited successfully').get_response()
