from drf_yasg.utils import swagger_auto_schema
from django.db.models import Count
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import datetime

from event.models import Event, CompetitionType
from event_filters.views.filter_service import EventFilterService
from event_filters.swagger_schemas import SwaggerDocs
from utils.pagination import EventPaginationView 
from event.constants.constants_event import REGIONS


class EventFilterView(APIView):
    @swagger_auto_schema(**SwaggerDocs.EventFilter.get)
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
            competition_types = CompetitionType.objects.filter(name__in=competition_type).values_list('id', flat=True)
            if not competition_types:
                return Response({'error': 'No valid competition types found'}, status=status.HTTP_400_BAD_REQUEST)

            # Filter events that have at least one of the specified types
            events = events.filter(competition_type__id__in=competition_types)

            # Ensure that the event contains all the specified types
            events = events.annotate(num_types=Count('competition_type')).filter(num_types__gte=len(competition_type)).distinct()

        if name:
            events = events.filter(name__icontains=name)

        if date_from:
            try:
                date_from = datetime.strptime(date_from, '%Y-%m-%d').date()
                events = events.filter(date_to__gte=date_from)
            except ValueError:
                return Response({'error': 'Invalid date_from format. Use YYYY-MM-DD.'}, status=status.HTTP_400_BAD_REQUEST)

        if date_to:
            try:
                date_to = datetime.strptime(date_to, '%Y-%m-%d').date()
                events = events.filter(date_from__lte=date_to)
            except ValueError:
                return Response({'error': 'Invalid date_to format. Use YYYY-MM-DD.'}, status=status.HTTP_400_BAD_REQUEST)

        if place is not None:
            if place not in dict(REGIONS).keys():
                return Response({'error': 'Invalid region'}, status=status.HTTP_400_BAD_REQUEST)
            events = events.filter(place_region=place)

        if distance_min or distance_max:
            try:
                if distance_min is not None:
                    distance_min = float(distance_min)
                    if distance_min < 0 or distance_min > 1000:
                        return Response({'error': 'distance_min must be between 0 and 1000'}, status=status.HTTP_400_BAD_REQUEST)

                if distance_max is not None:
                    distance_max = float(distance_max)
                    if distance_max < 0 or distance_max > 1000:
                        return Response({'error': 'distance_max must be between 0 and 1000'}, status=status.HTTP_400_BAD_REQUEST)

                # Ensure distance_min is less than or equal to distance_max
                if distance_min is not None and distance_max is not None and distance_min > distance_max:
                    return Response({'error': 'distance_min must be less than or equal to distance_max'}, status=status.HTTP_400_BAD_REQUEST)

                events = EventFilterService.filter_by_distance(events, distance_min, distance_max)
            except ValueError:
                return Response({'error': 'Invalid distance format'}, status=status.HTTP_400_BAD_REQUEST)

        # Create an instance of EventPaginationView and call its get method
        paginator_view = EventPaginationView()
        return paginator_view.get(request, events)
