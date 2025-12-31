# Project Variables
PYTHON = python3
PIP = pip
VENV = .venv
ACTIVATE = . $(VENV)/bin/activate

# Default target
.DEFAULT_GOAL := help

##@ Help
help: ## Display this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

##@ Setup
.env: ## Create default .env file (Defaults to test mode)
	@echo "PYTHONPATH=." > .env
	@echo "ENV=test" >> .env
	@echo "OLLAMA_URL=http://localhost:11434" >> .env
	@echo "NICEGUI_NATIVE=False" >> .env
	@echo ".env file created with ENV=test."

install: .env ## Create virtualenv and install dependencies
	$(PYTHON) -m venv $(VENV)
	$(ACTIVATE) && $(PIP) install --upgrade pip
	$(ACTIVATE) && $(PIP) install -r apps/architect/requirements.txt
	@echo "Installation complete."

##@ Development

# Run in local mode by overriding the ENV variable
run: ## Launch NiceGUI application in LOCAL mode
	$(ACTIVATE) && export PYTHONPATH=. && ENV=local python3 -m apps.architect.main

# Run in test mode (uses the .env default)
run-test: ## Launch NiceGUI application in TEST mode
	$(ACTIVATE) && export PYTHONPATH=. && python3 -m apps.architect.main

test: ## Run pytest-bdd tests
	$(ACTIVATE) && export PYTHONPATH=. && pytest tests/

docker-run: ## Build and start containers using Docker Compose
	docker compose -f infra/local/docker-compose.yml up --build

##@ Cleanup
clean: ## Remove virtualenv and python cache files
	rm -rf $(VENV)
	find . -type d -name "__pycache__" -exec rm -rf {} +

.PHONY: help install run run-test test docker-run clean