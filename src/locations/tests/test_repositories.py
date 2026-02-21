from django.db import IntegrityError
from django.test import TestCase

from ..models import Location, WeatherSnapshot
from ..repositories import (
    LocationRepository,
    WeatherSnapshotRepository,
)


class LocationModelTest(TestCase):

    def setUp(self):
        self.location_repository = LocationRepository()
        self.location1 = Location.objects.create(
            city="Santiago",
            country="Chile",
            latitude=-33.45,
            longitude=-70.67,
        )
        self.location2 = Location.objects.create(
            city="Sao Paulo",
            country="Brazil",
            latitude=-23.55,
            longitude=-46.63,
        )

    def test_find_location_by_id__success(self):
        """
        success test: Test that a location can be found by its id with get_location_by_id
        """
        location = self.location_repository.get_location_by_id(self.location1.id)
        location_id = location.id

        found_location = self.location_repository.get_location_by_id(location_id)
        self.assertEqual(location_id, found_location.id)

    def test_find_location_by_id__failure(self):
        """
        failure test: Test that if get_location_by_id is passed a non existant id, a DoesNotExist exception is raised
        """
        not_existant_id = Location.objects.all().last().id + 1
        with self.assertRaises(Location.DoesNotExist):
            self.location_repository.get_location_by_id(not_existant_id)

    def test_get_all_locations__success(self):
        """
        success test: Test that all locations are returned with get_all_locations
        """
        locations = self.location_repository.get_all_locations()
        self.assertQuerySetEqual(
            locations,
            Location.objects.all(),
            lambda x: x,
            ordered=False,
        )

    def test_create_location__success(self):
        """
        success test: Test that a location can be created with create_location, assuring that the city name/country name and latitude/longitude dont already exist in the database
        """
        new_city = "Paris"
        new_country = "France"
        new_latitude = 48.8566
        new_longitude = 2.3522
        # before, ill make sure the location doesn't exist
        self.assertFalse(
            Location.objects.filter(
                city=new_city,
                country=new_country,
            ).exists()
        )
        self.assertFalse(
            Location.objects.filter(
                latitude=new_latitude,
                longitude=new_longitude,
            ).exists()
        )

        new_location = self.location_repository.create_location(
            new_city,
            new_country,
            new_latitude,
            new_longitude,
        )
        self.assertEqual(new_location.city, new_city)
        self.assertEqual(new_location.country, new_country)
        self.assertEqual(new_location.latitude, new_latitude)
        self.assertEqual(new_location.longitude, new_longitude)
        self.assertTrue(Location.objects.get(id=new_location.id))

    def test_create_location__already_exists_failure(self):
        """
        failure test: Test that if create_location is passed a city name/country name and latitude/longitude that already exist in the database, an IntegrityError is raised
        """
        with self.assertRaises(IntegrityError):
            self.location_repository.create_location(
                self.location1.city,
                self.location1.country,
                0,
                0,
            )

        with self.assertRaises(IntegrityError):
            self.location_repository.create_location(
                "Paris",
                "France",
                self.location1.latitude,
                self.location1.longitude,
            )


class WeatherSnapshotModelTest(TestCase):
    def setUp(self):
        self.weather_snapshot_repository = WeatherSnapshotRepository()
        self.location1 = Location.objects.create(
            city="Santiago",
            country="Chile",
            latitude=-33.45,
            longitude=-70.67,
        )

    def test_create_weather_snapshot__success(self):
        """
        success test: Test that a weather snapshot can be created with create_weather_snapshot
        """
        # 'mocked' weather, based on the response from the open-meteo api
        weather_data = {
            "latitude": 39.5,
            "longitude": -0.375,
            "current": {
                "temperature_2m": 17.7,
                "relative_humidity_2m": 32,
                "apparent_temperature": 15.7,
                "weather_code": 0,
                "pressure_msl": 1032.1,
                "wind_speed_10m": 4.8,
            },
        }
        weather_snapshot = self.weather_snapshot_repository.create_weather_snapshot(
            self.location1,
            weather_data,
        )
        self.assertEqual(weather_snapshot.location, self.location1)
        self.assertEqual(weather_snapshot.temperature_2m, 17.7)
        self.assertEqual(weather_snapshot.relative_humidity_2m, 32)
        self.assertEqual(weather_snapshot.apparent_temperature, 15.7)
        self.assertEqual(weather_snapshot.weather_code, 0)
        self.assertEqual(weather_snapshot.surface_pressure, 1032.1)
        self.assertEqual(weather_snapshot.wind_speed_10m, 4.8)
        self.assertTrue(WeatherSnapshot.objects.get(id=weather_snapshot.id))
