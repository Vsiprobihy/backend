from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.permissions import IsOrganizer
from organization.models import OrganizationAccess, OrganizerEvent
from organization.serializers import (
    OrganizerEventSerializer,
)
from swager.organization import SwaggerDocs


User = get_user_model()


class OrganizerEventListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOrganizer]

    @swagger_auto_schema(**SwaggerDocs.Organization.get)
    def get(self, request):
        if request.user.is_authenticated:
            events = OrganizerEvent.objects.filter(users_access__user=request.user)
            serializer = OrganizerEventSerializer(events, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response([], status=status.HTTP_200_OK)

    @swagger_auto_schema(**SwaggerDocs.Organization.post)
    def post(self, request):
        serializer = OrganizerEventSerializer(data=request.data)
        if serializer.is_valid():
            organization = serializer.save()
            OrganizationAccess.objects.create(
                user=request.user,
                organization=organization,
                role=OrganizationAccess.OWNER,
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrganizerEventDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOrganizer]

    @swagger_auto_schema(**SwaggerDocs.Organization.get)
    def get(self, request, pk):
        if request.user.is_authenticated:
            event = OrganizerEvent.objects.filter(users_access__user=request.user, pk=pk).first()
            if event:
                serializer = OrganizerEventSerializer(event)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({'error': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

    @swagger_auto_schema(**SwaggerDocs.Organization.put)
    def put(self, request, pk):
        event = OrganizerEvent.objects.filter(users_access__user=request.user, pk=pk).first()
        if not event:
            return Response({'error': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = OrganizerEventSerializer(event, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(**SwaggerDocs.Organization.delete)
    def delete(self, request, pk):
        event = OrganizerEvent.objects.filter(users_access__user=request.user, pk=pk).first()
        if event:
            event.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'error': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)


class InviteModeratorView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOrganizer]

    @swagger_auto_schema(**SwaggerDocs.Organization.post)
    def post(self, request):
        organization_id = request.data.get('organization_id')
        email = request.data.get('email')
        message = request.data.get('message', '')

        user = User.objects.filter(email=email).first()
        if not user:
            return Response(
                {'error': 'User with this email not found'},
                status=status.HTTP_404_NOT_FOUND,
            )

        organization = OrganizerEvent.objects.filter(id=organization_id).first()
        if not organization:
            return Response(
                {'error': 'Organization not found'},
                status=status.HTTP_404_NOT_FOUND,
            )

        is_owner = OrganizationAccess.objects.filter(
            organization=organization, user=request.user, role=OrganizationAccess.OWNER
        ).exists()
        if not is_owner:
            return Response(
                {'error': 'You are not the owner of this organization'},
                status=status.HTTP_403_FORBIDDEN,
            )

        OrganizationAccess.objects.create(
            user=user, organization=organization, role=OrganizationAccess.MODERATOR
        )

        return Response(
            {'success': 'Moderator invited successfully'},
            status=status.HTTP_200_OK
        )
