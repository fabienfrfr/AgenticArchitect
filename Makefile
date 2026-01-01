# Project Variables
PYTHON = python3
PIP = pip
VENV = .venv
ACTIVATE = . $(VENV)/bin/activate

# Deployment configuration
DOMAIN = thearchitect.dev
USER = ubuntu

# Default target
.DEFAULT_GOAL := help

##@ Help
help: ## Display this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

##@ Setup
.env: ## Create default .env file ONLY if it doesn't exist
	@if [ ! -f .env ]; then \
		echo "PYTHONPATH=." > .env; \
		echo "ENV=test" >> .env; \
		echo "OLLAMA_URL=http://localhost:11434" >> .env; \
		echo "NICEGUI_NATIVE=False" >> .env; \
		echo "DOMAIN=$(DOMAIN)" >> .env; \
		echo "USER=$(USER)" >> .env; \
		echo "POSTGRES_PASSWORD=$$(openssl rand -hex 32)" >> .env; \
		echo "LANGFUSE_SECRET_KEY=$$(openssl rand -hex 32)" >> .env; \
		echo "NEXTAUTH_SECRET=$$(openssl rand -hex 32)" >> .env; \
		echo "✅ .env file created with secure unique keys."; \
	else \
		echo "⚠️  .env file already exists. Skipping to protect existing secrets."; \
	fi

install: .env ## Create virtualenv and install dependencies
	$(PYTHON) -m venv $(VENV)
	$(ACTIVATE) && $(PIP) install --upgrade pip
	$(ACTIVATE) && $(PIP) install -r requirements.txt
	@echo "Installation complete."

##@ Development
run: ## Launch application in LOCAL mode
	$(ACTIVATE) && export PYTHONPATH=. && ENV=local python3 -m architect.main

run-test: ## Launch application in TEST mode
	$(ACTIVATE) && export PYTHONPATH=. && python3 -m architect.main

test: ## Run pytest-bdd tests
	$(ACTIVATE) && export PYTHONPATH=. && pytest tests/

docker-run: ## Build and start local containers
	docker compose -f infra/local/docker-compose.yml up --build

vps-setup: ## Update VPS and install Docker + Compose
	@echo "🛠️  Updating system and installing Docker on $(DOMAIN)..."
	ssh $(USER)@$(DOMAIN) "sudo apt update && sudo apt install -y docker.io docker-compose-v2"
	@echo "👤 Adding user to docker group..."
	ssh $(USER)@$(DOMAIN) "sudo usermod -aG docker $(USER)"
	@echo "✅ Setup complete!"
	@echo "⚠️  IMPORTANT: You must manually log out and log back in to the VPS for permissions to take effect."

##@ Deployment
deploy: ## Deploy the project to OVH VPS via SSH/Rsync
	@echo "📤 Uploading AgenticArchitect to $(DOMAIN)..."
	ssh $(USER)@$(DOMAIN) "mkdir -p ~/AgenticArchitect"
	rsync -avz --exclude='.git' --exclude='.venv' --exclude='__pycache__' ./ $(USER)@$(DOMAIN):~/AgenticArchitect
	@echo "🚀 Launching Production Stack on VPS..."
	ssh $(USER)@$(DOMAIN) "cd ~/AgenticArchitect && docker compose -f infra/vps/docker-compose.prod.yml up -d --build"

##@ Cleanup
clean: ## Remove virtualenv and python cache files
	rm -rf $(VENV)
	find . -type d -name "__pycache__" -exec rm -rf {} +

.PHONY: help install run run-test test docker-run vps-setup deploy clean