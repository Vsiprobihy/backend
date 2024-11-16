from django.urls import path

from additional_items.views import AdditionalItemsDetailView


urlpatterns = [
    path(
        'organizer-events/events/additional-items/<int:distance_id>/',
        AdditionalItemsDetailView.as_view(),
        name='event_additional-items_detail',
    )
]
