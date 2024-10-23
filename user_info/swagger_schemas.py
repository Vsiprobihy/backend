from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

user_info_response = swagger_auto_schema(
    operation_description="Get the first and last name of an authorized user or a stub for an unauthorized user",
    responses={
        200: openapi.Response(
            description="Issuing a username, but if the user is not authorized, a stub is issued",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "username": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description="User's full name or 'User' if not authenticated"
                    )
                }
            ),
            examples={
                "application/json": {"username": "Иван Иванов"}
            }
        )
    }
)
