from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class UserInfoView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Get the first and last name of an authorized user or a stub for an unauthorized user",
        responses={
            200: openapi.Response(
                description="Issuing a username, but if the user is not authorized, a stub is issued",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "username": openapi.Schema(type=openapi.TYPE_STRING, description="User's full name or 'User' if not authenticated")
                    }
                ),
                examples={
                    "application/json": {"username": "Alex Smith"}
                }
            )
        }
    )
    def get(self, request):
        if request.user.is_authenticated:
            user_name = f"{request.user.first_name} {request.user.last_name}"
        else:
            user_name = "User"

        return Response({"username": user_name})
