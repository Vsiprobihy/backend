from django.urls import path, include

from rest_framework.routers import DefaultRouter
from .views import CompetitionsTypeViewSet

router = DefaultRouter()
router.register(r"competitions-type", CompetitionsTypeViewSet, basename="competitions_type")

urlpatterns = [
    path("", include(router.urls)),
    # на майбутне
    # path('/user/<int:user_id>/approve-organizer/', ApproveOrganizerView.as_view(), name='approve-organizer')
]
