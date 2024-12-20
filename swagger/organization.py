from drf_yasg import openapi

from organization.serializers import OrganizationSerializer  # noqa


class SwaggerDocs:

    class Organization:
        get = {
            'tags': ['Organization'],
            'responses': {
                200: openapi.Response('Success', OrganizationSerializer),
                404: 'Organizer not found',
            },
            'operation_description': 'Retrieve the details of an event organizer by event_id. The event_id is used to find the organizer associated with a specific event.',  # noqa: E501
        }

        post = {
            'tags': ['Organization'],
            'request_body': OrganizationSerializer,
            'responses': {
                200: openapi.Response('Updated organizer', OrganizationSerializer),
                404: 'Organizer not found',
            },
            'operation_description': 'Update the details of an event organizer by event_id. The event_id is used to find the organizer, and the request body contains the updated information about the organizer.',  # noqa: E501
        }

        put = {
            'tags': ['Organization'],
            'request_body': OrganizationSerializer,
            'responses': {
                200: openapi.Response('Updated organizer', OrganizationSerializer),
                404: 'Organizer not found',
            },
            'operation_description': 'Update the details of an event organizer by event_id. The event_id is used to find the organizer, and the request body contains the updated information about the organizer.',  # noqa: E501
        }

        patch = {
            'tags': ['Organization'],
            'request_body': OrganizationSerializer,
            'responses': {
                200: openapi.Response(
                    'Partially updated organizer', OrganizationSerializer
                ),
                404: 'Organizer not found',
            },
            'operation_description': 'Partially update an event organizer by event_id. Only the fields provided in the request body will be updated.',  # noqa: E501
        }

        delete = {
            'tags': ['Organization'],
            'responses': {
                204: 'Organizer deleted successfully',
                404: 'Organizer not found',
            },
            'operation_description': 'Delete an event organizer by event_id. The event_id is used to find and delete the organizer associated with a specific event.',  # noqa: E501
        }
