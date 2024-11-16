from django.urls import path

from distance_details.views import DistanceDetailView


urlpatterns = [
    path(
        'organizer-events/events/distances/<int:event_id>/',
        DistanceDetailView.as_view(),
        name='event_distances_detail',
    ),
]
