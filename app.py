"""
FPL Dashboard – Backend Proxy Server
=====================================
Proxies requests to the FPL public API and adds CORS headers.
Also serves the frontend index.html so everything runs from one URL.

Local usage:
    pip install -r requirements.txt
    python app.py

Production (Render):
    gunicorn app:app
"""

import os
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import requests

# frontend/ folder sits next to this file
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "frontend")

app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path="")
CORS(app)

FPL_BASE = "https://fantasy.premierleague.com/api"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-GB,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://fantasy.premierleague.com/",
    "Origin": "https://fantasy.premierleague.com",
    "DNT": "1",
}


def fpl_get(path: str) -> dict:
    url = f"{FPL_BASE}/{path}"
    response = requests.get(url, headers=HEADERS, timeout=20)
    response.raise_for_status()
    return response.json()


# ── Frontend ──────────────────────────────────────────────────────────────────

@app.route("/")
def serve_frontend():
    return send_from_directory(FRONTEND_DIR, "index.html")


# ── API Endpoints ─────────────────────────────────────────────────────────────

@app.route("/api/league/<int:liga_id>")
def get_league(liga_id: int):
    try:
        page = 1
        all_results = []
        league_info = None
        while True:
            data = fpl_get(
                f"leagues-classic/{liga_id}/standings/?page_standings={page}"
            )
            if league_info is None:
                league_info = data
            all_results.extend(data.get("standings", {}).get("results", []))
            if not data.get("standings", {}).get("has_next", False):
                break
            page += 1
        league_info["standings"]["results"] = all_results
        return jsonify(league_info)
    except requests.exceptions.HTTPError as exc:
        return jsonify({"error": str(exc)}), exc.response.status_code
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


@app.route("/api/manager/<int:manager_id>/history")
def get_history(manager_id: int):
    try:
        return jsonify(fpl_get(f"entry/{manager_id}/history/"))
    except requests.exceptions.HTTPError as exc:
        return jsonify({"error": str(exc)}), exc.response.status_code
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


@app.route("/api/bootstrap")
def get_bootstrap():
    try:
        data = fpl_get("bootstrap-static/")
        return jsonify({
            "events": data.get("events", []),
            "total_players": data.get("total_players", 0),
            "game_settings": data.get("game_settings", {}),
        })
    except requests.exceptions.HTTPError as exc:
        return jsonify({"error": str(exc)}), exc.response.status_code
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


@app.route("/api/manager/<int:manager_id>/picks/<int:gw>")
def get_picks(manager_id: int, gw: int):
    try:
        return jsonify(fpl_get(f"entry/{manager_id}/event/{gw}/picks/"))
    except requests.exceptions.HTTPError as exc:
        return jsonify({"error": str(exc)}), exc.response.status_code
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


# ── Run ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"\n🏆  FPL Dashboard  →  http://localhost:{port}\n")
    app.run(debug=True, port=port, host="0.0.0.0")
