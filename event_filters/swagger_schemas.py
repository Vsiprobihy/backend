from drf_yasg import openapi
from event.serializers.events import EventSerializer
from event.constants.constants_event import REGIONS, COMPETITION_TYPES

class SwaggerDocs:

    class EventFilter:

        get = {
            'operation_description': "Filtering events by competition type, name, month, year, location, and distance",
            'manual_parameters': [
                openapi.Parameter('page', openapi.IN_QUERY, description="Type number of page (Pagination)", type=openapi.TYPE_STRING),
                openapi.Parameter(
                    'competition_type',
                    openapi.IN_QUERY,
                    description="Type of competition (running, trail, cycling)",
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(type=openapi.TYPE_STRING, enum=[competition for competition, name in COMPETITION_TYPES]),
                    collectionFormat='multi'
                ),
                openapi.Parameter('name', openapi.IN_QUERY, description="Event name", type=openapi.TYPE_STRING),
                openapi.Parameter('month', openapi.IN_QUERY, description="Event month (1-12)", type=openapi.TYPE_INTEGER),
                openapi.Parameter('year', openapi.IN_QUERY, description="Event year", type=openapi.TYPE_INTEGER),
                openapi.Parameter(
                    'place',
                    openapi.IN_QUERY,
                    description="Event location (select from available regions)",
                    type=openapi.TYPE_STRING,
                    enum=[code for code, name in REGIONS]
                ),
                openapi.Parameter('distance_min', openapi.IN_QUERY, description="Minimum distance (km)", type=openapi.TYPE_NUMBER),
                openapi.Parameter('distance_max', openapi.IN_QUERY, description="Maximum distance (km)", type=openapi.TYPE_NUMBER),
            ],
            'responses': {
                200: EventSerializer(many=True),
                400: 'Invalid distance range',
            }
        }
