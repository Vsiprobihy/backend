from django.urls import path

from organization.views import InviteModeratorView, OrganizerEventDetailView, OrganizerEventListCreateView


urlpatterns = [
    path('organizer-events/', OrganizerEventListCreateView.as_view(), name='organizer-event-list-create'),
    path('organizer-events/<int:pk>/', OrganizerEventDetailView.as_view(), name='organizer-event-detail'),
    path('organizer-events/invite-moderator/', InviteModeratorView.as_view(), name='invite-moderator')
]
