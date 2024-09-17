from django.urls import path
from .views import EventFilterView

urlpatterns = [
    path('events/filter/', EventFilterView.as_view(), name='event-filter'),
]
