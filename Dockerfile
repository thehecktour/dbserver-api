# Base image
FROM python:3.12-slim

# Set working directory to /app
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libsqlite3-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

# Copy dependency files
COPY pyproject.toml poetry.lock* /app/

# Install dependencies (without installing the project itself)
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# Copy project code
COPY . /app

# Expose Django default port
EXPOSE 8000

# Set working directory to src (where manage.py is)
WORKDIR /app/src

# Default command to run Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
