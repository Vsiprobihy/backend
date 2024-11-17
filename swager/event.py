from drf_yasg import openapi

from organizer_event.serializers import EventSerializer


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
            'request_body': openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'name': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description='Name of the event',
                        default='Winter Wonderland Run 2024',
                    ),
                    'competition_type': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'name': openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                    description='Type of competition',
                                    default='running',
                                )
                            },
                        ),
                        description='List of competition types',
                    ),
                    'date_from': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        format=openapi.FORMAT_DATE,
                        description='Event start date',
                        default='2024-10-28',
                    ),
                    'date_to': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        format=openapi.FORMAT_DATE,
                        description='Event end date',
                        default='2024-10-28',
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
                        type=openapi.TYPE_STRING,
                        description='Event description',
                        default='Embrace the winter spirit with our Winter Wonderland Run!',
                    ),
                    'registration_link': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        format=openapi.FORMAT_URI,
                        description='Registration link',
                        default='http://site.com/registration/winter-wonderland-run-2024',
                    ),
                    'hide_participants': openapi.Schema(
                        type=openapi.TYPE_BOOLEAN,
                        description='Whether to hide participants',
                        default=True,
                    ),
                    'organizer_id': openapi.Schema(
                        type=openapi.TYPE_INTEGER,
                        description='ID of the organizer',
                        default=1,
                    ),
                    'date_from': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE,
                                                description='Event start date', default='2024-10-28'),
                    # noqa: E501, F601
                    'date_to': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE,
                                              description='Event end date', default='2024-10-28'),  # noqa: E501, F601
                    'place': openapi.Schema(type=openapi.TYPE_STRING, description='Location of the event',
                                            default='Lviv'),  # noqa: E501, F601
                    'place_region': openapi.Schema(type=openapi.TYPE_STRING, description='Location of the event',
                                                   default='lviv_region'),  # noqa: E501, F601
                    'description': openapi.Schema(type=openapi.TYPE_STRING, description='Event description',
                                                  default='Embrace the winter spirit with our Winter Wonderland Run!'),
                    # noqa: E501, F601
                    'registration_link': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_URI,
                                                        description='Registration link',
                                                        default='http://site.com/registration/winter-wonderland-run-2024'),
                    # noqa: E501, F601
                    'hide_participants': openapi.Schema(type=openapi.TYPE_BOOLEAN,
                                                        description='Whether to hide participants', default=True),
                    # noqa: E501, F601
                    'organizer_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the organizer',
                                                   default=1),  # noqa: E501, F601
                    'distances': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'name': openapi.Schema(type=openapi.TYPE_STRING, description='Name of the distance',
                                                       default='5km Snow Run'),  # noqa: E501
                                'competition_type': openapi.Schema(type=openapi.TYPE_STRING,
                                                                   description='Type of competition',
                                                                   default='running'),  # noqa: E501
                                'category': openapi.Schema(type=openapi.TYPE_STRING,
                                                           description='Category of participants', default='adults'),
                                # noqa: E501
                                'length': openapi.Schema(type=openapi.TYPE_NUMBER,
                                                         description='Length of the distance in km', default=5.0),
                                # noqa: E501
                                'start_number_from': openapi.Schema(type=openapi.TYPE_INTEGER,
                                                                    description='Starting number', default=1),
                                # noqa: E501
                                'start_number_to': openapi.Schema(type=openapi.TYPE_INTEGER,
                                                                  description='Ending number', default=300),
                                # noqa: E501
                                'show_start_number': openapi.Schema(type=openapi.TYPE_BOOLEAN,
                                                                    description='Show start number', default=True),
                                # noqa: E501
                                'show_name_on_number': openapi.Schema(type=openapi.TYPE_BOOLEAN,
                                                                      description='Show name on the number',
                                                                      default=True),  # noqa: E501
                                'age_from': openapi.Schema(type=openapi.TYPE_INTEGER, description='Minimum age',
                                                           default=16),  # noqa: E501
                                'age_to': openapi.Schema(type=openapi.TYPE_INTEGER, description='Maximum age',
                                                         default=60),  # noqa: E501
                                'cost': openapi.Schema(type=openapi.TYPE_NUMBER, description='Cost of the distance',
                                                       default=55),  # noqa: E501
                                'is_free': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Is the distance free',
                                                          default=False),  # noqa: E501
                                'promo_only_registration': openapi.Schema(type=openapi.TYPE_BOOLEAN,
                                                                          description='Promo-only registration',
                                                                          default=False),  # noqa: E501
                                'allow_registration': openapi.Schema(type=openapi.TYPE_BOOLEAN,
                                                                     description='Allow registration', default=True),
                                # noqa: E501
                                'additional_options': openapi.Schema(
                                    type=openapi.TYPE_ARRAY,
                                    items=openapi.Schema(
                                        type=openapi.TYPE_OBJECT,
                                        properties={
                                            'item_type': openapi.Schema(type=openapi.TYPE_STRING,
                                                                        description='Type of additional option',
                                                                        default='t_shirt'),  # noqa: E501
                                            'price': openapi.Schema(type=openapi.TYPE_NUMBER,
                                                                    description='Price of additional option',
                                                                    default=250),  # noqa: E501
                                        }
                                    ),
                                    description='Additional options for the distance'
                                ),
                            }
                        ),
                        description='List of distances',
                    ),
                    'extended_description': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description='Extended description of the event',
                        default='Experience the beauty of winter while getting fit!',
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
                    'organizer_id',
                    'additional_items',
                    'distances',
                ],
            ),
            'responses': {
                201: openapi.Response('Event created successfully', EventSerializer),
                400: 'Bad request',
            },
            'operation_description': 'Create a new event with all related details including organizer, additional items, and distances.',
            # noqa: E501
        }

    class EventDetail:
        get = {
            'tags': ['Events'],
            'responses': {
                200: openapi.Response('Success', EventSerializer),
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
                200: openapi.Response('Success', EventSerializer),
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
                200: openapi.Response('Success', EventSerializer),
                404: 'Event not found',
            },
            'operation_description': 'Partially update event details without organizer, additional_items, or distances fields.',
            # noqa: E501
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
