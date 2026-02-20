from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, SignInForm
from global_values import WEATHER_CODES
import requests

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = SignUpForm()

    return render(request, 'accounts/signup.jinja2', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = SignInForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = SignInForm()

    return render(request, 'accounts/login.jinja2', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


def home_view(request):
    return render(request, 'home.jinja2')


@login_required
def dashboard_view(request):
    weather_data = None
    error_message = None

    # Default fallback location (London, UK)
    lat, lon, city, country = 51.5074, -0.1278, 'London', 'United Kingdom'
    location_source = 'default'

    try:
        # Try to get user's location from IP
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')

        # For localhost, try to get external IP
        if ip in ('127.0.0.1', 'localhost', '::1'):
            try:
                ip_response = requests.get('https://api.ipify.org?format=json', timeout=5)
                if ip_response.status_code == 200:
                    ip = ip_response.json().get('ip')
            except:
                pass

        # Get location from IP
        try:
            geo_response = requests.get(f'http://ip-api.com/json/{ip}', timeout=5)
            if geo_response.status_code == 200:
                geo_data = geo_response.json()
                if geo_data.get('status') == 'success':
                    lat = geo_data.get('lat')
                    lon = geo_data.get('lon')
                    city = geo_data.get('city', 'Unknown')
                    country = geo_data.get('country', '')
                    location_source = 'ip'
        except:
            pass

        # Fetch weather from Open-Meteo (no API key required)
        weather_url = (
            f'https://api.open-meteo.com/v1/forecast?'
            f'latitude={lat}&longitude={lon}&'
            f'current=temperature_2m,relative_humidity_2m,apparent_temperature,'
            f'weather_code,pressure_msl,wind_speed_10m'
        )
        weather_response = requests.get(weather_url, timeout=10)

        if weather_response.status_code == 200:
            data = weather_response.json()
            current = data['current']
            weather_code = current['weather_code']
            description, icon = WEATHER_CODES.get(weather_code, ('Unknown', 'cloudy'))

            weather_data = {
                'city': city,
                'country': country,
                'temperature': round(current['temperature_2m']),
                'feels_like': round(current['apparent_temperature']),
                'humidity': round(current['relative_humidity_2m']),
                'description': description,
                'icon': icon,
                'wind_speed': round(current['wind_speed_10m']),
                'pressure': round(current['pressure_msl']),
                'location_source': location_source,
            }
        else:
            error_message = f"Weather API error: {weather_response.status_code}"
    except requests.RequestException as e:
        error_message = f"Network error: {str(e)}"
    except (KeyError, ValueError) as e:
        error_message = f"Error parsing weather data: {str(e)}"

    

    return render(request, 'dashboard.jinja2', {
        'weather': weather_data,
        'error_message': error_message,
    })
