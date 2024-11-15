from django.db import models

from authentication.models import CustomUser
from event.constants.constants_distance import CATEGORY_CHOICES
from event.constants.constants_event import (
    COMPETITION_TYPES,
    REGIONS,
    STATUS_CHOICES,
    STATUS_PENDING,
)


class OrganizerEvent(models.Model):
    name = models.CharField(max_length=255)
    site_url = models.URLField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField()
    instagram_url = models.URLField(blank=True, null=True)
    facebook_url = models.URLField(blank=True, null=True)
    telegram_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name


class OrganizationAccess(models.Model):
    OWNER = 'owner'
    MODERATOR = 'organizer'

    ROLE_CHOICES = [
        (OWNER, 'Owner'),
        (MODERATOR, 'Organizer'),
    ]

    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='organization_access', null=False
    )
    organization = models.ForeignKey(
        OrganizerEvent, on_delete=models.CASCADE, related_name='users_access', null=False
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, null=False)

    class Meta:
        unique_together = ('user', 'organization')

    def __str__(self):
        return (
            f'{self.user.email} - {self.get_role_display()} в {self.organization.name}'
        )


class DistanceEvent(models.Model):

    name = models.CharField(max_length=255)
    competition_type = models.CharField(
        max_length=50, choices=COMPETITION_TYPES, default='running'
    )
    category = models.CharField(
        max_length=50, choices=CATEGORY_CHOICES, default='adults'
    )
    length = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )  # Distance in km or meters
    start_number_from = models.PositiveIntegerField(blank=True, null=True)
    start_number_to = models.PositiveIntegerField(blank=True, null=True)
    show_start_number = models.BooleanField(default=False)
    show_name_on_number = models.BooleanField(default=False)
    age_from = models.PositiveIntegerField(blank=True, null=True)
    age_to = models.PositiveIntegerField(blank=True, null=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    is_free = models.BooleanField(default=False)
    promo_only_registration = models.BooleanField(default=False)
    allow_registration = models.BooleanField(default=True)
    event = models.ForeignKey(
        'Event', related_name='distances', on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class AdditionalItemEvent(models.Model):
    TRANSFER = 'transfer'
    MEDAL = 'medal'
    T_SHIRT = 't_shirt'

    ITEM_TYPES = [
        (TRANSFER, 'Трансфер'),
        (MEDAL, 'Медаль'),
        (T_SHIRT, 'Футболка'),
    ]

    item_type = models.CharField(max_length=50, choices=ITEM_TYPES)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    distance = models.ForeignKey(DistanceEvent, related_name='additional_options', on_delete=models.CASCADE, null=False)

    def __str__(self):
        return f'{self.get_item_type_display()} - {self.price}'


class CompetitionType(models.Model):
    name = models.CharField(max_length=50, unique=False)

    def __str__(self):
        return self.name


class Event(models.Model):

    name = models.CharField(max_length=255)
    competition_type = models.ManyToManyField(CompetitionType, related_name='events')
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
    organizer = models.ForeignKey(
        OrganizerEvent, on_delete=models.CASCADE, related_name='events', null=False
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
