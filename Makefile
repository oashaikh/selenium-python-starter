.DEFAULT_GOAL := help
PYTHON ?= python

.PHONY: help install test test-headless test-smoke test-headed clean

help:  ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?##' $(MAKEFILE_LIST) | awk 'BEGIN{FS=":.*?## "}; {printf "  %-14s %s\n", $$1, $$2}'

install:  ## Install dev deps
	$(PYTHON) -m pip install -r requirements-dev.txt

test:  ## Run all tests
	pytest

test-headless:  ## Run only headless unit tests (no browser launch)
	pytest -m headless

test-smoke:  ## Smoke subset
	pytest -m smoke

test-headed:  ## Run with visible browser
	HEADED=1 pytest

clean:  ## Remove caches and reports
	rm -rf .pytest_cache test-results report.html junit.xml htmlcov .coverage
