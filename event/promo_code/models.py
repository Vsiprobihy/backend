from django.db import models


class PromoCode(models.Model):
    FLAT_DISCOUNT = 'flat'
    PERCENTAGE_DISCOUNT = 'percentage'
    SUM_REGISTRATION = 'sum_registration'
    FREE = 'free'
    PROMO_TYPE_CHOICES = [
        (FLAT_DISCOUNT, 'Flat Discount'),
        (PERCENTAGE_DISCOUNT, 'Percentage Discount'),
        (SUM_REGISTRATION, 'Sum Registration Discount'),
        (FREE, 'Free Discount'),
    ]

    name = models.CharField(max_length=255)
    promo_type = models.CharField(max_length=20, choices=PROMO_TYPE_CHOICES)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=False)
    is_single_use = models.BooleanField(default=False)
    distance = models.ForeignKey(
        'distance_details.DistanceEvent',
        related_name='promo_codes',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.name} - {self.get_promo_type_display()} ({self.discount_value})'
