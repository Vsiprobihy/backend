from datetime import date

import pytest
from django.contrib.auth import get_user_model

from event.distance_details.models import DistanceEvent
from organization.models import Organization
from event.models import Event


User = get_user_model()


@pytest.mark.django_db
def test_create_event():
    organizer = Organization.objects.create(
        name='Test Organizer', phone_number='+1234567890', email='organizer@example.com'
    )

    event = Event.objects.create(
        name='Test Event',
        competition_type='running',
        date_from=date.today(),
        date_to=date.today(),
        place='Test Place',
        description='Test description',
        organizer=organizer,
    )

    assert event.name == 'Test Event'
    assert event.organizer.name == 'Test Organizer'
    assert event.competition_type == 'running'
    assert str(event) == 'Test Event'


@pytest.mark.django_db
def test_distance_event():
    event = Event.objects.create(
        name='Test Event',
        competition_type='running',
        date_from=date.today(),
        date_to=date.today(),
        place='Test Place',
        description='Test description',
        organizer=Organization.objects.create(
            name='Organizer', phone_number='+1234567890', email='organizer@example.com'
        ),
    )

    distance = DistanceEvent.objects.create(name='5K Run', cost=20.00, event=event)

    assert distance.name == '5K Run'
    assert distance.event.name == 'Test Event'
    assert str(distance) == '5K Run'
