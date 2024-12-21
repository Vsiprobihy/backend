from django.db import models

from authentication.models import CustomUser


class OrganizerRequest(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='organizerRequests')
    isApproved = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request by {self.user.firstName} - {'Approved' if self.isApproved else 'Pending'}"
