.PHONY: setup start stop reset run validate help

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'

setup: ## Install dependencies and prepare .env
	pip install -r requirements.txt
	@test -f .env || (cp .env.example .env && echo "Created .env — add your GOOGLE_API_KEY")

start: ## Start Langfuse and validate environment
	bash scripts/start.sh

stop: ## Stop Langfuse containers
	docker compose -f langfuse/docker-compose.yml down

reset: ## Reset Langfuse (removes all data)
	bash scripts/reset.sh

run: ## Run the incident response system
	python -m app.main

validate: ## Validate environment setup
	bash scripts/validate_env.sh
