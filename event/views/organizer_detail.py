from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from event.models import OrganizerEvent
from event.serializers.organizer_detail import OrganizerEventSerializer
from swagger_docs import SwaggerDocs


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