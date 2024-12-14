from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.permissions import IsOrganizer
from organization.models import Organization, Organizer
from organization.serializers import OrganizationSerializer
from swagger.organization import SwaggerDocs


User = get_user_model()


class OrganizationListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOrganizer]

    @swagger_auto_schema(**SwaggerDocs.Organization.get_list)
    def get(self, request):
        if request.user.is_authenticated:
            organization = Organization.objects.filter(organizer_organization__user=request.user)
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
                role=Organizer.OWNER,
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrganizationDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOrganizer]

    @swagger_auto_schema(**SwaggerDocs.Organization.get)
    def get(self, request, organization_id):
        if request.user.is_authenticated:
            organization = Organization.objects.filter(organizer_organization__user=request.user, pk=organization_id).first()  # noqa: E501
            if organization:
                serializer = OrganizationSerializer(organization, context={'request': request})
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({'error': 'You dont have permission to this action'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

    @swagger_auto_schema(**SwaggerDocs.Organization.put)
    def put(self, request, organization_id):
        organization = Organization.objects.filter(organizer_organization__user=request.user, pk=organization_id).first()  # noqa: E501
        if not organization:
            return Response({'error': 'You dont have permission to this action'}, status=status.HTTP_404_NOT_FOUND)

        serializer = OrganizationSerializer(organization, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(**SwaggerDocs.Organization.patch)
    def patch(self, request, organization_id):
        organization = Organization.objects.filter(organizer_organization__user=request.user, pk=organization_id).first()  # noqa: E501
        if not organization:
            return Response({'error': 'You dont have permission to this action'}, status=status.HTTP_404_NOT_FOUND)

        serializer = OrganizationSerializer(organization, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(**SwaggerDocs.Organization.delete)
    def delete(self, request, organization_id):
        event = Organization.objects.filter(organizer_organization__user=request.user, pk=organization_id).first()
        if event:
            event.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'error': 'You dont have permission to this action'}, status=status.HTTP_404_NOT_FOUND)


class InviteModeratorView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOrganizer]

    @swagger_auto_schema(**SwaggerDocs.Organization.post)
    def post(self, request, organization_id):
        email = request.data.get('email')
        message = request.data.get('message', '')  # noqa: F841

        user = User.objects.filter(email=email).first()
        if not user:
            return Response(
                {'error': 'User with this email not found'},
                status=status.HTTP_404_NOT_FOUND,
            )

        organization = Organization.objects.filter(pk=organization_id).first()
        if not organization:
            return Response(
                {'error': 'Organization not found'},
                status=status.HTTP_404_NOT_FOUND,
            )

        is_owner = Organizer.objects.filter(
            organization=organization, user=request.user, role=Organizer.OWNER
        ).exists()
        if not is_owner:
            return Response(
                {'error': 'You are not the owner of this organization'},
                status=status.HTTP_403_FORBIDDEN,
            )

        Organizer.objects.create(
            user=user, organization=organization, role=Organizer.MODERATOR
        )

        return Response(
            {'success': 'Moderator invited successfully'},
            status=status.HTTP_200_OK
        )
