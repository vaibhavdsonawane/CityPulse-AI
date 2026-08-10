import os
import threading
import webbrowser
from app import create_app, db

app = create_app()

def open_browser():
    """Opens the default web browser to the local app URL."""
    webbrowser.open_new('http://127.0.0.1:5000/')

if __name__ == '__main__':
    # Flask's debug mode restarts the server twice. 
    # This check ensures the browser only opens one single tab!
    if os.environ.get('WERKZEUG_RUN_MAIN') != 'true':
        threading.Timer(1.25, open_browser).start()
        
    app.run(debug=True, host='127.0.0.1', port=5000)