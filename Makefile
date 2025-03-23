SHELL = /bin/sh

.DEFAULT_GOAL:=help

##@ Pipenv
.PHONY: shell
shell: ## Activate pipenv shell.
	pipenv shell

.PHONY: install
install: ## Install dependencies using pipenv.
	pipenv install

# https://misc.flogisoft.com/bash/tip_colors_and_formatting
RED="\\e[91m"
GREEN="\\e[32m"
BLUE="\\e[94m"
YELLOW="\\e[33m"
REGULAR="\\e[39m"

REPORTS=".coverage-reports"
SRC="/home/lmu/workspace/personal/blue-green-parking"
VERSION=$(shell cat ${SRC}/__init__.py | head -n 1 | cut -d" " -f 3 | tr -d "'")
# Change the version command to adapt it to your needs

help: ## Prompts help for every command
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
    awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

warn:
	@echo "${BLUE}This is a warning to use in other commands.${REGULAR}"

clean-py:  ## Remove Python artifacts like .pyc and pycache
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

build:  ## Build docker image with credentials from .env
	@docker build --build-arg $(shell cat .env | grep PYPI) -t test-image:active ./

show-version:  ## Shows the explicit version of the component
	@echo ${VERSION}

bump-version:
	bumpversion patch --allow-dirty

d diff:  ## Show diff of the first unstaged file
	git diff --name-only | head -n 1 | xargs git diff

a add:  ## Add the first unstaged file, run it after make diff
	@git diff --name-only | head -n 1 | xargs git add -v

black:  ## Launch black against all added files
	@git diff --cached --name-only -- '***.py' | xargs -L 1 black -l 100

linting: ## Check linting with Pylint -- generates report
	pylint --rcfile=setup.cfg ${SRC}/ | tee ${REPORTS}/pylint.txt

flake:  ## Check style and linting with Flake8 - generates report
	@flake8 --tee --output-file=${REPORTS}/flake8.txt\
	&& echo "${GREEN}Passed Flake8 style review.${REGULAR}" \
	|| (echo "${RED}Flake8 style review failed.${REGULAR}" ; exit 1)

check-upgradable:  ## Prompt a list of upgradable Python packages
	@echo "${YELLOW}This task may take up to a minute.${REGULAR}"
	pip-check -H -l | tee ${REPORTS}/upgradable.txt

graph:  ## Show the dependency inverted graph with ARG highlighted, usage: make graph ARG="requests"
	pipenv graph --reverse | grep --color=always -e^ -e ${ARG}


(shell pwd):/mnt swaggerapi/swagger-ui
	xdg-open http://localhost:8081

dead-code:  ## Look for dead code with Vulture
	@vulture ${SRC}/ | tee ${REPORTS}/vulture.txt