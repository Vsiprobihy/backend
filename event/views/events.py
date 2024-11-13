from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_yasg.utils import swagger_auto_schema

from event.models import AdditionalItemEvent, DistanceEvent, Event, OrganizationAccess
from event.serializers.additional_items import AdditionalItemEventSerializer
from event.serializers.distance_detail import DistanceEventSerializer
from event.serializers.events import EventSerializer

from swagger_docs import SwaggerDocs
from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied
from authentication.permissions import IsOrganizer


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

        if not OrganizationAccess.objects.filter(organization=event.organizer, user=user).exists():
            raise PermissionDenied("You do not have permission to access this event.")

        return event

    @swagger_auto_schema(**SwaggerDocs.Event.get)
    def get(self, request, pk):
        event = self.get_object(pk)
        serializer = EventSerializer(event)
        return Response(serializer.data)

    @swagger_auto_schema(**SwaggerDocs.Event.put)
    def put(self, request, pk):
        event = self.get_object(pk)
        serializer = EventSerializer(event, data=request.data, context={'request': request})
        
        if serializer.is_valid():
            updated_event = serializer.save()

            distances_data = request.data.get('distances', [])
            for distance_data in distances_data:
                distance_id = distance_data.get('id')
                if distance_id:
                    # Обновление существующей дистанции
                    distance = DistanceEvent.objects.filter(id=distance_id, event=updated_event).first()
                    if distance:
                        distance_serializer = DistanceEventSerializer(distance, data=distance_data, partial=True)
                        if distance_serializer.is_valid():
                            distance_serializer.save()
                else:
                    # Создание новой дистанции
                    distance_serializer = DistanceEventSerializer(data=distance_data)
                    if distance_serializer.is_valid():
                        distance_serializer.save(event=updated_event)

                # Обработка дополнительных опций для дистанции
                additional_options_data = distance_data.get('additional_options', [])
                for option_data in additional_options_data:
                    option_id = option_data.get('id')
                    if option_id:
                        # Обновление существующей опции
                        option = AdditionalItemEvent.objects.filter(id=option_id).first()
                        if option:
                            option_serializer = AdditionalItemEventSerializer(option, data=option_data, partial=True)
                            if option_serializer.is_valid():
                                option_serializer.save()
                    else:
                        # Создание новой дополнительной опции
                        option_serializer = AdditionalItemEventSerializer(data=option_data)
                        if option_serializer.is_valid():
                            option_serializer.save(event=updated_event)  # Указываем event_id

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(**SwaggerDocs.Event.patch)
    def patch(self, request, pk):
        event = self.get_object(pk)
        serializer = EventSerializer(event, data=request.data, partial=True, context={'request': request})
        
        if serializer.is_valid():
            updated_event = serializer.save()

            distances_data = request.data.get('distances', [])
            for distance_data in distances_data:
                distance_id = distance_data.get('id')
                if distance_id:
                    # Обновление существующей дистанции
                    distance = DistanceEvent.objects.filter(id=distance_id, event=updated_event).first()
                    if distance:
                        distance_serializer = DistanceEventSerializer(distance, data=distance_data, partial=True)
                        if distance_serializer.is_valid():
                            distance_serializer.save()
                else:
                    # Создание новой дистанции
                    distance_serializer = DistanceEventSerializer(data=distance_data)
                    if distance_serializer.is_valid():
                        distance_serializer.save(event=updated_event)

                # Обработка дополнительных опций для дистанции
                additional_options_data = distance_data.get('additional_options', [])
                for option_data in additional_options_data:
                    option_id = option_data.get('id')
                    if option_id:
                        # Обновление существующей опции
                        option = AdditionalItemEvent.objects.filter(id=option_id).first()
                        if option:
                            option_serializer = AdditionalItemEventSerializer(option, data=option_data, partial=True)
                            if option_serializer.is_valid():
                                option_serializer.save()
                    else:
                        # Создание новой дополнительной опции
                        option_serializer = AdditionalItemEventSerializer(data=option_data)
                        if option_serializer.is_valid():
                            option_serializer.save(event=updated_event)  # Указываем event_id

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(**SwaggerDocs.Event.delete)
    def delete(self, request, pk):
        event = self.get_object(pk)
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
