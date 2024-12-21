from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.models import CustomUser
from custom_admin.models import OrganizerRequest
from event.distance_details.models import DistanceEvent
from swagger.user import SwaggerDocs
from utils.custom_exceptions import BadRequestError, CreatedResponse, ForbiddenError, NotFoundError

from .models import UserDistanceRegistration
from .serializer import UserDistanceRegistrationSerializer


class UserDistanceRegistrationView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(**SwaggerDocs.UserDistanceRegistrationView.post)
    def post(self, request, distance_id):  # noqa
        user = request.user
        distance = DistanceEvent.objects.filter(id=distance_id).first()

        if not distance:
            return NotFoundError('Distance not found.').get_response()

        if UserDistanceRegistration.objects.filter(user=user, distance=distance).exists():
            return BadRequestError('You are already registered for this distance.').get_response()

        registration = UserDistanceRegistration.objects.create(user=user, distance=distance)
        serializer = UserDistanceRegistrationSerializer(registration)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RequestOrganizerView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(**SwaggerDocs.RequestOrganizerView.post)
    def post(self, request, user_id):  # noqa
        user = CustomUser.objects.filter(id=user_id).first()

        if not user:
            return NotFoundError('User not found.').get_response()

        if user.role != CustomUser.USER:
            return ForbiddenError('You do not have permission to perform this action.').get_response()

        if OrganizerRequest.objects.filter(user=user, is_approved=False).exists():
            return BadRequestError('You already have a pending request.').get_response()

        OrganizerRequest.objects.create(user=user)
        return CreatedResponse('Request submitted successfully.').get_response()
