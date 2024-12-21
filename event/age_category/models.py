from django.db import models


class AgeCategory(models.Model):

    name = models.CharField(max_length=255)
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female')])
    ageFrom = models.PositiveIntegerField()
    ageTo = models.PositiveIntegerField()
    distance = models.ForeignKey(
        'distance_details.DistanceEvent',
        related_name='ageCategories',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.name} ({self.ageFrom}-{self.ageTo} age, {self.gender})'
