.PHONY: help install test test-cov lint format clean pre-commit ci

# Default target
help: ## Show this help message
	@echo "Available targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Installation
install: ## Install dependencies
	poetry install

# Testing
test: ## Run tests
	poetry run pytest

test-cov: ## Run tests with coverage
	poetry run pytest --cov=src/tdd_ai_py --cov-report=term-missing

test-compression: ## Run compression/decompression round-trip tests
	./test_compression.sh

test-all: ## Run all tests (unit tests + compression tests)
	poetry run pytest
	./test_compression.sh

# Code quality
lint: ## Check code quality
	poetry run black --check src/ tests/
	poetry run isort --check-only src/ tests/
	poetry run flake8 src/ tests/
	poetry run mypy src/

format: ## Format code
	poetry run black src/ tests/
	poetry run isort src/ tests/

# Pre-commit
pre-commit: ## Run pre-commit hooks
	poetry run pre-commit run --all-files

# Cleanup
clean: ## Clean build artifacts
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache/ .mypy_cache/ .coverage htmlcov/

# CI pipeline
ci: install lint test-cov test-compression ## Run CI pipeline locally
