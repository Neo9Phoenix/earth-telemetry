import { useEffect, useState } from "react";
import axios from "axios";

// Automatically use localhost in dev, Render URL in prod
const BASE = import.meta.env.VITE_API_BASE || "";

export default function App() {
  const [data, setData] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  // Load latest EPIC data
  const load = () =>
    axios.get(`${BASE}/api/latest`)
      .then(res => setData(res.data))
      .catch(err => setError(err.message))
      .finally(() => setLoading(false));

  useEffect(() => { load(); }, []);

  // Loading state
  if (loading) return (
    <div style={{
      minHeight: "100vh",
      display: "grid",
      placeItems: "center",
      fontFamily: "system-ui",
      background: "linear-gradient(180deg,#0b1020,#0f1b3d 60%,#0b1020)",
      color: "#eef2ff"
    }}>
      <div style={{ opacity: 0.8 }}>⏳ Loading latest Earth data…</div>
    </div>
  );

  // Error state
  if (error) return (
    <div style={{
      minHeight: "100vh",
      display: "grid",
      placeItems: "center",
      fontFamily: "system-ui",
      background: "linear-gradient(180deg,#0b1020,#0f1b3d 60%,#0b1020)",
      color: "#eef2ff"
    }}>
      <div>❌ API error: {error}</div>
    </div>
  );

  // Main content
  return (
    <div style={{
      minHeight: "100vh",
      background: "linear-gradient(180deg,#0b1020,#0f1b3d 60%,#0b1020)",
      color: "#eef2ff",
      padding: "24px",
      fontFamily: "system-ui, Segoe UI, Roboto"
    }}>
      <div style={{ maxWidth: 960, margin: "0 auto" }}>
        <h1 style={{ margin: "0 0 8px" }}>🌎 NASA EPIC — Live Earth Image</h1>
        <p style={{ margin: "0 0 16px", opacity: 0.85 }}>
          <b>Date:</b> {data.date}{data.caption ? ` — ${data.caption}` : ""}
        </p>

        <div style={{
          background: "#111827",
          padding: 12,
          borderRadius: 12,
          boxShadow: "0 10px 30px rgba(0,0,0,0.35)"
        }}>
          <button
            onClick={() => { setLoading(true); load(); }}
            style={{
              padding: "8px 12px",
              borderRadius: 8,
              border: "1px solid #374151",
              background: "#1f2937",
              color: "#e5e7eb",
              marginBottom: "10px",
              cursor: "pointer"
            }}
          >
            🔄 Refresh
          </button>

          <img
            src={`${BASE}${data.image_local}`}
            alt="EPIC Earth"
            style={{
              width: "100%",
              borderRadius: 8,
              transition: "transform .4s ease"
            }}
            onMouseEnter={e => e.target.style.transform = "scale(1.01)"}
            onMouseLeave={e => e.target.style.transform = "scale(1.0)"}
          />
        </div>

        <p style={{ marginTop: 12 }}>
          <a
            href={data.image_url}
            target="_blank"
            rel="noreferrer"
            style={{ color: "#a5b4fc" }}
          >
            View original on NASA EPIC
          </a>
        </p>
      </div>
    </div>
  );
}
