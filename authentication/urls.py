from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from authentication.auth_views import google_login, google_account_info
from authentication.views import RegisterView, UserProfileView, AdminOnlyView, OrganizerOnlyView, PublicView

urlpatterns = [
    path('oauth/', include('social_django.urls', namespace='social')),
    path('oauth/login-success/', google_login, name='google_login'),
    path('google-account-info/', google_account_info, name='google_account_info'),
    path('register/', RegisterView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    #temp endpoints:
    path('admin-only/', AdminOnlyView.as_view(), name='admin-only'),
    path('organizer-only/', OrganizerOnlyView.as_view(), name='organizer-only'),
    path('public/', PublicView.as_view(), name='public'),
]

