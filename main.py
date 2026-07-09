from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
import pandas as pd
import time

app = Flask(__name__)

# 🟩 Full CORS-stöd för Render frontend
CORS(app, resources={r"/*": {"origins": "https://bentus-touren-frontend.onrender.com"}}, supports_credentials=True)

@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "https://bentus-touren-frontend.onrender.com"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    response.headers["Access-Control-Allow-Methods"] = "GET, OPTIONS"
    response.headers["Access-Control-Max-Age"] = "3600"
    return response

# 🟩 Fångar alla OPTIONS-anrop innan Flask försöker matcha route
@app.before_request
def handle_options():
    if request.method == "OPTIONS":
        response = make_response(jsonify({"status": "ok"}), 200)
        response.headers["Access-Control-Allow-Origin"] = "https://bentus-touren-frontend.onrender.com"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        response.headers["Access-Control-Allow-Methods"] = "GET, OPTIONS"
        response.headers["Access-Control-Max-Age"] = "3600"
        return response

# ---------------------------------------------------------
# 🟩 CORS JSON TEST — visar headers direkt i Chrome
# ---------------------------------------------------------
@app.route("/cors-json")
def cors_json():
    return jsonify({
        "Access-Control-Allow-Origin": "https://bentus-touren-frontend.onrender.com",
        "Access-Control-Allow-Headers": "Content-Type, Authorization",
        "Access-Control-Allow-Methods": "GET, OPTIONS",
        "Access-Control-Max-Age": "3600"
    })

# ---------------------------------------------------------
# Konfiguration
# ---------------------------------------------------------
FILE_URL = "https://docs.google.com/spreadsheets/d/1oBF2HfyMOp1xjGAcuUrduvgds4ToyuQz/export?format=xlsx"
CACHE_TTL = 300
_cache_workbook = None
_cache_timestamp = 0

# ---------------------------------------------------------
# Hjälpfunktioner
# ---------------------------------------------------------
def load_workbook():
    global _cache_workbook, _cache_timestamp
    now = time.time()

    if _cache_workbook is not None and (now - _cache_timestamp) < CACHE_TTL:
        return _cache_workbook

    try:
        wb = pd.ExcelFile(FILE_URL)
        _cache_workbook = wb
        _cache_timestamp = now
        return wb
    except Exception as e:
        return str(e)

def safe_sheet(wb, name):
    if name not in wb.sheet_names:
        return None, jsonify({"error": f"Fliken '{name}' finns inte."}), 404
    return wb.parse(name, header=None), None, None

def is_event_sheet(df):
    players = df.iloc[3:13, 1]
    return players.notna().sum() >= 5

# ---------------------------------------------------------
# Hälsokontroll
# ---------------------------------------------------------
@app.route("/")
@app.route("/dashboard")
def health_check():
    return jsonify({"status": "ok"}), 200

# ---------------------------------------------------------
# Lista deltävlingar
# ---------------------------------------------------------
@app.route("/events")
def list_events():
    wb = load_workbook()
    if isinstance(wb, str):
        return jsonify({"error": wb}), 500

    events = []
    for sheet in wb.sheet_names:
        name = sheet.lower()

        if name in ["dashboard", "tourställning"]:
            continue
        if name.startswith("deltävling"):
            continue

        df, err, code = safe_sheet(wb, sheet)
        if err:
            continue

        if is_event_sheet(df):
            events.append(sheet)

    return jsonify(events)

# ---------------------------------------------------------
# Huvudtabell
# ---------------------------------------------------------
@app.route("/event/<name>")
def event_main(name):
    wb = load_workbook()
    if isinstance(wb, str):
        return jsonify({"error": wb}), 500

    df, err, code = safe_sheet(wb, name)
    if err:
        return err, code

    try:
        main_table = df.iloc[3:13, 0:9]
        main_table.columns = ["Plac", "Spelare", "HCP", "PB", "NH", "LD", "Bonus", "Tot", "Tourpoäng"]
        main_table = main_table.dropna(subset=["Spelare"])
    except Exception:
        main_table = pd.DataFrame(columns=["Plac", "Spelare", "HCP", "PB", "NH", "LD", "Bonus", "Tot", "Tourpoäng"])

    try:
        team_table = df.iloc[21:27, 16:20]
        team_table.columns = ["Lag", "Resultat", "Plac", "Bonus"]
        team_table = team_table.dropna(subset=["Lag"])
    except Exception:
        team_table = pd.DataFrame(columns=["Lag", "Resultat", "Plac", "Bonus"])

    return jsonify({
        "event": name,
        "main": main_table.to_dict(orient="records"),
        "teams": team_table.to_dict(orient="records")
    })

# ---------------------------------------------------------
# NH
# ---------------------------------------------------------
@app.route("/event/<name>/nh")
def event_nh(name):
    wb = load_workbook()
    if isinstance(wb, str):
        return jsonify({"error": wb}), 500

    df, err, code = safe_sheet(wb, name)
    if err:
        return err, code

    try:
        nh_table = df.iloc[20:26, 0:2]
        nh_table.columns = ["Hål", "Vinnare"]
        nh_table = nh_table.dropna(subset=["Hål"])
    except Exception:
        nh_table = pd.DataFrame(columns=["Hål", "Vinnare"])

    return jsonify({"event": name, "nh": nh_table.to_dict(orient="records")})

# ---------------------------------------------------------
# LD
# ---------------------------------------------------------
@app.route("/event/<name>/ld")
def event_ld(name):
    wb = load_workbook()
    if isinstance(wb, str):
        return jsonify({"error": wb}), 500

    df, err, code = safe_sheet(wb, name)
    if err:
        return err, code

    try:
        ld_table = df.iloc[20:26, 3:5]
        ld_table.columns = ["Hål", "Vinnare"]
        ld_table = ld_table.dropna(subset=["Hål"])
    except Exception:
        ld_table = pd.DataFrame(columns=["Hål", "Vinnare"])

    return jsonify({"event": name, "ld": ld_table.to_dict(orient="records")})

# ---------------------------------------------------------
# Tourställning
# ---------------------------------------------------------
@app.route("/tour")
def tour_summary():
    wb = load_workbook()
    if isinstance(wb, str):
        return jsonify({"error": wb}), 500

    totals = {}

    for sheet in wb.sheet_names:
        name = sheet.lower()
        if name in ["dashboard", "tourställning"]:
            continue
        if name.startswith("deltävling"):
            continue

        df, err, code = safe_sheet(wb, sheet)
        if err:
            continue

        try:
            main_table = df.iloc[3:13, 0:9]
            main_table.columns = ["Plac", "Spelare", "HCP", "PB", "NH", "LD", "Bonus", "Tot", "Tourpoäng"]
        except Exception:
            continue

        for _, row in main_table.iterrows():
            player = str(row["Spelare"]).strip()
            points = row["Tourpoäng"]

            if not isinstance(points, (int, float)):
                continue

            totals[player] = totals.get(player, 0) + points

    sorted_totals = sorted(totals.items(), key=lambda x: x[1], reverse=True)
    result = [{"Spelare": p, "Totalpoäng": round(v, 1)} for p, v in sorted_totals]

    return jsonify(result)

# ---------------------------------------------------------
# Version (fingerprint)
# ---------------------------------------------------------
@app.route("/version")
def version():
    return jsonify({"backend_version": "2026-07-09-23:05"})

# ---------------------------------------------------------
# Startpunkt
# ---------------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
