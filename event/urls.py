from django.urls import path

from event.views.additional_items import AdditionalItemsDetailView
from event.views.distance_detail import DistanceDetailView
from event.views.event_registrations import EventRegistrationsListView, EventRegistrationDetailView
from event.views.events import EventsListView, EventDetailView
from event.views.organizer_detail import OrganizerDetailView


urlpatterns = [

    path('additional-items/<int:event_id>/', AdditionalItemsDetailView.as_view(), name='event_additional-items_detail'),
    path('distances/<int:event_id>/', DistanceDetailView.as_view(), name='event_distances_detail'),
    path('events/', EventsListView.as_view(), name='event_events_list'),
    path('events/<int:pk>/', EventDetailView.as_view(), name='event_events_detail'),
    path('organizers/<int:event_id>/', OrganizerDetailView.as_view(), name='event_organizers_detail'),
    path('registrations/', EventRegistrationsListView.as_view(), name='event-registration-list'),
    path('registrations/<int:pk>/', EventRegistrationDetailView.as_view(), name='event-registration-detail'),
]
