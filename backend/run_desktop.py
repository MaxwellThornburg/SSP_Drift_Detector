import uvicorn
import threading
import webview
from app.main import app

def start_server():
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")

if __name__ == "__main__":
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    
    webview.create_window(
        "SSP Drift Detector",
        "http://127.0.0.1:8000",
        width=1200,
        height=800,
        frameless=True,           # Removes window borders
        resizable=False,          # Fixed size like a launcher
        background_color="#0a0a0a",
        on_top=False,
        confirm_close=True
    )
    
    webview.start()