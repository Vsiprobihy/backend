from django.utils import timezone
from event.models import Event
from rest_framework.response import Response
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status

@swagger_auto_schema(
    method='get',
    responses={200: 'Successful Response', 400: 'Invalid parameters'},
    manual_parameters=[
        openapi.Parameter(
            name='count',
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_INTEGER,
            required=False,
            description='Number of upcoming events to return (default is 3)',
        )
    ]
)
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
        }
        for event in upcoming_events
    ]

    return Response({'events': event_data}, status=status.HTTP_200_OK)
