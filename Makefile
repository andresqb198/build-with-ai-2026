.PHONY: setup start stop reset run validate help

help: ## Mostrar esta ayuda
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'

setup: ## Instalar dependencias y preparar .env
	pip install -r requirements.txt
	@test -f .env || (cp .env.example .env && echo "Archivo .env creado — agrega tu GOOGLE_API_KEY")

start: ## Iniciar Langfuse y validar el entorno
	bash scripts/start.sh

stop: ## Detener los contenedores de Langfuse
	docker compose -f observability/docker-compose.yml down

reset: ## Reiniciar Langfuse (elimina todos los datos)
	bash scripts/reset.sh

run: ## Ejecutar el sistema de respuesta a incidentes
	python -m app.main

validate: ## Verificar la configuración del entorno
	bash scripts/validate_env.sh
