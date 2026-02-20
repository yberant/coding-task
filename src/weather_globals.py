# Open-Meteo weather code descriptions
WEATHER_CODES = {
    0: ('Clear sky', 'sunny'),
    1: ('Mainly clear', 'sunny'),
    2: ('Partly cloudy', 'cloudy'),
    3: ('Overcast', 'cloudy'),
    45: ('Foggy', 'fog'),
    48: ('Depositing rime fog', 'fog'),
    51: ('Light drizzle', 'drizzle'),
    53: ('Moderate drizzle', 'drizzle'),
    55: ('Dense drizzle', 'drizzle'),
    61: ('Slight rain', 'rain'),
    63: ('Moderate rain', 'rain'),
    65: ('Heavy rain', 'rain'),
    71: ('Slight snow', 'snow'),
    73: ('Moderate snow', 'snow'),
    75: ('Heavy snow', 'snow'),
    77: ('Snow grains', 'snow'),
    80: ('Slight rain showers', 'rain'),
    81: ('Moderate rain showers', 'rain'),
    82: ('Violent rain showers', 'rain'),
    85: ('Slight snow showers', 'snow'),
    86: ('Heavy snow showers', 'snow'),
    95: ('Thunderstorm', 'storm'),
    96: ('Thunderstorm with slight hail', 'storm'),
    99: ('Thunderstorm with heavy hail', 'storm'),
}

def format_weather_data(raw_data: dict) -> dict:
    """
    Formats raw weather data from Open-Meteo into a structured dictionary.
    """
    current = raw_data.get('current', {})
    weather_code = current.get('weather_code')
    description, icon = WEATHER_CODES.get(weather_code, ('Unknown', 'cloudy'))
    
    return {
        'temperature': round(current.get('temperature_2m', 0)),
        'feels_like': round(current.get('apparent_temperature', 0)),
        'humidity': round(current.get('relative_humidity_2m', 0)),
        'description': description,
        'icon': icon,
        'wind_speed': round(current.get('wind_speed_10m', 0)),
        'pressure': round(current.get('pressure_msl', 0)),
    }
