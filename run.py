import os
import sys
import webbrowser
import threading
from app import create_app, db

app = create_app()

# Automatically create database tables if they do not exist on launch
with app.app_context():
    db.create_all()

def open_browser():
    """Opens the web browser automatically without duplicating tabs on Werkzeug reload."""
    if not os.environ.get('WERKZEUG_RUN_MAIN'):
        webbrowser.open('http://127.0.0.1:5000/')

if __name__ == '__main__':
    print("=" * 70)
    print("🚀 CityPulse AI Application Starting...")
    print("🌐 Server running on: http://127.0.0.1:5000/")
    print("=" * 70)
    
    # Schedule browser launch 1.2 seconds after server starts
    threading.Timer(1.2, open_browser).start()
    
    app.run(debug=True, host='127.0.0.1', port=5000)