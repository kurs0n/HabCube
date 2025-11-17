"""
Main entry point for HabCube Backend
"""
import sys
print("WSGI: Starting import", file=sys.stderr, flush=True)

from app import create_app, db
print("WSGI: Imported create_app and db", file=sys.stderr, flush=True)

print("WSGI: Creating app", file=sys.stderr, flush=True)
application = create_app()
print("WSGI: App created successfully", file=sys.stderr, flush=True)

# Gunicorn expects 'application' by default, but we'll use explicit wsgi:application
app = application

if __name__ == "__main__":
    with application.app_context():
        db.create_all()
    application.run(host="0.0.0.0", port=5000)
