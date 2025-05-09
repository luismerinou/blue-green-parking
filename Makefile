SHELL = /bin/sh

.DEFAULT_GOAL := help

# Colors for output
RED="\\e[91m"
GREEN="\\e[32m"
YELLOW="\\e[33m"
REGULAR="\\e[39m"

SRC="/home/lmu/workspace/personal/blue-green-parking"

run:
	streamlit run src/Home.py

help: ## Show available commands
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
    awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

ruff-check: ## Run Ruff to check code linting
	ruff check ${SRC} \
	&& echo "${GREEN}Code passed Ruff linting.${REGULAR}" \
	|| (echo "${RED}Ruff linting failed.${REGULAR}" ; exit 1)

ruff-apply: ## Apply Ruff's suggested fixes to the code
	ruff --fix ${SRC} \
	&& echo "${GREEN}Code formatted successfully with Ruff.${REGULAR}" \
	|| (echo "${RED}Ruff failed to apply fixes.${REGULAR}" ; exit 1)

ruff-check-file: ## Run Ruff to check a specific file passed as an argument
	@if [ -z "$(file)" ]; then \
		echo "${RED}Please specify a file using the 'file' argument.${REGULAR}"; \
		exit 1; \
	fi
	ruff check $(file) \
	&& echo "${GREEN}$(file) passed Ruff linting.${REGULAR}" \
	|| (echo "${RED}$(file) failed Ruff linting.${REGULAR}" ; exit 1)

ruff-check-dir: ## Run Ruff to check all files in a specific directory passed as an argument
	@if [ -z "$(dir)" ]; then \
		echo "${RED}Please specify a directory using the 'dir' argument.${REGULAR}"; \
		exit 1; \
	fi
	ruff check $(dir) \
	&& echo "${GREEN}Code in $(dir) passed Ruff linting.${REGULAR}" \
	|| (echo "${RED}Code in $(dir) failed Ruff linting.${REGULAR}" ; exit 1)

clean-py:  ## Remove Python artifacts like .pyc and pycache
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

show-version:  ## Show the explicit version of the component
	@echo $(shell cat ${SRC}/__init__.py | head -n 1 | cut -d" " -f 3 | tr -d "'")

check-upgradable:  ## Check for upgradable Python packages
	@echo "${YELLOW}This task may take up to a minute.${REGULAR}"
	pip-check -H -l
