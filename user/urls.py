from django.urls import path

from .views import (
    AdditionalProfileDetailView,
    AdditionalProfileListView,
    RequestOrganizerView,
    UserDistanceRegistrationView,
    UserProfileView,
)


urlpatterns = [
    path('<int:user_id>/request-organizer/', RequestOrganizerView.as_view(), name='request-organizer'),
    path('distance/<int:distance_id>/register/', UserDistanceRegistrationView.as_view(), name='register-distance'),
    path(
        'profile/additional_profiles/',
        AdditionalProfileListView.as_view(),
        name='additional_profiles_list',
    ),
    path(
        'profile/additional_profiles/<int:id>/',
        AdditionalProfileDetailView.as_view(),
        name='additional_profile_detail',
    ),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
]
