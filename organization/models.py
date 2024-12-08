from django.db import models

from authentication.models import CustomUser


class Organization(models.Model):
    name = models.CharField(max_length=255)
    site_url = models.URLField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField()
    instagram_url = models.URLField(blank=True, null=True)
    facebook_url = models.URLField(blank=True, null=True)
    telegram_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name


class Organizer(models.Model):
    OWNER = 'owner'
    MODERATOR = 'organizer'

    ROLE_CHOICES = [
        (OWNER, 'Owner'),
        (MODERATOR, 'Organizer'),
    ]

    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='organizer_user', null=False
    )
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name='organizer_organization', null=False
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, null=False)

    class Meta:
        unique_together = ('user', 'organization')

    def __str__(self):
        return (
            f'{self.user.email} - {self.get_role_display()} в {self.organization.name}'
        )
