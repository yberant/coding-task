from django.contrib import admin
from django.urls import path, include
from accounts.views import home_view, dashboard_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('', home_view, name='home'),
]
