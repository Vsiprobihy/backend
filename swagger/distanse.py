from drf_yasg import openapi

from event.distance_details.serializers import FavoriteDistanceSerializer


class SwaggerDocs:

    class MyDistanceListView:
        get = {
            'tags': ['My Distance List'],
            'operation_description': 'My Distance List',  # noqa: E501
            'responses': {
                200: openapi.Response(
                    description='My list of distances',
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
                                'competitionType': openapi.Schema(
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
                                'startNumberFrom': openapi.Schema(
                                    type=openapi.TYPE_INTEGER,
                                    description='Start number.',
                                ),
                                'startNumberTo': openapi.Schema(
                                    type=openapi.TYPE_INTEGER, description='End number.'
                                ),
                                'ageFrom': openapi.Schema(
                                    type=openapi.TYPE_INTEGER,
                                    description='Minimum age.',
                                ),
                                'ageTo': openapi.Schema(
                                    type=openapi.TYPE_INTEGER,
                                    description='Maximum age.',
                                ),
                                'cost': openapi.Schema(
                                    type=openapi.TYPE_NUMBER,
                                    description='Participation cost.',
                                ),
                                'isFree': openapi.Schema(
                                    type=openapi.TYPE_BOOLEAN,
                                    description='Is event free.',
                                ),
                                'promoOnlyRegistration': openapi.Schema(
                                    type=openapi.TYPE_BOOLEAN,
                                    description='Promo registration only.',
                                ),
                                'allowRegistration': openapi.Schema(
                                    type=openapi.TYPE_BOOLEAN,
                                    description='Allow registration.',
                                ),
                                'showNameOnNumber': openapi.Schema(
                                    type=openapi.TYPE_BOOLEAN,
                                    description='Show name on number.',
                                ),
                                'showStartNumber': openapi.Schema(
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
            },
        }

    class FavoriteDistanceListView:
        get = {
            'tags': ['Favorite Distance List'],
            'operation_description': 'Favorite Distance List',  # noqa: E501
            'responses': {
                200: openapi.Response(
                    description='Favorite list of distances',
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
                                'competitionType': openapi.Schema(
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
                                'startNumberFrom': openapi.Schema(
                                    type=openapi.TYPE_INTEGER,
                                    description='Start number.',
                                ),
                                'startNumberTo': openapi.Schema(
                                    type=openapi.TYPE_INTEGER, description='End number.'
                                ),
                                'ageFrom': openapi.Schema(
                                    type=openapi.TYPE_INTEGER,
                                    description='Minimum age.',
                                ),
                                'ageTo': openapi.Schema(
                                    type=openapi.TYPE_INTEGER,
                                    description='Maximum age.',
                                ),
                                'cost': openapi.Schema(
                                    type=openapi.TYPE_NUMBER,
                                    description='Participation cost.',
                                ),
                                'isFree': openapi.Schema(
                                    type=openapi.TYPE_BOOLEAN,
                                    description='Is event free.',
                                ),
                                'promoOnlyRegistration': openapi.Schema(
                                    type=openapi.TYPE_BOOLEAN,
                                    description='Promo registration only.',
                                ),
                                'allowRegistration': openapi.Schema(
                                    type=openapi.TYPE_BOOLEAN,
                                    description='Allow registration.',
                                ),
                                'showNameOnNumber': openapi.Schema(
                                    type=openapi.TYPE_BOOLEAN,
                                    description='Show name on number.',
                                ),
                                'showStartNumber': openapi.Schema(
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
            },
        }

    class FavoriteDistanceDetailView:
        post = {
            'tags': ['Favorite Distance Detail'],
            'operation_description': 'Create a new Favorite Distance',  # noqa: E501
            'responses': {
                201: openapi.Response(
                    'Favorite Distance added successfully.', FavoriteDistanceSerializer
                ),
                400: 'Distance is already in favorites.',
                404: 'Distance not found.',
            },
        }

        delete = {
            'tags': ['Favorite Distance Detail'],
            'operation_description': 'Delete a Favorite Distance',  # noqa: E501
            'responses': {
                204: openapi.Response(description=''),
                400: 'Distance ID is required.',
                404: 'Favorite distance not found.',
            },
        }
