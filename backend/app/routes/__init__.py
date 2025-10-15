from flask import Blueprint, jsonify

from app import db
from app.routes.habits import habits_bp

# Health check blueprint
health_bp = Blueprint("health", __name__)


@health_bp.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint to verify service and database status"""
    try:
        db.session.execute(db.text("SELECT 1"))
        db_status = "healthy"
    except Exception as exc:
        db_status = f"unhealthy: {str(exc)}"

    return (
        jsonify({"status": "ok", "service": "HabCube Backend", "database": db_status}),
        200,
    )


api_bp = Blueprint("api", __name__)

# Register habits blueprint
api_bp.register_blueprint(habits_bp)
