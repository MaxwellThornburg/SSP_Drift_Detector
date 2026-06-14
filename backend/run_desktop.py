import uvicorn
import webview
import threading
import sys
import time
from app.main import app

def start_server():
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="warning")

if __name__ == "__main__":
    # Start the FastAPI server in a background thread
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    
    # Give the server a moment to start before opening the window
    time.sleep(1)
    
    # Create a native window using pywebview
    webview.create_window("SSP Drift Detector", "http://127.0.0.1:8000", width=1200, height=800)
    webview.start()
    
    # When the window is closed, exit the application
    sys.exit(0)