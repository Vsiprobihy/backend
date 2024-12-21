import requests
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from social_django.models import UserSocialAuth


@login_required
def google_login(request):
    user = request.user

    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    refresh_token = str(refresh)

    return JsonResponse(
        {
            'accessToken': access_token,
            'refreshToken': refresh_token,
        }
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def google_account_info(request):
    user = request.user

    try:
        social_user = UserSocialAuth.objects.get(user=user, provider='google-oauth2')
    except UserSocialAuth.DoesNotExist:
        return JsonResponse(
            {'error': 'User is not authenticated with Google'}, status=400
        )

    access_token = social_user.extra_data.get('access_token')

    response = requests.get(
        'https://www.googleapis.com/oauth2/v1/userinfo',
        params={'alt': 'json', 'access_token': access_token},
    )

    if response.status_code == 200:
        user_info = response.json()
        return JsonResponse(user_info)
    else:
        return JsonResponse(
            {'error': 'Failed to fetch user info from Google'},
            status=response.status_code,
        )
