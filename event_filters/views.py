import re

from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from event.models import Event
from event.serializers import EventSerializer


class EventFilterView(APIView):
    def get(self, request):
        competition_type = request.GET.get('competition_type', None)
        name = request.GET.get('name', None)
        month = request.GET.get('month', None)
        year = request.GET.get('year', None)
        place = request.GET.get('place', None)
        distance_min = request.GET.get('distance_min', None)
        distance_max = request.GET.get('distance_max', None)

        events = Event.objects.all()

        if competition_type:
            events = events.filter(competition_type=competition_type)

        if name:
            events = events.filter(name__icontains=name)

        if month:
            events = events.filter(Q(date_from__month=month) | Q(date_to__month=month))

        if year:
            events = events.filter(Q(date_from__year=year) | Q(date_to__year=year))

        if place:
            events = events.filter(place__icontains=place)

        if distance_min and distance_max:
            try:
                distance_min = float(distance_min)
                distance_max = float(distance_max)

                filtered_events = []
                for event in events:
                    for distance in event.distances.all():
                        match = re.search(r'(\d+)(\s?км|\s?km)', distance.name, re.IGNORECASE)
                        if match:
                            distance_value = float(match.group(1))
                            if distance_min <= distance_value <= distance_max:
                                filtered_events.append(event)
                                break

                # Use filtered_events to count and serialize
                event_count = len(filtered_events)
                serializer = EventSerializer(filtered_events, many=True)

                response_data = {
                    'count': event_count,
                    'events': serializer.data
                }

                return Response(response_data, status=status.HTTP_200_OK)
            
            except ValueError:
                return Response({'error': 'Invalid distance range'}, status=status.HTTP_400_BAD_REQUEST)

        # If no distance filter, use the original events for count and serialization
        event_count = events.count()
        serializer = EventSerializer(events, many=True)

        response_data = {
            'count': event_count,
            'events': serializer.data
        }

        return Response(response_data, status=status.HTTP_200_OK)
