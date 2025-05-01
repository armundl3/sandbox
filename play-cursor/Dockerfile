FROM python:3.11-slim

WORKDIR /play_cursor

# Copy the rest of the application
COPY . .

# Install poetry
RUN pip install poetry

# Configure poetry to not create a virtual environment
RUN poetry config virtualenvs.create false

# Install dependencies
RUN poetry install --no-interaction --no-ansi


# Expose the port the app runs on
EXPOSE 8000