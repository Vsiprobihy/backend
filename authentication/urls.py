from django.urls import include, path
from djoser.views import UserViewSet
from rest_framework_simplejwt.views import TokenRefreshView

from authentication.auth_views import google_account_info, google_login
from authentication.views import (
    AdditionalProfileDetailView,
    AdditionalProfileListView,
    LoginView,
    RegisterView,
    UserAvatarUploadView,
    UserProfileView,
)


urlpatterns = [
    path('oauth/', include('social_django.urls', namespace='social')),
    path('oauth/login-success/', google_login, name='google_login'),
    path('google-account-info/', google_account_info, name='google_account_info'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path(
        'reset_password/',
        UserViewSet.as_view({'post': 'reset_password'}),
        name='reset_password',
    ),
    path(
        'reset_password_confirm/',
        UserViewSet.as_view({'post': 'reset_password_confirm'}),
        name='reset_password_confirm',
    ),
    path(
        'profile/upload-avatar/', UserAvatarUploadView.as_view(), name='upload-avatar'
    ),
    path(
        'profile/additional_profiles/',
        AdditionalProfileListView.as_view(),
        name='additional_profiles_list',
    ),
    path(
        'profile/additional_profiles/<int:profile_id>/',
        AdditionalProfileDetailView.as_view(),
        name='additional_profile_detail',
    ),
]
