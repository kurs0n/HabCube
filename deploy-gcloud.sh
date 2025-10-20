# (Re)create migration job for Cloud Run
create_migration_job() {
    log_info "Tworzenie/aktualizacja zadania migracji Cloud Run..."

    IMAGE_TAG="${REGION}-docker.pkg.dev/${PROJECT_ID}/habcube/habcube-backend:latest"
    SERVICE_ACCOUNT="${SERVICE_ACCOUNT:-cloud-run-service-account@${PROJECT_ID}.iam.gserviceaccount.com}"
    VPC_CONNECTOR_FULL_PATH="projects/${PROJECT_ID}/locations/${REGION}/connectors/vpc"

    # Delete job if exists
    if gcloud run jobs describe habcube-migrate --region "$REGION" &>/dev/null; then
        log_warn "Usuwam istniejące zadanie migracji habcube-migrate..."
        gcloud run jobs delete habcube-migrate --region "$REGION" --quiet
    fi

    gcloud run jobs create habcube-migrate \
        --image "$IMAGE_TAG" \
        --region "$REGION" \
        --service-account "$SERVICE_ACCOUNT" \
        --vpc-connector "$VPC_CONNECTOR_FULL_PATH" \
        --set-cloudsql-instances "$CLOUD_SQL_CONNECTION_NAME" \
        --set-env-vars "FLASK_ENV=production,DB_HOST=/cloudsql/${CLOUD_SQL_CONNECTION_NAME},DB_PORT=5432,DB_USER=${DB_USER},DB_NAME=${DB_NAME},REDIS_HOST=${REDIS_HOST},REDIS_PORT=${REDIS_PORT:-6379}" \
        --update-secrets "DB_PASSWORD=db-password:latest,REDIS_PASSWORD=redis-password:latest,SECRET_KEY=flask-key:latest,JWT_SECRET_KEY=jwt-key:latest" \
        --command "flask" --args "db","upgrade" \
        --task-timeout 5m

    log_info "Zadanie migracji habcube-migrate utworzone/odświeżone ✓"
}
#!/bin/bash

# HabCube - Google Cloud Deployment Script
# Automatyzuje proces budowania i wdrażania aplikacji na Google Cloud Run

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Helper functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if required tools are installed
check_requirements() {
    log_info "Sprawdzanie wymagań..."

    if ! command -v gcloud &> /dev/null; then
        log_error "gcloud CLI nie jest zainstalowane. Zainstaluj z: https://cloud.google.com/sdk/docs/install"
        exit 1
    fi

    if ! command -v docker &> /dev/null; then
        log_error "Docker nie jest zainstalowany. Zainstaluj z: https://docs.docker.com/get-docker/"
        exit 1
    fi

    log_info "Wszystkie wymagania spełnione ✓"
}

# Load environment variables
load_env() {
    if [ -f ".env.gcloud" ]; then
        log_info "Wczytuję zmienne z .env.gcloud..."
        set -a
        source <(grep -v '^#' .env.gcloud | grep -v '^$' | sed 's/\r$//')
        set +a
    else
        log_warn "Plik .env.gcloud nie istnieje. Skopiuj z .env.gcloud.template i wypełnij wartościami."
        exit 1
    fi
}

# Validate required variables
validate_env() {
    log_info "Walidacja zmiennych środowiskowych..."

    required_vars=("PROJECT_ID" "REGION" "CLOUD_SQL_CONNECTION_NAME" "REDIS_HOST")

    for var in "${required_vars[@]}"; do
        if [ -z "${!var}" ]; then
            log_error "Brakująca zmienna: $var"
            exit 1
        fi
    done

    log_info "Zmienne środowiskowe OK ✓"
}

# Configure gcloud
configure_gcloud() {
    log_info "Konfiguracja gcloud..."

    gcloud config set project "$PROJECT_ID"
    gcloud config set run/region "$REGION"
    gcloud config set compute/region "$REGION"

    log_info "gcloud skonfigurowany dla projektu: $PROJECT_ID, region: $REGION ✓"
}

