from drf_yasg import openapi

from event.serializers import EventSerializer
from utils.constants.constants_event import COMPETITION_TYPES, REGIONS


class SwaggerDocs:

    class PublicEventListView:
        get = {
            'tags': ['Public Event'],
            'operation_description': 'Retrieve detailed information list event',
            'responses': {
                200: EventSerializer,
                404: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_STRING, description='Event not found.'
                        )
                    },
                    required=['detail'],
                ),
                500: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='Internal server error while retrieving the event.',
                        )
                    },
                    required=['detail'],
                ),
            },
        }

    class PublicEventDetailView:
        get = {
            'tags': ['Public Event'],
            'operation_description': 'Retrieve detailed information about a specific event by its ID.',
            'responses': {
                200: EventSerializer,
                404: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_STRING, description='Event not found.'
                        )
                    },
                    required=['detail'],
                ),
                500: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='Internal server error while retrieving the event.',
                        )
                    },
                    required=['detail'],
                ),
            },
        }

    class PublicEventFilterView:

        get = {
            'tags': ['Public Event'],
            'operation_description': 'Filtering events by competition type, name, location, distance, and date range',
            'manual_parameters': [
                openapi.Parameter(
                    'page', openapi.IN_QUERY, description='Page number for pagination', type=openapi.TYPE_STRING
                ),
                openapi.Parameter(
                    'competition_type',
                    openapi.IN_QUERY,
                    description='Type of competition (e.g., running, trail, cycling)',
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(
                        type=openapi.TYPE_STRING,
                        enum=[competition for competition, name in COMPETITION_TYPES]
                    ),
                    collectionFormat='multi'
                ),
                openapi.Parameter(
                    'name', openapi.IN_QUERY, description='Event name', type=openapi.TYPE_STRING
                ),
                openapi.Parameter(
                    'dateFrom',
                    openapi.IN_QUERY,
                    description='Start date of the event (YYYY-MM-DD)',
                    type=openapi.TYPE_STRING
                ),
                openapi.Parameter(
                    'dateTo',
                    openapi.IN_QUERY,
                    description='End date of the event (YYYY-MM-DD)',
                    type=openapi.TYPE_STRING
                ),
                openapi.Parameter(
                    'place',
                    openapi.IN_QUERY,
                    description='Event location (select from available regions)',
                    type=openapi.TYPE_STRING,
                    enum=[code for code, name in REGIONS]
                ),
                openapi.Parameter(
                    'distance_min', openapi.IN_QUERY, description='Minimum distance (km)', type=openapi.TYPE_NUMBER
                ),
                openapi.Parameter(
                    'distance_max', openapi.IN_QUERY, description='Maximum distance (km)', type=openapi.TYPE_NUMBER
                ),
            ],
            'responses': {
                200: openapi.Response(
                    description='List of events with count and pagination',
                    schema=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'pagination': openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'next_page': openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        description='URL for the next page of results',
                                        nullable=True
                                    ),
                                    'current_page': openapi.Schema(
                                        type=openapi.TYPE_INTEGER, description='Current page number'
                                    ),
                                    'previous_page': openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        description='URL for the previous page of results',
                                        nullable=True
                                    ),
                                    'num_pages': openapi.Schema(
                                        type=openapi.TYPE_INTEGER, description='Total number of pages'
                                    ),
                                },
                                required=['current_page', 'num_pages'],
                            ),
                            'items_count': openapi.Schema(
                                type=openapi.TYPE_INTEGER, description='Total number of events matching the filters'
                            ),
                            'items': openapi.Schema(
                                type=openapi.TYPE_ARRAY,
                                items=openapi.Items(  # noqa
                                    type=openapi.TYPE_OBJECT,
                                    properties={
                                        'name': openapi.Schema(type=openapi.TYPE_STRING),
                                        'competitionType': openapi.Schema(
                                            type=openapi.TYPE_ARRAY,
                                            items=openapi.Items(type=openapi.TYPE_STRING),  # noqa
                                        ),
                                        'dateFrom': openapi.Schema(type=openapi.TYPE_STRING),
                                        'dateTo': openapi.Schema(type=openapi.TYPE_STRING),
                                        'placeRegion': openapi.Schema(type=openapi.TYPE_STRING),
                                        'place': openapi.Schema(type=openapi.TYPE_STRING),
                                        'photos': openapi.Schema(type=openapi.TYPE_OBJECT, nullable=True),
                                        'distances': openapi.Schema(
                                            type=openapi.TYPE_ARRAY,
                                            items=openapi.Items(  # noqa
                                                type=openapi.TYPE_OBJECT,
                                                properties={
                                                    'name': openapi.Schema(type=openapi.TYPE_STRING),
                                                },
                                                required=['name'],
                                            ),
                                        ),
                                    },
                                    required=[
                                        'name',
                                        'competitionType',
                                        'dateFrom',
                                        'dateTo',
                                        'placeRegion',
                                        'place',
                                        'distances'
                                    ],
                                ),
                            ),
                        },
                        required=['pagination', 'items_count', 'items'],
                    )
                ),
                400: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='Invalid filter parameters. Possible errors include invalid date format, '
                                        'region, or distance range. For example, distance_min must be less than or '
                                        'equal to distance_max.'
                        )
                    },
                    required=['error'],
                ),
                500: openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='Internal server error while processing the request.'
                        )
                    },
                    required=['error'],
                ),
            }
        }
