from unittest.mock import patch

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from social_django.models import UserSocialAuth


User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    return User.objects.create_user(
        email='user@example.com',
        password='password123',
        firstName='John',
        lastName='Doe',
    )


@pytest.fixture
def authenticated_user(api_client, user):
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return api_client


@pytest.mark.django_db
def test_google_login_view(api_client, user):
    api_client.force_login(user)

    url = reverse('google_login')
    response = api_client.get(url)

    assert response.status_code == 200
    data = response.json()
    assert 'access_token' in data
    assert 'refresh_token' in data


@pytest.mark.django_db
def test_google_account_info_view_without_google_auth(authenticated_user):
    url = reverse('google_account_info')
    response = authenticated_user.get(url)

    assert response.status_code == 400
    assert response.json() == {'error': 'User is not authenticated with Google'}


@pytest.mark.django_db
@patch('requests.get')
def test_google_account_info_view_with_google_auth(mock_get, authenticated_user, user):
    social_user = UserSocialAuth.objects.create(
        user=user,
        provider='google-oauth2',
        uid='123456789',
        extra_data={'access_token': 'valid-access-token'},
    )

    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        'email': 'user@example.com',
        'name': 'John Doe',
    }

    url = reverse('google_account_info')
    response = authenticated_user.get(url)

    assert response.status_code == 200
    data = response.json()
    assert data['email'] == 'user@example.com'
    assert data['name'] == 'John Doe'


@pytest.mark.django_db
@patch('requests.get')
def test_google_account_info_view_google_api_failure(
    mock_get, authenticated_user, user
):
    social_user = UserSocialAuth.objects.create(
        user=user,
        provider='google-oauth2',
        uid='123456789',
        extra_data={'access_token': 'valid-access-token'},
    )

    mock_get.return_value.status_code = 500

    url = reverse('google_account_info')
    response = authenticated_user.get(url)

    assert response.status_code == 500
    assert response.json() == {'error': 'Failed to fetch user info from Google'}
