from datetime import datetime

from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.permissions import IsOrganizer
from organization.decorators import check_organization_access_decorator, extract_for_event_access_directly
from organization.models import OrganizationAccess
from organizer_event.models import Event
from organizer_event.serializers import EventSerializer
from swager.event import SwaggerDocs
from utils.pagination import Pagination


class BaseEventView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOrganizer]

    def get_object(self, pk):
        event = Event.objects.get(pk=pk)
        return event


class EventsListView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOrganizer]

    @swagger_auto_schema(**SwaggerDocs.EventList.get)
    def get(self, request):
        current_date = datetime.now().date()
        archives = request.GET.get('archives', None)

        organizer_access = OrganizationAccess.objects.filter(user=request.user)
        organizer_ids = organizer_access.values_list('organization__id', flat=True)

        if archives:
            events = (Event.objects.filter(organizer__id__in=organizer_ids)
                      .order_by('-date_from')
                      .filter(date_to__lt=current_date)
                      )
        else:
            events = (Event.objects.filter(organizer__id__in=organizer_ids)
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


class EventCreateView(BaseEventView):

    @swagger_auto_schema(**SwaggerDocs.EventCreate.post)
    def post(self, request):
        serializer = EventSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventDetailView(BaseEventView):

    @swagger_auto_schema(**SwaggerDocs.EventDetail.get)
    @check_organization_access_decorator(extract_for_event_access_directly)
    def get(self, request, pk):
        event = self.get_object(pk)
        serializer = EventSerializer(event)
        return Response(serializer.data)


class EventUpdateView(BaseEventView):

    @swagger_auto_schema(**SwaggerDocs.EventUpdate.put)
    @check_organization_access_decorator(extract_for_event_access_directly)
    def put(self, request, pk):
        event = self.get_object(pk)
        serializer = EventSerializer(event, data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventPartialUpdateView(BaseEventView):

    @swagger_auto_schema(**SwaggerDocs.EventPartialUpdate.patch)
    @check_organization_access_decorator(extract_for_event_access_directly)
    def patch(self, request, pk):
        event = self.get_object(pk)
        serializer = EventSerializer(event, data=request.data, partial=True, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventDeleteView(BaseEventView):

    @swagger_auto_schema(**SwaggerDocs.EventDelete.delete)
    @check_organization_access_decorator(extract_for_event_access_directly)
    def delete(self, request, pk):
        event = self.get_object(pk)
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
