from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from event.models import Event
from event.serializers.events import EventSerializer
from public_events.swagger_schemas import SwaggerDocs


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
            return Response({'detail': str(e)}, status=500)
