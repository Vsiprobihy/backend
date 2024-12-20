from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from authentication.models import CustomUser
from authentication.permissions import IsAdmin
from event.models import CompetitionType
from event.serializers import CompetitionTypeSerializer
from organization.models import Organizer
from swagger.custom_admin import SwaggerDocs
from utils.custom_exceptions import BadRequestError, CreatedResponse, ForbiddenError, SuccessResponse

from .models import OrganizerRequest


class RequestOrganizerView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, member_id):  # noqa
        user = CustomUser.objects.filter(id=member_id).first()

        if not user:
            return BadRequestError('User not found.').get_response()

        if OrganizerRequest.objects.filter(user=user, is_approved=False).exists():
            return BadRequestError('You already have a pending request.').get_response()

        OrganizerRequest.objects.create(user=user)
        return CreatedResponse('Request submitted successfully.').get_response()


class ApproveOrganizerView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request, member_id):  # noqa
        if not request.user.is_superuser:
            return ForbiddenError('Permission denied.').get_response()

        organizer_request = OrganizerRequest.objects.filter(user_id=member_id, is_approved=False).first()
        if not organizer_request:
            return BadRequestError('Request not found.').get_response()

        organizer_request.is_approved = True
        organizer_request.save()

        user = organizer_request.user
        user.role = Organizer.ORGANIZER
        user.save()

        return SuccessResponse('Request approved and user is now an organizer.').get_response()


class CompetitionsTypeViewSet(ModelViewSet):
    queryset = CompetitionType.objects.all()
    serializer_class = CompetitionTypeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(**SwaggerDocs.CompetitionsTypeViewSet.get)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(**SwaggerDocs.CompetitionsTypeViewSet.get)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(**SwaggerDocs.CompetitionsTypeViewSet.post)
    def create(self, request, *args, **kwargs):
        self.check_permissions(request)
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(**SwaggerDocs.CompetitionsTypeViewSet.put)
    def update(self, request, *args, **kwargs):
        self.check_permissions(request)
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(**SwaggerDocs.CompetitionsTypeViewSet.patch)
    def partial_update(self, request, *args, **kwargs):
        self.check_permissions(request)
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(**SwaggerDocs.CompetitionsTypeViewSet.delete)
    def destroy(self, request, *args, **kwargs):
        self.check_permissions(request)
        return super().destroy(request, *args, **kwargs)

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticatedOrReadOnly()]
        return [IsAdmin()]
