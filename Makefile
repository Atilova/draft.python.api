.PHONY: help ci fix-lint diff-lint

help:
	@echo "Available targets:"
	@echo "  help       - Show this help message"
	@echo "  fix-lint   - Auto-fix linting issues"
	@echo "  diff-lint  - Check for linting issues and show diffs"
	@echo "  test       - Run all tests"
	@echo "  ci         - Perform all CI checks"

ci: diff-lint test

test:
	@echo "Running tests with pytest..."
	pytest -c pyproject.toml

fix-lint:
	@echo "Fixing linting issues with ruff..."
	ruff --config pyproject.toml check --fix src/ main.py gunicorn.conf.py
	ruff --config pyproject.toml format src/ main.py gunicorn.conf.py

diff-lint:
	@echo "Checking linting issues with ruff..."
	ruff --config pyproject.toml check src/ main.py gunicorn.conf.py
	ruff --config pyproject.toml format --diff src/ main.py gunicorn.conf.py
