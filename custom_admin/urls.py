from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ApproveOrganizerView, CompetitionsTypeViewSet

router = DefaultRouter()
router.register(r'competitions-type', CompetitionsTypeViewSet, basename='competitions_type')

urlpatterns = [
    path('', include(router.urls)),
    path('member/<int:member_id>/approve-organizer/', ApproveOrganizerView.as_view(), name='approve-organizer'),
]
