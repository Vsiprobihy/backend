from functools import wraps

from django.core.exceptions import PermissionDenied

from event.distance_details.models import DistanceEvent
from event.models import Event
from organization.models import Organizer
from utils.custom_exceptions import BadRequestError, NotFoundError


def check_organization_access_decorator(event_extractor):
    """
    A decorator to check if the user has access to the organization associated with the event.

    :param event_extractor: A function that extracts the Event instance from the request and parameters.
    :raises PermissionDenied: If the user does not have access to the organization.
    :raises Http404: If the extracted Event does not exist.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(self, request, *args, **kwargs):
            try:
                event = event_extractor(request, *args, **kwargs)  # noqa: F841
            except Event.DoesNotExist:

                raise NotFoundError('Event not found.')

            user = request.user
            organization_id = kwargs.get('organization_id')

            organizer_access_exists = Organizer.objects.filter(
                user=user,
                organization_id=organization_id
            ).exists()

            if not organizer_access_exists:
                raise PermissionDenied('You do not have permission to access this event.')

            return view_func(self, request, *args, **kwargs)

        return _wrapped_view

    return decorator


def extract_event_from_distance(request, *args, **kwargs):
    """
    Extracts the Event instance associated with the given DistanceEvent.

    :param request: The HTTP request object.
    :raises DistanceEvent.DoesNotExist: If the DistanceEvent with the given ID does not exist.
    :return: The associated Event instance.
    """
    distance_id = kwargs.get('distance_id')
    distance = DistanceEvent.objects.select_related('event').get(pk=distance_id)
    return distance.event


def extract_event_directly(request, *args, **kwargs):
    """
    Extracts the Event instance directly using the event_id parameter.

    :param request: The HTTP request object.
    :raises Event.DoesNotExist: If the Event with the given ID does not exist.
    :return: The Event instance.
    """
    event_id = kwargs.get('event_id')
    return Event.objects.get(pk=event_id)


def extract_for_event_access_directly(request, *args, **kwargs):
    """
    Extracts the Event instance directly using the event_id parameter.

    :param request: The HTTP request object.
    :raises Event.DoesNotExist: If the Event with the given ID does not exist.
    :return: The Event instance.
    """
    event_id = kwargs.get('event_id')
    return Event.objects.get(pk=event_id)


def extract_organization_directly(request, *args, **kwargs):
    """
    Extracts the Organization instance directly using the organization_id parameter.

    :param request: The HTTP request object.
    :raises OrganizationAccess.DoesNotExist: If the Organization with the given ID does not exist.
    :return: The Organization instance.
    """
    organization_id = kwargs.get('organization_id')
    return Organizer.objects.get(pk=organization_id)


def check_organizer_access_decorator(organizer_extractor):
    """
    A decorator to check if the user has access to the organization associated with the event.

    :param organizer_extractor: A function that extracts the Event instance from the request and parameters.
    :raises PermissionDenied: If the user does not have access to the organization.
    :raises Http404: If the extracted Event does not exist.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(self, request, *args, **kwargs):
            if request.data:
                if request.data.get('organization_id') != kwargs.get('organization_id'):
                    raise BadRequestError('Parameter organization_id dont match with organization id')

            try:
                organizer = organizer_extractor(request, *args, **kwargs)  # noqa: F841

            except Organizer.DoesNotExist:
                raise NotFoundError('Organization not found.')

            user = request.user
            organization_id = kwargs.get('organization_id')

            organizer_access_exists = Organizer.objects.filter(
                user=user,
                organization_id=organization_id
            ).exists()

            if not organizer_access_exists:
                raise PermissionDenied('You do not have permission to access this organization.')

            return view_func(self, request, *args, **kwargs)

        return _wrapped_view

    return decorator
