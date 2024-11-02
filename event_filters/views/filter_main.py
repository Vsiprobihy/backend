from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import datetime

from event.models import Event
from event_filters.views.filter_service import EventFilterService
from event_filters.swagger_schemas import event_filter_schema
from utils.pagination import EventPaginationView 
from event.constants.constants_event import REGIONS, COMPETITION_TYPES


class EventFilterView(APIView):
    @event_filter_schema
    def get(self, request):
        competition_type = request.GET.get('competition_type', None)
        name = request.GET.get('name', None)
        month = request.GET.get('month', None)
        year = request.GET.get('year', None)
        place = request.GET.get('place', None)
        distance_min = request.GET.get('distance_min', None)
        distance_max = request.GET.get('distance_max', None)
        
        # Sorting by date
        events = Event.objects.all().order_by('-date_from')

        
        if competition_type is not None:
            if competition_type not in dict(COMPETITION_TYPES).keys():
                return Response({'error': 'Invalid competiton type'}, status=status.HTTP_400_BAD_REQUEST)
            events = events.filter(competition_type=competition_type)

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
                if year < 2000 or year > current_year + 1:
                    return Response({'error': 'Year must be between 2000 and no more than 1 year from the current year'}, status=status.HTTP_400_BAD_REQUEST)
                events = events.filter(Q(date_from__year=year) | Q(date_to__year=year))
            except ValueError:
                return Response({'error': 'Invalid year format'}, status=status.HTTP_400_BAD_REQUEST)

        if place is not None:
            if place not in dict(REGIONS).keys():
                return Response({'error': 'Invalid region'}, status=status.HTTP_400_BAD_REQUEST)
            events = events.filter(place_region=place)

        if distance_min and distance_max:
            try:
                distance_min = float(distance_min)
                distance_max = float(distance_max)
                events = EventFilterService.filter_by_distance(events, distance_min, distance_max)
            except ValueError:
                return Response({'error': 'Invalid distance range'}, status=status.HTTP_400_BAD_REQUEST)
        elif distance_max:
            try:
                distance_max = float(distance_max)
                events = EventFilterService.filter_by_distance(events, None, distance_max)
            except ValueError:
                return Response({'error': 'Invalid distance maximum'}, status=status.HTTP_400_BAD_REQUEST)

        # Create an instance of EventPaginationView and call its get method
        paginator_view = EventPaginationView()
        return paginator_view.get(request, events)
