.PHONY: clean build run


TITLE = Aiogram3TemplateBot
POETRY := $(shell which poetry)


clean:
	@echo "🧹 Cleaning cache and temporary files..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .pytest_cache .mypy_cache dist build
	@echo "✅ Clean complete."


# migrate:
# 	@echo "🚀 Running database migrations..."
# 	cd src && poetry run alembic upgrade head


build:
	$(MAKE) clean
	$(POETRY) install
# 	$(MAKE) migrate


run:
	$(POETRY) run python -m src.main