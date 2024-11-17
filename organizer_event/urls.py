from django.urls import path

from organizer_event.views import (
    EventCreateView,
    EventDeleteView,
    EventDetailView,
    EventPartialUpdateView,
    EventsListView,
    EventUpdateView,
)


urlpatterns = [
    path('events/', EventsListView.as_view(), name='events_list'),
    path('events/create/', EventCreateView.as_view(), name='event_create'),
    path('events/<int:id>/', EventDetailView.as_view(), name='event_detail'),
    path('events/<int:id>/update/', EventUpdateView.as_view(), name='event_update'),
    path('events/<int:id>/partial-update/', EventPartialUpdateView.as_view(), name='event_partial_update'),
    path('events/<int:id>/delete/', EventDeleteView.as_view(), name='event_delete'),
]
