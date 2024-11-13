from django.http import Http404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from event.models import AdditionalItemEvent, DistanceEvent, Event, EventRegistration
from event.serializers.event_registrations import (
    EventRegistrationDetailSerializer,
    EventRegistrationSerializer,
)
from swagger_docs import SwaggerDocs


class EventRegistrationsListView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(**SwaggerDocs.EventRegistration.post)
    def post(self, request):
        user = request.user
        event_id = request.data.get('event')
        distances_ids = request.data.get('distances', [])
        additional_items_ids = request.data.get('additional_items', [])

        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return Response(
                {'detail': 'Event not found.'}, status=status.HTTP_404_NOT_FOUND
            )

        if EventRegistration.objects.filter(user=user, event=event).exists():
            return Response(
                {'detail': 'User is already registered for this event.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        distances = DistanceEvent.objects.filter(id__in=distances_ids, event=event)
        if not distances.exists():
            return Response(
                {'detail': 'At least one valid distance must be selected.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        additional_items = AdditionalItemEvent.objects.filter(
            id__in=additional_items_ids, event=event
        )

        registration_data = {
            'event': event.id,
            'distances': [distance.id for distance in distances],
            'additional_items': [item.id for item in additional_items],
        }

        serializer = EventRegistrationSerializer(
            data=registration_data, context={'request': request}
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventRegistrationDetailView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_object(self, pk):
        try:
            return EventRegistration.objects.get(pk=pk)
        except EventRegistration.DoesNotExist:
            raise Http404

    @swagger_auto_schema(**SwaggerDocs.EventRegistration.get)
    def get(self, request, pk=None):
        registration = self.get_object(pk)
        serializer = EventRegistrationDetailSerializer(registration)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(**SwaggerDocs.EventRegistration.put)
    def put(self, request, pk=None):
        registration = self.get_object(pk)
        serializer = EventRegistrationDetailSerializer(registration, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(**SwaggerDocs.EventRegistration.patch)
    def patch(self, request, pk=None):
        registration = self.get_object(pk)
        serializer = EventRegistrationDetailSerializer(
            registration, data=request.data, partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(**SwaggerDocs.EventRegistration.delete)
    def delete(self, request, pk=None):
        registration = self.get_object(pk)
        registration.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
