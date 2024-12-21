from django.db import models
from django.utils.timezone import now

from authentication.models import CustomUser
from event.distance_details.models import DistanceEvent


class UserDistanceRegistration(models.Model):
    registration_date = models.DateTimeField(default=now)
    is_confirmed = models.BooleanField(default=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='distance_registrations')
    distance = models.ForeignKey(DistanceEvent, on_delete=models.CASCADE, related_name='user_registrations')

    class Meta:
        unique_together = ('user', 'distance')

    def __str__(self):
        return f'Registration of {self.user.first_name} for {self.distance.name}'
