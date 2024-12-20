from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ApproveOrganizerView, CompetitionsTypeViewSet, RequestOrganizerView


router = DefaultRouter()
router.register(r'competitions-type', CompetitionsTypeViewSet, basename='competitions_type')

urlpatterns = [
    path('', include(router.urls)),
    path('member/<int:member_id>/request-organizer/', RequestOrganizerView.as_view(), name='request-organizer'),
    path('member/<int:member_id>/approve-organizer/', ApproveOrganizerView.as_view(), name='approve-organizer')
]
