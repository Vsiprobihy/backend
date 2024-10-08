import pytest
from event.models import Event, EventRegistration, OrganizerEvent, DistanceEvent, AdditionalItemEvent
from django.contrib.auth import get_user_model
from datetime import date

User = get_user_model()


@pytest.mark.django_db
def test_create_event():
    organizer = OrganizerEvent.objects.create(
        name="Test Organizer",
        phone_number="+1234567890",
        email="organizer@example.com"
    )

    event = Event.objects.create(
        name="Test Event",
        competition_type="running",
        date_from=date.today(),
        date_to=date.today(),
        place="Test Place",
        description="Test description",
        organizer=organizer
    )

    assert event.name == "Test Event"
    assert event.organizer.name == "Test Organizer"
    assert event.competition_type == "running"
    assert str(event) == "Test Event"


@pytest.mark.django_db
def test_event_registration():
    user = User.objects.create_user(email="user@example.com", password="password123")
    organizer = OrganizerEvent.objects.create(
        name="Test Organizer",
        phone_number="+1234567890",
        email="organizer@example.com"
    )

    event = Event.objects.create(
        name="Test Event",
        competition_type="running",
        date_from=date.today(),
        date_to=date.today(),
        place="Test Place",
        description="Test description",
        organizer=organizer
    )

    registration = EventRegistration.objects.create(
        user=user,
        event=event,
        is_confirmed=True
    )

    assert registration.user.email == "user@example.com"
    assert registration.event.name == "Test Event"
    assert registration.is_confirmed
    assert str(registration) == f"user@example.com registered for Test Event on {registration.registration_date}"


@pytest.mark.django_db
def test_distance_event():
    event = Event.objects.create(
        name="Test Event",
        competition_type="running",
        date_from=date.today(),
        date_to=date.today(),
        place="Test Place",
        description="Test description",
        organizer=OrganizerEvent.objects.create(name="Organizer", phone_number="+1234567890",
                                                email="organizer@example.com")
    )

    distance = DistanceEvent.objects.create(
        name="5K Run",
        cost=20.00,
        event=event
    )

    assert distance.name == "5K Run"
    assert distance.event.name == "Test Event"
    assert str(distance) == "5K Run"
