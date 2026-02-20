from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError

from .services import find_city_data, get_weather_data
from .models import Location
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods


@login_required
@csrf_exempt
@api_view(['GET', 'POST'])
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
    if request.method == 'GET':
        return render(request, 'locations/create_location.jinja2')

    elif request.method == 'POST':
        find_method = request.POST.get('find_method')
        if find_method == 'name':
            city_name_input = request.POST.get('city_name', '')
            country_name_input = request.POST.get('country_name', '')
            
            if not city_name_input or not country_name_input:
                messages.error(request, "Missing 'city_name' or 'country_name' in POST params for search by name mode")
                return redirect('create_location')
            
            # Check if the city already exists to avoid unnecessary API calls
            if Location.objects.filter(city=city_name_input, country=country_name_input).exists():
                messages.error(request, f"City location: {city_name_input}, {country_name_input} already exists in database")
                return redirect('create_location')

            city_data = find_city_data(city_name_input=city_name_input, country_name_input=country_name_input)

        elif find_method == 'coordinates':
            lat_val = request.POST.get('latitude')
            lon_val = request.POST.get('longitude')
            if not lat_val or not lon_val:
                messages.error(request, "Missing 'latitude' or 'longitude' in POST params for search by coordinates mode")
                return redirect('create_location')
            
            lat = float(lat_val)
            lon = float(lon_val)
            
            city_data = find_city_data(latitude_input=lat, longitude_input=lon)
        else:
            messages.error(request, "Invalid find method. Must be 'name' or 'coordinates'")
            return redirect('create_location')

        if not city_data:
            messages.error(request, "City not found with those values")
            return redirect('create_location')
            
        city_name, country_name, lat, lon = city_data

        try:
            Location.objects.create(
                city=city_name,
                country=country_name,
                latitude=lat,
                longitude=lon,
            )
            messages.success(request, f"City Location: {city_name}, {country_name} created successfully")
            return redirect('dashboard')
        except IntegrityError:
            messages.error(request, f"Found City location ({city_name}, {country_name}) already exists in database")
            return redirect('create_location')
        
    else:
        return Response({"error": "Invalid method"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@login_required
def list_locations_view(request):
    if request.method == 'GET':
        locations = Location.objects.all().order_by('-id')
        return render(request, 'locations/tracked_locations.jinja2', {
            'locations': locations
        })
    else:
        return Response({"error": "Invalid method"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


import time
# TODO: implement CACHE
def get_weather_data_view(request):
    if request.method == "GET":
        id = request.GET.get('id')
        if not id:
            return Response({"error": "Missing 'id' in GET params"}, status=status.HTTP_400_BAD_REQUEST)
        location = Location.objects.get(id=id)
        # TODO: delete this. this only for testing loading state
        time.sleep(2)
        weather_data, error_msg = get_weather_data(location.latitude, location.longitude)
        return render(request, 'locations/tracked_weather_data.jinja2', {
            'weather_data': weather_data,
            'error_msg': error_msg,
            'location': location,
        })
    else:
        return Response({"error": "Invalid method"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@login_required
@require_http_methods(["DELETE"])
def delete_location_view(request, location_id):
    try:
        location = Location.objects.get(id=location_id)
    except Location.DoesNotExist:
        return Response({"error": f"Location with id: {location_id} not found"}, status=status.HTTP_404_NOT_FOUND)
    location.delete()

    response = HttpResponse()
    response['HX-Refresh'] = 'true'
    return response