import json
from datetime import datetime
from pathlib import Path
import requests

EPIC_API = "https://epic.gsfc.nasa.gov/api/natural"

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
IMAGES_DIR = DATA_DIR / "images"
DATA_DIR.mkdir(parents=True, exist_ok=True)
IMAGES_DIR.mkdir(parents=True, exist_ok=True)

def build_image_url(item):
    dt = datetime.strptime(item["date"], "%Y-%m-%d %H:%M:%S")
    yyyy, mm, dd = dt.strftime("%Y"), dt.strftime("%m"), dt.strftime("%d")
    image_id = item["image"]
    return f"https://epic.gsfc.nasa.gov/archive/natural/{yyyy}/{mm}/{dd}/png/{image_id}.png"

def main():
    r = requests.get(EPIC_API, timeout=30)
    r.raise_for_status()
    data = r.json()
    if not data:
        print("No EPIC frames available.")
        return

    latest = data[0]
    img_url = build_image_url(latest)

    dt = datetime.strptime(latest["date"], "%Y-%m-%d %H:%M:%S")
    file_name = f'{dt.strftime("%Y-%m-%d")}_{latest["image"]}.png'
    img_path = IMAGES_DIR / file_name

    if not img_path.exists():
        ir = requests.get(img_url, timeout=60)
        ir.raise_for_status()
        img_path.write_bytes(ir.content)

    payload = {
        "date": latest["date"],
        "caption": latest.get("caption"),
        "image_name": latest["image"],
        "image_url": img_url,
        "image_local": f"/images/{file_name}",
    }
    (DATA_DIR / "metadata.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print("Saved:")
    print("  -", img_path)
    print("  -", DATA_DIR / "metadata.json")

if __name__ == "__main__":
    main()
