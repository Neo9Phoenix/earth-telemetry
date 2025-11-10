from pathlib import Path
from datetime import datetime
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS

# auto-refresh imports
from apscheduler.schedulers.background import BackgroundScheduler
from fetch_epic import main as fetch_once

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
IMAGES_DIR = DATA_DIR / "images"

app = Flask(__name__)
CORS(app)

# ---- helpers ----
def cleanup_images(keep: int = 5):
    """Keep only the newest N images in data/images/."""
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    imgs = sorted(IMAGES_DIR.glob("*.png"), key=lambda p: p.stat().st_mtime, reverse=True)
    for old in imgs[keep:]:
        try:
            old.unlink()
        except Exception as e:
            print("Cleanup error:", old, e)

def warm_start():
    """Fetch once on boot and cleanup cache."""
    try:
        fetch_once()
        cleanup_images(keep=5)
        print("Warm fetch & cleanup complete.")
    except Exception as e:
        print("Warm fetch failed:", e)

# ---- routes ----
@app.get("/api/latest")
def latest():
    meta = (DATA_DIR / "metadata.json")
    if not meta.exists():
        return jsonify({"error": "No data cached yet"}), 404
    return app.response_class(meta.read_text(encoding="utf-8"), mimetype="application/json")

@app.get("/images/<path:name>")
def images(name):
    return send_from_directory(IMAGES_DIR, name)

@app.get("/")
def root():
    return jsonify({"ok": True, "endpoints": ["/api/latest", "/images/<file>"]})

# ---- boot ----
if __name__ == "__main__":
    # 1) warm fetch + cleanup now
    warm_start()

    # 2) schedule fetch + cleanup every 3 hours
    scheduler = BackgroundScheduler(daemon=True)
    def scheduled_job():
        fetch_once()
        cleanup_images(keep=5)
        print("Scheduled fetch & cleanup @", datetime.now().isoformat())
    scheduler.add_job(scheduled_job, "interval", hours=3, next_run_time=datetime.now())
    scheduler.start()

    # 3) run API
    app.run(host="127.0.0.1", port=5000, debug=True)