# Build Docker image
build_image() {
    log_info "Budowanie obrazu Docker..."

    IMAGE_TAG="${REGION}-docker.pkg.dev/${PROJECT_ID}/habcube/habcube-backend:latest"

    docker build -t "$IMAGE_TAG" ./backend

    log_info "Obraz zbudowany: $IMAGE_TAG ✓"
}

# Push to Artifact Registry
push_image() {
    log_info "Wypychanie obrazu do Artifact Registry..."

    # Configure Docker auth
    gcloud auth configure-docker "${REGION}-docker.pkg.dev" --quiet

    IMAGE_TAG="${REGION}-docker.pkg.dev/${PROJECT_ID}/habcube/habcube-backend:latest"

    docker push "$IMAGE_TAG"

    log_info "Obraz wypchnięty do Artifact Registry ✓"
}

# Deploy to Cloud Run
deploy_service() {
    log_info "Wdrażanie na Cloud Run..."

    IMAGE_TAG="${REGION}-docker.pkg.dev/${PROJECT_ID}/habcube/habcube-backend:latest"
    SERVICE_ACCOUNT="cloud-run-service-account@${PROJECT_ID}.iam.gserviceaccount.com"

    gcloud run deploy habcube-backend \
    --image "$IMAGE_TAG" \
    --platform managed \
    --region "$REGION" \
    --allow-unauthenticated \
    --port 5000 \
    --service-account "$SERVICE_ACCOUNT" \
    --add-cloudsql-instances "$CLOUD_SQL_CONNECTION_NAME" \
    --vpc-connector "projects/${PROJECT_ID}/locations/${REGION}/connectors/vpc" \
    --set-env-vars "\
FLASK_ENV=production,\
DB_HOST=/cloudsql/${CLOUD_SQL_CONNECTION_NAME},\
DB_PORT=5432,\
DB_USER=${DB_USER:-habcubeuser},\
DB_NAME=${DB_NAME:-habcube},\
REDIS_HOST=${REDIS_HOST},\
REDIS_PORT=${REDIS_PORT:-6379}" \
    --update-secrets "\
DB_PASSWORD=db-password:latest,\
REDIS_PASSWORD=redis-password:latest,\
SECRET_KEY=flask-key:latest,\
JWT_SECRET_KEY=jwt-key:latest"

    log_info "Wdrożenie ukończone ✓"
}

# Get service URL
get_service_url() {
    SERVICE_URL=$(gcloud run services describe habcube-backend \
        --region="$REGION" \
        --format="value(status.url)")

    log_info "URL serwisu: $SERVICE_URL"
    echo "$SERVICE_URL" > .service_url
}

# Test health endpoint
test_health() {
    log_info "Testowanie endpointu /health..."

    if [ -f ".service_url" ]; then
        SERVICE_URL=$(cat .service_url)
    else
        get_service_url
        SERVICE_URL=$(cat .service_url)
    fi

    sleep 5  # Poczekaj aż serwis się uruchomi

    HEALTH_RESPONSE=$(curl -s "${SERVICE_URL}/health")

    echo "$HEALTH_RESPONSE" | jq . || echo "$HEALTH_RESPONSE"

    if echo "$HEALTH_RESPONSE" | grep -q "healthy"; then
        log_info "Health check OK ✓"
    else
        log_warn "Health check zwrócił nieoczekiwaną odpowiedź"
    fi
}

# Run database migrations
run_migrations() {
    log_info "Uruchamianie migracji bazy danych..."

    gcloud run jobs execute habcube-migrate \
        --region="$REGION" \
        --wait

    log_info "Migracje zakończone ✓"
}

