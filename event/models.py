from django.db import models

from authentication.models import CustomUser


class OrganizerEvent(models.Model):
    name = models.CharField(max_length=255)
    site_url = models.URLField(blank=True, null=True)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    instagram_url = models.URLField(blank=True, null=True)
    facebook_url = models.URLField(blank=True, null=True)
    telegram_url = models.URLField(blank=True, null=True)

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
    event = models.ForeignKey('Event', related_name='additional_items', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.get_item_type_display()} - {self.price}"


class DistanceEvent(models.Model):
    name = models.CharField(max_length=255)
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_free = models.BooleanField(default=False)
    event = models.ForeignKey('Event', related_name='distances', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Event(models.Model):
    COMPETITION_TYPES = [
        ('running', 'Біг'),
        ('trail', 'Трейл'),
        ('ultramarathon', 'Ультрамарафон'),
        ('cycling', 'Велоспорт'),
        ('online', 'Online'),
        ('walking', 'Ходьба'),
        ('ocr', 'OCR'),
        ('swimming', 'Плавання'),
        ('triathlon', 'Тріатлон'),
    ]

    name = models.CharField(max_length=255)
    competition_type = models.CharField(max_length=50, choices=COMPETITION_TYPES)
    date_from = models.DateField()
    date_to = models.DateField()
    place = models.CharField(max_length=255)
    photos = models.ImageField(upload_to='event_photos/', blank=True, null=True)
    description = models.TextField()
    registration_link = models.URLField(blank=True, null=True)
    hide_participants = models.BooleanField(default=False)
    extended_description = models.TextField(blank=True, null=True)
    schedule_pdf = models.FileField(upload_to='event_schedule/', blank=True, null=True)
    organizer = models.ForeignKey(OrganizerEvent, on_delete=models.CASCADE, related_name='events')

    def __str__(self):
        return self.name


class EventRegistration(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='registrations')
    event = models.ForeignKey('Event', on_delete=models.CASCADE, related_name='registrations')
    distances = models.ManyToManyField('DistanceEvent', blank=True, related_name='registrations')
    additional_items = models.ManyToManyField('AdditionalItemEvent', blank=True, related_name='registrations')
    registration_date = models.DateTimeField(auto_now_add=True)
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.email} registered for {self.event.name} on {self.registration_date}"

