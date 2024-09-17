from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from event.models import Event
from event.serializers import EventSerializer
from django.db.models import Q
import re

class EventFilterView(APIView):
    def get(self, request):
        # Get filtering parameters from GET request
        competition_type = request.GET.get('competition_type', None)
        name = request.GET.get('name', None)
        month = request.GET.get('month', None)
        year = request.GET.get('year', None)
        place = request.GET.get('place', None)
        distance_min = request.GET.get('distance_min', None)
        distance_max = request.GET.get('distance_max', None)

        # Base QuerySet for Event objects
        events = Event.objects.all()

        # Apply filters
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

        # Filter by distance range
        if distance_min and distance_max:
            try:
                # Attempt to convert to float numbers.
                # If values cannot be converted to numbers
                # (e.g., user entered non-numeric data), an error will occur.
                distance_min = float(distance_min)
                distance_max = float(distance_max)

                # Apply distance filtering
                # events = events.filter(
                #     distances__name__regex=rf'(\d+)(\s?км|\s?km)'
                # ).distinct()

                filtered_events = []
                for event in events:
                    # Check each event's distance
                    for distance in event.distances.all():
                        # Extract number from string
                        match = re.search(rf'(\d+)(\s?км|\s?km)', distance.name)
                        if match:
                            distance_value = float(match.group(1))
                            # If distance is within the range
                            if distance_min <= distance_value <= distance_max:
                                filtered_events.append(event)
                                break  # If at least one distance fits, add the event

                events = filtered_events

            except ValueError:
                return Response({"error": "Invalid distance range"}, status=status.HTTP_400_BAD_REQUEST)

        # Serialize results
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
