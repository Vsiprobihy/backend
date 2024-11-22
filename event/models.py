from django.db import models

from organization.models import Organization
from utils.constants.constants_event import (
    REGIONS,
    STATUS_CHOICES,
    STATUS_PENDING,
)


class CompetitionType(models.Model):
    name = models.CharField(max_length=50, unique=False)

    def __str__(self):
        return self.name


class Event(models.Model):

    name = models.CharField(max_length=255)
    competition_type = models.ManyToManyField(CompetitionType, related_name='event')
    date_from = models.DateField()
    date_to = models.DateField()
    place_region = models.CharField(max_length=255, choices=REGIONS, null=True)
    place = models.CharField(max_length=255)
    photos = models.ImageField(upload_to='event_photos/', blank=True, null=True)
    description = models.TextField()
    registration_link = models.URLField(blank=True, null=True)
    hide_participants = models.BooleanField(default=False)
    extended_description = models.TextField(blank=True, null=True)
    schedule_pdf = models.FileField(upload_to='event_schedule/', blank=True, null=True)
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name='event_organization', null=False
    )
    status = models.CharField(
        max_length=12, choices=STATUS_CHOICES, default=STATUS_PENDING
    )

    def __str__(self):
        return self.name

    def approve_event(self):
        """Method for approving the event by the administrator."""
        self.status = self.STATUS_UNPUBLISHED
        self.save()

    def publish_event(self):
        """Method for publishing an event by the organizer."""
        if self.status == self.STATUS_UNPUBLISHED:
            self.status = self.STATUS_PUBLISHED
            self.save()
