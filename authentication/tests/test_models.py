import pytest
from django.contrib.auth import get_user_model


CustomUser = get_user_model()


@pytest.mark.django_db
def test_create_user():
    user = CustomUser.objects.create_user(
        email='user@example.com',
        password='testpass123',
        firstName='John',
        lastName='Doe',
    )
    assert user.email == 'user@example.com'
    assert user.check_password('testpass123')
    assert user.isActive
    assert not user.isStaff
    assert not user.is_superuser


@pytest.mark.django_db
def test_create_user_no_email():
    with pytest.raises(ValueError) as excinfo:
        CustomUser.objects.create_user(email=None, password='testpass123')
    assert str(excinfo.value) == 'The given email must be set'


@pytest.mark.django_db
def test_create_superuser():
    superuser = CustomUser.objects.create_superuser(
        email='admin@example.com',
        password='adminpass123',
        firstName='Admin',
        lastName='User',
    )
    assert superuser.email == 'admin@example.com'
    assert superuser.check_password('adminpass123')
    assert superuser.isActive
    assert superuser.isStaff
    assert superuser.is_superuser


@pytest.mark.django_db
def test_user_string_representation():
    user = CustomUser.objects.create_user(
        email='user@example.com',
        password='testpass123',
        firstName='John',
        lastName='Doe',
    )
    assert str(user) == 'user@example.com'


@pytest.mark.django_db
def test_user_fields():
    user = CustomUser.objects.create_user(
        email='user@example.com',
        password='testpass123',
        firstName='John',
        lastName='Doe',
        gender='M',
        dateOfBirth='1990-01-01',
        tShirtSize='M',
        country='USA',
        city='New York',
        phoneNumber='+1234567890',
        sportsClub='NY Club',
        emergencyContactName='Jane Doe',
        emergencyContactPhone='+0987654321',
    )
    assert user.firstName == 'John'
    assert user.lastName == 'Doe'
    assert user.gender == 'M'
    assert str(user.dateOfBirth) == '1990-01-01'
    assert user.tShirtSize == 'M'
    assert user.country == 'USA'
    assert user.city == 'New York'
    assert user.phoneNumber == '+1234567890'
    assert user.sportsClub == 'NY Club'
    assert user.emergencyContactName == 'Jane Doe'
    assert user.emergencyContactPhone == '+0987654321'
