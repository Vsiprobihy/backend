from drf_yasg import openapi

from organizer_event.serializers import EventSerializer
from swagger.event_variables import Request, Responce


class SwaggerDocs:

    class EventList:
        get = {
            'tags': ['Events'],
            'responses': {
                200: openapi.Response('Success', EventSerializer),
                404: 'Event not found',
            },
            'operation_description': 'Retrieve event details by ID.',
        }

    class EventCreate:
        post = {
            'tags': ['Events'],
            'request_body': Request.EventRequestBody,
            'responses': {
                201: Responce.EventResponse,
                400: 'Bad request',
            },
            'operation_description': 'Create a new event with all related details including organizer, additional items, and distances.',  # noqa: E501
        }

    class EventDetail:
        get = {
            'tags': ['Events'],
            'responses': {
                200: Responce.EventResponse,
                404: 'Event not found',
            },
            'operation_description': 'Retrieve event details by ID.',
        }

    class EventUpdate:
        put = {
            'tags': ['Events'],
            'request_body': openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'name': openapi.Schema(
                        type=openapi.TYPE_STRING, description='Name of the event'
                    ),
                    'competition_type': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description='Type of competition',
                        default='running',
                    ),
                    'date_from': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        format=openapi.FORMAT_DATE,
                        description='Event start date',
                    ),
                    'date_to': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        format=openapi.FORMAT_DATE,
                        description='Event end date',
                    ),
                    'place': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description='Location of the event',
                        default='Lviv',
                    ),
                    'place_region': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description='Location of the event',
                        default='lviv_region',
                    ),
                    'description': openapi.Schema(
                        type=openapi.TYPE_STRING, description='Event description'
                    ),
                    'registration_link': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        format=openapi.FORMAT_URI,
                        description='Registration link',
                    ),
                    'hide_participants': openapi.Schema(
                        type=openapi.TYPE_BOOLEAN,
                        description='Whether to hide participants',
                    ),
                    'extended_description': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description='Extended description of the event',
                    ),
                },
                required=[
                    'name',
                    'competition_type',
                    'date_from',
                    'date_to',
                    'place',
                    'place_region',
                    'description',
                    'registration_link',
                    'hide_participants',
                ],
            ),
            'responses': {
                200: Responce.EventResponse,
                404: 'Event not found',
            },
            'operation_description': 'Update event details without organizer, additional_items, or distances fields.',
        }

    class EventPartialUpdate:
        patch = {
            'tags': ['Events'],
            'request_body': openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'name': openapi.Schema(
                        type=openapi.TYPE_STRING, description='Name of the event'
                    ),
                    'competition_type': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description='Type of competition',
                        default='running',
                    ),
                    'date_from': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        format=openapi.FORMAT_DATE,
                        description='Event start date',
                    ),
                    'date_to': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        format=openapi.FORMAT_DATE,
                        description='Event end date',
                    ),
                    'place': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description='Location of the event',
                        default='Lviv',
                    ),
                    'place_region': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description='Location of the event',
                        default='lviv_region',
                    ),
                    'description': openapi.Schema(
                        type=openapi.TYPE_STRING, description='Event description'
                    ),
                    'registration_link': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        format=openapi.FORMAT_URI,
                        description='Registration link',
                    ),
                    'hide_participants': openapi.Schema(
                        type=openapi.TYPE_BOOLEAN,
                        description='Whether to hide participants',
                    ),
                    'extended_description': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description='Extended description of the event',
                    ),
                },
            ),
            'responses': {
                200: Responce.EventResponse,
                404: 'Event not found',
            },
            'operation_description': 'Partially update event details without organizer, additional_items, or distances fields.',  # noqa: E501
        }

    class EventDelete:
        delete = {
            'tags': ['Events'],
            'responses': {
                204: 'Event deleted successfully',
                404: 'Event not found',
            },
            'operation_description': 'Delete an event by ID.',
        }
