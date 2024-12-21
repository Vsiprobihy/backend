from django.urls import path

from event.distance_details.views import FavoriteDistanceDetailView, FavoriteDistanceListView, MyDistanceListView


urlpatterns = [
    path('my/', MyDistanceListView.as_view(), name='my-distance'),
    path('favorites/', FavoriteDistanceListView.as_view(), name='favorite-distances-list'),
    path('favorites/<int:distance_id>/', FavoriteDistanceDetailView.as_view(), name='favorite-distance-detail'),
]
