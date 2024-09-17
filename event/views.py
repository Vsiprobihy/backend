from django.http import Http404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from swagger_docs import SwaggerDocs
from .models import AdditionalItemEvent, DistanceEvent, Event, OrganizerEvent, EventRegistration
from .serializers import AdditionalItemEventSerializer, DistanceEventSerializer, EventSerializer, \
    OrganizerEventSerializer, EventRegistrationSerializer, EventRegistrationDetailSerializer


class AdditionalItemsDetailView(APIView):
    def get_object(self, pk):
        try:
            return AdditionalItemEvent.objects.get(pk=pk)
        except AdditionalItemEvent.DoesNotExist:
            raise Http404

    def get_objects_by_event(self, event_id):
        return AdditionalItemEvent.objects.filter(event_id=event_id)

    @swagger_auto_schema(**SwaggerDocs.AdditionalItem.post)
    def post(self, request, event_id):
        data = request.data.copy()
        data['event'] = event_id

        serializer = AdditionalItemEventSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(**SwaggerDocs.AdditionalItem.get)
    def get(self, request, event_id):
        items = AdditionalItemEvent.objects.filter(event_id=event_id)
        if not items.exists():
            return Response({"detail": "No additional items found for this event."}, status=404)

        serializer = AdditionalItemEventSerializer(items, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(**SwaggerDocs.AdditionalItem.put)
    def put(self, request, event_id):
        if isinstance(request.data, dict):
            data_list = [request.data]
        elif isinstance(request.data, list):
            data_list = request.data
        else:
            return Response({"detail": "Expected a dictionary or a list of items."}, status=status.HTTP_400_BAD_REQUEST)

        items = self.get_objects_by_event(event_id)
        if not items.exists():
            return Response({"detail": "No additional items found for this event."}, status=404)

        updated_data = []
        for data in data_list:
            item = items.filter(id=data.get('id')).first()
            if not item:
                return Response({"detail": f"Item with id {data.get('id')} not found."}, status=404)

            serializer = AdditionalItemEventSerializer(item, data=data)
            if serializer.is_valid():
                serializer.save()
                updated_data.append(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(updated_data, status=status.HTTP_200_OK)

    @swagger_auto_schema(**SwaggerDocs.AdditionalItem.patch)
    def patch(self, request, event_id):
        if isinstance(request.data, dict):
            data_list = [request.data]
        elif isinstance(request.data, list):
            data_list = request.data
        else:
            return Response({"detail": "Expected a dictionary or a list of items."}, status=status.HTTP_400_BAD_REQUEST)

        items = AdditionalItemEvent.objects.filter(event_id=event_id)
        if not items.exists():
            return Response({"detail": "No additional items found for this event."}, status=404)

        updated_data = []
        for data in data_list:
            item_id = data.get('id')
            if not item_id:
                return Response({"detail": "Each item must include an 'id' field."}, status=status.HTTP_400_BAD_REQUEST)

            item = items.filter(id=item_id).first()
            if not item:
                return Response({"detail": f"Item with id {item_id} not found."}, status=status.HTTP_404_NOT_FOUND)

            serializer = AdditionalItemEventSerializer(item, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                updated_data.append(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(updated_data, status=status.HTTP_200_OK)

    @swagger_auto_schema(**SwaggerDocs.AdditionalItem.delete)
    def delete(self, request, pk):
        item = self.get_object(pk)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DistanceDetailView(APIView):
    def get_object(self, pk):
        try:
            return DistanceEvent.objects.get(pk=pk)
        except DistanceEvent.DoesNotExist:
            raise Http404

    def get_objects_by_event(self, event_id):
        return DistanceEvent.objects.filter(event_id=event_id)

    @swagger_auto_schema(**SwaggerDocs.Distance.post)
    def post(self, request, event_id):
        data = request.data.copy()
        data['event'] = event_id
        serializer = DistanceEventSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(**SwaggerDocs.Distance.get)
    def get(self, request, event_id):
        distances = self.get_objects_by_event(event_id)
        if not distances.exists():
            return Response({"detail": "No distances found for this event."}, status=404)

        serializer = DistanceEventSerializer(distances, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(**SwaggerDocs.Distance.put)
    def put(self, request, event_id):
        if isinstance(request.data, dict):
            data_list = [request.data]
        elif isinstance(request.data, list):
            data_list = request.data
        else:
            return Response({"detail": "Expected a dictionary or a list of items."}, status=status.HTTP_400_BAD_REQUEST)

        distances = self.get_objects_by_event(event_id)
        if not distances.exists():
            return Response({"detail": "No distances found for this event."}, status=404)

        updated_data = []
        for data in data_list:
            if 'event' in data:
                del data['event']

            # Находим объект по id
            item = distances.filter(id=data.get('id')).first()
            if not item:
                return Response({"detail": f"Distance with id {data.get('id')} not found."}, status=404)

            data['event'] = event_id

            serializer = DistanceEventSerializer(item, data=data)
            if serializer.is_valid():
                serializer.save()
                updated_data.append(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(updated_data, status=status.HTTP_200_OK)

    @swagger_auto_schema(**SwaggerDocs.Distance.patch)
    def patch(self, request, event_id):
        if isinstance(request.data, dict):
            data_list = [request.data]
        elif isinstance(request.data, list):
            data_list = request.data
        else:
            return Response({"detail": "Expected a dictionary or a list of items."}, status=status.HTTP_400_BAD_REQUEST)

        distances = self.get_objects_by_event(event_id)
        if not distances.exists():
            return Response({"detail": "No distances found for this event."}, status=404)

        updated_data = []
        for data in data_list:
            item_id = data.get('id')
            if not item_id:
                return Response({"detail": "Each item must include an 'id' field."}, status=status.HTTP_400_BAD_REQUEST)

            item = distances.filter(id=item_id).first()
            if not item:
                return Response({"detail": f"Distance with id {item_id} not found."}, status=status.HTTP_404_NOT_FOUND)

            # Частичное обновление (partial=True)
            serializer = DistanceEventSerializer(item, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                updated_data.append(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(updated_data, status=status.HTTP_200_OK)

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


class OrganizerDetailView(APIView):
    def get_object(self, pk):
        return OrganizerEvent.objects.get(pk=pk)

    @swagger_auto_schema(**SwaggerDocs.Organizer.get)
    def get(self, request, event_id):
        try:
            organizer = OrganizerEvent.objects.get(events__id=event_id)
            serializer = OrganizerEventSerializer(organizer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except OrganizerEvent.DoesNotExist:
            return Response({"detail": "Organizer not found."}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(**SwaggerDocs.Organizer.put)
    def put(self, request, event_id):
        try:
            organizer = OrganizerEvent.objects.get(
                events__id=event_id)
            serializer = OrganizerEventSerializer(organizer, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except OrganizerEvent.DoesNotExist:
            return Response({"detail": "Organizer not found."}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(**SwaggerDocs.Organizer.patch)
    def patch(self, request, event_id):
        try:
            organizer = OrganizerEvent.objects.get(
                events__id=event_id)
            serializer = OrganizerEventSerializer(organizer, data=request.data,
                                                  partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except OrganizerEvent.DoesNotExist:
            return Response({"detail": "Organizer not found."}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(**SwaggerDocs.Organizer.delete)
    def delete(self, request, event_id):
        try:
            organizer = OrganizerEvent.objects.get(
                events__id=event_id)
            organizer.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except OrganizerEvent.DoesNotExist:
            return Response({"detail": "Organizer not found."}, status=status.HTTP_404_NOT_FOUND)


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
            return Response({"detail": "Event not found."}, status=status.HTTP_404_NOT_FOUND)

        if EventRegistration.objects.filter(user=user, event=event).exists():
            return Response({"detail": "User is already registered for this event."},
                            status=status.HTTP_400_BAD_REQUEST)

        distances = DistanceEvent.objects.filter(id__in=distances_ids, event=event)
        if not distances.exists():
            return Response({"detail": "At least one valid distance must be selected."},
                            status=status.HTTP_400_BAD_REQUEST)

        additional_items = AdditionalItemEvent.objects.filter(id__in=additional_items_ids, event=event)

        registration_data = {
            'event': event.id,
            'distances': [distance.id for distance in distances],
            'additional_items': [item.id for item in additional_items]
        }

        serializer = EventRegistrationSerializer(data=registration_data, context={'request': request})

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
        serializer = EventRegistrationDetailSerializer(registration, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(**SwaggerDocs.EventRegistration.delete)
    def delete(self, request, pk=None):
        registration = self.get_object(pk)
        registration.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

