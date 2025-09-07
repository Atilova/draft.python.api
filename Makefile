.PHONY: help ci test fix-lint diff-lint dbcheck dbmigrate dbmakemigrations

help:
	@echo "Available targets:"
	@echo "  help             - Show this help message"
	@echo "  ci               - Perform all CI checks"
	@echo "  test             - Run all tests"
	@echo "  fix-lint         - Auto-fix linting issues"
	@echo "  diff-lint        - Check for linting issues and show diffs"
	@echo "  dbcheck          - Show current Alembic revision"
	@echo "  dbmigrate        - Apply all Alembic migrations (upgrade head)"
	@echo "  dbmakemigrations - Create new Alembic migration based on models"

ci: diff-lint test

test:
	@echo "Running tests with pytest..."
	pytest -c pyproject.toml

fix-lint:
	@echo "Fixing linting issues with ruff..."
	ruff --config pyproject.toml check --fix src/ pkgs/ migrations/ main.py gunicorn.conf.py
	ruff --config pyproject.toml format src/ pkgs/ migrations/ main.py gunicorn.conf.py

diff-lint:
	@echo "Checking linting issues with ruff..."
	ruff --config pyproject.toml check src/ pkgs/ migrations/ main.py gunicorn.conf.py
	ruff --config pyproject.toml format --diff src/ pkgs/ migrations/ main.py gunicorn.conf.py

dbcheck:
	alembic current

dbmigrate:
	alembic upgrade head

dbmakemigrations:
	alembic revision --autogenerate
