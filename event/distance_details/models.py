from django.db import models

from authentication.models import CustomUser
from utils.constants.constants_distance import CATEGORY_CHOICES
from utils.constants.constants_event import COMPETITION_TYPES


class DistanceEvent(models.Model):

    name = models.CharField(max_length=255)
    competitionType = models.CharField(
        max_length=50, choices=COMPETITION_TYPES, default='running'
    )
    category = models.CharField(
        max_length=50, choices=CATEGORY_CHOICES, default='adults'
    )
    length = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )  # Distance in km or meters
    startNumberFrom = models.PositiveIntegerField(blank=True, null=True)
    startNumberTo = models.PositiveIntegerField(blank=True, null=True)
    showStartNumber = models.BooleanField(default=False)
    showNameOnNumber = models.BooleanField(default=False)
    ageFrom = models.PositiveIntegerField(blank=True, null=True)
    ageTo = models.PositiveIntegerField(blank=True, null=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    isFree = models.BooleanField(default=False)
    promoOnlyRegistration = models.BooleanField(default=False)
    allowRegistration = models.BooleanField(default=True)
    event = models.ForeignKey(
        'event.Event', related_name='distances', on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class FavoriteDistance(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='favoriteDistances'
    )
    distance = models.ForeignKey(
        DistanceEvent,
        on_delete=models.CASCADE,
        related_name='favoriteBy'
    )
    createdAt = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'distance')

    def __str__(self):
        return f'{self.user.email} - {self.distance.name}'


class CostChangeRule(models.Model):
    distance = models.ForeignKey(
        'distance_details.DistanceEvent',
        related_name='costChangeRules',
        on_delete=models.CASCADE,
        db_index=True
    )
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    fromParticipants = models.PositiveIntegerField(null=True, blank=True)
    fromDate = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'Cost: {self.cost}, From Participants: {self.fromParticipants}, From Date: {self.fromDate}'
