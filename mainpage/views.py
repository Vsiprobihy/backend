from django.utils import timezone
from django.conf import settings
from event.models import Event
from rest_framework.response import Response
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status

@swagger_auto_schema(
    method='get',
    responses={200: 'Successful Response', 400: 'Invalid parameters'}
)
@api_view(['GET'])
def mainpage(request):
    """
    API endpoint for receiving events that will happen in the next 5 days.
    """
    today = timezone.now().date()
    
    # Get start and end days from settings.py for request to database
    start_date_offset = int(request.GET.get('start_date', settings.MAIN_PAGE_START_DATE_DAYS_AHEAD))
    end_date_offset = int(request.GET.get('end_date', settings.MAIN_PAGE_EVENT_DAYS_AHEAD))

    # Calculate dates to filter
    start_date = today + timezone.timedelta(days=start_date_offset)
    end_date = today + timezone.timedelta(days=end_date_offset)

    events = Event.objects.filter(date_from__range=(start_date, end_date))

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
        for event in events
    ]

    return Response({'events': event_data}, status=status.HTTP_200_OK)
