from django.http import Http404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.permissions import IsOrganizer
from event.models import AdditionalItemEvent, DistanceEvent, Event, OrganizationAccess
from event.serializers.distance_detail import DistanceEventSerializer
from swagger_docs import SwaggerDocs


class DistanceDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOrganizer]

    def get_event(self, event_id):
        try:
            return Event.objects.get(pk=event_id)
        except Event.DoesNotExist:
            raise Http404

    def check_user_permission(self, event):
        user = self.request.user
        if not OrganizationAccess.objects.filter(
            organization=event.organizer, user=user
        ).exists():
            raise PermissionDenied('You do not have permission to access this event.')

    def get_object(self, pk):
        try:
            return DistanceEvent.objects.get(pk=pk)
        except DistanceEvent.DoesNotExist:
            raise Http404

    def _get_objects_by_event(self, event_id):
        return DistanceEvent.objects.filter(event_id=event_id)

    @swagger_auto_schema(**SwaggerDocs.Distance.post)
    def post(self, request, event_id):
        event = self.get_event(event_id)
        self.check_user_permission(event)

        data = request.data.copy()
        data['event'] = event_id
        serializer = DistanceEventSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(**SwaggerDocs.Distance.get)
    def get(self, request, event_id):
        event = self.get_event(event_id)
        self.check_user_permission(event)

        distances = self._get_objects_by_event(event_id)
        if not distances.exists():
            return Response(
                {'detail': 'No distances found for this event.'}, status=404
            )

        serializer = DistanceEventSerializer(distances, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(**SwaggerDocs.Distance.put)
    def put(self, request, event_id):
        event = self.get_event(event_id)
        self.check_user_permission(event)

        if isinstance(request.data, dict):
            data_list = [request.data]
        elif isinstance(request.data, list):
            data_list = request.data
        else:
            return Response(
                {'detail': 'Expected a dictionary or a list of items.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        distances = self._get_objects_by_event(event_id)
        if not distances.exists():
            return Response(
                {'detail': 'No distances found for this event.'}, status=404
            )

        updated_data = []
        for data in data_list:
            # Ensure the event is set correctly
            data['event'] = event_id

            item = distances.filter(id=data.get('id')).first()
            if not item:
                return Response(
                    {'detail': f"Distance with id {data.get('id')} not found."},
                    status=404,
                )

            # Handle updating additional options if included in the request
            additional_options_data = data.pop('additional_options', None)

            # Update the DistanceEvent instance
            serializer = DistanceEventSerializer(item, data=data)
            if serializer.is_valid():
                updated_distance = serializer.save()

                # Handle additional options separately if present
                if additional_options_data is not None:
                    for option_data in additional_options_data:
                        option_data['event'] = event
                        option_data['distance'] = updated_distance
                        AdditionalItemEvent.objects.filter(id=option_data.get('id')).update(**option_data)

                updated_data.append(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(updated_data, status=status.HTTP_200_OK)

    @swagger_auto_schema(**SwaggerDocs.Distance.patch)
    def patch(self, request, event_id):
        event = self.get_event(event_id)
        self.check_user_permission(event)

        if isinstance(request.data, dict):
            data_list = [request.data]
        elif isinstance(request.data, list):
            data_list = request.data
        else:
            return Response(
                {'detail': 'Expected a dictionary or a list of items.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        distances = self._get_objects_by_event(event_id)
        if not distances.exists():
            return Response(
                {'detail': 'No distances found for this event.'}, status=404
            )

        updated_data = []
        for data in data_list:
            item_id = data.get('id')
            if not item_id:
                return Response(
                    {'detail': "Each item must include an 'id' field."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            item = distances.filter(id=item_id).first()
            if not item:
                return Response(
                    {'detail': f'Distance with id {item_id} not found.'},
                    status=status.HTTP_404_NOT_FOUND,
                )

            # Handle updating additional options if present
            additional_options_data = data.pop('additional_options', None)

            serializer = DistanceEventSerializer(item, data=data, partial=True)
            if serializer.is_valid():
                updated_distance = serializer.save()

                # Update additional options if provided
                if additional_options_data is not None:
                    for option_data in additional_options_data:
                        option_data['event'] = event
                        option_data['distance'] = updated_distance
                        AdditionalItemEvent.objects.filter(id=option_data.get('id')).update(**option_data)

                updated_data.append(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(updated_data, status=status.HTTP_200_OK)

    @swagger_auto_schema(**SwaggerDocs.Distance.delete)
    def delete(self, request, event_id):
        event = self.get_event(event_id)
        self.check_user_permission(event)

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

            distance = DistanceEvent.objects.filter(
                id=item_id, event_id=event_id
            ).first()
            if not distance:
                return Response(
                    {'detail': f'Distance with id {item_id} not found.'},
                    status=status.HTTP_404_NOT_FOUND,
                )

            distance.delete()
            deleted_ids.append(item_id)

        return Response({'deleted_ids': deleted_ids}, status=status.HTTP_204_NO_CONTENT)
