FROM python:3.13-slim

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen --no-dev

# Copy application code
COPY . .

# Run migrations and start server
EXPOSE 8000

CMD ["uv", "run", "python", "src/manage.py", "runserver", "0.0.0.0:8000"]
