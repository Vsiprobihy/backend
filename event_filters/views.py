from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from event.models import Event
from event.serializers import EventSerializer
from django.db.models import Q

class EventFilterView(APIView):
    def get(self, request):
        # Get filter parameters from the GET request
        competition_type = request.GET.get('competition_type', None)
        name = request.GET.get('name', None)
        month = request.GET.get('month', None)
        year = request.GET.get('year', None)
        place = request.GET.get('place', None)
        distance_km = request.GET.get('distance_km', None)

        # Base QuerySet for Event objects
        events = Event.objects.all()

        # Apply filters
        if competition_type:
            events = events.filter(competition_type=competition_type)
        
        if name:
            events = events.filter(name__icontains=name)

        # Filter by month for date_from and date_to
        if month:
            events = events.filter(
                Q(date_from__month=month) | Q(date_to__month=month)
            )

        if year:
            events = events.filter(
                Q(date_from__year=year) | Q(date_to__year=year)
            )

        if place:
            events = events.filter(place__icontains=place)

        if distance_km:
            events = events.filter(distances__name__regex=rf'^{distance_km}\s?(км|km)')
        # Serialize the results
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
