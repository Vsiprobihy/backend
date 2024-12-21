import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    return User.objects.create_user(
        email='user@example.com',
        password='String1!',
        firstName='John',
        lastName='Doe',
    )


@pytest.mark.django_db
def test_register_success(api_client):
    url = reverse('register')
    data = {
        'email': 'newuser@example.com',
        'password': 'String1!',
        'password2': 'String1!',
    }
    response = api_client.post(url, data)

    assert response.status_code == status.HTTP_201_CREATED
    assert 'access_token' in response.data
    assert 'refresh_token' in response.data
    assert isinstance(response.data['access_token'], dict)
    assert 'value' in response.data['access_token']
    assert 'expires' in response.data['access_token']
    assert isinstance(response.data['refresh_token'], dict)
    assert 'value' in response.data['refresh_token']
    assert 'expires' in response.data['refresh_token']


@pytest.mark.django_db
def test_register_failure(api_client):
    url = reverse('register')
    data = {
        'email': 'newuser@example.com',
        'password': 'String1!',
        'password2': 'Example!2',
    }
    response = api_client.post(url, data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'non_field_errors' in response.data
    assert 'Passwords must match' in response.data['non_field_errors']


@pytest.mark.django_db
def test_get_user_profile(api_client, user):
    api_client.force_authenticate(user=user)
    url = reverse('user_profile')
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data['firstName'] == 'John'
    assert response.data['lastName'] == 'Doe'


@pytest.mark.django_db
def test_update_user_profile_put(api_client, user):
    api_client.force_authenticate(user=user)
    url = reverse('user_profile')
    data = {'firstName': 'Jane', 'lastName': 'Smith', 'city': 'New York'}
    response = api_client.put(url, data)

    assert response.status_code == status.HTTP_200_OK
    assert response.data['firstName'] == 'Jane'
    assert response.data['lastName'] == 'Smith'
    assert response.data['city'] == 'New York'


@pytest.mark.django_db
def test_update_user_profile_patch(api_client, user):
    api_client.force_authenticate(user=user)
    url = reverse('user_profile')
    data = {'firstName': 'Jane'}
    response = api_client.patch(url, data)

    assert response.status_code == status.HTTP_200_OK
    assert response.data['firstName'] == 'Jane'
    assert response.data['lastName'] == 'Doe'
