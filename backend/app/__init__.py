import os
import sys

print("app/__init__.py: Start", file=sys.stderr, flush=True)

print("app/__init__.py: Importing flask", file=sys.stderr, flush=True)
from flask import Flask
print("app/__init__.py: Importing flask_cors", file=sys.stderr, flush=True)
from flask_cors import CORS
print("app/__init__.py: Importing flask_jwt_extended", file=sys.stderr, flush=True)
from flask_jwt_extended import JWTManager
print("app/__init__.py: Importing flask_migrate", file=sys.stderr, flush=True)
from flask_migrate import Migrate
print("app/__init__.py: Importing flask_sqlalchemy", file=sys.stderr, flush=True)
from flask_sqlalchemy import SQLAlchemy
print("app/__init__.py: All imports done", file=sys.stderr, flush=True)

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()


def create_app(config_name=None):
    app = Flask(__name__)

    # Config
    if config_name is None:
        config_name = os.getenv("FLASK_ENV", "development")

    app.config.from_object(f"app.config.{config_name.capitalize()}Config")

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    CORS(app)

    # Conditionally initialize Swagger
    from app.swagger import init_swagger

    init_swagger(app)

    # Blueprinty
    from app.routes import api_bp, health_bp

    app.register_blueprint(health_bp)
    app.register_blueprint(api_bp, url_prefix="/api/v1")

    # Register CLI commands
    from app import cli

    cli.init_app(app)

    return app
