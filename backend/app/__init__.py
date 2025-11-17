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

    # Conditionally initialize Swagger (disabled on Cloud Run by default)
    enable_swagger = os.getenv("ENABLE_SWAGGER_DOCS", "").lower() in {"1", "true", "yes", "on"}
    running_on_cloud_run = bool(os.getenv("K_SERVICE"))
    
    if not running_on_cloud_run or enable_swagger:
        from app.swagger import init_swagger
        init_swagger(app)

    # Register blueprints
    from app.routes import health_bp, api_bp

    app.register_blueprint(health_bp)
    app.register_blueprint(api_bp, url_prefix="/api/v1")
    
    # Debug: Log registered routes
    import sys
    print("=== Registered Flask Routes ===", file=sys.stderr, flush=True)
    for rule in app.url_map.iter_rules():
        print(f"{rule.endpoint}: {rule.rule} [{', '.join(rule.methods)}]", file=sys.stderr, flush=True)
    print("================================", file=sys.stderr, flush=True)

    # Register CLI commands
    from app import cli
    cli.init_app(app)

    return app
