# Play Cursor

A FastAPI-based application for exploring and learning.

## Local Development

### Prerequisites
- Python 3.11.0 (using pyenv)
- Poetry (Python package manager)

### Setting up the Development Environment

1. Install dependencies using Poetry:
```bash
poetry install
```

2. Activate the virtual environment:
```bash
poetry shell
```

3. Run the application:
```bash
uvicorn play_cursor.main:app --reload
```

The application will be available at `http://localhost:8000`

### API Documentation
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Docker Deployment

### Using Docker Compose (Recommended)

1. Build and start the container:
```bash
docker-compose up --build
```

2. To run in detached mode:
```bash
docker-compose up -d
```

3. To stop the container:
```bash
docker-compose down
```

### Using Docker Directly

#### Building the Docker Image
```bash
docker build -t play-cursor .
```

#### Running the Docker Container
```bash
docker run -p 8000:8000 play-cursor
```

The application will be available at `http://localhost:8000`

### API Documentation (Docker)
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Project Structure
```
play-cursor/
├── play_cursor/
│   └── main.py
├── tests/
├── pyproject.toml
├── poetry.lock
├── Dockerfile
├── docker-compose.yml
└── README.md
```
