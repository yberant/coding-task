# Weather Dashboard

A Django application for tracking weather conditions with customizable widgets. Uses Open-Meteo API for weather data.

## Prerequisites

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) package manager
- Docker (optional)

## Getting Started

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
    └── manage.py
```
