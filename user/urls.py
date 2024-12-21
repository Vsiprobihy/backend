from django.urls import path

from .views import RequestOrganizerView, UserDistanceRegistrationView


urlpatterns = [
    path('<int:user_id>/request-organizer/', RequestOrganizerView.as_view(), name='request-organizer'),
    path('distance/<int:distance_id>/register/', UserDistanceRegistrationView.as_view(), name='register-distance'),
]
