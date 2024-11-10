from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema

from user_info.swagger_schemas import SwaggerDocs


class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(**SwaggerDocs.UserInfo.get)
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.first_name or request.user.last_name:
                user_name = (
                    f"{request.user.first_name} {request.user.last_name}".strip()
                )
            else:
                user_name = None

            avatar_url = (
                request.build_absolute_uri(request.user.avatar.url)
                if request.user.avatar
                else None
            )
        else:
            user_name = None
            avatar_url = None

        return Response({"username": user_name, "avatar": avatar_url})
