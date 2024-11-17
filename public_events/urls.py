from django.urls import path

from .views import PublicEventDetailView, PublicEventFilterView, PublicEventListView


urlpatterns = [
    path('', PublicEventListView.as_view(), name='public-event-list'),
    path('<int:id>/', PublicEventDetailView.as_view(), name='public-event-detail'),
    path('filter/', PublicEventFilterView.as_view(), name='public-event-filter'),
]
