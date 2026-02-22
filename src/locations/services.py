import os
from typing import Optional

import requests
from django.core.cache import cache


def get_cached_weather_data(location_id: int):
    """
    Gets the weather data from the cache for a given location id.
    """
    try:
        cache_key = f"weather_{location_id}"
        return cache.get(cache_key)
    except Exception as exception:
        # NOTE: in production this should be logged
        print(f"error getting cache of snapshot for city: {location_id}, {exception}")
        return None


def set_cached_weather_data(location_id: int, weather_data: dict):
    """
    Sets the weather data in the cache for a given location id.
    The cache will expire in 15 minutes.
    """
    try:
        cache_key = f"weather_{location_id}"
        cache.set(cache_key, weather_data, timeout=60 * 15)
    except Exception as exception:
        # NOTE: in production this should be logged
        print(f"error setting cache of snapshot for city: {location_id}, {exception}")

def find_city_data(**kwargs) -> Optional[tuple[str, str, float, float]]:
    """
    Find city data quering the google geolocation API, return a tuple with the following values in order:
        - city name (as appears from the api result)
        - country name (as appears from the api result)
        - centralized latitude (as appears from the api result)
        - centralized longitude (as appears from the api result)
    If the city is not found, returns None instead.
    As for the params, we can search by:
        - city name and country name (city_name_input: str, country_name_input: str)
        - latitude and longitude (latitude_input: float, longitude_input: float)
    """

    latitude_input = kwargs.get("latitude_input")
    longitude_input = kwargs.get("longitude_input")
    city_name_input = kwargs.get("city_name_input")
    country_name_input = kwargs.get("country_name_input")

    api_key = os.getenv("GEOCODING_API_KEY")

    params = ""
    if latitude_input and longitude_input:
        params += f"latlng={latitude_input},{longitude_input}"
    elif city_name_input and country_name_input:
        params += f"address={city_name_input}, {country_name_input}"
    else:
        raise ValueError("Missing latitude and longitude or city and country name")
    url = f"https://maps.googleapis.com/maps/api/geocode/json?{params}&key={api_key}&result_type=locality&language=en"
    response = requests.get(url)
    if response.status_code == 200 and response.json().get("results"):
        city_data = response.json()
        address_components = city_data.get("results")[0].get("address_components")

        # find city name and country name (as appears from the api result (Is important that we have a consistent source instead of saving human typed values in the database
        city_name = next(
            (
                component["long_name"]
                for component in address_components
                if "locality" in component["types"]
            ),
            None,
        )
        country_name = next(
            (
                component["long_name"]
                for component in address_components
                if "country" in component["types"]
            ),
            None,
        )

        if city_name and country_name:
            lat = city_data.get("results")[0].get("geometry").get("location").get("lat")
            lng = city_data.get("results")[0].get("geometry").get("location").get("lng")
            return city_name, country_name, lat, lng
    elif response.status_code != 200:
        raise ValueError("Error fetching city data: " + response.text)
    return None


def get_weather_data(
    latitude: float,
    longitude: float,
) -> Optional[dict]:
    """
    Uses Open-Meteo Forecast API to get current weather data for a given latitude and longitude.
    if the request is successful, returns the weather data.
    if the request fails, raises an exception.

    Args:
        latitude (float):  Latitude of the location.
        longitude (float): Longitude of the location.


    """
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,pressure_msl,wind_speed_10m"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error fetching weather data: {response.text}")
