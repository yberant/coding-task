from django.urls import path

from . import views

urlpatterns = [
    path("create/", views.create_location_view, name="create_location"),
    path("list/", views.list_locations_view, name="list_locations"),
    path(
        "delete/<int:location_id>/", views.delete_location_view, name="delete_location"
    ),
    path("get-weather/", views.get_weather_data_view, name="get_weather_data"),
    path(
        "weather-history/<int:location_id>/",
        views.get_weather_shanpshots_of_location_view,
        name="weather_history",
    ),
]
