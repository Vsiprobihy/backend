from django.urls import path

from organization.views import InviteModeratorView, OrganizerEventDetailView, OrganizerEventListCreateView


urlpatterns = [
    path('', OrganizerEventListCreateView.as_view(), name='organizer-event-list-create'),
    path('<int:pk>/', OrganizerEventDetailView.as_view(), name='organizer-event-detail'),
    path('invite-moderator/', InviteModeratorView.as_view(), name='invite-moderator')
]
