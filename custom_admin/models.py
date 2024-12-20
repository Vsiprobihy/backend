from django.db import models

from authentication.models import CustomUser


class OrganizerRequest(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='organizer_requests')
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request by {self.user.first_name} - {'Approved' if self.is_approved else 'Pending'}"
