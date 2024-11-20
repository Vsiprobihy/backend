from django.urls import path

from organizer_event.views import EventDetailView, EventsListCreateView


urlpatterns = [
    path('<int:organizer_id>/events/', EventsListCreateView.as_view(), name='events_list_create'),
    path('<int:organizer_id>/events/<int:event_id>/', EventDetailView.as_view(), name='event_detail'),
]
