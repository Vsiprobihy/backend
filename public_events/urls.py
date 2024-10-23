from django.urls import path
from .views import PublicEventDetailView

urlpatterns = [
    path('events/<int:pk>/', PublicEventDetailView.as_view(), name='public-event-detail'),
]
