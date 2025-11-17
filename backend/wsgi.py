"""
Main entry point for HabCube Backend
"""
import sys
print("WSGI: Starting import", file=sys.stderr, flush=True)

from app import create_app, db
print("WSGI: Imported modules", file=sys.stderr, flush=True)

print("WSGI: Creating app", file=sys.stderr, flush=True)
app = create_app()
print("WSGI: App created successfully", file=sys.stderr, flush=True)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000)