# Seed database with sample data
seed_database() {
    log_info "Seedowanie bazy danych przykładowymi danymi..."

    IMAGE_TAG="${REGION}-docker.pkg.dev/${PROJECT_ID}/habcube/habcube-backend:latest"
    SERVICE_ACCOUNT="${SERVICE_ACCOUNT:-cloud-run-service-account@${PROJECT_ID}.iam.gserviceaccount.com}"
    VPC_CONNECTOR_FULL_PATH="projects/${PROJECT_ID}/locations/${REGION}/connectors/vpc"

    # Delete seed job if exists
    if gcloud run jobs describe habcube-seed --region "$REGION" &>/dev/null; then
        log_warn "Usuwam istniejące zadanie seedowania habcube-seed..."
        gcloud run jobs delete habcube-seed --region "$REGION" --quiet
    fi

    # Create seed job
    gcloud run jobs create habcube-seed \
        --image "$IMAGE_TAG" \
        --region "$REGION" \
        --service-account "$SERVICE_ACCOUNT" \
        --vpc-connector "$VPC_CONNECTOR_FULL_PATH" \
        --set-cloudsql-instances "$CLOUD_SQL_CONNECTION_NAME" \
        --set-env-vars "FLASK_ENV=production,DB_HOST=/cloudsql/${CLOUD_SQL_CONNECTION_NAME},DB_PORT=5432,DB_USER=${DB_USER},DB_NAME=${DB_NAME},REDIS_HOST=${REDIS_HOST},REDIS_PORT=${REDIS_PORT:-6379}" \
        --update-secrets "DB_PASSWORD=db-password:latest,REDIS_PASSWORD=redis-password:latest,SECRET_KEY=flask-key:latest,JWT_SECRET_KEY=jwt-key:latest" \
        --command "flask" --args "seed" \
        --task-timeout 5m

    # Execute seed job
    gcloud run jobs execute habcube-seed \
        --region="$REGION" \
        --wait

    log_info "Seedowanie zakończone ✓"
}

# Show logs
show_logs() {
    log_info "Wyświetlanie ostatnich logów..."

    gcloud run services logs read habcube-backend \
        --region="$REGION" \
        --limit=50
}

# Main menu
main_menu() {
    echo ""
    echo "╔═══════════════════════════════════════╗"
    echo "║   HabCube - Google Cloud Deployment  ║"
    echo "╚═══════════════════════════════════════╝"
    echo ""
    echo "Wybierz opcję:"
    echo "  1) Pełne wdrożenie (build + push + deploy)"
    echo "  2) Tylko build obrazu"
    echo "  3) Tylko push obrazu"
    echo "  4) Tylko deploy na Cloud Run"
    echo "  5) Uruchom migracje"
    echo "  6) Test health endpoint"
    echo "  7) Pokaż logi"
    echo "  8) Wyjście"
    echo "  9) (Re)utwórz zadanie migracji Cloud Run"
    echo " 10) Zaseeduj bazę danych przykładowymi danymi"
    echo ""
    read -p "Opcja [1-10]: " choice

    case $choice in
        1)
            check_requirements
            load_env
            validate_env
            configure_gcloud
            build_image
            push_image
            deploy_service
            get_service_url
            test_health
            ;;
        2)
            check_requirements
            load_env
            validate_env
            build_image
            ;;
        3)
            check_requirements
            load_env
            validate_env
            configure_gcloud
            push_image
            ;;
        4)
            check_requirements
            load_env
            validate_env
            configure_gcloud
            deploy_service
            get_service_url
            ;;
        5)
            check_requirements
            load_env
            validate_env
            configure_gcloud
            run_migrations
            ;;
        6)
            check_requirements
            load_env
            test_health
            ;;
        7)
            check_requirements
            load_env
            validate_env
            configure_gcloud
            show_logs
            ;;
        8)
            log_info "Do widzenia!"
            exit 0
            ;;
        9)
            check_requirements
            load_env
            validate_env
            configure_gcloud
            create_migration_job
            ;;
        10)
            check_requirements
            load_env
            validate_env
            configure_gcloud
            seed_database
            ;;
        *)
            log_error "Nieprawidłowa opcja"
            main_menu
            ;;
    esac
}

# Run main menu
main_menu
