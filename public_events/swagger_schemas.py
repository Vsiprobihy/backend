from drf_yasg import openapi

from event.serializers.events import EventSerializer


class SwaggerDocs:

    class TakeEvent:
        get = {
            "tags": ["Public Events"],
            "operation_description": "Retrieve detailed information about a specific event by its ID.",
            "responses": {
                200: EventSerializer,
                404: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "detail": openapi.Schema(
                            type=openapi.TYPE_STRING, description="Event not found."
                        )
                    },
                    required=["detail"],
                ),
                500: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "detail": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Internal server error while retrieving the event.",
                        )
                    },
                    required=["detail"],
                ),
            },
        }
