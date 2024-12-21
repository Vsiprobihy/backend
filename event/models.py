from django.db import models

from organization.models import Organization
from utils.constants.constants_event import (
    COMPETITION_TYPES,
    REGIONS,
    STATUS_CHOICES,
    STATUS_PENDING,
)


class CompetitionType(models.Model):
    name = models.CharField(max_length=50, choices=COMPETITION_TYPES)

    def __str__(self):
        return self.name


class Event(models.Model):

    name = models.CharField(max_length=255)
    competitionType = models.ManyToManyField(CompetitionType, related_name='event')
    dateFrom = models.DateField()
    dateTo = models.DateField()
    placeRegion = models.CharField(max_length=255, choices=REGIONS, null=True)
    place = models.CharField(max_length=255)
    photos = models.ImageField(upload_to='event_photos/', blank=True, null=True)
    description = models.TextField()
    registrationLink = models.URLField(blank=True, null=True)
    hideParticipants = models.BooleanField(default=False)
    extendedDescription = models.TextField(blank=True, null=True)
    schedulePdf = models.FileField(upload_to='event_schedule/', blank=True, null=True)
    coOrganizer = models.TextField(blank=True, null=True)
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name='eventOrganization', null=False
    )
    status = models.CharField(
        max_length=12, choices=STATUS_CHOICES, default=STATUS_PENDING, db_index=True
    )

    def __str__(self):
        return self.name
