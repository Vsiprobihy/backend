from drf_yasg import openapi
from authentication.serializers import RegisterSerializer, UserProfileSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from event.serializers.additional_items import AdditionalItemEventSerializer
from event.serializers.distance_detail import DistanceEventSerializer
from event.serializers.event_registrations import EventRegistrationSerializer, EventRegistrationDetailSerializer
from event.serializers.events import EventSerializer
from event.serializers.organizer_detail import OrganizerEventSerializer


class SwaggerDocs:
    class Register:
        post = {
            'request_body': RegisterSerializer,
            'responses': {
                201: openapi.Response(
                    description='User registered successfully',
                    schema=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'access': openapi.Schema(
                                type=openapi.TYPE_STRING,
                                description='Access token for authentication',
                                example='your_access_token_here'
                            ),
                            'refresh': openapi.Schema(
                                type=openapi.TYPE_STRING,
                                description='Refresh token for obtaining a new access token',
                                example='your_refresh_token_here'
                            ),
                        },
                    )
                ),
                400: openapi.Response(
                    description='Bad request',
                    schema=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'email': openapi.Schema(
                                type=openapi.TYPE_ARRAY,
                                items=openapi.Items(type=openapi.TYPE_STRING),
                                description="Error messages related to the email field",
                                example=["This field is required."]
                            ),
                            'password': openapi.Schema(
                                type=openapi.TYPE_ARRAY,
                                items=openapi.Items(type=openapi.TYPE_STRING),
                                description="Error messages related to the password field",
                                example=["This field is required."]
                            ),
                            'password2': openapi.Schema(
                                type=openapi.TYPE_ARRAY,
                                items=openapi.Items(type=openapi.TYPE_STRING),
                                description="Error messages related to the password confirmation field",
                                example=["Passwords must match."]
                            ),
                        },
                        required=['email', 'password', 'password2']
                    )
                ),
            },
            'operation_description': "User Registration Endpoint.",
        }

    class Profile:
        get = {
            'responses': {200: UserProfileSerializer},
            'operation_description': "Get user profile data",
        }
        put = {
            'request_body': UserProfileSerializer,
            'responses': {200: UserProfileSerializer},
            'operation_description': "Update user profile data",
        }

        patch = {
            'request_body': UserProfileSerializer,
            'responses': {200: UserProfileSerializer},
            'operation_description': "Partial update of user profile data",
        }

    class Token:
        post = {
            'request_body': TokenObtainPairSerializer,
            'responses': {
                200: openapi.Response('Token Response', TokenObtainPairSerializer),
            },
            'operation_description': "Login with JWT token",
        }

    class Event:
        get = {
            'tags': ['Events'],
            'responses': {
                200: openapi.Response('Success', EventSerializer),
                404: 'Event not found',
            },
            'operation_description': "Retrieve event details by ID.",
        }
        post = {
            'tags': ['Events'],
            'request_body': openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'name': openapi.Schema(type=openapi.TYPE_STRING, description='Name of the event', default='string'),
                    'competition_type': openapi.Schema(
                        type=openapi.TYPE_STRING, 
                        description='Type of competition', 
                        default='running'  # Дефолтное значение
                    ),
                    'date_from': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE, description='Event start date', default='2024-09-29'),
                    'date_to': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE, description='Event end date', default='2024-09-29'),
                    'place': openapi.Schema(type=openapi.TYPE_STRING, description='Location of the event', default='string'),
                    'description': openapi.Schema(type=openapi.TYPE_STRING, description='Event description', default='string'),
                    'registration_link': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_URI, description='Registration link', default='http://site.com/registation/'),
                    'hide_participants': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Whether to hide participants', default=True),
                    'organizer': openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'name': openapi.Schema(type=openapi.TYPE_STRING, description='Name of the organizer', default='string'),
                            'site_url': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_URI, description='Website of the organizer', default='http://site.com/'),
                            'phone_number': openapi.Schema(type=openapi.TYPE_STRING, description='Phone number of the organizer', default='1230001'),
                            'email': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL, description='Email of the organizer', default='user@example.com'),
                            'instagram_url': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_URI, description='Instagram link', default='http://instagramurl.com/'),
                            'facebook_url': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_URI, description='Facebook link', default='http://facebookurl.com/'),
                            'telegram_url': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_URI, description='Telegram link', default='http://telegramurl.com/'),
                        }
                    ),
                    'additional_items': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'item_type': openapi.Schema(type=openapi.TYPE_STRING, description='Type of additional item', default='transfer'),
                                'price': openapi.Schema(type=openapi.TYPE_STRING, description='Price of additional item', default='100'),
                            },
                        ),
                        description='List of additional items'
                    ),
                    'distances': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'name': openapi.Schema(type=openapi.TYPE_STRING, description='Name of the distance', default='10km'),
                                'cost': openapi.Schema(type=openapi.TYPE_STRING, description='Cost of the distance', default='200'),
                                'is_free': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Is the distance free', default=False),
                            }
                        ),
                        description='List of distances'
                    ),
                    'extended_description': openapi.Schema(type=openapi.TYPE_STRING, description='Extended description of the event', default='string'),
                },
                required=['name', 'competition_type', 'date_from', 'date_to', 'place', 'description', 'registration_link', 'hide_participants', 'organizer', 'additional_items', 'distances']
            ),
            'responses': {
                201: openapi.Response('Event created successfully', EventSerializer),
                400: 'Bad request',
            },
            'operation_description': "Create a new event with all related details including organizer, additional items, and distances.",
        }
        put = {
            'tags': ['Events'],
            'request_body': openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'name': openapi.Schema(type=openapi.TYPE_STRING, description='Name of the event'),
                    'competition_type': openapi.Schema(type=openapi.TYPE_STRING, description='Type of competition', default='running'),
                    'date_from': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE, description='Event start date'),
                    'date_to': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE, description='Event end date'),
                    'place': openapi.Schema(type=openapi.TYPE_STRING, description='Location of the event'),
                    'description': openapi.Schema(type=openapi.TYPE_STRING, description='Event description'),
                    'registration_link': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_URI, description='Registration link'),
                    'hide_participants': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Whether to hide participants'),
                    'extended_description': openapi.Schema(type=openapi.TYPE_STRING, description='Extended description of the event'),
                },
                required=['name', 'competition_type', 'date_from', 'date_to', 'place', 'description', 'registration_link', 'hide_participants']
            ),
            'responses': {
                200: openapi.Response('Success', EventSerializer),
                404: 'Event not found',
            },
            'operation_description': "Update event details without organizer, additional_items, or distances fields.",
        }
        patch = {
            'tags': ['Events'],
            'request_body': openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'name': openapi.Schema(type=openapi.TYPE_STRING, description='Name of the event'),
                    'competition_type': openapi.Schema(type=openapi.TYPE_STRING, description='Type of competition', default='running'),
                    'date_from': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE, description='Event start date'),
                    'date_to': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE, description='Event end date'),
                    'place': openapi.Schema(type=openapi.TYPE_STRING, description='Location of the event'),
                    'description': openapi.Schema(type=openapi.TYPE_STRING, description='Event description'),
                    'registration_link': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_URI, description='Registration link'),
                    'hide_participants': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Whether to hide participants'),
                    'extended_description': openapi.Schema(type=openapi.TYPE_STRING, description='Extended description of the event'),
                },
            ),
            'responses': {
                200: openapi.Response('Success', EventSerializer),
                404: 'Event not found',
            },
            'operation_description': "Partially update event details without organizer, additional_items, or distances fields.",
        }
        delete = {
            'tags': ['Events'],
            'responses': {
                204: 'Event deleted successfully',
                404: 'Event not found',
            },
            'operation_description': "Delete an event by ID.",
        }

    class EventRegistration:
        post = {
            'tags': ['Event Registration'],
            'request_body': openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'event': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID of the event to register for."),
                    'distances': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(type=openapi.TYPE_INTEGER),
                        description="List of distance IDs selected by the user. At least one distance is required."
                    ),
                    'additional_items': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(type=openapi.TYPE_INTEGER),
                        description="List of additional item IDs selected by the user, such as t-shirts or medals. This field is optional."
                    ),
                },
                required=['event', 'distances'],
                example={
                    "event": 1,
                    "distances": [1, 2],
                    "additional_items": [1, 2]
                }
            ),
            'responses': {
                201: openapi.Response(
                    'User successfully registered for the event',
                    EventRegistrationSerializer,
                    examples={
                        "application/json": {
                            "event": 1,
                            "distances": [1, 2],
                            "additional_items": [1, 2],
                            "registration_date": "2024-09-17T12:34:56.789Z",
                            "is_confirmed": False
                        }
                    }
                ),
                400: openapi.Response('Bad request. Either the event does not exist, the user is already registered, or invalid distances/additional items were provided.'),
                404: openapi.Response('Event not found. The event ID provided does not match any existing event.')
            },
            'operation_description': """
            Registers a user for an event. The user is authenticated via JWT, and the event is identified by its ID.
            The request body should include the event ID, a list of distance IDs the user wants to participate in, and optionally, additional item IDs.
            The response will include the event registration details, such as the event ID, selected distances, additional items, registration date, and confirmation status.
            """,
            'operation_id': 'registerUserForEvent',
        }

        get = {
            'tags': ['Event Registration'],
            'responses': {
                200: openapi.Response(
                    'Successfully retrieved event registration details',
                    EventRegistrationDetailSerializer,
                    examples={
                        "application/json": {
                            "user": {
                                "first_name": "John",
                                "last_name": "Doe",
                                "gender": "M",
                                "date_of_birth": "1990-01-01",
                                "t_shirt_size": "L",
                                "country": "USA",
                                "city": "New York",
                                "phone_number": "+123456789",
                                "sports_club": "NY Marathon Club",
                                "emergency_contact_name": "Jane Doe",
                                "emergency_contact_phone": "+987654321"
                            },
                            "event": 1,
                            "distances": [1, 2],
                            "additional_items": [1, 2],
                            "registration_date": "2024-09-17T12:34:56.789Z",
                            "is_confirmed": False
                        }
                    }
                ),
                404: openapi.Response('Event registration not found. The registration ID does not exist.'),
            },
            'operation_description': """
            Retrieves detailed information about a specific event registration, including user information, the selected event, distances, additional items, registration date, and whether the registration has been confirmed.
            """,
            'operation_id': 'getEventRegistration',
        }

        put = {
            'tags': ['Event Registration'],
            'request_body': openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'event': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID of the event to update registration for."),
                    'distances': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(type=openapi.TYPE_INTEGER),
                        description="List of updated distance IDs selected by the user."
                    ),
                    'additional_items': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(type=openapi.TYPE_INTEGER),
                        description="List of updated additional item IDs selected by the user."
                    ),
                },
                required=['event', 'distances'],
                example={
                    "event": 1,
                    "distances": [1, 2],
                    "additional_items": [1, 2]
                }
            ),
            'responses': {
                200: openapi.Response(
                    'Updated event registration successfully',
                    EventRegistrationDetailSerializer,
                    examples={
                        "application/json": {
                            "event": 1,
                            "distances": [1, 2],
                            "additional_items": [1, 2],
                            "registration_date": "2024-09-17T12:34:56.789Z",
                            "is_confirmed": False
                        }
                    }
                ),
                404: openapi.Response('Event registration not found. The registration ID does not exist.'),
            },
            'operation_description': """
            Updates the details of an existing event registration. You can change the distances the user is registered for, update additional items, or modify other registration details.
            The event itself cannot be changed; only distances and additional items can be updated.
            """,
            'operation_id': 'updateEventRegistration',
        }

        patch = {
            'tags': ['Event Registration'],
            'request_body': openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'distances': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(type=openapi.TYPE_INTEGER),
                        description="List of updated distance IDs selected by the user."
                    ),
                    'additional_items': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(type=openapi.TYPE_INTEGER),
                        description="List of updated additional item IDs selected by the user."
                    ),
                },
                example={
                    "distances": [5],
                    "additional_items": [1]
                }
            ),
            'responses': {
                200: openapi.Response(
                    'Partially updated event registration',
                    EventRegistrationDetailSerializer,
                    examples={
                        "application/json": {
                            "event": 1,
                            "distances": [1],
                            "additional_items": [1],
                            "registration_date": "2024-09-17T12:34:56.789Z",
                            "is_confirmed": False
                        }
                    }
                ),
                404: openapi.Response('Event registration not found. The registration ID does not exist.'),
            },
            'operation_description': """
            Partially updates an existing event registration. This can include modifying the distances or additional items associated with the registration.
            Only the fields provided in the request body will be updated.
            """,
            'operation_id': 'partialUpdateEventRegistration',
        }

        delete = {
            'tags': ['Event Registration'],
            'responses': {
                204: 'Event registration deleted successfully',
                404: 'Event registration not found',
            },
            'operation_description': """
            Deletes a specific event registration by its ID. This operation cannot be undone.
            """,
            'operation_id': 'deleteEventRegistration',
        }

    class Organizer:
        get = {
            'tags': ['Organizers'],
            'responses': {
                200: openapi.Response('Success', OrganizerEventSerializer),
                404: 'Organizer not found',
            },
            'operation_description': "Retrieve the details of an event organizer by event_id. The event_id is used to find the organizer associated with a specific event.",
        }

        put = {
            'tags': ['Organizers'],
            'request_body': OrganizerEventSerializer,
            'responses': {
                200: openapi.Response('Updated organizer', OrganizerEventSerializer),
                404: 'Organizer not found',
            },
            'operation_description': "Update the details of an event organizer by event_id. The event_id is used to find the organizer, and the request body contains the updated information about the organizer.",
        }

        patch = {
            'tags': ['Organizers'],
            'request_body': OrganizerEventSerializer,
            'responses': {
                200: openapi.Response('Partially updated organizer', OrganizerEventSerializer),
                404: 'Organizer not found',
            },
            'operation_description': "Partially update an event organizer by event_id. Only the fields provided in the request body will be updated.",
        }

        delete = {
            'tags': ['Organizers'],
            'responses': {
                204: 'Organizer deleted successfully',
                404: 'Organizer not found',
            },
            'operation_description': "Delete an event organizer by event_id. The event_id is used to find and delete the organizer associated with a specific event.",
        }

    class AdditionalItem:
        get = {
            'tags': ['Additional Items'],
            'responses': {
                200: openapi.Response('Success', AdditionalItemEventSerializer),
                404: 'Additional item not found',
            },
            'operation_description': "Retrieve details of additional items for an event by ID.",
        }

        post = {
            'tags': ['Additional Items'],
            'manual_parameters': [
                openapi.Parameter('event_id', openapi.IN_PATH, description="Event ID", type=openapi.TYPE_INTEGER)
            ],
            'request_body': openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'item_type': openapi.Schema(type=openapi.TYPE_STRING),
                    'price': openapi.Schema(type=openapi.TYPE_NUMBER),
                }
            ),
            'responses': {
                201: openapi.Response('Additional item added successfully', AdditionalItemEventSerializer),
                400: 'Bad request',
            },
            'operation_description': "Add additional items (e.g., T-shirt, Medal) for an event.",
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
                            description='ID of the additional item'
                        ),
                        'item_type': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='Item type, choices: "transfer", "medal", "t_shirt"'
                        ),
                        'price': openapi.Schema(
                            type=openapi.TYPE_NUMBER,
                            description='Item price'
                        ),
                        'is_free': openapi.Schema(
                            type=openapi.TYPE_BOOLEAN,
                            description='Is the item free'
                        ),
                    },
                    required=['id', 'item_type', 'price', 'is_free'],
                ),
            ),
            'responses': {
                200: openapi.Response('Updated additional items', AdditionalItemEventSerializer(many=True)),
                404: 'Additional items not found',
            },
            'operation_description': "Update additional items for an event by ID and Event_ID.",
        }

        patch = {
            'tags': ['Additional Items'],
            'request_body': openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'id': openapi.Schema(
                        type=openapi.TYPE_INTEGER,
                        description='ID of the additional item (required for update)'
                    ),
                    'item_type': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description='Type of the item, choices: "transfer", "medal", "t_shirt"'
                    ),
                    'price': openapi.Schema(
                        type=openapi.TYPE_NUMBER,
                        description='Price of the item'
                    ),
                    'is_free': openapi.Schema(
                        type=openapi.TYPE_BOOLEAN,
                        description='Is the item free or not'
                    ),
                },
                required=['id'],
            ),
            'responses': {
                200: openapi.Response('Successfully updated additional item', AdditionalItemEventSerializer),
                404: 'Additional item not found',
            },
            'operation_description': "Partial update of additional items for an event by ID.",
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
                            example=1
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
                        "application/json": {
                            "detail": "Each item must include an 'id' field."
                        }
                    }
                ),
                404: openapi.Response(
                    description='One or more additional items not found',
                    examples={
                        "application/json": {
                            "detail": "Item with id X not found for this event."
                        }
                    }
                ),
            },
        }


    class Distance:
        get = {
            'tags': ['Distances'],
            'operation_description': "Retrieve a list of distances associated with a specific event identified by the event_id passed in the URL.",
            'responses': {
                200: openapi.Response(
                    description='A list of distances for the event',
                    schema=openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'id': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID of the distance."),
                                'name': openapi.Schema(type=openapi.TYPE_STRING, description="Name of the distance."),
                                'competition_type': openapi.Schema(type=openapi.TYPE_STRING, description="Type of competition."),
                                'category': openapi.Schema(type=openapi.TYPE_STRING, description="Category of participants."),
                                'length': openapi.Schema(type=openapi.TYPE_NUMBER, description="Distance length."),
                                'start_number_from': openapi.Schema(type=openapi.TYPE_INTEGER, description="Start number."),
                                'start_number_to': openapi.Schema(type=openapi.TYPE_INTEGER, description="End number."),
                                'age_from': openapi.Schema(type=openapi.TYPE_INTEGER, description="Minimum age."),
                                'age_to': openapi.Schema(type=openapi.TYPE_INTEGER, description="Maximum age."),
                                'cost': openapi.Schema(type=openapi.TYPE_NUMBER, description="Participation cost."),
                                'is_free': openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Is event free."),
                                'promo_only_registration': openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Promo registration only."),
                                'allow_registration': openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Allow registration."),
                                'show_name_on_number': openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Show name on number."),
                                'show_start_number': openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Show start number."),
                                'event': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID of the event."),
                            },
                        ),
                    ),
                ),
                404: openapi.Response(
                    description='No distances found for the specified event.',
                    examples={
                        "application/json": {
                            "detail": "No distances found for this event."
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
                    'name': openapi.Schema(type=openapi.TYPE_STRING, description="Name of the distance."),
                    'competition_type': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        enum=['running', 'trail', 'ultramarathon', 'cycling', 'online', 'walking', 'ocr', 'swimming', 'triathlon'],
                        description="Type of competition (e.g., running, cycling, etc.)."
                    ),
                    'category': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        enum=['adults', 'children', 'men', 'women', 'disabled', 'veterans', 'pupils', 'boys', 'juniors', 'students', 'teachers'],
                        description="Category of participants (e.g., adults, children, etc.)."
                    ),
                    'length': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_DECIMAL, description="Distance length (in km or meters)."),
                    'start_number_from': openapi.Schema(type=openapi.TYPE_INTEGER, description="Starting number range."),
                    'start_number_to': openapi.Schema(type=openapi.TYPE_INTEGER, description="Ending number range."),
                    'show_start_number': openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Whether to show the start number."),
                    'show_name_on_number': openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Whether to show the name on the number."),
                    'age_from': openapi.Schema(type=openapi.TYPE_INTEGER, description="Minimum age of participants."),
                    'age_to': openapi.Schema(type=openapi.TYPE_INTEGER, description="Maximum age of participants."),
                    'cost': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_DECIMAL, description="Cost of participation."),
                    'is_free': openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Indicates if the event is free."),
                    'promo_only_registration': openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Restrict registration to promo users only."),
                    'allow_registration': openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Allow participants to register."),
                },
                required=['name', 'is_free'],
            ),
            'responses': {
                201: openapi.Response('Distance created successfully', DistanceEventSerializer),
                400: 'Bad request',
            },
            'operation_description': "Create a new distance for an event. The event is identified by the event_id passed in the URL.",
        }

        put = {
            'tags': ['Distances'],
            'operation_description': """
            Update one or more distances for a specific event. The `event_id` is passed through the URL, and each distance 
            should have a valid `id` to identify which distance is being updated. All fields will be fully replaced with the new data.
            """,
            'request_body': openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                    'id': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID of the distance to update."),
                    'name': openapi.Schema(type=openapi.TYPE_STRING, description="Name of the distance."),
                    'competition_type': openapi.Schema(type=openapi.TYPE_STRING, description="Type of competition."),
                    'category': openapi.Schema(type=openapi.TYPE_STRING, description="Category of participants."),
                    'allow_registration': openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Allow participants to register."),
                    'length': openapi.Schema(type=openapi.TYPE_NUMBER, description="Distance length."),
                    'start_number_from': openapi.Schema(type=openapi.TYPE_INTEGER, description="Start number."),
                    'start_number_to': openapi.Schema(type=openapi.TYPE_INTEGER, description="End number."),
                    'age_from': openapi.Schema(type=openapi.TYPE_INTEGER, description="Minimum age."),
                    'age_to': openapi.Schema(type=openapi.TYPE_INTEGER, description="Maximum age."),
                    'cost': openapi.Schema(type=openapi.TYPE_NUMBER, description="Participation cost."),
                    'is_free': openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Is event free."),
                    'promo_only_registration': openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Promo registration only."),
                    'show_name_on_number': openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Show name on number."),
                    'show_start_number': openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Show start number."),
                }),
            ),
            'responses': {
                200: openapi.Response(
                    description='Updated distances',
                    schema=openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'id': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID of the created distance."),
                                'name': openapi.Schema(type=openapi.TYPE_STRING, description="Name of the distance."),
                                'competition_type': openapi.Schema(type=openapi.TYPE_STRING, description="Type of competition."),
                                'category': openapi.Schema(type=openapi.TYPE_STRING, description="Category of participants."),
                                'length': openapi.Schema(type=openapi.TYPE_NUMBER, description="Distance length."),
                                'start_number_from': openapi.Schema(type=openapi.TYPE_INTEGER, description="Start number."),
                                'start_number_to': openapi.Schema(type=openapi.TYPE_INTEGER, description="End number."),
                                'age_from': openapi.Schema(type=openapi.TYPE_INTEGER, description="Minimum age."),
                                'age_to': openapi.Schema(type=openapi.TYPE_INTEGER, description="Maximum age."),
                                'cost': openapi.Schema(type=openapi.TYPE_NUMBER, description="Participation cost."),
                                'is_free': openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Is event free."),
                                'promo_only_registration': openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Promo registration only."),
                                'allow_registration': openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Allow registration."),
                                'show_name_on_number': openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Show name on number."),
                                'show_start_number': openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Show start number."),
                                'event': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID of the event."),
                            },
                        ),
                    ),
                ),
                400: openapi.Response(
                    description='Bad request due to validation errors',
                    examples={
                        "application/json": {
                            "detail": "Expected a dictionary or a list of items."
                        }
                    },
                ),
                404: openapi.Response(
                    description='Distance or event not found',
                    examples={
                        "application/json": {
                            "detail": "Distance with id X not found."
                        }
                    },
                ),
            },
        }

        patch = {
            'tags': ['Distances'],
            'operation_description': """
            Partially update one or more distances associated with a specific event identified by the `event_id` in the URL. 
            You can update one or more fields of the distances. The `id` field is required to identify each distance to be updated.
            """,
            'request_body': openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                    'id': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID of the distance to update."),
                    'name': openapi.Schema(type=openapi.TYPE_STRING, description="Name of the distance."),
                    'competition_type': openapi.Schema(type=openapi.TYPE_STRING, description="Type of competition."),
                    'category': openapi.Schema(type=openapi.TYPE_STRING, description="Category of participants."),
                    'allow_registration': openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Allow participants to register."),
                    'length': openapi.Schema(type=openapi.TYPE_NUMBER, description="Distance length."),
                    'start_number_from': openapi.Schema(type=openapi.TYPE_INTEGER, description="Start number."),
                    'start_number_to': openapi.Schema(type=openapi.TYPE_INTEGER, description="End number."),
                    'age_from': openapi.Schema(type=openapi.TYPE_INTEGER, description="Minimum age."),
                    'age_to': openapi.Schema(type=openapi.TYPE_INTEGER, description="Maximum age."),
                    'cost': openapi.Schema(type=openapi.TYPE_NUMBER, description="Participation cost."),
                    'is_free': openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Is event free."),
                    'promo_only_registration': openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Promo registration only."),
                    'show_name_on_number': openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Show name on number."),
                    'show_start_number': openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Show start number."),
                }),
            ),
            'responses': {
                200: openapi.Response(
                    description='Partially updated distances',
                    schema=openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'id': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID of the created distance."),
                                'name': openapi.Schema(type=openapi.TYPE_STRING, description="Name of the distance."),
                                'competition_type': openapi.Schema(type=openapi.TYPE_STRING, description="Type of competition."),
                                'category': openapi.Schema(type=openapi.TYPE_STRING, description="Category of participants."),
                                'length': openapi.Schema(type=openapi.TYPE_NUMBER, description="Distance length."),
                                'start_number_from': openapi.Schema(type=openapi.TYPE_INTEGER, description="Start number."),
                                'start_number_to': openapi.Schema(type=openapi.TYPE_INTEGER, description="End number."),
                                'age_from': openapi.Schema(type=openapi.TYPE_INTEGER, description="Minimum age."),
                                'age_to': openapi.Schema(type=openapi.TYPE_INTEGER, description="Maximum age."),
                                'cost': openapi.Schema(type=openapi.TYPE_NUMBER, description="Participation cost."),
                                'is_free': openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Is event free."),
                                'promo_only_registration': openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Promo registration only."),
                                'allow_registration': openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Allow registration."),
                                'show_name_on_number': openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Show name on number."),
                                'show_start_number': openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Show start number."),
                                'event': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID of the event."),
                            },
                        ),
                    ),
                ),
                400: openapi.Response(
                    description='Bad request due to validation errors',
                    examples={
                        "application/json": {
                            "detail": "Expected a dictionary or a list of items."
                        }
                    },
                ),
                404: openapi.Response(
                    description='Distance or event not found',
                    examples={
                        "application/json": {
                            "detail": "Distance with id X not found."
                        }
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
                            example=1
                        ),
                    },
                    required=['id'],
                ),
            ),
            'responses': {
                204: 'Distances deleted successfully',
                400: openapi.Response(
                    description='Bad request due to missing or invalid IDs',
                    examples={
                        "application/json": {
                            "detail": "ID is required."
                        }
                    }
                ),
                404: openapi.Response(
                    description='One or more distances not found',
                    examples={
                        "application/json": {
                            "detail": "One or more distances not found for this event."
                        }
                    }
                ),
            },
        }

