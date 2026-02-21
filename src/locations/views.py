import time

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from global_values import WEATHER_CODES

from .models import Location
from .repositories import (
    LocationRepository,
    WeatherSnapshotRepository,
)
from .services import (
    find_city_data,
    get_cached_weather_data,
    get_weather_data,
    set_cached_weather_data,
)

locationRepository = LocationRepository()
weatherSnapshotRepository = WeatherSnapshotRepository()


@login_required
@csrf_exempt
@api_view(["GET", "POST"])
def create_location_view(request):
    """
    Create a new location in the database.
    This view can receive two types of requests:
        1. By city name and country name (find_method='name')
        2. By latitude and longitude (find_method='coordinates')
    params (inside request params):
        find_method: str
        city_name: str
        country_name: str
        latitude: float
        longitude: float
    returns:
        Response
    """
    if request.method == "GET":
        return render(request, "locations/create_location.jinja2")

    elif request.method == "POST":
        find_method = request.POST.get("find_method")
        if find_method == "name":
            city_name_input = request.POST.get("city_name", "")
            country_name_input = request.POST.get("country_name", "")

            if not city_name_input or not country_name_input:
                messages.error(
                    request,
                    "Missing 'city_name' or 'country_name' in POST params for search by name mode",
                )
                return redirect("create_location")

            # Check if the city already exists to avoid unnecessary API calls
            # if Location.objects.filter(city=city_name_input, country=country_name_input).exists():
            if locationRepository.filter_location_by_name(
                city_name=city_name_input, country_name=country_name_input
            ):
                messages.error(
                    request,
                    f"City location: {city_name_input}, {country_name_input} already exists in database",
                )
                return redirect("create_location")

            city_data = find_city_data(
                city_name_input=city_name_input, country_name_input=country_name_input
            )

        elif find_method == "coordinates":
            lat_val = request.POST.get("latitude")
            lon_val = request.POST.get("longitude")
            if not lat_val or not lon_val:
                messages.error(
                    request,
                    "Missing 'latitude' or 'longitude' in POST params for search by coordinates mode",
                )
                return redirect("create_location")

            lat = float(lat_val)
            lon = float(lon_val)

            city_data = find_city_data(latitude_input=lat, longitude_input=lon)
        else:
            messages.error(
                request, "Invalid find method. Must be 'name' or 'coordinates'"
            )
            return redirect("create_location")

        if not city_data:
            messages.error(request, "City not found with those values")
            return redirect("create_location")

        city_name, country_name, lat, lon = city_data

        try:
            locationRepository.create_location(
                city_name=city_name,
                country_name=country_name,
                latitude=lat,
                longitude=lon,
            )
        except Exception as exception:
            messages.error(request, exception)
            return redirect("create_location")
        messages.success(
            request, f"City Location: {city_name}, {country_name} created successfully"
        )
        return redirect("dashboard")

    else:
        return Response(
            {"error": "Invalid method"}, status=status.HTTP_405_METHOD_NOT_ALLOWED
        )


@login_required
def list_locations_view(request):
    if request.method == "GET":
        locations = locationRepository.get_all_locations(order_by="-id")
        return render(
            request, "locations/tracked_locations.jinja2", {"locations": locations}
        )
    else:
        return Response(
            {"error": "Invalid method"}, status=status.HTTP_405_METHOD_NOT_ALLOWED
        )


def get_weather_data_view(request):
    if request.method == "GET":
        id = request.GET.get("id")
        if not id:
            return Response(
                {"error": "Missing 'id' in GET params"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        location = locationRepository.get_location_by_id(id)
        # refresh mode only would be true if this request was triggered by the refresh button
        refresh_mode = request.GET.get("refresh_mode", False)

        cached_weather_data = get_cached_weather_data(id)
        if cached_weather_data and not refresh_mode:
            weather_data = cached_weather_data
            error_msg = None
        else:
            # NOTE: this sleep is only here for testing loading state and cache retrieval
            time.sleep(1)
            weather_data, error_msg = get_weather_data(
                location.latitude, location.longitude
            )
            set_cached_weather_data(id, weather_data)
            try:
                weatherSnapshotRepository.create_weather_snapshot(
                    location, weather_data
                )
            except Exception as exception:
                # NOTE: in real production environments, this should send an error log to some monitorization service instead of a simple print
                print("Error creating weather snapshot: ", exception)
                messages.error(request, exception)

        # Get description and icon from global mapping
        # weather_code = weather_data.get('current', {}).get('weather_code', -1) if weather_data else -1
        if weather_data.get("current"):
            weather_code = weather_data.get("current").get("weather_code")
        else:
            weather_code = -1
        description, icon = WEATHER_CODES.get(weather_code, ("Unknown", "cloudy"))

        return render(
            request,
            "locations/tracked_weather_data.jinja2",
            {
                "weather_data": weather_data,
                "error_msg": error_msg,
                "location": location,
                "description": description,
                "icon": icon,
            },
        )
    else:
        return Response(
            {"error": "Invalid method"}, status=status.HTTP_405_METHOD_NOT_ALLOWED
        )


@login_required
@require_http_methods(["DELETE"])
def delete_location_view(request, location_id):
    try:
        location = locationRepository.get_location_by_id(location_id)
    except Exception as exception:
        return Response({"error": exception}, status=status.HTTP_404_NOT_FOUND)
    locationRepository.delete_location(location)

    response = HttpResponse()
    response["HX-Refresh"] = "true"
    return response


@login_required
def get_weather_shanpshots_of_location_view(request, location_id):
    try:
        location = locationRepository.get_location_by_id(location_id)
        weather_snapshots = location.weather_snapshots.all().order_by("-created_at")
        return render(
            request,
            "locations/weather_history.jinja2",
            {
                "weather_snapshots": weather_snapshots,
                "location": location,
                "WEATHER_CODES": WEATHER_CODES,
            },
        )
    except Exception as exception:
        return render(request, "error_page.jinja2", {"error": exception})
