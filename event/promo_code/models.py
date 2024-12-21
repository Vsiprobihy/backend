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
    promoType = models.CharField(max_length=20, choices=PROMO_TYPE_CHOICES)
    discountValue = models.DecimalField(max_digits=10, decimal_places=2)
    isActive = models.BooleanField(default=False)
    isSingleUse = models.BooleanField(default=False)
    distance = models.ForeignKey(
        'distance_details.DistanceEvent',
        related_name='promoCodes',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.name} - {self.get_promoType_display()} ({self.discountValue})'
