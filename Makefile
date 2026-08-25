.PHONY: help setup lint test dev-up dev-down clean

help:
	@echo "DevCorp AI Development Commands:"
	@echo "  make setup     - Install Python and Node dependencies"
	@echo "  make lint      - Run code quality linter (Ruff)"
	@echo "  make test      - Run automated unit test suite"
	@echo "  make dev-up    - Start local PostgreSQL, Redis, and LiteLLM"
	@echo "  make dev-down  - Stop local services"
	@echo "  make clean     - Clean temporary artifacts and caches"

setup:
	pip install -e ".[dev,demo]"

lint:
	ruff check .
	ruff format --check .

test:
	pytest tests/unit/ -v

dev-up:
	docker compose -f docker-compose.dev.yml up -d

dev-down:
	docker compose -f docker-compose.dev.yml down

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	rm -rf build/ dist/ *.egg-info/
