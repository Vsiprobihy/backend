from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .swagger_schemas import user_info_response

class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]

    @user_info_response
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.first_name or request.user.last_name:
                user_name = f"{request.user.first_name} {request.user.last_name}".strip()
            else:
                user_name = None
            
            avatar_url = request.build_absolute_uri(request.user.avatar.url) if request.user.avatar else None
        else:
            user_name = None
            avatar_url = None

        return Response({"username": user_name, "avatar": avatar_url})
