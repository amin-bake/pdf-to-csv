"""
WSGI entry point for production deployment.

This file provides a WSGI-compatible entry point for production servers
like Gunicorn, Waitress, or uWSGI.

Usage with Gunicorn (Linux/Mac):
    gunicorn --bind 0.0.0.0:8000 --workers 4 --timeout 120 wsgi:app

Usage with Waitress (Windows):
    waitress-serve --host 0.0.0.0 --port 8000 --threads 4 wsgi:app

For development, use:
    python app.py
"""

from app import app

if __name__ == "__main__":
    # This block is only executed when running this file directly
    # It's not used by WSGI servers
    app.run()
