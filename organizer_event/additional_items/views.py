from django.http import Http404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from organization.decorators import check_organization_access_decorator, extract_event_from_distance
from organizer_event.additional_items.models import AdditionalItemEvent
from organizer_event.additional_items.serializers import AdditionalItemEventSerializer
from swagger.additional_items import SwaggerDocs


class AdditionalItemsDetailView(APIView):
    def get_object(self, pk):
        try:
            return AdditionalItemEvent.objects.get(pk=pk)
        except AdditionalItemEvent.DoesNotExist:
            raise Http404

    def _get_objects_by_distance(self, distance_id):
        return AdditionalItemEvent.objects.filter(distance_id=distance_id)

    @swagger_auto_schema(**SwaggerDocs.AdditionalItem.post)
    def post(self, request, distance_id):
        data = request.data.copy()
        data['distance'] = distance_id

        if not data.get('distance'):
            return Response(
                {'distance': 'Distance must be specified when adding an AdditionalItem to an existing event.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = AdditionalItemEventSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(**SwaggerDocs.AdditionalItem.get)
    @check_organization_access_decorator(extract_event_from_distance)
    def get(self, request, distance_id):
        items = AdditionalItemEvent.objects.filter(distance_id=distance_id)
        if not items.exists():
            return Response(
                {'detail': 'No additional items found for this event.'}, status=404
            )

        serializer = AdditionalItemEventSerializer(items, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(**SwaggerDocs.AdditionalItem.put)
    @check_organization_access_decorator(extract_event_from_distance)
    def put(self, request, distance_id):
        if isinstance(request.data, dict):
            data_list = [request.data]
        elif isinstance(request.data, list):
            data_list = request.data
        else:
            return Response(
                {'detail': 'Expected a dictionary or a list of items.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        items = self._get_objects_by_distance(distance_id)
        if not items.exists():
            return Response(
                {'detail': 'No additional items found for this event.'}, status=404
            )

        updated_data = []
        for data in data_list:
            item = items.filter(id=data.get('id')).first()
            if not item:
                return Response(
                    {'detail': f"Item with id {data.get('id')} not found."}, status=404
                )

            serializer = AdditionalItemEventSerializer(item, data=data)
            if serializer.is_valid():
                serializer.save()
                updated_data.append(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(updated_data, status=status.HTTP_200_OK)

    @swagger_auto_schema(**SwaggerDocs.AdditionalItem.patch)
    @check_organization_access_decorator(extract_event_from_distance)
    def patch(self, request, distance_id):
        if isinstance(request.data, dict):
            data_list = [request.data]
        elif isinstance(request.data, list):
            data_list = request.data
        else:
            return Response(
                {'detail': 'Expected a dictionary or a list of items.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        items = self._get_objects_by_distance(distance_id)
        if not items.exists():
            return Response(
                {'detail': 'No additional items found for this event.'}, status=404
            )

        updated_data = []
        for data in data_list:
            item_id = data.get('id')
            if not item_id:
                return Response(
                    {'detail': "Each item must include an 'id' field."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            item = items.filter(id=item_id).first()
            if not item:
                return Response(
                    {'detail': f'Item with id {item_id} not found.'},
                    status=status.HTTP_404_NOT_FOUND,
                )

            serializer = AdditionalItemEventSerializer(item, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                updated_data.append(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(updated_data, status=status.HTTP_200_OK)

    @swagger_auto_schema(**SwaggerDocs.AdditionalItem.delete)
    @check_organization_access_decorator(extract_event_from_distance)
    def delete(self, request, distance_id):
        ids = request.data
        if not isinstance(ids, list):
            return Response(
                {'detail': 'Expected a list of IDs.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        deleted_ids = []
        for data in ids:
            item_id = data.get('id')
            if not item_id:
                return Response(
                    {'detail': "Each item must include an 'id' field."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            item = AdditionalItemEvent.objects.filter(
                id=item_id, distance_id=distance_id
            ).first()
            if not item:
                return Response(
                    {'detail': f'Item with id {item_id} not found for this event.'},
                    status=status.HTTP_404_NOT_FOUND,
                )

            item.delete()
            deleted_ids.append(item_id)

        return Response({'deleted_ids': deleted_ids}, status=status.HTTP_204_NO_CONTENT)
