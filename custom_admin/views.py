from drf_yasg.utils import swagger_auto_schema
from rest_framework.viewsets import ModelViewSet

from authentication.permissions import IsAdmin
from event.models import CompetitionType
from event.serializers import CompetitionTypeSerializer
from swagger.custom_admin import SwaggerDocs


class CompetitionsTypeViewSet(ModelViewSet):
    queryset = CompetitionType.objects.all()
    serializer_class = CompetitionTypeSerializer
    permission_classes = [IsAdmin]

    @swagger_auto_schema(**SwaggerDocs.CompetitionsTypeViewSet.get)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(**SwaggerDocs.CompetitionsTypeViewSet.get)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(**SwaggerDocs.CompetitionsTypeViewSet.post)
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(**SwaggerDocs.CompetitionsTypeViewSet.put)
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(**SwaggerDocs.CompetitionsTypeViewSet.patch)
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(**SwaggerDocs.CompetitionsTypeViewSet.delete)
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
