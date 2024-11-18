from swagger.event_variables import Request, Responce


class SwaggerDocs:

    class EventList:
        get = {
            'tags': ['Events'],
            'responses': {
                200: Responce.EventResponse,
                404: 'Event not found',
            },
            'operation_description': 'Retrieve event details by ID.',
        }

    class EventCreate:
        post = {
            'tags': ['Events'],
            'request_body': Request.EventRequestBody,
            'responses': {
                201: Responce.EventResponse,
                400: 'Bad request',
            },
            'operation_description': 'Create a new event with all related details including organizer, additional items, and distances.',  # noqa: E501
        }

    class EventDetail:
        get = {
            'tags': ['Events'],
            'responses': {
                200: Responce.EventResponse,
                404: 'Event not found',
            },
            'operation_description': 'Retrieve event details by ID.',
        }

    class EventUpdate:
        put = {
            'tags': ['Events'],
            'request_body': Request.EventRequestBody,
            'responses': {
                200: Responce.EventResponse,
                404: 'Event not found',
            },
            'operation_description': 'Update event details without organizer, additional_items, or distances fields.',
        }

    class EventPartialUpdate:
        patch = {
            'tags': ['Events'],
            'request_body': Request.EventRequestBody,
            'responses': {
                200: Responce.EventResponse,
                404: 'Event not found',
            },
            'operation_description': 'Partially update event details without organizer, additional_items, or distances fields.',  # noqa: E501
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
