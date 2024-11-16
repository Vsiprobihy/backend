from django.urls import path

from .views.filter_main import EventFilterView


urlpatterns = [
    path('filter/', EventFilterView.as_view(), name='event-filter'),
]
