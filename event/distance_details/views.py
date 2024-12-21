from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from swagger.distanse import SwaggerDocs
from user.models import UserDistanceRegistration
from user.serializer import UserDistanceRegistrationSerializer
from utils.custom_exceptions import BadRequestError, NotFoundError

from .models import DistanceEvent, FavoriteDistance
from .serializers import FavoriteDistanceSerializer


class MyDistanceListView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(**SwaggerDocs.MyDistanceListView.get)
    def get(self, request):  # noqa
        distances = UserDistanceRegistration.objects.filter(user=request.user, is_confirmed=True)
        if distances:
            serializer = UserDistanceRegistrationSerializer(distances, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response([], status=status.HTTP_200_OK)


class FavoriteDistanceListView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(**SwaggerDocs.FavoriteDistanceListView.get)
    def get(self, request):  # noqa
        favorites = FavoriteDistance.objects.filter(user=request.user)
        if favorites:
            serializer = FavoriteDistanceSerializer(favorites, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response([], status=status.HTTP_200_OK)


class FavoriteDistanceDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(**SwaggerDocs.FavoriteDistanceDetailView.post)
    def post(self, request, distance_id):  # noqa

        distance = DistanceEvent.objects.filter(id=distance_id).first()

        if not distance:
            return NotFoundError('Distance not found.').get_response()

        favorite, created = FavoriteDistance.objects.get_or_create(user=request.user, distance=distance)

        if not created:
            return BadRequestError('Distance is already in favorites.').get_response()

        serializer = FavoriteDistanceSerializer(favorite)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(**SwaggerDocs.FavoriteDistanceDetailView.delete)
    def delete(self, request, distance_id):  # noqa

        if not distance_id:
            return BadRequestError('Distance ID is required.').get_response()

        favorite = FavoriteDistance.objects.filter(user=request.user, distance_id=distance_id).first()
        if not favorite:
            return NotFoundError('Favorite distance not found.').get_response()

        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
