.PHONY: help install test clean backup setup status

# Default target
help:
	@echo "CrowdStrike Correlation Rules Backup Tool"
	@echo "=========================================="
	@echo ""
	@echo "Available commands:"
	@echo "  install    - Install dependencies"
	@echo "  test       - Run compatibility tests"
	@echo "  clean      - Clean up generated files"
	@echo "  backup     - Run backup (requires credentials)"
	@echo "  setup      - Interactive setup"
	@echo "  status     - Check configuration status"
	@echo "  package    - Create distributable package"
	@echo "  lint       - Run code linting"
	@echo ""

# Install dependencies
install:
	pip install -r requirements.txt

# Run compatibility tests
test:
	python test_compatibility.py

# Clean up generated files
clean:
	rm -rf __pycache__/
	rm -rf */__pycache__/
	rm -rf .pytest_cache/
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -name "*.pyc" -delete
	find . -name "*.pyo" -delete

# Run backup (requires credentials)
backup:
	python cli.py backup

# Interactive setup
setup:
	python cli.py setup

# Check configuration status
status:
	python cli.py status

# Create distributable package
package: clean
	python setup.py sdist bdist_wheel

# Run code linting (requires flake8)
lint:
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

# Install in development mode
dev-install:
	pip install -e .

# Run with verbose logging
backup-verbose:
	python cli.py backup --verbose

# Run dry-run backup
backup-dry-run:
	python cli.py backup --dry-run 