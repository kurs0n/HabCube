# Google Cloud Deployment - Quick Reference

## Szybka ściąga dla deployment na GCP

### 1. Przygotowanie (jednorazowe)

```bash
# 1. Sprawdź wymagania
make gcloud-setup

# 2. Skopiuj template i wypełnij dane
cp .env.gcloud.template .env.gcloud
nano .env.gcloud  # lub vim/code

# 3. Zobacz pełną dokumentację
make gcloud-docs
# lub
cat GOOGLE_CLOUD_DEPLOYMENT.md
```

### 2. Deployment - Opcja A (Interaktywna)

```bash
# Uruchom interaktywny skrypt
./deploy-gcloud.sh

# Wybierz opcję 1 dla pełnego deployment
```

### 3. Deployment - Opcja B (Ręczna, krok po kroku)

```bash
# Ustaw zmienne z .env.gcloud
source .env.gcloud

# Build obrazu
docker build -t ${REGION}-docker.pkg.dev/${PROJECT_ID}/habcube-repo/habcube-backend:latest ./backend

# Push do Artifact Registry
gcloud auth configure-docker ${REGION}-docker.pkg.dev
docker push ${REGION}-docker.pkg.dev/${PROJECT_ID}/habcube-repo/habcube-backend:latest

# Deploy na Cloud Run
gcloud run deploy habcube-backend \
  --image ${REGION}-docker.pkg.dev/${PROJECT_ID}/habcube-repo/habcube-backend:latest \
  --region ${REGION} \
  --platform managed \
  --allow-unauthenticated \
  --port 5000 \
  # ... (reszta flag - zobacz GOOGLE_CLOUD_DEPLOYMENT.md)
```

### 4. Po deployment

```bash
# Sprawdź URL serwisu
gcloud run services describe habcube-backend \
  --region=${REGION} \
  --format="value(status.url)"

# Test health endpoint
curl https://YOUR-SERVICE-URL/health

# Zobacz logi
gcloud run services logs read habcube-backend \
  --region=${REGION} \
  --limit=50
```

### 5. Kluczowe różnice: Local vs Google Cloud

| Aspekt | Local (Docker Compose) | Google Cloud |
|--------|------------------------|--------------|
| **Database** | PostgreSQL container | Cloud SQL for PostgreSQL |
| **DB_HOST** | `postgres` | `127.0.0.1` (Cloud SQL Proxy) |
| **Redis** | Redis container | Memorystore for Redis |
| **REDIS_HOST** | `redis` | IP Memorystore (np. `10.x.x.x`) |
| **Secrets** | `.env` file | Secret Manager |
| **PORT** | `5000` | `5000` (ale Cloud Run domyślnie używa 8080) |
| **Scaling** | Manual | Automatic (serverless) |
| **HTTPS** | Nie | Tak (automatyczne) |

### 6. Najczęstsze problemy

#### "could not translate host name"
- **Przyczyna:** `DB_HOST` jest ustawiony na `postgres` zamiast `127.0.0.1`
- **Rozwiązanie:** W Google Cloud ustaw `DB_HOST=127.0.0.1`

#### "Permission denied" na secretach
- **Przyczyna:** Service Account nie ma uprawnień
- **Rozwiązanie:** Dodaj rolę `roles/secretmanager.secretAccessor`

#### Redis connection timeout
- **Przyczyna:** Brak VPC Connector lub zły IP
- **Rozwiązanie:** Sprawdź VPC Connector i IP Memorystore

### 7. Komendy Makefile

```bash
make gcloud-setup   # Sprawdź wymagania
make gcloud-deploy  # Interaktywny deployment
make gcloud-docs    # Pokaż dokumentację
```

### 8. Struktura zmiennych w .env.gcloud

```env
# Minimalne wymagane zmienne
PROJECT_ID=twoj-projekt-id
REGION=europe-west1
CLOUD_SQL_CONNECTION_NAME=PROJECT:REGION:INSTANCE
REDIS_HOST=10.x.x.x  # IP z Memorystore
```

### 9. Checklist przed deployment

- [ ] Projekt GCP utworzony i billing włączony
- [ ] Wszystkie API włączone (Cloud Run, SQL, Redis, etc.)
- [ ] VPC Network skonfigurowana
- [ ] Cloud SQL instancja utworzona
- [ ] Memorystore Redis utworzona
- [ ] Secrety utworzone w Secret Manager
- [ ] Service Account z odpowiednimi uprawnieniami
- [ ] VPC Connector utworzony
- [ ] Artifact Registry repository utworzone
- [ ] Plik `.env.gcloud` wypełniony
- [ ] gcloud CLI zainstalowane i zalogowane

### 10. Przydatne linki

- [Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Cloud SQL for PostgreSQL](https://cloud.google.com/sql/docs/postgres)
- [Memorystore for Redis](https://cloud.google.com/memorystore/docs/redis)
- [Secret Manager](https://cloud.google.com/secret-manager/docs)
- [Full Deployment Guide](./GOOGLE_CLOUD_DEPLOYMENT.md)
