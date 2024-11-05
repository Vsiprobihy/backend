from drf_yasg.utils import swagger_auto_schema
from django.db.models import Q, Count
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
        month = request.GET.get('month', None)
        year = request.GET.get('year', None)
        place = request.GET.get('place', None)
        distance_min = request.GET.get('distance_min', None)
        distance_max = request.GET.get('distance_max', None)
        
        # Sorting by date
        events = Event.objects.all().order_by('-date_from')

        if competition_type:
            # Get the IDs of competition types that are passed in the request
            competition_types = CompetitionType.objects.filter(name__in=competition_type).values_list('id', flat=True)
            if not competition_types:
                return Response({'error': 'No valid competition types found'}, status=status.HTTP_400_BAD_REQUEST)

            # Filter events that have at least one of the specified types
            events = events.filter(competition_type__id__in=competition_types)
            
            # Ensure that the number of unique types for the event matches the number of types provided
            events = events.annotate(num_types=Count('competition_type')).filter(num_types=len(competition_type)).distinct()

        if name:
            events = events.filter(name__icontains=name)

        if month:
            try:
                month = int(month)
                if month < 1 or month > 12:
                    return Response({'error': 'Month must be between 1 and 12'}, status=status.HTTP_400_BAD_REQUEST)
                events = events.filter(Q(date_from__month=month) | Q(date_to__month=month))
            except ValueError:
                return Response({'error': 'Invalid month format'}, status=status.HTTP_400_BAD_REQUEST)

        if year:
            try:
                year = int(year)
                current_year = datetime.now().year
                if year < 1900 or year > current_year + 10:
                    return Response({'error': 'Year must be between 1900 and the next 10 years'}, status=status.HTTP_400_BAD_REQUEST)
                events = events.filter(Q(date_from__year=year) | Q(date_to__year=year))
            except ValueError:
                return Response({'error': 'Invalid year format'}, status=status.HTTP_400_BAD_REQUEST)

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
