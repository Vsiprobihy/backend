from django.db import models

from utils.constants.constants_distance import CATEGORY_CHOICES
from utils.constants.constants_event import COMPETITION_TYPES


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
        'organizer_event.Event', related_name='distances', on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name
