.PHONY: build run

build:
	@echo "Installing dependencies..."
	poetry install
	@echo "Build complete."

run:
	@echo "Starting FastSimpleCRM..."
	cd src && poetry run python run.py
