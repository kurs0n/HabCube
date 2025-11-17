import os
import sys

print("app/__init__.py: Start", file=sys.stderr, flush=True)

print("app/__init__.py: Importing flasgger", file=sys.stderr, flush=True)
from flasgger import Swagger
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

    # Swagger configuration
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": "apispec",
                "route": "/apispec.json",
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/api/docs/",
    }

    swagger_template = {
        "info": {
            "title": "HabCube API",
            "description": "API for managing habits and tracking progress",
            "version": "1.0.0",
        },
        "basePath": "/api/v1",
    }

    Swagger(app, config=swagger_config, template=swagger_template)

    # Blueprinty
    from app.routes import api_bp, health_bp

    app.register_blueprint(health_bp)
    app.register_blueprint(api_bp, url_prefix="/api/v1")

    # Register CLI commands
    from app import cli

    cli.init_app(app)

    return app
