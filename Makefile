SRC := src/ main.py gunicorn.conf.py

.PHONY: help fix-lint diff-lint test run-gunicorn ci

help:
	@echo "Available targets:"
	@echo "  help          - Show this help message"
	@echo "  fix-lint      - Auto-fix linting issues"
	@echo "  diff-lint     - Check for linting issues and show diffs"
	@echo "  test          - Run all tests"
	@echo "  run-gunicorni - Start gunicorn server"
	@echo "  ci            - Perform all CI checks"

fix-lint:
	@echo "Fixing linting issues with ruff..."
	uv run ruff --config pyproject.toml check --fix $(SRC)
	uv run ruff --config pyproject.toml format $(SRC)

diff-lint:
	@echo "Checking linting issues with ruff..."
	uv run ruff --config pyproject.toml check $(SRC)
	uv run ruff --config pyproject.toml format --diff $(SRC)

test:
	@echo "Running tests with pytest..."
	uv run pytest -c pyproject.toml

run-gunicorn:
	@echo "Running gunicorn..."
	uv run gunicorn main:app --config=gunicorn.conf.py

ci: diff-lint test
