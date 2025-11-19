.PHONY: help build up down restart logs clean test lint format shell db-shell api-docs

# Export CURRENT_UID for docker-compose
export CURRENT_UID := $(shell id -u):$(shell id -g)

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

build: ## Zbuduj obrazy Docker
	docker-compose build

up: ## Uruchom wszystkie serwisy
	docker-compose up -d
	@echo "Waiting for backend to be ready..."
	@sleep 3
	@echo "Running migrations..."
	@docker-compose exec backend flask db upgrade || echo "Migrations failed or already applied"
	@echo "Seeding database..."
	@docker-compose exec backend flask seed || echo "Database already seeded or backend not ready yet"

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

db-seed: ## Wypełnij bazę danych przykładowymi danymi
	docker-compose exec backend flask seed

# Setup
init: build up migrate-up ## Inicjalizacja projektu (build + up + migrations)
	@echo ""
	@echo "Projekt zainicjalizowany"
	@echo "Backend: http://localhost:5000"
	@echo "Adminer: http://localhost:8080"
	@echo ""

# Setup with seed data
init-dev: init db-seed ## Inicjalizacja projektu z przykładowymi danymi
	@echo "✓ Projekt zainicjalizowany z przykładowymi danymi"

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

# Google Cloud deployment
gcloud-setup: ## Sprawdź wymagania dla GCP deployment
	@echo "Sprawdzanie wymagań dla Google Cloud..."
	@command -v gcloud >/dev/null 2>&1 || { echo "❌ gcloud CLI nie jest zainstalowane"; exit 1; }
	@command -v docker >/dev/null 2>&1 || { echo "❌ Docker nie jest zainstalowany"; exit 1; }
	@echo "✓ gcloud CLI zainstalowane"
	@echo "✓ Docker zainstalowany"
	@echo ""
	@echo "Następne kroki:"
	@echo "1. Skopiuj .env.gcloud.template do .env.gcloud"
	@echo "2. Wypełnij wartości w .env.gcloud"
	@echo "3. Uruchom: ./deploy-gcloud.sh"

gcloud-deploy: ## Uruchom interaktywny deployment na Google Cloud
	./deploy-gcloud.sh

gcloud-docs: ## Otwórz dokumentację deployment na GCP
	@cat GOOGLE_CLOUD_DEPLOYMENT.md | less
