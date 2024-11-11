from drf_yasg import openapi
<<<<<<< Updated upstream
from event.constants.constants_event import REGIONS, COMPETITION_TYPES
=======

from event.constants.constants_event import COMPETITION_TYPES, REGIONS
from event.serializers.events import EventSerializer
>>>>>>> Stashed changes


class SwaggerDocs:

    class EventFilter:

        get = {
            'operation_description': 'Filtering events by competition type, name, location, distance, and date range',
            'manual_parameters': [
                openapi.Parameter(
                    'page',
                    openapi.IN_QUERY,
                    description='Page number for pagination',
                    type=openapi.TYPE_STRING,
                ),
                openapi.Parameter(
                    'competition_type',
                    openapi.IN_QUERY,
                    description='Type of competition (e.g., running, trail, cycling)',
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(
                        type=openapi.TYPE_STRING,
                        enum=[competition for competition, name in COMPETITION_TYPES],
                    ),
                    collectionFormat='multi',
                ),
                openapi.Parameter(
                    'name',
                    openapi.IN_QUERY,
                    description='Event name',
                    type=openapi.TYPE_STRING,
                ),
                openapi.Parameter(
                    'date_from',
                    openapi.IN_QUERY,
                    description='Start date of the event (YYYY-MM-DD)',
                    type=openapi.TYPE_STRING,
                ),
                openapi.Parameter(
                    'date_to',
                    openapi.IN_QUERY,
                    description='End date of the event (YYYY-MM-DD)',
                    type=openapi.TYPE_STRING,
                ),
                openapi.Parameter(
                    'place',
                    openapi.IN_QUERY,
                    description='Event location (select from available regions)',
                    type=openapi.TYPE_STRING,
                    enum=[code for code, name in REGIONS],
                ),
                openapi.Parameter(
                    'distance_min',
                    openapi.IN_QUERY,
                    description='Minimum distance (km)',
                    type=openapi.TYPE_NUMBER,
                ),
                openapi.Parameter(
                    'distance_max',
                    openapi.IN_QUERY,
                    description='Maximum distance (km)',
                    type=openapi.TYPE_NUMBER,
                ),
            ],
<<<<<<< Updated upstream

            'responses': {
                200: openapi.Response(
                    description="List of events with count",
                    schema=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'count': openapi.Schema(type=openapi.TYPE_INTEGER, description='Total number of events matching the filters'),
                            'events': openapi.Schema(
                                type=openapi.TYPE_ARRAY,
                                items=openapi.Items(
                                    type=openapi.TYPE_OBJECT,
                                    properties={
                                        'name': openapi.Schema(type=openapi.TYPE_STRING),
                                        'competition_type': openapi.Schema(
                                            type=openapi.TYPE_ARRAY,
                                            items=openapi.Items(type=openapi.TYPE_INTEGER),
                                        ),
                                        'date_from': openapi.Schema(type=openapi.TYPE_STRING),
                                        'date_to': openapi.Schema(type=openapi.TYPE_STRING),
                                        'place_region': openapi.Schema(type=openapi.TYPE_STRING),
                                        'place': openapi.Schema(type=openapi.TYPE_STRING),
                                        'photos': openapi.Schema(type=openapi.TYPE_OBJECT, nullable=True),
                                        'distances': openapi.Schema(
                                            type=openapi.TYPE_ARRAY,
                                            items=openapi.Items(
                                                type=openapi.TYPE_OBJECT,
                                                properties={
                                                    'name': openapi.Schema(type=openapi.TYPE_STRING),
                                                },
                                                required=['name'],  # Обязательное поле name в distances
                                            ),
                                        ),
                                    },
                                    required=['name', 'competition_type', 'date_from', 'date_to', 'place_region', 'place', 'distances'],  # Обязательные поля
                                ),
                            ),
                        },
                        required=['count', 'events'],
                    )
                ),

=======
            'responses': {
                200: EventSerializer(many=True),
>>>>>>> Stashed changes
                400: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='Invalid filter parameters. Possible errors include invalid date format, region, or distance range. For example, distance_min must be less than or equal to distance_max.',
                        )
                    },
                    required=['error'],
                ),
                500: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='Internal server error while processing the request.',
                        )
                    },
                    required=['error'],
                ),
            },
        }
