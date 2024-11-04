from drf_yasg import openapi

class SwaggerDocs:

    class MainPage:

        event_schema = openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Event ID'),
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='Event name'),
                'date_from': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, description='Event start date'),
                'date_to': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, description='Event end date (optional)'),
                'place': openapi.Schema(type=openapi.TYPE_STRING, description='Event place'),
                'competition_type': openapi.Schema(type=openapi.TYPE_STRING, description='Type of competition'),
                'photos': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_URI, description='URL of event photo (optional)'),
                'distances': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'name': openapi.Schema(type=openapi.TYPE_STRING, description='Distance name'),
                            'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Distance ID'),
                        }
                    ),
                    description='List of event distances'
                ),
            },
            required=['id', 'name', 'date_from', 'date_to', 'place', 'competition_type', 'distances']
        )

        mainpage_response_schema = openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'events': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=event_schema,
                    description='List of upcoming events'
                )
            },
            required=['events']
        )

        get = {
            'operation_description': "Get upcoming events for the main page",
            'responses': {
                200: mainpage_response_schema,
                400: 'Invalid parameters',
            },
            'manual_parameters': [
                openapi.Parameter(
                    name='count',
                    in_=openapi.IN_QUERY,
                    type=openapi.TYPE_INTEGER,
                    required=False,
                    description='Number of upcoming events to return (default is 3)',
                )
            ]
        }
