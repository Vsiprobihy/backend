from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.models import AdditionalProfile, CustomUser
from authentication.serializers import AdditionalProfileDetailSerializer, AdditionalProfileSerializer
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

        if OrganizerRequest.objects.filter(user=user, isApproved=False).exists():
            return BadRequestError('You already have a pending request.').get_response()

        OrganizerRequest.objects.create(user=user)
        return CreatedResponse('Request submitted successfully.').get_response()


class AdditionalProfileListView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(**SwaggerDocs.AdditionalProfileList.get)
    def get(self, request):
        profiles = request.user.additional_profiles.all()
        serializer = AdditionalProfileSerializer(profiles, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(**SwaggerDocs.AdditionalProfileList.post)
    def post(self, request):
        serializer = AdditionalProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdditionalProfileDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(**SwaggerDocs.AdditionalProfileDetail.get)
    def get(self, request, _id):
        try:
            profile = request.user.additional_profiles.get(id=_id)
            serializer = AdditionalProfileDetailSerializer(profile)
            return Response(serializer.data)
        except AdditionalProfile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(**SwaggerDocs.AdditionalProfileDetail.put)
    def put(self, request, _id):
        try:
            profile = request.user.additional_profiles.get(id=_id)
            serializer = AdditionalProfileDetailSerializer(profile, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except AdditionalProfile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(**SwaggerDocs.AdditionalProfileDetail.delete)
    def delete(self, request, _id):
        try:
            profile = request.user.additional_profiles.get(id=_id)
            profile.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except AdditionalProfile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
