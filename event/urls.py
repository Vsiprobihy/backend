from django.urls import path

from .views import (
    AdditionalItemsDetailView,
    DistanceDetailView,
    EventDetailView,
    EventRegistrationDetailView,
    EventRegistrationsListView,
    EventsListView,
    OrganizerDetailView,
)


urlpatterns = [

    path('additional-items/<int:event_id>/', AdditionalItemsDetailView.as_view(), name='event_additional-items_detail'),
    path('distances/<int:event_id>/', DistanceDetailView.as_view(), name='event_distances_detail'),
    path('events/', EventsListView.as_view(), name='event_events_list'),
    path('events/<int:pk>/', EventDetailView.as_view(), name='event_events_detail'),
    path('organizers/<int:event_id>/', OrganizerDetailView.as_view(), name='event_organizers_detail'),
    path('registrations/', EventRegistrationsListView.as_view(), name='event-registration-list'),
    path('registrations/<int:pk>/', EventRegistrationDetailView.as_view(), name='event-registration-detail'),
]
