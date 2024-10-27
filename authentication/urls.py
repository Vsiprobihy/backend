from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

from authentication.auth_views import google_login, google_account_info
from authentication.views import RegisterView, UserProfileView, LoginView, UserAvatarUploadView

urlpatterns = [
    path('oauth/', include('social_django.urls', namespace='social')),
    path('oauth/login-success/', google_login, name='google_login'),
    path('google-account-info/', google_account_info, name='google_account_info'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('profile/upload-avatar/', UserAvatarUploadView.as_view(), name='upload-avatar'),
]
