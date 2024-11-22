from datetime import datetime

from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.permissions import IsOrganizer
from organization.decorators import (
    check_organization_access_decorator,
    check_organizer_access_decorator,
    extract_for_event_access_directly,
    extract_organization_directly,
)
from organization.models import Organizer
from event.models import Event
from event.serializers import EventSerializer
from swagger.event import SwaggerDocs
from utils.custom_exceptions import NotFoundError
from utils.pagination import Pagination


class EventsListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOrganizer]

    @swagger_auto_schema(**SwaggerDocs.EventsListCreateView.get)
    @check_organizer_access_decorator(extract_organization_directly)
    def get(self, request, organization_id):
        current_date = datetime.now().date()
        archives = request.GET.get('archives', None)
        user = request.user

        organizer = Organizer.objects.filter(
            user=user,
            organization_id=organization_id,
        )
        organizer_ids = organizer.values_list('organization__id', flat=True)

        if archives:
            events = (Event.objects.filter(organization__id__in=organizer_ids)
                      .order_by('-date_from')
                      .filter(date_to__lt=current_date)
                      )
        else:
            events = (Event.objects.filter(organization__id__in=organizer_ids)
                      .order_by('-date_from')
                      )

        paginator = Pagination()
        paginator.page_size = 6  # temporary long value

        paginated_events = paginator.paginate_queryset(events, request)

        if paginated_events is not None:
            serializer = EventSerializer(paginated_events, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(**SwaggerDocs.EventsListCreateView.post)
    @check_organizer_access_decorator(extract_organization_directly)
    def post(self, request, organization_id):
        serializer = EventSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOrganizer]

    def get_object(self, event_id, organization_id):
        try:
            event = (Event.objects.select_related('organizer')
                     .prefetch_related('distances')
                     .get(pk=event_id, organization_id=organization_id)
                     )
        except Event.DoesNotExist:
            raise NotFoundError('Event not found.')
        return event

    @swagger_auto_schema(**SwaggerDocs.EventDetailView.get)
    @check_organization_access_decorator(extract_for_event_access_directly)
    def get(self, request, organization_id, event_id):
        event = self.get_object(event_id, organization_id)
        serializer = EventSerializer(event)
        return Response(serializer.data)

    @swagger_auto_schema(**SwaggerDocs.EventDetailView.put)
    @check_organization_access_decorator(extract_for_event_access_directly)
    def put(self, request, organization_id, event_id):
        event = self.get_object(event_id, organization_id)
        request.data['organization_id'] = organization_id
        serializer = EventSerializer(event, data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(**SwaggerDocs.EventDetailView.patch)
    @check_organization_access_decorator(extract_for_event_access_directly)
    def patch(self, request, organizer_id, event_id):
        event = self.get_object(event_id, organizer_id)
        serializer = EventSerializer(event, data=request.data, partial=True, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(**SwaggerDocs.EventDetailView.delete)
    @check_organization_access_decorator(extract_for_event_access_directly)
    def delete(self, request, organizer_id, event_id):
        event = self.get_object(event_id, organizer_id)
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
