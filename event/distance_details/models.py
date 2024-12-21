from django.db import models

from authentication.models import CustomUser
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
        'event.Event', related_name='distances', on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class FavoriteDistance(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='favorite_distances'
    )
    distance = models.ForeignKey(
        DistanceEvent,
        on_delete=models.CASCADE,
        related_name='favorite_by'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'distance')

    def __str__(self):
        return f'{self.user.email} - {self.distance.name}'


class CostChangeRule(models.Model):
    distance = models.ForeignKey(
        'distance_details.DistanceEvent',
        related_name='cost_change_rules',
        on_delete=models.CASCADE,
        db_index=True
    )
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    from_participants = models.PositiveIntegerField(null=True, blank=True)
    from_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'Cost: {self.cost}, From Participants: {self.from_participants}, From Date: {self.from_date}'
