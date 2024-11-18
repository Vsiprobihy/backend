import logging
import re
from datetime import datetime

from django.db.models import Count
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from organizer_event.models import CompetitionType, Event
from organizer_event.serializers import EventSerializer
from public_events.serializers import PublicEventSerializer
from swagger.public_events import SwaggerDocs
from utils.constants.constants_event import REGIONS
from utils.pagination import Pagination


logger = logging.getLogger(__name__)


class PublicEventListView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(**SwaggerDocs.PublicEventListView.get)
    def get(self, request):
        events = (Event.objects.filter(status='published').order_by('-date_from'))

        paginator = Pagination()
        paginator.page_size = 3

        paginated_events = paginator.paginate_queryset(events, request)

        if paginated_events is not None:
            serializer = PublicEventSerializer(paginated_events, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = PublicEventSerializer(events, many=True)

        return Response(serializer.data)


class PublicEventDetailView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(**SwaggerDocs.PublicEventDetailView.get)
    def get(self, request, pk):
        try:
            event = Event.objects.get(pk=pk, status='published')
            serializer = PublicEventSerializer(event)
            return Response(serializer.data)
        except Event.DoesNotExist:
            return Response({'detail': 'Event not found.'}, status=404)
        except Exception as e:
            logger.error(f'Error retrieving event {pk}: {str(e)}')
            return Response({'detail': 'Something went wrong. Please try again later.'}, status=500)


class PublicEventFilterView(APIView):
    pagination_class = Pagination

    @swagger_auto_schema(**SwaggerDocs.PublicEventFilterView.get)
    def get(self, request):
        competition_type = request.GET.getlist('competition_type')
        name = request.GET.get('name', None)
        date_from = request.GET.get('date_from', None)
        date_to = request.GET.get('date_to', None)
        place = request.GET.get('place', None)
        distance_min = request.GET.get('distance_min', None)
        distance_max = request.GET.get('distance_max', None)

        # Sorting by date
        events = Event.objects.all().order_by('-date_from')

        if competition_type:
            # Get the IDs of the competition types passed in the request
            competition_types = CompetitionType.objects.filter(
                name__in=competition_type
            ).values_list('id', flat=True)
            if not competition_types:
                return Response(
                    {'error': 'No valid competition types found'},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Filter events that have at least one of the specified types
            events = events.filter(competition_type__id__in=competition_types)

            # Ensure that the event contains all the specified types
            events = (
                events.annotate(num_types=Count('competition_type'))
                .filter(num_types__gte=len(competition_type))
                .distinct()
            )

        if name:
            events = events.filter(name__icontains=name)

        if date_from:
            try:
                date_from = datetime.strptime(date_from, '%Y-%m-%d').date()
                events = events.filter(date_to__gte=date_from)
            except ValueError:
                return Response(
                    {'error': 'Invalid date_from format. Use YYYY-MM-DD.'},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        if date_to:
            try:
                date_to = datetime.strptime(date_to, '%Y-%m-%d').date()
                events = events.filter(date_from__lte=date_to)
            except ValueError:
                return Response(
                    {'error': 'Invalid date_to format. Use YYYY-MM-DD.'},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        if place is not None:
            if place not in dict(REGIONS).keys():
                return Response(
                    {'error': 'Invalid region'}, status=status.HTTP_400_BAD_REQUEST
                )
            events = events.filter(place_region=place)

        if distance_min or distance_max:
            try:
                if distance_min is not None:
                    distance_min = float(distance_min)
                    if distance_min < 0 or distance_min > 1000:
                        return Response(
                            {'error': 'distance_min must be between 0 and 1000'},
                            status=status.HTTP_400_BAD_REQUEST,
                        )

                if distance_max is not None:
                    distance_max = float(distance_max)
                    if distance_max < 0 or distance_max > 1000:
                        return Response(
                            {'error': 'distance_max must be between 0 and 1000'},
                            status=status.HTTP_400_BAD_REQUEST,
                        )

                # Ensure distance_min is less than or equal to distance_max
                if (
                        distance_min is not None
                        and distance_max is not None
                        and distance_min > distance_max
                ):
                    return Response(
                        {
                            'error': 'distance_min must be less than or equal to distance_max'
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                events = EventFilterService.filter_by_distance(
                    events, distance_min, distance_max
                )
            except ValueError:
                return Response(
                    {'error': 'Invalid distance format'},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        paginator = self.pagination_class()
        paginated_events = paginator.paginate_queryset(events, request)

        serializer = EventSerializer(paginated_events, many=True)
        return paginator.get_paginated_response(serializer.data)


class EventFilterService:
    @staticmethod
    def filter_by_distance(events, distance_min, distance_max):
        filtered_events = []
        for event in events:
            for distance in event.distances.all():
                match = re.search(
                    r'(\d+)(\s?км|\s?km|\s?м|\s?m)', distance.name, re.IGNORECASE
                )
                if match:
                    distance_value = float(match.group(1))
                    unit = match.group(2).strip().lower()

                    if unit in ['м', 'm']:
                        distance_value /= 1000

                    if (distance_min is None or distance_value >= distance_min) and (
                            distance_max is None or distance_value <= distance_max
                    ):
                        filtered_events.append(event)
                        break
        return filtered_events
