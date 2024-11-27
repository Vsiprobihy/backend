from django.db import models


class AgeCategory(models.Model):

    name = models.CharField(max_length=255)
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female')])
    age_from = models.PositiveIntegerField()
    age_to = models.PositiveIntegerField()
    distance = models.ForeignKey(
        'distance_details.DistanceEvent',
        related_name='age_categories',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.name} ({self.age_from}-{self.age_to} age, {self.gender})'
