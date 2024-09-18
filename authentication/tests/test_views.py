import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    return User.objects.create_user(
        email='user@example.com',
        password='password123',
        first_name='John',
        last_name='Doe'
    )


@pytest.mark.django_db
def test_register_success(api_client):
    url = reverse('register')
    data = {
        'email': 'newuser@example.com',
        'password': 'password123',
        'password2': 'password123',
    }
    response = api_client.post(url, data)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['message'] == 'User registered successfully'


@pytest.mark.django_db
def test_register_failure(api_client):
    url = reverse('register')
    data = {
        'email': 'newuser@example.com',
        'password': 'password123',
        'password2': 'wrongpassword',
    }
    response = api_client.post(url, data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'Passwords must match.' in str(response.data)


@pytest.mark.django_db
def test_get_user_profile(api_client, user):
    api_client.force_authenticate(user=user)
    url = reverse('user_profile')
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data['first_name'] == 'John'
    assert response.data['last_name'] == 'Doe'


@pytest.mark.django_db
def test_update_user_profile_put(api_client, user):
    api_client.force_authenticate(user=user)
    url = reverse('user_profile')
    data = {
        'first_name': 'Jane',
        'last_name': 'Smith',
        'city': 'New York'
    }
    response = api_client.put(url, data)

    assert response.status_code == status.HTTP_200_OK
    assert response.data['first_name'] == 'Jane'
    assert response.data['last_name'] == 'Smith'
    assert response.data['city'] == 'New York'


@pytest.mark.django_db
def test_update_user_profile_patch(api_client, user):
    api_client.force_authenticate(user=user)
    url = reverse('user_profile')
    data = {'first_name': 'Jane'}
    response = api_client.patch(url, data)

    assert response.status_code == status.HTTP_200_OK
    assert response.data['first_name'] == 'Jane'
    assert response.data['last_name'] == 'Doe'

