from drf_yasg import openapi

from event.distance_details.serializers import DistanceEventSerializer


class SwaggerDocs:

    class Distances:
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
