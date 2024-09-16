from django.urls import path
from .views import (
    AdditionalItemsDetailView,
    DistancesListView, DistanceDetailView,
    EventsListView, EventDetailView,
    OrganizersListView, OrganizerDetailView,
    EventRegistrationsListView, EventRegistrationDetailView
)

urlpatterns = [

    path('additional-items/<int:event_id>/', AdditionalItemsDetailView.as_view(), name='event_additional-items_detail'),
    path('distances/', DistancesListView.as_view(), name='event_distances_list'),
    path('distances/<int:pk>/', DistanceDetailView.as_view(), name='event_distances_detail'),
    path('events/', EventsListView.as_view(), name='event_events_list'),
    path('events/<int:pk>/', EventDetailView.as_view(), name='event_events_detail'),
    path('organizers/', OrganizersListView.as_view(), name='event_organizers_list'),
    path('organizers/<int:pk>/', OrganizerDetailView.as_view(), name='event_organizers_detail'),
    path('registrations/', EventRegistrationsListView.as_view(), name='event_registrations_list'),
    path('registrations/<int:pk>/', EventRegistrationDetailView.as_view(), name='event_registrations_detail'),
]
