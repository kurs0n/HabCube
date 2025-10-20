import os
from datetime import timedelta


class Config:
    """Base configuration"""

    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")

    # Database Configuration
    # Supports both local Docker Compose and Google Cloud SQL
    DB_USER = os.getenv("DB_USER", "habcube")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "habcube")
    DB_NAME = os.getenv("DB_NAME", "habcube")
    DB_HOST = os.getenv("DB_HOST", "postgres")
    DB_PORT = os.getenv("DB_PORT", "5432")

    # Dynamiczne budowanie SQLALCHEMY_DATABASE_URI z uwzględnieniem Cloud SQL Proxy Unix Socket
    _database_url_from_env = os.getenv("DATABASE_URL")
    if _database_url_from_env:
        SQLALCHEMY_DATABASE_URI = _database_url_from_env
    elif DB_HOST and DB_HOST.startswith('/cloudsql/'):
        # Połączenie przez Unix socket dla Cloud SQL Proxy
        unix_socket_path = f"{DB_HOST}"
        SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@/{DB_NAME}?host={unix_socket_path}"
    else:
        # Standardowe połączenie TCP/IP (lokalnie lub w innych środowiskach)
        SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT Configuration
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt-secret-key-change-in-production")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)

    # Redis Configuration
    # Supports both local Docker Compose and Google Cloud Memorystore
    REDIS_HOST = os.getenv("REDIS_HOST", "redis")  # IP address for Memorystore
    REDIS_PORT = os.getenv("REDIS_PORT", "6379")
    REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "")

    _redis_url_from_env = os.getenv("REDIS_URL")
    if _redis_url_from_env:
        REDIS_URL = _redis_url_from_env
    elif REDIS_PASSWORD:
        REDIS_URL = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/0"
    else:
        REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/0"

    # CORS Configuration
    CORS_HEADERS = "Content-Type"


class DevelopmentConfig(Config):
    """Development configuration"""

    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production configuration"""

    DEBUG = False
    TESTING = False


class TestingConfig(Config):
    """Testing configuration"""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
