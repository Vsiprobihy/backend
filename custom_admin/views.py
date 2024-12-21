from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from authentication.models import CustomUser
from authentication.permissions import IsAdmin
from event.models import CompetitionType
from event.serializers import CompetitionTypeSerializer
from swagger.custom_admin import SwaggerDocs
from user.models import UserDistanceRegistration
from utils.custom_exceptions import ForbiddenError, NotFoundError, SuccessResponse

from .models import OrganizerRequest


class ApproveDistanceRegistrationView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    @swagger_auto_schema(**SwaggerDocs.ApproveDistanceRegistrationView.post)
    def post(self, request, registration_id):  # noqa
        registration = UserDistanceRegistration.objects.filter(id=registration_id, is_confirmed=False).first()

        if not registration:
            return NotFoundError('Registration not found or already confirmed.').get_response()

        registration.is_confirmed = True
        registration.save()

        return SuccessResponse('Registration approved successfully.').get_response()


class ApproveOrganizerView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    @swagger_auto_schema(**SwaggerDocs.ApproveOrganizerView.post)
    def post(self, request, user_id):  # noqa
        if not request.user.is_superuser:
            return ForbiddenError('You do not have permission to perform this action.').get_response()

        organizer_request = OrganizerRequest.objects.filter(user_id=user_id, is_approved=False).first()
        if not organizer_request:
            return NotFoundError('Request not found.').get_response()

        organizer_request.is_approved = True
        organizer_request.save()

        user = organizer_request.user
        user.role = CustomUser.ORGANIZER
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
