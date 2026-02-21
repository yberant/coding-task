from django.contrib import admin
from django.urls import include, path

from accounts.views import dashboard_view, home_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("locations/", include("locations.urls")),
    path("dashboard/", dashboard_view, name="dashboard"),
    path("", home_view, name="home"),
]
