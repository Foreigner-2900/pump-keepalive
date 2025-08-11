# server.py
import os
import time
import threading
import requests
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running"

def _ping_loop():
    """Periodically ping target URL from env REPLIT_URL."""
    target = os.getenv("REPLIT_URL")  # paste your Replit dev url here (or set in Render env)
    if not target:
        print("No REPLIT_URL set — ping loop disabled.")
        return
    interval = int(os.getenv("PING_INTERVAL", "240"))  # seconds, default 240 (4 min)
    print("Ping loop starting. target=", target, "interval=", interval)
    while True:
        try:
            requests.get(target, timeout=10)
            print("Pinged", target)
        except Exception as e:
            print("Ping error:", e)
        time.sleep(interval)

# start ping thread at import time (works with gunicorn)
threading.Thread(target=_ping_loop, daemon=True).start()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
