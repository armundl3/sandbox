# Variables
DOCKER_COMPOSE = docker-compose
DOCKER = docker
APP_NAME = deepseek-api
PYTHON = python3

# Colors for pretty printing
BLUE := \033[34m
GREEN := \033[32m
RED := \033[31m
RESET := \033[0m

.PHONY: help build start stop restart logs clean test lint format deploy dev down ps

# Default target
.DEFAULT_GOAL := help

# Show help
help:
	@echo "$(BLUE)DeepSeek API Management Commands:$(RESET)"
	@echo "$(GREEN)make build$(RESET)      - Build Docker images"
	@echo "$(GREEN)make start$(RESET)      - Start all services"
	@echo "$(GREEN)make stop$(RESET)       - Stop all services"
	@echo "$(GREEN)make restart$(RESET)    - Restart all services"
	@echo "$(GREEN)make logs$(RESET)       - View logs"
	@echo "$(GREEN)make clean$(RESET)      - Remove containers, volumes, and images"
	@echo "$(GREEN)make test$(RESET)       - Run tests"
	@echo "$(GREEN)make dev$(RESET)        - Start development environment"
	@echo "$(GREEN)make down$(RESET)       - Stop and remove containers"
	@echo "$(GREEN)make ps$(RESET)         - Show running containers"

# Build Docker images
build:
	@echo "$(BLUE)Building Docker images...$(RESET)"
	$(DOCKER_COMPOSE) build --no-cache

# Start services
start:
	@echo "$(BLUE)Starting services...$(RESET)"
	$(DOCKER_COMPOSE) up -d
	@echo "$(GREEN)Services started. API available at http://localhost:8000$(RESET)"
	@echo "$(GREEN)API documentation available at http://localhost:8000/docs$(RESET)"

# Stop services
stop:
	@echo "$(BLUE)Stopping services...$(RESET)"
	$(DOCKER_COMPOSE) stop

# Restart services
restart: stop start

# View logs
logs:
	@echo "$(BLUE)Showing logs...$(RESET)"
	$(DOCKER_COMPOSE) logs -f

# Clean up
clean:
	@echo "$(RED)Cleaning up...$(RESET)"
	$(DOCKER_COMPOSE) down -v --rmi all --remove-orphans
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -r {} +
	find . -type d -name "*.egg" -exec rm -r {} +
	find . -type d -name ".pytest_cache" -exec rm -r {} +
	find . -type d -name ".coverage" -exec rm -r {} +

# Run tests
test:
	@echo "$(BLUE)Running tests...$(RESET)"
	$(DOCKER_COMPOSE) run --rm api pytest -v

# Start development environment
dev:
	@echo "$(BLUE)Starting development environment...$(RESET)"
	$(DOCKER_COMPOSE) up --build

# Stop and remove containers
down:
	@echo "$(BLUE)Stopping and removing containers...$(RESET)"
	$(DOCKER_COMPOSE) down

# Show running containers
ps:
	@echo "$(BLUE)Showing running containers...$(RESET)"
	$(DOCKER_COMPOSE) ps