# Google Cloud Deployment Guide - HabCube

Przewodnik krok po kroku do wdrożenia aplikacji HabCube na Google Cloud Platform.

## Architektura na GCP

- **Cloud Run** - Backend Flask (serwis `habcube-backend`)
- **Cloud SQL for PostgreSQL** - Baza danych (zastępuje kontener `postgres`)
- **Memorystore for Redis** - Cache (zastępuje kontener `redis`)
- **Secret Manager** - Zarządzanie poufnymi danymi
- **Artifact Registry** - Rejestr obrazów Docker

## Wymagania wstępne

1. Zainstalowany `gcloud CLI`
2. Skonfigurowane konto GCP z włączoną płatnością
3. Projekt GCP utworzony
4. Uprawnienia do tworzenia zasobów w projekcie

## Część 1: Konfiguracja GCP

### 1.1 Ustaw zmienne projektu

```bash
# Ustaw swój projekt
export PROJECT_ID="twoj-projekt-id"
export REGION="europe-west1"
export ZONE="europe-west1-b"

# Skonfiguruj gcloud
gcloud config set project $PROJECT_ID
gcloud config set run/region $REGION
gcloud config set compute/region $REGION
gcloud config set compute/zone $ZONE
```

### 1.2 Włącz wymagane API

```bash
gcloud services enable \
    run.googleapis.com \
    sqladmin.googleapis.com \
    redis.googleapis.com \
    secretmanager.googleapis.com \
    servicenetworking.googleapis.com \
    compute.googleapis.com \
    artifactregistry.googleapis.com
```

### 1.3 Utwórz sieć VPC (opcjonalnie, możesz użyć default)

```bash
# Jeśli chcesz utworzyć dedykowaną sieć
gcloud compute networks create habcube-vpc --subnet-mode=auto

# Lub użyj domyślnej sieci
export VPC_NETWORK="default"
```

### 1.4 Skonfiguruj Private Service Connection

Wymagane dla Cloud SQL i Memorystore z prywatnymi IP.

```bash
# Zarezerwuj zakres IP dla Google managed services
gcloud compute addresses create google-managed-services-range \
    --global \
    --purpose=VPC_PEERING \
    --prefix-length=20 \
    --network=$VPC_NETWORK \
    --description="IP range for Google managed services"

# Utwórz Private Service Connection
gcloud services vpc-peerings connect \
    --service=servicenetworking.googleapis.com \
    --network=$VPC_NETWORK \
    --ranges=google-managed-services-range \
    --project=$PROJECT_ID
```

## Część 2: Baza danych - Cloud SQL for PostgreSQL

### 2.1 Utwórz instancję Cloud SQL

```bash
# Ustaw hasło dla PostgreSQL (użyj silnego hasła!)
export POSTGRES_PASSWORD="twoje-silne-haslo-postgres"

# Utwórz instancję
gcloud sql instances create habcube-postgres \
    --database-version=POSTGRES_15 \
    --region=$REGION \
    --tier=db-f1-micro \
    --database-flags=cloudsql.iam_authentication=Off \
    --root-password=$POSTGRES_PASSWORD \
    --network=$VPC_NETWORK \
    --no-assign-ip \
    --enable-private-ip
```

**Uwaga:** Dla produkcji rozważ większy tier (np. `db-custom-2-7680`).

### 2.2 Utwórz bazę danych i użytkownika

```bash
# Utwórz bazę danych
gcloud sql databases create habcube \
    --instance=habcube-postgres

# Utwórz dedykowanego użytkownika dla aplikacji
gcloud sql users create habcubeuser \
    --instance=habcube-postgres \
    --password=$POSTGRES_PASSWORD
```

### 2.3 Zapisz Connection Name

```bash
# Pobierz Connection Name instancji (format: PROJECT_ID:REGION:INSTANCE_NAME)
export CLOUD_SQL_CONNECTION_NAME=$(gcloud sql instances describe habcube-postgres \
    --format="value(connectionName)")

echo "Cloud SQL Connection Name: $CLOUD_SQL_CONNECTION_NAME"
# Zapisz to - będzie potrzebne podczas deploymentu
```

## Część 3: Cache - Memorystore for Redis

### 3.1 Utwórz instancję Redis

```bash
# Ustaw hasło dla Redis
export REDIS_PASSWORD="twoje-silne-haslo-redis"

# Utwórz instancję Memorystore
gcloud redis instances create habcube-redis \
    --region=$REGION \
    --size=1 \
    --tier=BASIC \
    --connect-mode=DIRECT_PEERING \
    --network=$VPC_NETWORK \
    --auth-enabled \
    --project=$PROJECT_ID
```

**Uwaga:** Dla produkcji z high availability użyj `--tier=STANDARD_HA`.

### 3.2 Ustaw hasło Redis

```bash
gcloud redis instances update habcube-redis \
    --region=$REGION \
    --password=$REDIS_PASSWORD
```

