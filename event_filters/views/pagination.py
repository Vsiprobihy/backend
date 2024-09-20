from django.core.paginator import Paginator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from event.serializers.events import EventSerializer

class EventPaginationView(APIView):
    def get(self, request, events):
        page = request.GET.get('page', 1)  # Default page number
        page_size = 12  # (Pagination)Number of events per page

        paginator = Paginator(events, page_size)
        paginated_events = paginator.get_page(page)

        serializer = EventSerializer(paginated_events, many=True)
        
        response_data = {
            'count': paginator.count,
            'events': serializer.data
        }

        return Response(response_data, status=status.HTTP_200_OK)
