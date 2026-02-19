from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Location(models.Model):
    city = models.CharField(max_length=90) # longest city name is 86 chars
    country = models.CharField(max_length=60) # longest country name in 56 chars
    latitude = models.FloatField(
        validators=[
            MinValueValidator(-90),
            MaxValueValidator(90),
        ]
    )
    longitude = models.FloatField(
        validators=[
            MinValueValidator(-180),
            MaxValueValidator(180),
        ]
    )

    class Meta:
        unique_together = [['city', 'country']]