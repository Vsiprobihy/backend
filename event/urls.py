from django.urls import path

from event.views.events import EventDetailView, EventsCreateView


urlpatterns = [
    path('organizer-events/events/', EventsCreateView.as_view(), name='event_events_list'),
    path('organizer-events/events/<int:pk>/', EventDetailView.as_view(), name='event_events_detail'),
]
