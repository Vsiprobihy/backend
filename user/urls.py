from django.urls import path

from .views import RequestOrganizerView

urlpatterns = [
    path('member/<int:member_id>/request-organizer/', RequestOrganizerView.as_view(), name='request-organizer'),
]
