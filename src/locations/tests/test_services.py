from unittest.mock import patch

from django.core.cache import cache
from django.test import TestCase

from ..services import (
    ApiCallService,
    CacheService,
)
from .mocks import (
    MOCK_CACHE_DATA,
    MOCK_GEOCODING_API_RESPONSE,
    MOCK_WEATHER_API_RESPONSE,
)


class TestApiServices(TestCase):

    def setUp(self):
        self.apiCallService = ApiCallService()

    @patch("locations.services.requests.get")
    def test__find_city_data__find_by_name_success(self, mock_get):
        """
        success test: Test that find_city_data can find a city by name and country name, mocking the api call response
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = MOCK_GEOCODING_API_RESPONSE

        city_name_input = (
            MOCK_GEOCODING_API_RESPONSE.get("results")[0]
            .get("address_components")[0]
            .get("long_name")
        )
        country_name_input = (
            MOCK_GEOCODING_API_RESPONSE.get("results")[0]
            .get("address_components")[1]
            .get("long_name")
        )

        result = self.apiCallService.find_city_data(
            city_name_input=city_name_input, country_name_input=country_name_input
        )
        self.assertEqual(
            result,
            (
                city_name_input,
                country_name_input,
                MOCK_GEOCODING_API_RESPONSE.get("results")[0]
                .get("geometry")
                .get("location")
                .get("lat"),
                MOCK_GEOCODING_API_RESPONSE.get("results")[0]
                .get("geometry")
                .get("location")
                .get("lng"),
            ),
        )

    @patch("locations.services.requests.get")
    def test__find_city_data__find_by_latlng_success(self, mock_get):
        """
        success test: Test that find_city_data can find a city by latitude and longitude, mocking the api call response
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = MOCK_GEOCODING_API_RESPONSE

        latitude_input = (
            MOCK_GEOCODING_API_RESPONSE.get("results")[0]
            .get("geometry")
            .get("location")
            .get("lat")
        )
        longitude_input = (
            MOCK_GEOCODING_API_RESPONSE.get("results")[0]
            .get("geometry")
            .get("location")
            .get("lng")
        )

        result = self.apiCallService.find_city_data(
            latitude_input=latitude_input, longitude_input=longitude_input
        )
        self.assertEqual(
            result,
            (
                MOCK_GEOCODING_API_RESPONSE.get("results")[0]
                .get("address_components")[0]
                .get("long_name"),
                MOCK_GEOCODING_API_RESPONSE.get("results")[0]
                .get("address_components")[1]
                .get("long_name"),
                latitude_input,
                longitude_input,
            ),
        )

    @patch("locations.services.requests.get")
    def test__find_city_data__not_found_failure(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"results": []}
        result = self.apiCallService.find_city_data(
            city_name_input="some city", country_name_input="some country"
        )
        self.assertIsNone(result)

    @patch("locations.services.requests.get")
    def test__find_city_data__server_error_failure(self, mock_get):
        mock_get.return_value.status_code = 500
        text_error = "some error"
        mock_get.return_value.response.text = text_error
        with self.assertRaises(
            ValueError, msg=f"Error fetching city data: {text_error}"
        ):
            self.apiCallService.find_city_data(
                city_name_input="some city", country_name_input="some country"
            )

    @patch("locations.services.requests.get")
    def test__get_weather_data__success(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = MOCK_WEATHER_API_RESPONSE
        result = self.apiCallService.get_weather_data(latitude=0, longitude=0)
        self.assertEqual(result, MOCK_WEATHER_API_RESPONSE)

    @patch("locations.services.requests.get")
    def test__get_weather_data__server_error_failure(self, mock_get):
        mock_get.return_value.status_code = 500
        text_error = "some error"
        mock_get.return_value.text = text_error
        with self.assertRaises(
            Exception, msg=f"Error fetching weather data: {text_error}"
        ):
            self.apiCallService.get_weather_data(latitude=0, longitude=0)


class testCache(TestCase):
    def setUp(self):
        cache.clear()
        self.cacheService = CacheService()

    def test__get_cached_weather_data__unexistent_key(self):
        unexistent_location_id = 1
        self.assertIsNone(
            self.cacheService.get_cached_weather_data(unexistent_location_id)
        )

    def test__get_cached_weather_data__existent_key(self):
        location_id = 1
        weather_data = MOCK_CACHE_DATA
        self.cacheService.set_cached_weather_data(location_id, weather_data)
        self.assertEqual(
            self.cacheService.get_cached_weather_data(location_id), weather_data
        )

    def test__set_cached_weather_data__success(self):
        location_id = 1
        weather_data = MOCK_CACHE_DATA
        self.cacheService.set_cached_weather_data(location_id, weather_data)
        self.assertEqual(
            self.cacheService.get_cached_weather_data(location_id), weather_data
        )
