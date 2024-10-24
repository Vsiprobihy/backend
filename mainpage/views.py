# event/views.py
from django.utils import timezone
from event.models import Event
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from mainpage.swagger_schemas import mainpage_schema

@mainpage_schema
@api_view(['GET'])
def mainpage(request):
    """
    API endpoint for receiving the next upcoming events.
    """
    today = timezone.now().date()
    
    # Get the count of events to return from the request or default to 3
    count = int(request.GET.get('count', 3))

    # Filter upcoming events
    upcoming_events = Event.objects.filter(date_from__gte=today).order_by('date_from')[:count]

    event_data = [
        {
            'id': event.id,
            'name': event.name,
            'date_from': event.date_from.isoformat(),
            'date_to': event.date_to.isoformat() if event.date_to else None,
            'place': event.place,
            'competition_type': event.competition_type,
            'photos': event.photos.url if event.photos else None,
            'distances': [
                {
                    'name': distance.name,
                    'id': distance.id,
                }
                for distance in event.distances.all()
            ],
        }
        for event in upcoming_events
    ]

    return Response({'events': event_data}, status=status.HTTP_200_OK)
