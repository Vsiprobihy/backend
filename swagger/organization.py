from swagger.organization_variables import Request, Response


class SwaggerDocs:

    class Organization:
        get_list = {
            'tags': ['Organization'],
            'responses': {
                200: Response.OrganizationsListResponse,
                404: 'Organizer not found',
            },
            'operation_description': 'Retrieve the details of an event organizer by event_id. The event_id is used to find the organizer associated with a specific event.',  # noqa: E501
        }

        get = {
            'tags': ['Organization'],
            'responses': {
                200: Response.OrganizationResponse,
                404: 'Organizer not found',
            },
            'operation_description': 'Retrieve the details of an event organizer by event_id. The event_id is used to find the organizer associated with a specific event.',  # noqa: E501
        }

        post = {
            'tags': ['Organization'],
            'request_body': Request.OrganizationRequestBody,
            'responses': {
                201: Response.OrganizationResponse,
                404: 'Organizer not found',
            },
            'operation_description': 'Update the details of an event organizer by event_id. The event_id is used to find the organizer, and the request body contains the updated information about the organizer.',  # noqa: E501
        }

        put = {
            'tags': ['Organization'],
            'request_body': Request.OrganizationRequestBody,
            'responses': {
                200: Response.OrganizationResponse,
                404: 'Organizer not found',
            },
            'operation_description': 'Update the details of an event organizer by event_id. The event_id is used to find the organizer, and the request body contains the updated information about the organizer.',  # noqa: E501
        }

        patch = {
            'tags': ['Organization'],
            'request_body': Request.OrganizationRequestBody,
            'responses': {
                200: Response.OrganizationResponse,
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
