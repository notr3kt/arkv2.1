# S1NGULARITY Makefile
# Common commands for development and deployment

.PHONY: help install dev docker-up docker-down docker-logs test clean

# Default target
.DEFAULT_GOAL := help

help: ## Show this help message
	@echo "S1NGULARITY - Available Commands"
	@echo "================================="
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies in virtual environment
	@echo "📦 Creating virtual environment and installing dependencies..."
	python3.11 -m venv venv
	. venv/bin/activate && pip install -r requirements.txt
	@echo "✅ Installation complete!"
	@echo "Activate with: source venv/bin/activate"

dev: ## Start development server (local)
	@echo "🚀 Starting development server..."
	@if [ ! -f .env ]; then \
		echo "⚠️  .env file not found. Copying .env.example..."; \
		cp .env.example .env; \
		echo "⚠️  Please edit .env and add your API keys!"; \
		exit 1; \
	fi
	docker-compose up -d postgres redis
	@echo "⏳ Waiting for database..."
	@sleep 3
	python -c "import asyncio; from database import init_db; asyncio.run(init_db())" || true
	uvicorn main:app --reload --host 0.0.0.0 --port 8000

docker-up: ## Start all services with Docker Compose
	@echo "🐳 Starting S1NGULARITY with Docker Compose..."
	@if [ ! -f .env ]; then \
		echo "⚠️  .env file not found. Copying .env.example..."; \
		cp .env.example .env; \
		echo "⚠️  Please edit .env and add your API keys!"; \
		exit 1; \
	fi
	docker-compose up -d --build
	@echo "⏳ Waiting for services to start..."
	@sleep 10
	@echo "🏥 Health check..."
	@curl -f http://localhost:8000/health || echo "⚠️  Health check failed"
	@echo ""
	@echo "✅ Services started!"
	@echo "   • API: http://localhost:8000"
	@echo "   • Docs: http://localhost:8000/docs"

docker-down: ## Stop all Docker services
	@echo "🛑 Stopping services..."
	docker-compose down
	@echo "✅ All services stopped"

docker-logs: ## Show Docker logs
	docker-compose logs -f api

docker-clean: ## Remove all containers, volumes, and images
	@echo "🧹 Cleaning up Docker resources..."
	docker-compose down -v
	docker system prune -f
	@echo "✅ Cleanup complete"

test: ## Run tests
	@echo "🧪 Running tests..."
	pytest -v --cov=. --cov-report=html
	@echo "✅ Tests complete! Open htmlcov/index.html for coverage report"

test-quick: ## Run tests without coverage
	@echo "🧪 Running tests (no coverage)..."
	pytest -v

lint: ## Run linters
	@echo "🔍 Running linters..."
	black --check .
	ruff check .
	mypy .
	@echo "✅ Linting complete"

format: ## Format code with black
	@echo "✨ Formatting code..."
	black .
	ruff check --fix .
	@echo "✅ Formatting complete"

db-init: ## Initialize database
	@echo "🗄️  Initializing database..."
	python -c "import asyncio; from database import init_db; asyncio.run(init_db())"
	@echo "✅ Database initialized"

db-reset: ## Reset database (WARNING: deletes all data)
	@echo "⚠️  WARNING: This will delete all data!"
	@read -p "Are you sure? (y/N): " confirm; \
	if [ "$$confirm" = "y" ]; then \
		python -c "import asyncio; from database import get_db_manager; asyncio.run(get_db_manager().drop_tables())"; \
		python -c "import asyncio; from database import init_db; asyncio.run(init_db())"; \
		echo "✅ Database reset complete"; \
	else \
		echo "Cancelled"; \
	fi

clean: ## Clean up temporary files
	@echo "🧹 Cleaning temporary files..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.log" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name ".coverage" -delete 2>/dev/null || true
	rm -f s1ngularity.db 2>/dev/null || true
	@echo "✅ Cleanup complete"

check-env: ## Verify environment configuration
	@echo "🔍 Checking environment configuration..."
	@if [ ! -f .env ]; then \
		echo "❌ .env file not found"; \
		exit 1; \
	fi
	@python -c "import os; from dotenv import load_dotenv; load_dotenv(); \
		required = ['JOBDIVA_CLIENT_ID', 'TAVILY_API_KEY']; \
		missing = [k for k in required if not os.getenv(k)]; \
		print('❌ Missing keys:', missing) if missing else print('✅ All required keys present')"

health: ## Check service health
	@echo "🏥 Checking service health..."
	@curl -s http://localhost:8000/health | python -m json.tool || echo "❌ Service not responding"

quick-start: ## Quick start wizard (recommended for first-time setup)
	@bash start.sh

# Development helpers
shell: ## Open Python shell with app context
	@python -i -c "from main import *; from database import *; import asyncio"

# Production commands
prod-build: ## Build production Docker image
	@echo "🏗️  Building production image..."
	docker build -t s1ngularity:latest .
	@echo "✅ Build complete"

prod-deploy: ## Deploy to production (requires .env.production)
	@echo "🚀 Deploying to production..."
	@if [ ! -f .env.production ]; then \
		echo "❌ .env.production not found"; \
		exit 1; \
	fi
	docker-compose -f docker-compose.yml --env-file .env.production up -d
	@echo "✅ Deployment complete"
