from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from authentication.permissions import IsOrganizer
from organization.models import OrganizationAccess, OrganizerEvent
from organization.serializers import (
    OrganizationAccessSerializer,
    OrganizerEventSerializer,
)
from swagger_docs import SwaggerDocs


User = get_user_model()


class OrganizerEventListCreateView(generics.ListCreateAPIView):
    serializer_class = OrganizerEventSerializer
    permission_classes = [permissions.IsAuthenticated, IsOrganizer]

    @swagger_auto_schema(**SwaggerDocs.Organizer.get)
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return OrganizerEvent.objects.none()
        return OrganizerEvent.objects.filter(users_access__user=self.request.user)

    def perform_create(self, serializer):
        organization = serializer.save()
        OrganizationAccess.objects.create(
            user=self.request.user,
            organization=organization,
            role=OrganizationAccess.OWNER,
        )


class OrganizerEventDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrganizerEventSerializer
    permission_classes = [permissions.IsAuthenticated, IsOrganizer]

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return OrganizerEvent.objects.none()
        return OrganizerEvent.objects.filter(users_access__user=self.request.user)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class InviteModeratorView(generics.GenericAPIView):
    serializer_class = OrganizationAccessSerializer
    permission_classes = [permissions.IsAuthenticated, IsOrganizer]

    def post(self, request, *args, **kwargs):
        organization_id = request.data.get('organization_id')
        email = request.data.get('email')
        message = request.data.get('message', '')  # noqa: F841

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {'error': 'User with this email not found'},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            organization = OrganizerEvent.objects.get(id=organization_id)
        except OrganizerEvent.DoesNotExist:
            return Response(
                {'error': 'Organization not found'}, status=status.HTTP_404_NOT_FOUND
            )

        # Check that the current user is the owner of the organization
        owner_access = OrganizationAccess.objects.filter(
            organization=organization, user=request.user, role=OrganizationAccess.OWNER
        ).exists()
        if not owner_access:
            return Response(
                {'error': 'You are not the owner of this organization'},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Adding a new moderator
        OrganizationAccess.objects.create(
            user=user, organization=organization, role=OrganizationAccess.MODERATOR
        )

        return Response(
            {'success': 'Moderator invited successfully'}, status=status.HTTP_200_OK
        )
