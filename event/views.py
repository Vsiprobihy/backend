from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from swagger_docs import SwaggerDocs
from .models import AdditionalItemEvent, DistanceEvent, Event, OrganizerEvent, EventRegistration
from .serializers import AdditionalItemEventSerializer, DistanceEventSerializer, EventSerializer, \
    OrganizerEventSerializer, EventRegistrationSerializer


# Additional Items
class AdditionalItemsListView(APIView):

    @swagger_auto_schema(**SwaggerDocs.AdditionalItem.post)
    def post(self, request):
        serializer = AdditionalItemEventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdditionalItemsDetailView(APIView):
    def get_object(self, pk):
        return AdditionalItemEvent.objects.get(pk=pk)

    @swagger_auto_schema(**SwaggerDocs.AdditionalItem.get)
    def get(self, request, pk):
        item = self.get_object(pk)
        serializer = AdditionalItemEventSerializer(item)
        return Response(serializer.data)

    @swagger_auto_schema(**SwaggerDocs.AdditionalItem.put)
    def put(self, request, pk):
        item = self.get_object(pk)
        serializer = AdditionalItemEventSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(**SwaggerDocs.AdditionalItem.patch)
    def patch(self, request, pk):
        item = self.get_object(pk)
        serializer = AdditionalItemEventSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(**SwaggerDocs.AdditionalItem.delete)
    def delete(self, request, pk):
        item = self.get_object(pk)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Distances
class DistancesListView(APIView):
    @swagger_auto_schema(**SwaggerDocs.Distance.get)
    def get(self, request):
        distances = DistanceEvent.objects.all()
        serializer = DistanceEventSerializer(distances, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(**SwaggerDocs.Distance.post)
    def post(self, request):
        serializer = DistanceEventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DistanceDetailView(APIView):
    def get_object(self, pk):
        return DistanceEvent.objects.get(pk=pk)

    @swagger_auto_schema(**SwaggerDocs.Distance.get)
    def get(self, request, pk):
        distance = self.get_object(pk)
        serializer = DistanceEventSerializer(distance)
        return Response(serializer.data)

    @swagger_auto_schema(**SwaggerDocs.Distance.put)
    def put(self, request, pk):
        distance = self.get_object(pk)
        serializer = DistanceEventSerializer(distance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(**SwaggerDocs.Distance.patch)
    def patch(self, request, pk):
        distance = self.get_object(pk)
        serializer = DistanceEventSerializer(distance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(**SwaggerDocs.Distance.delete)
    def delete(self, request, pk):
        distance = self.get_object(pk)
        distance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Events
class EventsListView(APIView):

    @swagger_auto_schema(**SwaggerDocs.Event.post)
    def post(self, request):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventDetailView(APIView):
    def get_object(self, pk):
        return Event.objects.get(pk=pk)

    @swagger_auto_schema(**SwaggerDocs.Event.get)
    def get(self, request, pk):
        event = self.get_object(pk)
        serializer = EventSerializer(event)
        return Response(serializer.data)

    @swagger_auto_schema(**SwaggerDocs.Event.put)
    def put(self, request, pk):
        event = self.get_object(pk)
        serializer = EventSerializer(event, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(**SwaggerDocs.Event.patch)
    def patch(self, request, pk):
        event = self.get_object(pk)
        serializer = EventSerializer(event, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(**SwaggerDocs.Event.delete)
    def delete(self, request, pk):
        event = self.get_object(pk)
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Organizers
class OrganizersListView(APIView):
    @swagger_auto_schema(**SwaggerDocs.Organizer.get)
    def get(self, request):
        organizers = OrganizerEvent.objects.all()
        serializer = OrganizerEventSerializer(organizers, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(**SwaggerDocs.Organizer.post)
    def post(self, request):
        serializer = OrganizerEventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrganizerDetailView(APIView):
    def get_object(self, pk):
        return OrganizerEvent.objects.get(pk=pk)

    @swagger_auto_schema(**SwaggerDocs.Organizer.get)
    def get(self, request, pk):
        organizer = self.get_object(pk)
        serializer = OrganizerEventSerializer(organizer)
        return Response(serializer.data)

    @swagger_auto_schema(**SwaggerDocs.Organizer.put)
    def put(self, request, pk):
        organizer = self.get_object(pk)
        serializer = OrganizerEventSerializer(organizer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(**SwaggerDocs.Organizer.patch)
    def patch(self, request, pk):
        organizer = self.get_object(pk)
        serializer = OrganizerEventSerializer(organizer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(**SwaggerDocs.Organizer.delete)
    def delete(self, request, pk):
        organizer = self.get_object(pk)
        organizer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Event Registrations
class EventRegistrationsListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(**SwaggerDocs.EventRegistration.get)
    def get(self, request):
        registrations = EventRegistration.objects.all()
        serializer = EventRegistrationSerializer(registrations, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(**SwaggerDocs.EventRegistration.post)
    def post(self, request):
        serializer = EventRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventRegistrationDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        return EventRegistration.objects.get(pk=pk)

    @swagger_auto_schema(**SwaggerDocs.EventRegistration.get)
    def get(self, request, pk):
        registration = self.get_object(pk)
        serializer = EventRegistrationSerializer(registration)
        return Response(serializer.data)

    @swagger_auto_schema(**SwaggerDocs.EventRegistration.put)
    def put(self, request, pk):
        registration = self.get_object(pk)
        serializer = EventRegistrationSerializer(registration, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(**SwaggerDocs.EventRegistration.patch)
    def patch(self, request, pk):
        registration = self.get_object(pk)
        serializer = EventRegistrationSerializer(registration, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(**SwaggerDocs.EventRegistration.delete)
    def delete(self, request, pk):
        registration = self.get_object(pk)
        registration.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
