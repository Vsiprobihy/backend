from django.urls import path

from event.views.additional_items import AdditionalItemsDetailView
from event.views.distance_detail import DistanceDetailView
from event.views.event_registrations import EventRegistrationsListView, EventRegistrationDetailView
from event.views.events import EventsListView, EventDetailView
from event.views.organizer_detail import InviteModeratorView, OrganizerEventListCreateView, OrganizerEventDetailView


urlpatterns = [

    path('additional-items/<int:event_id>/', AdditionalItemsDetailView.as_view(), name='event_additional-items_detail'),
    path('distances/<int:event_id>/', DistanceDetailView.as_view(), name='event_distances_detail'),
    path('events/', EventsListView.as_view(), name='event_events_list'),
    path('events/<int:pk>/', EventDetailView.as_view(), name='event_events_detail'),
    path('organizer-events/', OrganizerEventListCreateView.as_view(), name='organizer-event-list-create'),
    path('organizer-events/<int:pk>/', OrganizerEventDetailView.as_view(), name='organizer-event-detail'),
    path('invite-moderator/', InviteModeratorView.as_view(), name='invite-moderator'),
    path('registrations/', EventRegistrationsListView.as_view(), name='event-registration-list'),
    path('registrations/<int:pk>/', EventRegistrationDetailView.as_view(), name='event-registration-detail'),
]
