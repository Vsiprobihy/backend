from drf_yasg import openapi


class SwaggerDocs:

    class UserInfo:

        get = {
            'operation_description': 'Get the first and last name of an authorized user or a stub for an unauthorized user, and their avatar URL if available',
            'responses': {
                200: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'username': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="User's full name or 'User' if not authenticated",
                        ),
                        'avatar': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Full URL of the user's avatar, or null if not authenticated or no avatar set",
                        ),
                    },
                    required=['username', 'avatar'],
                    example={
                        'username': 'Alex Morni',
                        'avatar': 'http://example.com/media/uploads/user/user-1.jpg',
                    },
                ),
                401: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='Authentication credentials were not provided or are invalid',
                        )
                    },
                    required=['detail'],
                ),
                500: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='An unexpected error occurred on the server',
                        )
                    },
                    required=['detail'],
                ),
            },
        }
