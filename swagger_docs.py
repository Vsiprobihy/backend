from drf_yasg import openapi
from authentication.serializers import RegisterSerializer, UserProfileSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from event.serializers import EventSerializer, EventRegistrationSerializer, OrganizerEventSerializer, \
    AdditionalItemEventSerializer, DistanceEventSerializer


class SwaggerDocs:
    class Register:
        post = {
            'request_body': RegisterSerializer,
            'responses': {
                201: openapi.Response('User registered successfully'),
                400: 'Bad request'
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
            'request_body': EventSerializer,
            'responses': {
                201: openapi.Response('Event created successfully', EventSerializer),
                400: 'Bad request',
            },
            'operation_description': "Create a new event with associated organizer, additional items, and distances.",
        }
        put = {
            'tags': ['Events'],
            'request_body': EventSerializer,
            'responses': {
                200: openapi.Response('Success', EventSerializer),
                404: 'Event not found',
            },
            'operation_description': "Update event details by ID.",
        }
        patch = {
            'tags': ['Events'],
            'request_body': EventSerializer,
            'responses': {
                200: openapi.Response('Success', EventSerializer),
                404: 'Event not found',
            },
            'operation_description': "Partially update event details by ID.",
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
            'request_body': EventRegistrationSerializer,
            'responses': {
                201: openapi.Response('User registered for the event', EventRegistrationSerializer),
                400: 'Bad request',
                404: 'Event not found',
            },
            'operation_description': "Register a user for an event. The user is identified via JWT, and the event is identified by its ID.",
        }
        get = {
            'tags': ['Event Registration'],
            'responses': {
                200: openapi.Response('Success', EventRegistrationSerializer),
                404: 'Event registration not found',
            },
            'operation_description': "Retrieve details of a specific event registration by ID.",
        }
        put = {
            'tags': ['Event Registration'],
            'request_body': EventRegistrationSerializer,
            'responses': {
                200: openapi.Response('Updated event registration', EventRegistrationSerializer),
                404: 'Event registration not found',
            },
            'operation_description': "Update event registration details by ID.",
        }
        patch = {
            'tags': ['Event Registration'],
            'request_body': EventRegistrationSerializer,
            'responses': {
                200: openapi.Response('Partially updated event registration', EventRegistrationSerializer),
                404: 'Event registration not found',
            },
            'operation_description': "Partially update event registration details by ID.",
        }
        delete = {
            'tags': ['Event Registration'],
            'responses': {
                204: 'Event registration deleted successfully',
                404: 'Event registration not found',
            },
            'operation_description': "Delete an event registration by ID.",
        }

    class Organizer:
        get = {
            'tags': ['Organizers'],
            'responses': {
                200: openapi.Response('Success', OrganizerEventSerializer),
                404: 'Organizer not found',
            },
            'operation_description': "Retrieve the details of an event organizer by ID.",
        }
        post = {
            'tags': ['Organizers'],
            'request_body': OrganizerEventSerializer,
            'responses': {
                201: openapi.Response('Organizer created successfully', OrganizerEventSerializer),
                400: 'Bad request',
            },
            'operation_description': "Create a new organizer for an event.",
        }
        put = {
            'tags': ['Organizers'],
            'request_body': OrganizerEventSerializer,
            'responses': {
                200: openapi.Response('Updated organizer', OrganizerEventSerializer),
                404: 'Organizer not found',
            },
            'operation_description': "Update an event organizer by ID.",
        }
        patch = {
            'tags': ['Organizers'],
            'request_body': OrganizerEventSerializer,
            'responses': {
                200: openapi.Response('Partially updated organizer', OrganizerEventSerializer),
                404: 'Organizer not found',
            },
            'operation_description': "Partially update an event organizer by ID.",
        }
        delete = {
            'tags': ['Organizers'],
            'responses': {
                204: 'Organizer deleted successfully',
                404: 'Organizer not found',
            },
            'operation_description': "Delete an event organizer by ID.",
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
            'responses': {
                204: 'Additional item deleted successfully',
                404: 'Additional item not found',
            },
            'operation_description': "Delete additional items for an event by ID.",
        }

    class Distance:
        get = {
            'tags': ['Distances'],
            'responses': {
                200: openapi.Response('Success', DistanceEventSerializer),
                404: 'Distance not found',
            },
            'operation_description': "Retrieve details of event distances by ID.",
        }
        post = {
            'tags': ['Distances'],
            'request_body': openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'name': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description='Name of the distance (e.g., "5K Run")',
                    ),
                    'cost': openapi.Schema(
                        type=openapi.TYPE_NUMBER,
                        description='Cost of the distance in numeric format, leave null if free.',
                        example=100.00,
                    ),
                    'is_free': openapi.Schema(
                        type=openapi.TYPE_BOOLEAN,
                        description='Indicates whether the distance is free or not. If True, cost should be null.',
                        example=False,
                    ),
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
            'request_body': DistanceEventSerializer,
            'responses': {
                200: openapi.Response('Updated distance', DistanceEventSerializer),
                404: 'Distance not found',
            },
            'operation_description': "Update event distance by ID.",
        }
        patch = {
            'tags': ['Distances'],
            'request_body': DistanceEventSerializer,
            'responses': {
                200: openapi.Response('Partially updated distance', DistanceEventSerializer),
                404: 'Distance not found',
            },
            'operation_description': "Partially update event distance by ID.",
        }
        delete = {
            'tags': ['Distances'],
            'responses': {
                204: 'Distance deleted successfully',
                404: 'Distance not found',
            },
            'operation_description': "Delete event distance by ID.",
        }
