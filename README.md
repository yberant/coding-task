# Weather Dashboard

A Django application for tracking weather conditions with customizable widgets. Uses Open-Meteo API for weather data.

## Prerequisites

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) package manager
- Docker (optional)

## Getting Started

### Env variables

an .env file must be created with the following variables:

- GEOCODING_API_KEY: Your geocoding_api_key
- REDIS_PUBLIC_URL: A redis url (for caching)

### Without Docker

1. Install dependencies:

```bash
uv sync
```

2. Run migrations:

```bash
uv run python src/manage.py migrate
```

3. Create a superuser (optional):

```bash
uv run python src/manage.py createsuperuser
```

4. Start the development server:

```bash
uv run python src/manage.py runserver
```

The app will be available at http://localhost:8000

### With Docker

1. Build and start the container:

```bash
docker compose up --build
```

This will automatically run migrations and start the server.

The app will be available at http://localhost:8000

To run in detached mode:

```bash
docker compose up -d --build
```

To stop:

```bash
docker compose down
```

## Usage

1. Visit http://localhost:8000
2. Create an account or sign in
3. View your weather dashboard with current location weather

## Testing

To run tests, using uv:

```bash
uv run python src/manage.py test locations
```

To run test from docker (container must be running):

```bash
docker compose exec web uv run python src/manage.py test locations
```

## Project Structure

```
weather-dashboard/
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml
├── uv.lock
└── src/
    ├── accounts/       # Authentication app
    ├── config/         # Django settings
    ├── templates/      # Jinja2 templates
    |── locations/      # Locations app
    |   ├── models.py   # Models for the locations app (Location and WeatherSnapshot)
    |   ├── services.py # Services for the locations app (Api Calling and Cache)
    |   ├── repositories.py # Repositories for the locations app (model interaction)
    |   ├── views.py    # Views for the locations app
    |   ├── urls.py     # URLs for the locations app
    |   └── tests/      # Tests for the locations app
    |       ├── test_services.py # Tests for services
    |       ├── test_repositories.py # Tests for repositories
    |       └── test_views.py    # Tests for views (currently just for list_locations_view)
    |── db.sqlite3 # Database file
    |── .env # Environment variables (must be created, is on .gitignore)
    |── global_values.py # Global values for the application
    |── templates/
    |   ├── base.html   # Base template
    |   ├── home.html   # Home template
    |   ├── error_page.html  # Error page template
    |   ├── dashboard.html   # Dashboard template
    |   |── accounts/  # Accounts templates
    |   |   ├── login.html   # Login template
    |   |   └── signup.html   # Signup template
    |   └── locations/  # Locations templates
    |       ├── create_location.html # Create location template
    |       ├── tracked_locations.html # List locations template
    |       ├── tracked_location_data.html # Location data template
    |       ├── weather_data.html # weather data of location and card buttons template
    |       └── weather_history.html # weather shanpshots of location template
    └── manage.py
```
