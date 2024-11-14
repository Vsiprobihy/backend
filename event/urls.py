from django.urls import path

from event.views.additional_items import AdditionalItemsDetailView
from event.views.distance_detail import DistanceDetailView
from event.views.events import EventDetailView, EventsListView
from event.views.organizer_detail import InviteModeratorView, OrganizerEventDetailView, OrganizerEventListCreateView


urlpatterns = [
    path(
        'organizer-events/events/additional-items/<int:event_id>/',
        AdditionalItemsDetailView.as_view(),
        name='event_additional-items_detail',
    ),
    path(
        'organizer-events/events/distances/<int:event_id>/',
        DistanceDetailView.as_view(),
        name='event_distances_detail',
    ),
    path('organizer-events/events/', EventsListView.as_view(), name='event_events_list'),
    path('organizer-events/events/<int:pk>/', EventDetailView.as_view(), name='event_events_detail'),
    path('organizer-events/', OrganizerEventListCreateView.as_view(), name='organizer-event-list-create'),
    path('organizer-events/<int:pk>/', OrganizerEventDetailView.as_view(), name='organizer-event-detail'),
    path('organizer-events/invite-moderator/', InviteModeratorView.as_view(), name='invite-moderator')
]
