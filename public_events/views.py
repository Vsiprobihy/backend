import logging

from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from event.models import Event
from event.serializers.events import EventSerializer
from public_events.swagger_schemas import SwaggerDocs


logger = logging.getLogger(__name__)

class PublicEventDetailView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(**SwaggerDocs.TakeEvent.get)
    def get(self, request, pk):
        try:
            event = Event.objects.get(pk=pk)
            serializer = EventSerializer(event)
            return Response(serializer.data)
        except Event.DoesNotExist:
            return Response({'detail': 'Event not found.'}, status=404)
        except Exception as e:
            logger.error(f'Error retrieving event {pk}: {str(e)}')
            return Response({'detail': 'Something went wrong. Please try again later.'}, status=500)
