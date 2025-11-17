"""
Main entry point for HabCube Backend
"""
import sys
print("WSGI: Starting import", file=sys.stderr, flush=True)

try:
    from app import create_app, db
    print("WSGI: Imported create_app and db", file=sys.stderr, flush=True)

    print("WSGI: Creating app", file=sys.stderr, flush=True)
    application = create_app()
    print("WSGI: App created successfully", file=sys.stderr, flush=True)
    
    # Gunicorn expects 'application' by default, but we'll use explicit wsgi:application
    app = application
    
    print("WSGI: Checking routes...", file=sys.stderr, flush=True)
    with application.app_context():
        for rule in application.url_map.iter_rules():
            print(f"WSGI Route: {rule.endpoint} -> {rule.rule}", file=sys.stderr, flush=True)
    print("WSGI: Initialization complete!", file=sys.stderr, flush=True)
    
except Exception as e:
    print(f"WSGI: FATAL ERROR during init: {e}", file=sys.stderr, flush=True)
    import traceback
    traceback.print_exc(file=sys.stderr)
    raise

if __name__ == "__main__":
    with application.app_context():
        db.create_all()
    application.run(host="0.0.0.0", port=5000)
