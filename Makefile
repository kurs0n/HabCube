.PHONY: help build up down restart logs clean test lint format shell db-shell api-docs

# Export CURRENT_UID for docker-compose
export CURRENT_UID := $(shell id -u):$(shell id -g)

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

build: ## Zbuduj obrazy Docker
	docker-compose build

up: ## Uruchom wszystkie serwisy
	docker-compose up -d

down: ## Zatrzymaj wszystkie serwisy
	docker-compose down

restart: ## Zrestartuj wszystkie serwisy
	docker-compose restart

logs: ## Pokaż logi wszystkich serwisów
	docker-compose logs -f

logs-backend: ## Pokaż logi backendu
	docker-compose logs -f backend

logs-db: ## Pokaż logi bazy danych
	docker-compose logs -f postgres

ps: ## Pokaż status serwisów
	docker-compose ps

clean: ## Usuń kontenery i wolumeny (UWAGA: usuwa dane!)
	docker-compose down -v
	docker system prune -f

clean-all: ## Usuń wszystko włącznie z obrazami
	docker-compose down -v --rmi all
	docker system prune -af

# Development commands
shell: ## Otwórz shell w kontenerze backendu
	docker-compose exec backend bash

flask-shell: ## Otwórz Flask shell
	docker-compose exec backend flask shell

db-shell: ## Połącz się z bazą danych PostgreSQL
	docker-compose exec postgres psql -U habcube_user -d habcube

redis-shell: ## Połącz się z Redis CLI
	docker-compose exec redis redis-cli -a habcube_redis

# Database migrations
migrate-init: ## Inicjalizuj migracje (pierwsze uruchomienie)
	docker-compose exec backend flask db init

migrate-create: ## Stwórz nową migrację
	@read -p "Wpisz opis migracji: " desc; \
	docker-compose exec backend flask db migrate -m "$$desc"

migrate-up: ## Aplikuj migracje
	docker-compose exec backend flask db upgrade

migrate-down: ## Cofnij ostatnią migrację
	docker-compose exec backend flask db downgrade

# Testing
test: ## Uruchom testy
	docker-compose exec backend pytest

test-cov: ## Uruchom testy z pokryciem
	docker-compose exec backend pytest --cov=app --cov-report=html --cov-report=term

test-verbose: ## Uruchom testy w trybie verbose
	docker-compose exec backend pytest -v

test-watch: ## Uruchom testy w trybie watch (automatyczne ponowne uruchamianie)
	docker-compose exec backend pytest-watch

# Code quality
lint: ## Sprawdź kod (flake8, pylint, mypy)
	docker-compose run --rm --no-deps code-quality sh -c "cd /usr/src && flake8 . && pylint app/ && mypy app/"

format: ## Auto-formatuj kod (black, isort)
	docker-compose run --rm --no-deps code-quality sh -c "cd /usr/src && black . && isort ."

format-check: ## Sprawdź formatowanie bez zmian
	docker-compose run --rm --no-deps code-quality sh -c "cd /usr/src && black --check . && isort --check ."

type-check: ## Sprawdź typy (mypy)
	docker-compose run --rm --no-deps code-quality sh -c "cd /usr/src && mypy app/ --ignore-missing-imports"

fix: ## Auto-napraw co się da (format + autoflake)
	docker-compose run --rm --no-deps code-quality sh -c "cd /usr/src && black . && isort . && flake8 . --exit-zero"

quality: format lint ## Auto-formatuj i sprawdź jakość kodu

# Database operations
db-backup: ## Zrób backup bazy danych
	@mkdir -p backups
	docker-compose exec postgres pg_dump -U habcube_user habcube > backups/backup_$$(date +%Y%m%d_%H%M%S).sql
	@echo "Backup zapisany w backups/"

db-restore: ## Przywróć bazę danych z backupu (użyj: make db-restore FILE=backup.sql)
	@if [ -z "$(FILE)" ]; then \
		echo "Użyj: make db-restore FILE=ścieżka/do/backup.sql"; \
		exit 1; \
	fi
	cat $(FILE) | docker-compose exec -T postgres psql -U habcube_user habcube

# Setup
init: build up ## Inicjalizacja projektu (build + up)
	@echo ""
	@echo "Projekt zainicjalizowany"
	@echo "Backend: http://localhost:5000"
	@echo "Adminer: http://localhost:8080"
	@echo ""

# Monitoring
health: ## Sprawdź health check backendu
	@curl -s http://localhost:5000/health | python3 -m json.tool

api-docs: ## Otwórz Swagger UI
	@echo "Otwieranie dokumentacji API..."
	@echo "Swagger UI: http://localhost:5000/api/docs/"
	@xdg-open http://localhost:5000/api/docs/ 2>/dev/null || open http://localhost:5000/api/docs/ 2>/dev/null || echo "Otwórz ręcznie: http://localhost:5000/api/docs/"

# Development workflow
dev: up logs ## Uruchom w trybie deweloperskim i pokaż logi

dev-restart: restart logs ## Zrestartuj i pokaż logi

# Quick commands
rebuild: ## Przebuduj i uruchom ponownie
	docker-compose down
	docker-compose build
	docker-compose up -d

fresh: ## Świeży start (usuwa dane!)
	docker-compose down -v
	docker-compose build
	docker-compose up -d
