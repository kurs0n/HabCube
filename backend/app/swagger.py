"""Helpers for conditionally enabling Flasgger documentation."""
from __future__ import annotations

from typing import Any, Callable

from flask import Flask


def _noop_decorator(*_: Any, **__: Any) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """No-op decorator when Swagger is disabled."""
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        return func
    return decorator


def swag_from(*args: Any, **kwargs: Any) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Conditionally apply swag_from decorator based on config."""
    # Import config here to avoid circular imports
    from app.config import Config
    
    if not Config.ENABLE_SWAGGER_DOCS:
        return _noop_decorator(*args, **kwargs)

    from flasgger import swag_from as flasgger_swag_from
    return flasgger_swag_from(*args, **kwargs)


def init_swagger(app: Flask) -> None:
    """Initialize Swagger/Flasgger if enabled in config."""
    if not app.config.get("ENABLE_SWAGGER_DOCS", False):
        app.logger.info(
            "Swagger docs disabled. Set ENABLE_SWAGGER_DOCS=true to enable."
        )
        return

    from flasgger import Swagger

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
    app.logger.info("Swagger docs enabled at /api/docs/")
