from django.http import Http404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from event.models import AdditionalItemEvent
from event.serializers.additional_items import AdditionalItemEventSerializer
from swagger_docs import SwaggerDocs


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