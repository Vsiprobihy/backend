from drf_yasg import openapi

from event.serializers.additional_items import AdditionalItemEventSerializer
from event.serializers.distance_detail import DistanceEventSerializer
from event.serializers.events import EventSerializer
from event.serializers.organizer_detail import OrganizerEventSerializer


class SwaggerDocs:

    class Event:
        get = {
            'tags': ['Events'],
            'responses': {
                200: openapi.Response('Success', EventSerializer),
                404: 'Event not found',
            },
            'operation_description': 'Retrieve event details by ID.',
        }
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
                    'date_from': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE, description='Event start date', default='2024-10-28'),  # noqa: E501, F601
                    'date_to': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE, description='Event end date', default='2024-10-28'),  # noqa: E501, F601
                    'place': openapi.Schema(type=openapi.TYPE_STRING, description='Location of the event', default='Lviv'),  # noqa: E501, F601
                    'place_region': openapi.Schema(type=openapi.TYPE_STRING, description='Location of the event', default='lviv_region'),  # noqa: E501, F601
                    'description': openapi.Schema(type=openapi.TYPE_STRING, description='Event description', default='Embrace the winter spirit with our Winter Wonderland Run!'),  # noqa: E501, F601
                    'registration_link': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_URI, description='Registration link', default='http://site.com/registration/winter-wonderland-run-2024'),  # noqa: E501, F601
                    'hide_participants': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Whether to hide participants', default=True),  # noqa: E501, F601
                    'organizer_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the organizer', default=1),  # noqa: E501, F601
                    'distances': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'name': openapi.Schema(type=openapi.TYPE_STRING, description='Name of the distance', default='5km Snow Run'),  # noqa: E501
                                'competition_type': openapi.Schema(type=openapi.TYPE_STRING, description='Type of competition', default='running'),  # noqa: E501
                                'category': openapi.Schema(type=openapi.TYPE_STRING, description='Category of participants', default='adults'),  # noqa: E501
                                'length': openapi.Schema(type=openapi.TYPE_NUMBER, description='Length of the distance in km', default=5.0),  # noqa: E501
                                'start_number_from': openapi.Schema(type=openapi.TYPE_INTEGER, description='Starting number', default=1),  # noqa: E501
                                'start_number_to': openapi.Schema(type=openapi.TYPE_INTEGER, description='Ending number', default=300),  # noqa: E501
                                'show_start_number': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Show start number', default=True),  # noqa: E501
                                'show_name_on_number': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Show name on the number', default=True),  # noqa: E501
                                'age_from': openapi.Schema(type=openapi.TYPE_INTEGER, description='Minimum age', default=16),  # noqa: E501
                                'age_to': openapi.Schema(type=openapi.TYPE_INTEGER, description='Maximum age', default=60),  # noqa: E501
                                'cost': openapi.Schema(type=openapi.TYPE_NUMBER, description='Cost of the distance', default=55),  # noqa: E501
                                'is_free': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Is the distance free', default=False),  # noqa: E501
                                'promo_only_registration': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Promo-only registration', default=False),  # noqa: E501
                                'allow_registration': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Allow registration', default=True),  # noqa: E501
                                'additional_options': openapi.Schema(
                                    type=openapi.TYPE_ARRAY,
                                    items=openapi.Schema(
                                        type=openapi.TYPE_OBJECT,
                                        properties={
                                            'item_type': openapi.Schema(type=openapi.TYPE_STRING, description='Type of additional option', default='t_shirt'),  # noqa: E501
                                            'price': openapi.Schema(type=openapi.TYPE_NUMBER, description='Price of additional option', default=250),  # noqa: E501
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
            'operation_description': 'Create a new event with all related details including organizer, additional items, and distances.',  # noqa: E501
        }
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
            'operation_description': 'Partially update event details without organizer, additional_items, or distances fields.',  # noqa: E501
        }
        delete = {
            'tags': ['Events'],
            'responses': {
                204: 'Event deleted successfully',
                404: 'Event not found',
            },
            'operation_description': 'Delete an event by ID.',
        }

    class Organizer:
        get = {
            'tags': ['Organizers'],
            'responses': {
                200: openapi.Response('Success', OrganizerEventSerializer),
                404: 'Organizer not found',
            },
            'operation_description': 'Retrieve the details of an event organizer by event_id. The event_id is used to find the organizer associated with a specific event.',  # noqa: E501
        }

        put = {
            'tags': ['Organizers'],
            'request_body': OrganizerEventSerializer,
            'responses': {
                200: openapi.Response('Updated organizer', OrganizerEventSerializer),
                404: 'Organizer not found',
            },
            'operation_description': 'Update the details of an event organizer by event_id. The event_id is used to find the organizer, and the request body contains the updated information about the organizer.',  # noqa: E501
        }

        patch = {
            'tags': ['Organizers'],
            'request_body': OrganizerEventSerializer,
            'responses': {
                200: openapi.Response(
                    'Partially updated organizer', OrganizerEventSerializer
                ),
                404: 'Organizer not found',
            },
            'operation_description': 'Partially update an event organizer by event_id. Only the fields provided in the request body will be updated.',  # noqa: E501
        }

        delete = {
            'tags': ['Organizers'],
            'responses': {
                204: 'Organizer deleted successfully',
                404: 'Organizer not found',
            },
            'operation_description': 'Delete an event organizer by event_id. The event_id is used to find and delete the organizer associated with a specific event.',  # noqa: E501
        }

    class AdditionalItem:
        get = {
            'tags': ['Additional Items'],
            'responses': {
                200: openapi.Response('Success', AdditionalItemEventSerializer),
                404: 'Additional item not found',
            },
            'operation_description': 'Retrieve details of additional items for an event by ID.',
        }

        post = {
            'tags': ['Additional Items'],
            'manual_parameters': [
                openapi.Parameter(
                    'event_id',
                    openapi.IN_PATH,
                    description='Event ID',
                    type=openapi.TYPE_INTEGER,
                )
            ],
            'request_body': openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'item_type': openapi.Schema(type=openapi.TYPE_STRING),
                    'price': openapi.Schema(type=openapi.TYPE_NUMBER),
                },
            ),
            'responses': {
                201: openapi.Response(
                    'Additional item added successfully', AdditionalItemEventSerializer
                ),
                400: 'Bad request',
            },
            'operation_description': 'Add additional items (e.g., T-shirt, Medal) for an event.',
        }

        put = {
            'tags': ['Additional Items'],
            'request_body': openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Items(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(
                            type=openapi.TYPE_INTEGER,
                            description='ID of the additional item',
                        ),
                        'item_type': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='Item type, choices: "transfer", "medal", "t_shirt"',
                        ),
                        'price': openapi.Schema(
                            type=openapi.TYPE_NUMBER, description='Item price'
                        ),
                        'is_free': openapi.Schema(
                            type=openapi.TYPE_BOOLEAN, description='Is the item free'
                        ),
                    },
                    required=['id', 'item_type', 'price', 'is_free'],
                ),
            ),
            'responses': {
                200: openapi.Response(
                    'Updated additional items', AdditionalItemEventSerializer(many=True)
                ),
                404: 'Additional items not found',
            },
            'operation_description': 'Update additional items for an event by ID and Event_ID.',
        }

        patch = {
            'tags': ['Additional Items'],
            'request_body': openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'id': openapi.Schema(
                        type=openapi.TYPE_INTEGER,
                        description='ID of the additional item (required for update)',
                    ),
                    'item_type': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description='Type of the item, choices: "transfer", "medal", "t_shirt"',
                    ),
                    'price': openapi.Schema(
                        type=openapi.TYPE_NUMBER, description='Price of the item'
                    ),
                    'is_free': openapi.Schema(
                        type=openapi.TYPE_BOOLEAN, description='Is the item free or not'
                    ),
                },
                required=['id'],
            ),
            'responses': {
                200: openapi.Response(
                    'Successfully updated additional item',
                    AdditionalItemEventSerializer,
                ),
                404: 'Additional item not found',
            },
            'operation_description': 'Partial update of additional items for an event by ID.',
        }

        delete = {
            'tags': ['Additional Items'],
            'operation_description': """
            Delete multiple additional items associated with a specific event identified by the `event_id` in the URL.
            The `id` field is required to identify each additional item to be deleted.
            """,
            'request_body': openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(
                            type=openapi.TYPE_INTEGER,
                            description='ID of the additional item to delete',
                            example=1,
                        ),
                    },
                    required=['id'],
                ),
            ),
            'responses': {
                204: 'Additional items deleted successfully',
                400: openapi.Response(
                    description='Bad request due to missing or invalid IDs',
                    examples={
                        'application/json': {
                            'detail': "Each item must include an 'id' field."
                        }
                    },
                ),
                404: openapi.Response(
                    description='One or more additional items not found',
                    examples={
                        'application/json': {
                            'detail': 'Item with id X not found for this event.'
                        }
                    },
                ),
            },
        }

    class Distance:
        get = {
            'tags': ['Distances'],
            'operation_description': 'Retrieve a list of distances associated with a specific event identified by the event_id passed in the URL.',  # noqa: E501
            'responses': {
                200: openapi.Response(
                    description='A list of distances for the event',
                    schema=openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'id': openapi.Schema(
                                    type=openapi.TYPE_INTEGER,
                                    description='ID of the distance.',
                                ),
                                'name': openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                    description='Name of the distance.',
                                ),
                                'competition_type': openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                    description='Type of competition.',
                                ),
                                'category': openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                    description='Category of participants.',
                                ),
                                'length': openapi.Schema(
                                    type=openapi.TYPE_NUMBER,
                                    description='Distance length.',
                                ),
                                'start_number_from': openapi.Schema(
                                    type=openapi.TYPE_INTEGER,
                                    description='Start number.',
                                ),
                                'start_number_to': openapi.Schema(
                                    type=openapi.TYPE_INTEGER, description='End number.'
                                ),
                                'age_from': openapi.Schema(
                                    type=openapi.TYPE_INTEGER,
                                    description='Minimum age.',
                                ),
                                'age_to': openapi.Schema(
                                    type=openapi.TYPE_INTEGER,
                                    description='Maximum age.',
                                ),
                                'cost': openapi.Schema(
                                    type=openapi.TYPE_NUMBER,
                                    description='Participation cost.',
                                ),
                                'is_free': openapi.Schema(
                                    type=openapi.TYPE_BOOLEAN,
                                    description='Is event free.',
                                ),
                                'promo_only_registration': openapi.Schema(
                                    type=openapi.TYPE_BOOLEAN,
                                    description='Promo registration only.',
                                ),
                                'allow_registration': openapi.Schema(
                                    type=openapi.TYPE_BOOLEAN,
                                    description='Allow registration.',
                                ),
                                'show_name_on_number': openapi.Schema(
                                    type=openapi.TYPE_BOOLEAN,
                                    description='Show name on number.',
                                ),
                                'show_start_number': openapi.Schema(
                                    type=openapi.TYPE_BOOLEAN,
                                    description='Show start number.',
                                ),
                                'event': openapi.Schema(
                                    type=openapi.TYPE_INTEGER,
                                    description='ID of the event.',
                                ),
                            },
                        ),
                    ),
                ),
                404: openapi.Response(
                    description='No distances found for the specified event.',
                    examples={
                        'application/json': {
                            'detail': 'No distances found for this event.'
                        }
                    },
                ),
            },
        }

        post = {
            'tags': ['Distances'],
            'request_body': openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'name': openapi.Schema(
                        type=openapi.TYPE_STRING, description='Name of the distance.'
                    ),
                    'competition_type': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        enum=[
                            'running',
                            'trail',
                            'ultramarathon',
                            'cycling',
                            'online',
                            'walking',
                            'ocr',
                            'swimming',
                            'triathlon',
                        ],
                        description='Type of competition (e.g., running, cycling, etc.).',
                    ),
                    'category': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        enum=[
                            'adults',
                            'children',
                            'men',
                            'women',
                            'disabled',
                            'veterans',
                            'pupils',
                            'boys',
                            'juniors',
                            'students',
                            'teachers',
                        ],
                        description='Category of participants (e.g., adults, children, etc.).',
                    ),
                    'length': openapi.Schema(
                        type=openapi.TYPE_NUMBER,
                        format=openapi.FORMAT_DECIMAL,
                        description='Distance length (in km or meters).',
                    ),
                    'start_number_from': openapi.Schema(
                        type=openapi.TYPE_INTEGER, description='Starting number range.'
                    ),
                    'start_number_to': openapi.Schema(
                        type=openapi.TYPE_INTEGER, description='Ending number range.'
                    ),
                    'show_start_number': openapi.Schema(
                        type=openapi.TYPE_BOOLEAN,
                        description='Whether to show the start number.',
                    ),
                    'show_name_on_number': openapi.Schema(
                        type=openapi.TYPE_BOOLEAN,
                        description='Whether to show the name on the number.',
                    ),
                    'age_from': openapi.Schema(
                        type=openapi.TYPE_INTEGER,
                        description='Minimum age of participants.',
                    ),
                    'age_to': openapi.Schema(
                        type=openapi.TYPE_INTEGER,
                        description='Maximum age of participants.',
                    ),
                    'cost': openapi.Schema(
                        type=openapi.TYPE_NUMBER,
                        format=openapi.FORMAT_DECIMAL,
                        description='Cost of participation.',
                    ),
                    'is_free': openapi.Schema(
                        type=openapi.TYPE_BOOLEAN,
                        description='Indicates if the event is free.',
                    ),
                    'promo_only_registration': openapi.Schema(
                        type=openapi.TYPE_BOOLEAN,
                        description='Restrict registration to promo users only.',
                    ),
                    'allow_registration': openapi.Schema(
                        type=openapi.TYPE_BOOLEAN,
                        description='Allow participants to register.',
                    ),
                },
                required=['name', 'is_free'],
            ),
            'responses': {
                201: openapi.Response(
                    'Distance created successfully', DistanceEventSerializer
                ),
                400: 'Bad request',
            },
            'operation_description': 'Create a new distance for an event. The event is identified by the event_id passed in the URL.',  # noqa: E501
        }

        put = {
            'tags': ['Distances'],
            'operation_description': """
            Update one or more distances for a specific event. The `event_id` is passed through the URL, and each distance
            should have a valid `id` to identify which distance is being updated. All fields will be fully replaced with the new data.
            """,  # noqa: E501
            'request_body': openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(
                            type=openapi.TYPE_INTEGER,
                            description='ID of the distance to update.',
                        ),
                        'name': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='Name of the distance.',
                        ),
                        'competition_type': openapi.Schema(
                            type=openapi.TYPE_STRING, description='Type of competition.'
                        ),
                        'category': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='Category of participants.',
                        ),
                        'allow_registration': openapi.Schema(
                            type=openapi.TYPE_BOOLEAN,
                            description='Allow participants to register.',
                        ),
                        'length': openapi.Schema(
                            type=openapi.TYPE_NUMBER, description='Distance length.'
                        ),
                        'start_number_from': openapi.Schema(
                            type=openapi.TYPE_INTEGER, description='Start number.'
                        ),
                        'start_number_to': openapi.Schema(
                            type=openapi.TYPE_INTEGER, description='End number.'
                        ),
                        'age_from': openapi.Schema(
                            type=openapi.TYPE_INTEGER, description='Minimum age.'
                        ),
                        'age_to': openapi.Schema(
                            type=openapi.TYPE_INTEGER, description='Maximum age.'
                        ),
                        'cost': openapi.Schema(
                            type=openapi.TYPE_NUMBER, description='Participation cost.'
                        ),
                        'is_free': openapi.Schema(
                            type=openapi.TYPE_BOOLEAN, description='Is event free.'
                        ),
                        'promo_only_registration': openapi.Schema(
                            type=openapi.TYPE_BOOLEAN,
                            description='Promo registration only.',
                        ),
                        'show_name_on_number': openapi.Schema(
                            type=openapi.TYPE_BOOLEAN,
                            description='Show name on number.',
                        ),
                        'show_start_number': openapi.Schema(
                            type=openapi.TYPE_BOOLEAN, description='Show start number.'
                        ),
                    },
                ),
            ),
            'responses': {
                200: openapi.Response(
                    description='Updated distances',
                    schema=openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'id': openapi.Schema(
                                    type=openapi.TYPE_INTEGER,
                                    description='ID of the created distance.',
                                ),
                                'name': openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                    description='Name of the distance.',
                                ),
                                'competition_type': openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                    description='Type of competition.',
                                ),
                                'category': openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                    description='Category of participants.',
                                ),
                                'length': openapi.Schema(
                                    type=openapi.TYPE_NUMBER,
                                    description='Distance length.',
                                ),
                                'start_number_from': openapi.Schema(
                                    type=openapi.TYPE_INTEGER,
                                    description='Start number.',
                                ),
                                'start_number_to': openapi.Schema(
                                    type=openapi.TYPE_INTEGER, description='End number.'
                                ),
                                'age_from': openapi.Schema(
                                    type=openapi.TYPE_INTEGER,
                                    description='Minimum age.',
                                ),
                                'age_to': openapi.Schema(
                                    type=openapi.TYPE_INTEGER,
                                    description='Maximum age.',
                                ),
                                'cost': openapi.Schema(
                                    type=openapi.TYPE_NUMBER,
                                    description='Participation cost.',
                                ),
                                'is_free': openapi.Schema(
                                    type=openapi.TYPE_BOOLEAN,
                                    description='Is event free.',
                                ),
                                'promo_only_registration': openapi.Schema(
                                    type=openapi.TYPE_BOOLEAN,
                                    description='Promo registration only.',
                                ),
                                'allow_registration': openapi.Schema(
                                    type=openapi.TYPE_BOOLEAN,
                                    description='Allow registration.',
                                ),
                                'show_name_on_number': openapi.Schema(
                                    type=openapi.TYPE_BOOLEAN,
                                    description='Show name on number.',
                                ),
                                'show_start_number': openapi.Schema(
                                    type=openapi.TYPE_BOOLEAN,
                                    description='Show start number.',
                                ),
                                'event': openapi.Schema(
                                    type=openapi.TYPE_INTEGER,
                                    description='ID of the event.',
                                ),
                            },
                        ),
                    ),
                ),
                400: openapi.Response(
                    description='Bad request due to validation errors',
                    examples={
                        'application/json': {
                            'detail': 'Expected a dictionary or a list of items.'
                        }
                    },
                ),
                404: openapi.Response(
                    description='Distance or event not found',
                    examples={
                        'application/json': {'detail': 'Distance with id X not found.'}
                    },
                ),
            },
        }

        patch = {
            'tags': ['Distances'],
            'operation_description': """
            Partially update one or more distances associated with a specific event identified by the `event_id` in the URL.
            You can update one or more fields of the distances. The `id` field is required to identify each distance to be updated.
            """,  # noqa: E501
            'request_body': openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(
                            type=openapi.TYPE_INTEGER,
                            description='ID of the distance to update.',
                        ),
                        'name': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='Name of the distance.',
                        ),
                        'competition_type': openapi.Schema(
                            type=openapi.TYPE_STRING, description='Type of competition.'
                        ),
                        'category': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='Category of participants.',
                        ),
                        'allow_registration': openapi.Schema(
                            type=openapi.TYPE_BOOLEAN,
                            description='Allow participants to register.',
                        ),
                        'length': openapi.Schema(
                            type=openapi.TYPE_NUMBER, description='Distance length.'
                        ),
                        'start_number_from': openapi.Schema(
                            type=openapi.TYPE_INTEGER, description='Start number.'
                        ),
                        'start_number_to': openapi.Schema(
                            type=openapi.TYPE_INTEGER, description='End number.'
                        ),
                        'age_from': openapi.Schema(
                            type=openapi.TYPE_INTEGER, description='Minimum age.'
                        ),
                        'age_to': openapi.Schema(
                            type=openapi.TYPE_INTEGER, description='Maximum age.'
                        ),
                        'cost': openapi.Schema(
                            type=openapi.TYPE_NUMBER, description='Participation cost.'
                        ),
                        'is_free': openapi.Schema(
                            type=openapi.TYPE_BOOLEAN, description='Is event free.'
                        ),
                        'promo_only_registration': openapi.Schema(
                            type=openapi.TYPE_BOOLEAN,
                            description='Promo registration only.',
                        ),
                        'show_name_on_number': openapi.Schema(
                            type=openapi.TYPE_BOOLEAN,
                            description='Show name on number.',
                        ),
                        'show_start_number': openapi.Schema(
                            type=openapi.TYPE_BOOLEAN, description='Show start number.'
                        ),
                    },
                ),
            ),
            'responses': {
                200: openapi.Response(
                    description='Partially updated distances',
                    schema=openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'id': openapi.Schema(
                                    type=openapi.TYPE_INTEGER,
                                    description='ID of the created distance.',
                                ),
                                'name': openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                    description='Name of the distance.',
                                ),
                                'competition_type': openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                    description='Type of competition.',
                                ),
                                'category': openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                    description='Category of participants.',
                                ),
                                'length': openapi.Schema(
                                    type=openapi.TYPE_NUMBER,
                                    description='Distance length.',
                                ),
                                'start_number_from': openapi.Schema(
                                    type=openapi.TYPE_INTEGER,
                                    description='Start number.',
                                ),
                                'start_number_to': openapi.Schema(
                                    type=openapi.TYPE_INTEGER, description='End number.'
                                ),
                                'age_from': openapi.Schema(
                                    type=openapi.TYPE_INTEGER,
                                    description='Minimum age.',
                                ),
                                'age_to': openapi.Schema(
                                    type=openapi.TYPE_INTEGER,
                                    description='Maximum age.',
                                ),
                                'cost': openapi.Schema(
                                    type=openapi.TYPE_NUMBER,
                                    description='Participation cost.',
                                ),
                                'is_free': openapi.Schema(
                                    type=openapi.TYPE_BOOLEAN,
                                    description='Is event free.',
                                ),
                                'promo_only_registration': openapi.Schema(
                                    type=openapi.TYPE_BOOLEAN,
                                    description='Promo registration only.',
                                ),
                                'allow_registration': openapi.Schema(
                                    type=openapi.TYPE_BOOLEAN,
                                    description='Allow registration.',
                                ),
                                'show_name_on_number': openapi.Schema(
                                    type=openapi.TYPE_BOOLEAN,
                                    description='Show name on number.',
                                ),
                                'show_start_number': openapi.Schema(
                                    type=openapi.TYPE_BOOLEAN,
                                    description='Show start number.',
                                ),
                                'event': openapi.Schema(
                                    type=openapi.TYPE_INTEGER,
                                    description='ID of the event.',
                                ),
                            },
                        ),
                    ),
                ),
                400: openapi.Response(
                    description='Bad request due to validation errors',
                    examples={
                        'application/json': {
                            'detail': 'Expected a dictionary or a list of items.'
                        }
                    },
                ),
                404: openapi.Response(
                    description='Distance or event not found',
                    examples={
                        'application/json': {'detail': 'Distance with id X not found.'}
                    },
                ),
            },
        }

        delete = {
            'tags': ['Distances'],
            'operation_description': """
            Delete multiple distances associated with a specific event identified by the `event_id` in the URL.
            The `id` field is required to identify each distance to be deleted.
            """,
            'request_body': openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(
                            type=openapi.TYPE_INTEGER,
                            description='ID of the distance to delete',
                            example=1,
                        ),
                    },
                    required=['id'],
                ),
            ),
            'responses': {
                204: 'Distances deleted successfully',
                400: openapi.Response(
                    description='Bad request due to missing or invalid IDs',
                    examples={'application/json': {'detail': 'ID is required.'}},
                ),
                404: openapi.Response(
                    description='One or more distances not found',
                    examples={
                        'application/json': {
                            'detail': 'One or more distances not found for this event.'
                        }
                    },
                ),
            },
        }
