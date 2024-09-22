# Makefile for linting and formatting

# Variables
PYTHON := poetry run python
FLAKE8 := poetry run flake8
BLACK := poetry run black
ISORT := poetry run isort
PYLINT := poetry run pylint
MYPY := poetry run mypy
BANDIT := poetry run bandit
COVERAGE := poetry run coverage

# Default target
.PHONY: all
all: tree lint fmt check-fmt test coverage

# Linting target
.PHONY: lint
lint:
	$(FLAKE8) --verbose .
	$(PYLINT) src

# Formatting target
.PHONY: fmt
fmt:
	$(BLACK) .
	$(ISORT) .

# Type checking target
.PHONY: type-check
type-check:
	MYPYPATH=$(pwd)/lib $(MYPY) --explicit-package-bases src

# Check formatting target (for CI)
.PHONY: check-fmt
check-fmt:
	$(BLACK) --check .
	$(ISORT) --check-only .

# Security linting target
.PHONY: security
security:
	$(BANDIT) -r .  

# Test target
.PHONY: test
test:
	$(PYTHON) -m pytest --maxfail=1 --disable-warnings -q

# Coverage target
.PHONY: coverage
coverage:
	$(PYTHON) -m pytest --cov=. --cov-report=term-missing --cov-report=html   

# Clean target
.PHONY: clean
clean:
	rm -rf *.pyc __pycache__ .pytest_cache .mypy_cache



# Generate project structure in plain text format
.PHONY: tree
tree:
	@tree --prune -I "__pycache__|venv|env|.git|dist|build|.mypy_cache|.pytest_cache|*.egg-info|.tox|.vscode|.idea|node_modules|docs/_build" > project_structure.txt
