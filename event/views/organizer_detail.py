from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, permissions
from event.models import OrganizerEvent
from event.serializers.organizer_detail import OrganizerEventSerializer
from swagger_docs import SwaggerDocs


class OrganizerEventListCreateView(generics.ListCreateAPIView):
    serializer_class = OrganizerEventSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(**SwaggerDocs.Organizer.get)
    def get_queryset(self):
        # Возвращаем только события организатора, привязанные к текущему пользователю
        return OrganizerEvent.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        # Устанавливаем текущего пользователя как организатора
        serializer.save(user=self.request.user)

class OrganizerEventDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrganizerEventSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Доступ к событию имеет только организатор, создавший его
        return OrganizerEvent.objects.filter(user=self.request.user)
    
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)