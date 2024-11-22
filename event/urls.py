from django.urls import path

from event.views import EventDetailView, EventsListCreateView


urlpatterns = [
    path('<int:organization_id>/event/', EventsListCreateView.as_view(), name='events_list_create'),
    path('<int:organization_id>/event/<int:event_id>/', EventDetailView.as_view(), name='event_detail'),
]
