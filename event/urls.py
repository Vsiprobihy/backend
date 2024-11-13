from django.urls import path

from event.views.events import EventDetailView, EventsListView
from event.views.organizer_detail import InviteModeratorView, OrganizerEventDetailView, OrganizerEventListCreateView


urlpatterns = [
    path('events/', EventsListView.as_view(), name='event_events_list'),
    path('events/<int:pk>/', EventDetailView.as_view(), name='event_events_detail'),
    path('organizer-events/', OrganizerEventListCreateView.as_view(), name='organizer-event-list-create'),
    path('organizer-events/<int:pk>/', OrganizerEventDetailView.as_view(), name='organizer-event-detail'),
    path('invite-moderator/', InviteModeratorView.as_view(), name='invite-moderator')
]
