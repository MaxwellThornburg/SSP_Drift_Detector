import uvicorn
import threading
import webview
import os
from app.main import app

def start_server():
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")

if __name__ == "__main__":
    # Start FastAPI in background thread
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    
    # Create native desktop window
    webview.create_window(
        "SSP Drift Detector",
        "http://127.0.0.1:8000",
        width=1200,
        height=800,
        resizable=True,
        min_size=(800, 600),
        background_color="#111827",  # Matches your dark theme
        text_select=True
    )
    
    webview.start()