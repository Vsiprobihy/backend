import os

from django.contrib.postgres.fields import ArrayField
from django.db import models

from authentication.models import CustomUser
from utils.data_validatiors import process_image, validate_file_size, validate_image_file


def organization_main_image_path(instance, filename):
    """Path to save the main image of the organization."""
    _, extension = os.path.splitext(filename)
    filename = f'organization-{instance.id}-main{extension}'
    return os.path.join('uploads/organization/main_images/', filename)


def organization_background_image_path(instance, filename):
    """Path to save the organization's background image."""
    _, extension = os.path.splitext(filename)
    filename = f'organization-{instance.id}-background{extension}'
    return os.path.join('uploads/organization/background_images/', filename)


class Organization(models.Model):
    name = models.CharField(max_length=255)
    siteUrl = models.URLField(blank=True, null=True)
    phoneNumbers = ArrayField(
        models.CharField(max_length=20), blank=True, default=list
    )
    email = models.EmailField()
    instagramUrl = models.URLField(blank=True, null=True)
    facebookUrl = models.URLField(blank=True, null=True)
    telegramUrl = models.URLField(blank=True, null=True)
    mainImage = models.ImageField(
        upload_to=organization_main_image_path,
        blank=True,
        null=True,
        max_length=255,
        validators=[validate_image_file, validate_file_size]
    )
    backgroundImage = models.ImageField(
        upload_to=organization_background_image_path,
        blank=True,
        null=True,
        max_length=255,
        validators=[validate_image_file, validate_file_size]
    )

    def save(self, *args, **kwargs):
        # Process images before saving them to the database
        if self.mainImage:
            process_image(self.mainImage, size=(300, 300))
        if self.backgroundImage:
            process_image(self.backgroundImage)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Organizer(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='organizerUser', null=False
    )
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name='organizerOrganization', null=False
    )

    class Meta:
        unique_together = ('user', 'organization')

    def __str__(self):
        return (
            f'{self.user.email} - {self.user.role} в {self.organization.name}'
        )
