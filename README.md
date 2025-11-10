# 🌍 Earth Telemetry API

A Python + Flask backend service that fetches and serves live NASA EPIC Earth imagery.  
It automatically refreshes data, caches the latest images, and exposes clean JSON + image endpoints.

---

## 🚀 Features
- **Flask API** with `GET /api/latest` and `/images/<file>` routes  
- **Automated NASA EPIC fetch** every few hours via APScheduler  
- **CORS-enabled** for frontend access (Vercel)  
- **Persistent caching** of image + metadata in `/data`  
- **Manual refresh** endpoint (`/api/refresh`) to trigger fetch on demand

---

## 🔗 Live Deployment
**Render:** [https://earth-telemetry-api.onrender.com](https://earth-telemetry-api.onrender.com)

---

## 🧭 API Endpoints

| Endpoint | Method | Description |
|-----------|--------|-------------|
| `/` | GET | Health check + endpoint list |
| `/api/latest` | GET | Returns the latest metadata.json (Earth image + date/time) |
| `/api/refresh` | GET/POST | Manually triggers an image refresh |
| `/images/<file>` | GET | Serves cached image from `/data/images` |

Example:
```bash
curl https://earth-telemetry-api.onrender.com/api/latest
```

### 🧩 Tech Stack

Python 3.10+
Flask
Flask-CORS
APScheduler
Render Web Service

### ⚙️ Local Development
```bash
git clone https://github.com/Neo9Phoenix/earth-telemetry.git
cd earth-telemetry
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python backend/app.py
```

Then open → http://127.0.0.1:5000/api/latest


### 🛰️ Credits

Data provided by NASA EPIC API
Developed by Neo

