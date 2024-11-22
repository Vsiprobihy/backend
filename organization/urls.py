from django.urls import path

from organization.views import InviteModeratorView, OrganizationDetailView, OrganizationListCreateView


urlpatterns = [
    path('', OrganizationListCreateView.as_view(), name='organization-list-create'),
    path('<int:organization_id>/', OrganizationDetailView.as_view(), name='organization-detail'),
    path('<int:organization_id>/invite-moderator/', InviteModeratorView.as_view(), name='invite-moderator')
]
