from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Location(models.Model):
    city = models.CharField(max_length=90)  # longest city name is 86 chars
    country = models.CharField(max_length=60)  # longest country name in 56 chars
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
        unique_together = [["city", "country"], ["latitude", "longitude"]]


class WeatherSnapshot(models.Model):
    location = models.ForeignKey(
        Location, on_delete=models.CASCADE, related_name="weather_snapshots"
    )
    temperature_2m = models.FloatField()
    relative_humidity_2m = models.FloatField()
    apparent_temperature = models.FloatField()
    weather_code = models.IntegerField()
    surface_pressure = models.FloatField()
    wind_speed_10m = models.FloatField()

    created_at = models.DateTimeField(auto_now_add=True)