### 3.3 Pobierz IP adres Redis

```bash
export REDIS_HOST=$(gcloud redis instances describe habcube-redis \
    --region=$REGION \
    --format="value(host)")

export REDIS_PORT=$(gcloud redis instances describe habcube-redis \
    --region=$REGION \
    --format="value(port)")

echo "Redis Host: $REDIS_HOST"
echo "Redis Port: $REDIS_PORT"
# Zapisz te wartości
```

## Część 4: Secret Manager - Zarządzanie poufnymi danymi

### 4.1 Utwórz secrety

```bash
# Secret dla PostgreSQL
echo -n "$POSTGRES_PASSWORD" | \
    gcloud secrets create habcube-db-password \
    --replication-policy="automatic" \
    --data-file=-

# Secret dla Redis
echo -n "$REDIS_PASSWORD" | \
    gcloud secrets create habcube-redis-password \
    --replication-policy="automatic" \
    --data-file=-

# Secret dla Flask SECRET_KEY (wygeneruj losowy klucz)
python3 -c 'import secrets; print(secrets.token_hex(32))' | \
    gcloud secrets create habcube-secret-key \
    --replication-policy="automatic" \
    --data-file=-

# Secret dla JWT_SECRET_KEY
python3 -c 'import secrets; print(secrets.token_hex(32))' | \
    gcloud secrets create habcube-jwt-secret \
    --replication-policy="automatic" \
    --data-file=-
```

## Część 5: Build i Deploy aplikacji

### 5.1 Utwórz Artifact Registry repository

```bash
gcloud artifacts repositories create habcube-repo \
    --repository-format=docker \
    --location=$REGION \
    --description="Docker repository for HabCube"

# Skonfiguruj Docker auth
gcloud auth configure-docker ${REGION}-docker.pkg.dev
```

### 5.2 Zbuduj i wypchnij obraz Docker

```bash
# Zbuduj obraz (z katalogu głównego projektu)
docker build -t ${REGION}-docker.pkg.dev/${PROJECT_ID}/habcube-repo/habcube-backend:latest \
    ./backend

# Wypchnij do Artifact Registry
docker push ${REGION}-docker.pkg.dev/${PROJECT_ID}/habcube-repo/habcube-backend:latest
```

### 5.3 Utwórz Service Account dla Cloud Run

```bash
# Utwórz dedykowany Service Account
gcloud iam service-accounts create habcube-run-sa \
    --display-name="HabCube Cloud Run Service Account"

export SERVICE_ACCOUNT="habcube-run-sa@${PROJECT_ID}.iam.gserviceaccount.com"

# Przyznaj uprawnienia
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:${SERVICE_ACCOUNT}" \
    --role="roles/secretmanager.secretAccessor"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:${SERVICE_ACCOUNT}" \
    --role="roles/cloudsql.client"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:${SERVICE_ACCOUNT}" \
    --role="roles/redis.viewer"
```

### 5.4 Deploy na Cloud Run

```bash
gcloud run deploy habcube-backend \
    --image ${REGION}-docker.pkg.dev/${PROJECT_ID}/habcube-repo/habcube-backend:latest \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --port 5000 \
    --service-account $SERVICE_ACCOUNT \
    --add-cloudsql-instances $CLOUD_SQL_CONNECTION_NAME \
    --vpc-connector projects/${PROJECT_ID}/locations/${REGION}/connectors/habcube-vpc-connector \
    --set-env-vars "\
PORT=5000,\
FLASK_ENV=production,\
DB_HOST=127.0.0.1,\
DB_PORT=5432,\
DB_USER=habcubeuser,\
DB_NAME=habcube,\
REDIS_HOST=${REDIS_HOST},\
REDIS_PORT=${REDIS_PORT}" \
    --update-secrets "\
DB_PASSWORD=habcube-db-password:latest,\
REDIS_PASSWORD=habcube-redis-password:latest,\
SECRET_KEY=habcube-secret-key:latest,\
JWT_SECRET_KEY=habcube-jwt-secret:latest"
```

**Uwaga:** Jeśli jeszcze nie masz VPC Connector, utwórz go:

```bash
gcloud compute networks vpc-access connectors create habcube-vpc-connector \
    --region=$REGION \
    --network=$VPC_NETWORK \
    --range=10.8.0.0/28
```

## Część 6: Migracje bazy danych

Po wdrożeniu musisz uruchomić migracje. Możesz to zrobić przez Cloud Run Jobs lub lokalnie.

### 6.1 Uruchom migracje przez Cloud Run Job

```bash
# Utwórz Job do migracji
gcloud run jobs create habcube-migrate \
    --image ${REGION}-docker.pkg.dev/${PROJECT_ID}/habcube-repo/habcube-backend:latest \
    --region $REGION \
    --service-account $SERVICE_ACCOUNT \
    --add-cloudsql-instances $CLOUD_SQL_CONNECTION_NAME \
    --set-env-vars "\
DB_HOST=127.0.0.1,\
DB_PORT=5432,\
DB_USER=habcubeuser,\
DB_NAME=habcube" \
    --update-secrets "\
DB_PASSWORD=habcube-db-password:latest" \
    --command "flask" \
    --args "db,upgrade"

# Uruchom migrację
gcloud run jobs execute habcube-migrate --region=$REGION
```

