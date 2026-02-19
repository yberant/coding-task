from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest

from .models import Location


@login_required
def create_location_view(request):

    if request.method == 'POST':
        pass
    else:
        return HttpResponseBadRequest("Invalid method")

@login_required
def list_locations_view(request):
    if request.method == 'GET':
        print("list locations")
        locations = Location.objects.all()
        return HttpResponse(f"list locations {locations.count()}")
    else:
        return HttpResponseBadRequest("Invalid method")


@login_required
def delete_location_view(request):
    if request.method == 'DELETE':
        pass
    else:
        return HttpResponseBadRequest("Invalid method")
