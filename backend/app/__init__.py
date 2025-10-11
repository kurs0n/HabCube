import os

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

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

    # Blueprinty
    from app.routes import api_bp, health_bp

    app.register_blueprint(health_bp)
    app.register_blueprint(api_bp, url_prefix="/api/v1")

    return app
