import pytest
from django.contrib.auth import get_user_model

CustomUser = get_user_model()


@pytest.mark.django_db
def test_create_user():
    user = CustomUser.objects.create_user(
        email="user@example.com",
        password="testpass123",
        first_name="John",
        last_name="Doe",
    )
    assert user.email == "user@example.com"
    assert user.check_password("testpass123")
    assert user.is_active
    assert not user.is_staff
    assert not user.is_superuser


@pytest.mark.django_db
def test_create_user_no_email():
    with pytest.raises(ValueError) as excinfo:
        CustomUser.objects.create_user(email=None, password="testpass123")
    assert str(excinfo.value) == "The given email must be set"


@pytest.mark.django_db
def test_create_superuser():
    superuser = CustomUser.objects.create_superuser(
        email="admin@example.com",
        password="adminpass123",
        first_name="Admin",
        last_name="User",
    )
    assert superuser.email == "admin@example.com"
    assert superuser.check_password("adminpass123")
    assert superuser.is_active
    assert superuser.is_staff
    assert superuser.is_superuser


@pytest.mark.django_db
def test_user_string_representation():
    user = CustomUser.objects.create_user(
        email="user@example.com",
        password="testpass123",
        first_name="John",
        last_name="Doe",
    )
    assert str(user) == "user@example.com"


@pytest.mark.django_db
def test_user_fields():
    user = CustomUser.objects.create_user(
        email="user@example.com",
        password="testpass123",
        first_name="John",
        last_name="Doe",
        gender="M",
        date_of_birth="1990-01-01",
        t_shirt_size="M",
        country="USA",
        city="New York",
        phone_number="+1234567890",
        sports_club="NY Club",
        emergency_contact_name="Jane Doe",
        emergency_contact_phone="+0987654321",
    )
    assert user.first_name == "John"
    assert user.last_name == "Doe"
    assert user.gender == "M"
    assert str(user.date_of_birth) == "1990-01-01"
    assert user.t_shirt_size == "M"
    assert user.country == "USA"
    assert user.city == "New York"
    assert user.phone_number == "+1234567890"
    assert user.sports_club == "NY Club"
    assert user.emergency_contact_name == "Jane Doe"
    assert user.emergency_contact_phone == "+0987654321"
