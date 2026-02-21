from django.contrib import admin

from .models import Location, WeatherSnapshot

admin.site.register(Location)
admin.site.register(WeatherSnapshot)
