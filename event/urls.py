from django.urls import path

from event.views.additional_items import AdditionalItemsDetailView
from event.views.distance_detail import DistanceDetailView
from event.views.events import EventDetailView, EventsCreateView


urlpatterns = [
    path(
        'organizer-events/events/additional-items/<int:distance_id>/',
        AdditionalItemsDetailView.as_view(),
        name='event_additional-items_detail',
    ),
    path(
        'organizer-events/events/distances/<int:event_id>/',
        DistanceDetailView.as_view(),
        name='event_distances_detail',
    ),
    path('organizer-events/events/', EventsCreateView.as_view(), name='event_events_list'),
    path('organizer-events/events/<int:pk>/', EventDetailView.as_view(), name='event_events_detail'),
]
