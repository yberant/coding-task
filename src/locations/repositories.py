from typing import Optional

from django.db import IntegrityError, transaction
from django.db.models import QuerySet

from .models import Location, WeatherSnapshot


class LocationRepository:
    def get_all_locations(self, order_by: str = "-id") -> QuerySet:
        """
        Returns all locations ordered by the given order_by parameter.

        params:

        """
        return Location.objects.order_by(order_by)

    def filter_location_by_name(self, city_name: str, country_name: str) -> QuerySet:
        """
        Returns all locations filtered by the given city_name and country_name parameters.
        """
        return Location.objects.filter(city=city_name, country=country_name)

    def get_location_by_id(self, id: int) -> Optional[Location]:
        """
        Returns the location with the given id.

        params:
            id (int): The id of the location.
        """
        try:
            return Location.objects.get(id=id)
        except Location.DoesNotExist as exception:
            raise Location.DoesNotExist(f"Location with id {id} not found")
        except Exception as exception:
            raise Exception(f"Error getting location by id: {exception}")

    def create_location(
        self, city_name: str, country_name: str, latitude: float, longitude: float
    ) -> Optional[Location]:
        """
        Creates a new location.

        params:
            city_name (str): The name of the city.
            country_name (str): The name of the country.
            latitude (float): The latitude of the location.
            longitude (float): The longitude of the location.
        """

        try:
            with transaction.atomic():
                return Location.objects.create(
                    city=city_name,
                    country=country_name,
                    latitude=latitude,
                    longitude=longitude,
                )
        except IntegrityError:
            raise IntegrityError(
                f"Location: {city_name}, {country_name} with latitude: {latitude}, longitude: {longitude} already exists",
            )
        except Exception as exception:
            raise Exception(f"Error creating location: {exception}") from exception

    def delete_location(self, location: Location) -> Location:
        """
        Deletes a location.

        params:
            location (Location): The location to delete.
        """
        location.delete()
        return location


class WeatherSnapshotRepository:
    def create_weather_snapshot(
        self,
        location: Location,
        weather_data: dict,
    ) -> Optional[WeatherSnapshot]:
        """
        Creates a new weather snapshot for the given location.
        """
        try:
            current_weather_data = weather_data.get("current")
            new_snapshot = WeatherSnapshot(
                **{
                    "temperature_2m": current_weather_data.get("temperature_2m"),
                    "relative_humidity_2m": current_weather_data.get(
                        "relative_humidity_2m"
                    ),
                    "apparent_temperature": current_weather_data.get(
                        "apparent_temperature"
                    ),
                    "weather_code": current_weather_data.get("weather_code"),
                    "surface_pressure": current_weather_data.get("pressure_msl"),
                    "wind_speed_10m": current_weather_data.get("wind_speed_10m"),
                }
            )
            new_snapshot.location = location
            with transaction.atomic():
                new_snapshot.save()

            # verify if there is more than 5 associated snapshots. Delete the oldest one if so.
            if location.weather_snapshots.count() > 5:
                location.weather_snapshots.order_by("created_at").first().delete()

            return new_snapshot
        except Exception as exception:
            raise Exception(f"Error creating weather snapshot: {exception}")
