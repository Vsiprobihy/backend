from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.permissions import IsOrganizer
from event.decorators import check_organization_access_decorator, extract_for_event_access_directly
from event.models import Event, OrganizationAccess
from event.serializers.events import EventSerializer
from swagger_docs import SwaggerDocs


class EventsListView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOrganizer]

    @swagger_auto_schema(**SwaggerDocs.Event.post)
    def post(self, request):
        serializer = EventSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOrganizer]

    def get_object(self, pk):
        event = Event.objects.get(pk=pk)
        user = self.request.user

        if not OrganizationAccess.objects.filter(
            organization=event.organizer, user=user
        ).exists():
            raise PermissionDenied('You do not have permission to access this event.')

        return event

    @swagger_auto_schema(**SwaggerDocs.Event.get)
    @check_organization_access_decorator(extract_for_event_access_directly)
    def get(self, request, pk):
        event = self.get_object(pk)
        serializer = EventSerializer(event)
        return Response(serializer.data)

    @swagger_auto_schema(**SwaggerDocs.Event.put)
    @check_organization_access_decorator(extract_for_event_access_directly)
    def put(self, request, pk):
        event = self.get_object(pk)
        serializer = EventSerializer(event, data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(**SwaggerDocs.Event.patch)
    @check_organization_access_decorator(extract_for_event_access_directly)
    def patch(self, request, pk):
        event = self.get_object(pk)
        serializer = EventSerializer(event, data=request.data, partial=True, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(**SwaggerDocs.Event.delete)
    @check_organization_access_decorator(extract_for_event_access_directly)
    def delete(self, request, pk):
        event = self.get_object(pk)
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
