from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ApproveOrganizerView, CompetitionsTypeViewSet, ApproveDistanceRegistrationView

router = DefaultRouter()
router.register(r'competitions-type', CompetitionsTypeViewSet, basename='competitions_type')

urlpatterns = [
    path('', include(router.urls)),
    path('user/<int:user_id>/approve-organizer/', ApproveOrganizerView.as_view(), name='approve-organizer'),
    path('distance-registration/<int:registration_id>/approve/', ApproveDistanceRegistrationView.as_view(),
         name='approve-distance-registration'),
]
