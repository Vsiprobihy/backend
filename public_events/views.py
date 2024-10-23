from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from event.models import Event
from event.serializers.events import EventSerializer
from drf_yasg.utils import swagger_auto_schema

class PublicEventDetailView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        tags=["Public Events"],
        responses={200: EventSerializer}
    )
    def get(self, request, pk):
        try:
            event = Event.objects.get(pk=pk)
            serializer = EventSerializer(event)
            return Response(serializer.data)
        except Event.DoesNotExist:
            return Response({"detail": "Event not found."}, status=404)
