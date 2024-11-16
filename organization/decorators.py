from functools import wraps

from django.core.exceptions import PermissionDenied
from django.http import Http404

from event.models import DistanceEvent, Event
from organization.models import OrganizationAccess


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
                event = event_extractor(request, *args, **kwargs)
            except Event.DoesNotExist:
                raise Http404('Event not found.')

            user = request.user
            if not OrganizationAccess.objects.filter(
                organization=event.organizer, user=user
            ).exists():
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
    event_id = kwargs.get('pk')
    return Event.objects.get(pk=event_id)
