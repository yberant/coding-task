MOCK_GEOCODING_API_RESPONSE = {
    "results": [
        {
            "address_components": [
                {
                    "long_name": "Santiago",
                    "types": ["locality", "political"],
                },
                {
                    "long_name": "Chile",
                    "types": ["country", "political"],
                },
            ],
            "geometry": {
                "location": {
                    "lat": 33.6844,
                    "lng": -70.3697,
                }
            },
        }
    ]
}

MOCK_WEATHER_API_RESPONSE = {
    "latitude": -33.5,
    "longitude": -70.625,
    "generationtime_ms": 0.09179115295410156,
    "utc_offset_seconds": -10800,
    "timezone": "America/Santiago",
    "timezone_abbreviation": "GMT-3",
    "elevation": 538.0,
    "current_units": {
        "time": "iso8601",
        "interval": "seconds",
        "temperature_2m": "°C",
        "relative_humidity_2m": "%",
        "apparent_temperature": "°C",
        "weather_code": "wmo code",
        "pressure_msl": "hPa",
        "wind_speed_10m": "km/h",
    },
    "current": {
        "time": "2026-02-21T13:15",
        "interval": 900,
        "temperature_2m": 30.6,
        "relative_humidity_2m": 29,
        "apparent_temperature": 31.3,
        "weather_code": 0,
        "pressure_msl": 1011.3,
        "wind_speed_10m": 13.2,
    },
}

MOCK_CACHE_DATA = {
    "timestamp": "2026-02-21T13:15",
    "data": {
        "latitude": 22.0,
        "longitude": 100.75,
        "generationtime_ms": 0.20992755889892578,
        "utc_offset_seconds": 0,
        "timezone": "GMT",
        "timezone_abbreviation": "GMT",
        "elevation": 561.0,
        "current_units": {
            "time": "iso8601",
            "interval": "seconds",
            "temperature_2m": "°C",
            "relative_humidity_2m": "%",
            "apparent_temperature": "°C",
            "weather_code": "wmo code",
            "pressure_msl": "hPa",
            "wind_speed_10m": "km/h",
        },
        "current": {
            "time": "2026-02-21T16:45",
            "interval": 900,
            "temperature_2m": 21.3,
            "relative_humidity_2m": 48,
            "apparent_temperature": 19.8,
            "weather_code": 1,
            "pressure_msl": 1010.0,
            "wind_speed_10m": 10.4,
        },
    },
}
