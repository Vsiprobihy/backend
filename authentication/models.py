from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from authentication.managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    T_SHIRT_SIZE_CHOICES = [
        ('XXS', 'Very Extra Small'),
        ('XS', 'Extra Small'),
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
        ('XXL', 'Extra Extra Large'),
        ('XXXL', 'Very Extra Extra Large'),
    ]

    USER = 'user'
    ORGANIZER = 'organizer'
    ADMIN = 'admin'

    ROLE_CHOICES = [
        (USER, 'User'),
        (ORGANIZER, 'Organizer'),
        (ADMIN, 'Administrator'),
    ]

    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female')], null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    t_shirt_size = models.CharField(max_length=5, choices=T_SHIRT_SIZE_CHOICES, null=True, blank=True)

    country = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)

    sports_club = models.CharField(max_length=100, null=True, blank=True)
    emergency_contact_name = models.CharField(max_length=100, null=True, blank=True)
    emergency_contact_phone = models.CharField(max_length=20, null=True, blank=True)
    events_registered = models.ManyToManyField('event.Event', through='event.EventRegistration', related_name='registered_users')

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=USER)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email
