from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .swagger_schemas import user_info_response

class UserInfoView(APIView):
    permission_classes = [AllowAny]

    @user_info_response
    def get(self, request):
        if request.user.is_authenticated:
            user_name = f"{request.user.first_name} {request.user.last_name}"
        else:
            user_name = "User"

        return Response({"username": user_name})
