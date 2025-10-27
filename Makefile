# Makefile for LekosEPR-API
# Usage examples:
# * make build — install dependencies and apply migrations
# * make run — launch the application
# * make deploy — build and launch from a clean state

.PHONY: migrate build run deploy clean

# -----------------------------
# Migrations
# -----------------------------
# migrate:
# 	@echo "🚀 Running database migrations..."
# 	cd src && poetry run alembic upgrade head

# -----------------------------
# Building application
# -----------------------------
build:
	@echo "📦 Installing dependencies..."
	poetry install
# 	$(MAKE) migrate
	@echo "✅ Build complete."

# -----------------------------
# Run project
# -----------------------------
run:
	@echo "▶️  Starting LekosEPR-API..."
	PYTHONPATH=src poetry run python -m src.run

# -----------------------------
# Deploy (build + run)
# -----------------------------
deploy:
	@echo "🚀 Deploying LekosEPR-API..."
	$(MAKE) build
	$(MAKE) run

# -----------------------------
# Clean temporary files
# -----------------------------
clean:
	@echo "🧹 Cleaning cache and temporary files..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .pytest_cache .mypy_cache dist build
	@echo "✅ Clean complete."