from django.core.paginator import Paginator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from event.serializers.events import EventSerializer


class EventPaginationView(APIView):
    def get(self, request, events):
        page = request.GET.get("page", 1)  # Default page number

        # Check if 'page' is a positive integer
        try:
            page = int(page)
            if page < 1:
                return Response(
                    {"error": "Page number must be a positive number"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except ValueError:
            return Response(
                {"error": "Page number must be an integer"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        page_size = 12  # Number of events per page

        paginator = Paginator(events, page_size)

        # Check if the requested page exists
        if page > paginator.num_pages:
            return Response(
                {"error": "Requested page exceeds available pages"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        paginated_events = paginator.get_page(page)

        serializer = EventSerializer(paginated_events, many=True)

        response_data = {"count": paginator.count, "events": serializer.data}

        return Response(response_data, status=status.HTTP_200_OK)
