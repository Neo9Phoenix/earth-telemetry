# backend/app.py
from pathlib import Path
from datetime import datetime
import os

from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler

from fetch_epic import main as fetch_once

# ----- Paths -----
ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
IMAGES_DIR = DATA_DIR / "images"

# ----- App -----
app = Flask(__name__)
CORS(app)

# ----- Helpers -----
def cleanup_images(keep: int = 5):
    """Keep only the newest N images in data/images/."""
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    imgs = sorted(IMAGES_DIR.glob("*.png"),
                  key=lambda p: p.stat().st_mtime,
                  reverse=True)
    for old in imgs[keep:]:
        try:
            old.unlink()
        except Exception as e:
            print("Cleanup error:", old, e)

def warm_start():
    """
    Fetch once and cleanup cache.
    Safe to call multiple times; used both locally and on first cloud request.
    """
    try:
        fetch_once()
        cleanup_images(keep=5)
        print("Warm fetch & cleanup complete.")
    except Exception as e:
        print("Warm fetch failed:", e)

# ----- Routes -----
@app.get("/api/latest")
def latest():
    meta = (DATA_DIR / "metadata.json")
    if not meta.exists():
        return jsonify({"error": "No data cached yet"}), 404
    return app.response_class(meta.read_text(encoding="utf-8"),
                              mimetype="application/json")

@app.get("/images/<path:name>")
def images(name: str):
    return send_from_directory(IMAGES_DIR, name)

@app.get("/")
def root():
    return jsonify({"ok": True, "endpoints": ["/api/latest", "/images/<file>"]})

# Manual refresh endpoint you can hit after deploy (or any time)
@app.route("/api/refresh", methods=["GET", "POST"])
def api_refresh():
    try:
        warm_start()
        return jsonify({"ok": True, "refreshed": True}), 200
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

# ----- Flask 3.x compatible "run once" init -----
_initialized = False

@app.before_request
def ensure_initialized():
    """
    Flask 3.x removed before_first_request; this guards a one-time warm_start
    when the first real request hits the service (works on Render + locally).
    """
    global _initialized
    if not _initialized:
        # If data already exists (e.g., you called /api/refresh) skip work
        if not (DATA_DIR / "metadata.json").exists():
            warm_start()
        _initialized = True

# ----- Local dev boot only -----
if __name__ == "__main__":
    # Warm immediately for local dev
    warm_start()

    # Local scheduler (free cloud dynos may sleep, so keep this local)
    scheduler = BackgroundScheduler(daemon=True)
    def scheduled_job():
        warm_start()
        print("Scheduled fetch & cleanup @", datetime.now().isoformat())
    scheduler.add_job(scheduled_job, "interval", hours=3, next_run_time=datetime.now())
    scheduler.start()

    # Use localhost for dev
    app.run(host="127.0.0.1", port=5000, debug=True)