### 6.2 Lub uruchom migracje lokalnie przez Cloud SQL Proxy

```bash
# Zainstaluj Cloud SQL Proxy
wget https://dl.google.com/cloudsql/cloud_sql_proxy.linux.amd64 -O cloud_sql_proxy
chmod +x cloud_sql_proxy

# Uruchom proxy w tle
./cloud_sql_proxy -instances=$CLOUD_SQL_CONNECTION_NAME=tcp:5432 &

# Ustaw zmienne środowiskowe
export DATABASE_URL="postgresql://habcubeuser:$POSTGRES_PASSWORD@127.0.0.1:5432/habcube"

# Uruchom migracje (z katalogu backend)
cd backend
flask db upgrade
```

## Część 7: Weryfikacja

### 7.1 Pobierz URL serwisu

```bash
export SERVICE_URL=$(gcloud run services describe habcube-backend \
    --region=$REGION \
    --format="value(status.url)")

echo "Service URL: $SERVICE_URL"
```

### 7.2 Testuj endpoint /health

```bash
curl $SERVICE_URL/health

# Powinno zwrócić:
# {
#   "database": "healthy",
#   "service": "HabCube Backend",
#   "status": "ok"
# }
```

### 7.3 Sprawdź logi

```bash
gcloud run services logs read habcube-backend --region=$REGION --limit=50
```

## Część 8: Aktualizacje i rozwój

### 8.1 Deploy nowej wersji

```bash
# Zbuduj nowy obraz
docker build -t ${REGION}-docker.pkg.dev/${PROJECT_ID}/habcube-repo/habcube-backend:v2 ./backend

# Wypchnij
docker push ${REGION}-docker.pkg.dev/${PROJECT_ID}/habcube-repo/habcube-backend:v2

# Deploy
gcloud run services update habcube-backend \
    --image ${REGION}-docker.pkg.dev/${PROJECT_ID}/habcube-repo/habcube-backend:v2 \
    --region=$REGION
```

### 8.2 Rollback do poprzedniej wersji

```bash
gcloud run services update-traffic habcube-backend \
    --to-revisions=PREVIOUS=100 \
    --region=$REGION
```

## Część 9: Czyszczenie zasobów (opcjonalnie)

```bash
# Usuń Cloud Run service
gcloud run services delete habcube-backend --region=$REGION

# Usuń Cloud SQL
gcloud sql instances delete habcube-postgres

# Usuń Redis
gcloud redis instances delete habcube-redis --region=$REGION

# Usuń secrety
gcloud secrets delete habcube-db-password
gcloud secrets delete habcube-redis-password
gcloud secrets delete habcube-secret-key
gcloud secrets delete habcube-jwt-secret

# Usuń VPC connector
gcloud compute networks vpc-access connectors delete habcube-vpc-connector --region=$REGION
```

## Wskazówki i best practices

1. **Nigdy nie commituj haseł** - używaj Secret Manager
2. **Używaj małych instancji dla testów** - skaluj dla produkcji
3. **Monitoruj koszty** - ustaw alerty budżetowe w GCP Console
4. **Włącz logi i monitoring** - Cloud Logging, Cloud Monitoring
5. **Backupy** - Cloud SQL automatycznie tworzy backupy, ale skonfiguruj retencję
6. **SSL/TLS** - Cloud Run automatycznie obsługuje HTTPS
7. **Custom domain** - możesz dodać własną domenę w Cloud Run

## Troubleshooting

### Problem: "could not translate host name"
- Sprawdź czy VPC Connector jest poprawnie skonfigurowany
- Upewnij się że `DB_HOST=127.0.0.1` dla Cloud SQL Proxy

### Problem: "Permission denied" na secretach
- Sprawdź uprawnienia Service Account (`roles/secretmanager.secretAccessor`)

### Problem: Redis connection failed
- Sprawdź czy VPC Connector łączy się z tą samą siecią co Memorystore
- Zweryfikuj IP i port Redis

### Problem: Deployment timeout
- Zwiększ `--timeout` w `gcloud run deploy`
- Sprawdź health check endpoint

## Podsumowanie

Gratulacje! 🎉 Twoja aplikacja HabCube działa teraz na Google Cloud Platform z:

- ✅ Serverless backend na Cloud Run
- ✅ Zarządzaną bazą PostgreSQL
- ✅ Zarządzanym cache Redis
- ✅ Bezpiecznymi secretami
- ✅ Automatycznym skalowaniem
- ✅ HTTPS out-of-the-box

URL produkcyjny: `$SERVICE_URL`
