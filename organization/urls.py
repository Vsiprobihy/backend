from django.urls import path

from organization.views import InviteOrganizerView, OrganizationDetailView, OrganizationListCreateView


urlpatterns = [
    path('', OrganizationListCreateView.as_view(), name='organization-list-create'),
    path('<int:organization_id>/', OrganizationDetailView.as_view(), name='organization-detail'),
    path('<int:organization_id>/invite-organizer/', InviteOrganizerView.as_view(), name='invite-organizer')
]
