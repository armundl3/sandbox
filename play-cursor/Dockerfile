FROM python:3.10.7-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry and disable venv creation
ENV POETRY_VERSION=2.1.3 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/var/cache/pypoetry'
RUN pip install "poetry==$POETRY_VERSION"

# Copy poetry files
COPY pyproject.toml poetry.lock README.md ./

# Install dependencies
RUN poetry install --no-interaction --no-ansi --no-root

# Copy the rest of the application
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Set environment variable for YouTube API key (can be overridden at runtime)
ENV YOUTUBE_API_KEY=""

# Command to run the application
CMD ["poetry", "run", "uvicorn", "play_cursor.main:app", "--host", "0.0.0.0", "--port", "8000"]