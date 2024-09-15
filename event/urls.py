from django.urls import path
from .views import (
    AdditionalItemsListView, AdditionalItemsDetailView,
    DistancesListView, DistanceDetailView,
    EventsListView, EventDetailView,
    OrganizersListView, OrganizerDetailView,
    EventRegistrationsListView, EventRegistrationDetailView
)

urlpatterns = [
    # Additional Items
    path('additional-items/', AdditionalItemsListView.as_view(), name='event_additional-items_list'),
    path('additional-items/<int:pk>/', AdditionalItemsDetailView.as_view(), name='event_additional-items_detail'),

    # Distances
    path('distances/', DistancesListView.as_view(), name='event_distances_list'),
    path('distances/<int:pk>/', DistanceDetailView.as_view(), name='event_distances_detail'),

    # Events
    path('events/', EventsListView.as_view(), name='event_events_list'),
    path('events/<int:pk>/', EventDetailView.as_view(), name='event_events_detail'),

    # Organizers
    path('organizers/', OrganizersListView.as_view(), name='event_organizers_list'),
    path('organizers/<int:pk>/', OrganizerDetailView.as_view(), name='event_organizers_detail'),

    # Event Registrations
    path('registrations/', EventRegistrationsListView.as_view(), name='event_registrations_list'),
    path('registrations/<int:pk>/', EventRegistrationDetailView.as_view(), name='event_registrations_detail'),
]
