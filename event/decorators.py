from functools import wraps

from django.core.exceptions import PermissionDenied
from django.http import Http404

from event.models import Event, OrganizationAccess


def check_organization_access_decorator(view_func):
    @wraps(view_func)
    def _wrapped_view(self, request, *args, **kwargs):
        event_id = kwargs.get('event_id')
        event = Event.objects.filter(pk=event_id).first()

        if event is None:
            raise Http404('Event not found.')

        user = request.user
        if not OrganizationAccess.objects.filter(organization=event.organizer, user=user).exists():
            raise PermissionDenied('You do not have permission to access this event.')

        return view_func(self, request, *args, **kwargs)

    return _wrapped_view
