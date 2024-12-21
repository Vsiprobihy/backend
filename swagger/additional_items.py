from drf_yasg import openapi

from event.additional_items.serializers import AdditionalItemEventSerializer


class SwaggerDocs:

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
            'request_body': openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'itemType': openapi.Schema(type=openapi.TYPE_STRING),
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
                        'itemType': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='Item type, choices: "transfer", "medal", "t_shirt"',
                        ),
                        'price': openapi.Schema(
                            type=openapi.TYPE_NUMBER, description='Item price'
                        ),
                        'isFree': openapi.Schema(
                            type=openapi.TYPE_BOOLEAN, description='Is the item free'
                        ),
                    },
                    required=['id', 'itemType', 'price', 'isFree'],
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
                    'itemType': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description='Type of the item, choices: "transfer", "medal", "t_shirt"',
                    ),
                    'price': openapi.Schema(
                        type=openapi.TYPE_NUMBER, description='Price of the item'
                    ),
                    'isFree': openapi.Schema(
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
