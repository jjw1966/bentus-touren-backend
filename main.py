from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "Bentus Touren backend är igång!"

@app.route("/resultat")
def resultat():
    # Exempeldata – byt ut mot riktig logik senare
    data = [
        {"Spelare": "Joachim", "Poäng": 42},
        {"Spelare": "Anders", "Poäng": 38},
        {"Spelare": "Mikael", "Poäng": 35},
        {"Spelare": "Jonas", "Poäng": 33}
    ]
    return jsonify(data)

@app.route("/spelare")
def spelare():
    data = [
        {"Namn": "Joachim", "Klubb": "Bentus", "Handicap": 12.4},
        {"Namn": "Anders", "Klubb": "Bentus", "Handicap": 10.8},
        {"Namn": "Mikael", "Klubb": "Bentus", "Handicap": 11.2}
    ]
    return jsonify(data)

@app.route("/lagspel")
def lagspel():
    data = [
        {"Lag": "Team A", "Poäng": 85},
        {"Lag": "Team B", "Poäng": 78},
        {"Lag": "Team C", "Poäng": 74}
    ]
    return jsonify(data)

@app.route("/tourstallning")
def tourstallning():
    data = [
        {"Placering": 1, "Spelare": "Joachim", "Poäng": 42},
        {"Placering": 2, "Spelare": "Anders", "Poäng": 38},
        {"Placering": 3, "Spelare": "Mikael", "Poäng": 35}
    ]
    return jsonify(data)

@app.route("/deltavlingar")
def deltavlingar():
    data = [
        {"Tävling": "Bentus Open", "Datum": "2026-06-15", "Vinnare": "Joachim"},
        {"Tävling": "Sommarcupen", "Datum": "2026-07-01", "Vinnare": "Anders"}
    ]
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

# ---------------------------------------------------------
# Debug‑route — visar vilka blad som hittas i Excel‑filen
# ---------------------------------------------------------
@app.route("/debug")
def debug():
    try:
        file_path = download_excel_from_drive()
        sheets = read_excel_data(file_path)
        print("🔍 DEBUG: Excel-blad funna:", list(sheets.keys()))
        return jsonify({
            "excel_file": file_path,
            "sheets_found": list(sheets.keys())
        })
    except Exception as e:
        print("❌ DEBUG ERROR:", e)
        return jsonify({"error": str(e)})


# ---------------------------------------------------------
# Health‑route — enkel status
# ---------------------------------------------------------
@app.route("/health")
def health():
    try:
        file_path = download_excel_from_drive()
        sheets = read_excel_data(file_path)
        sheet_names = list(sheets.keys())
        print("❤️ HEALTHCHECK: Excel-blad:", sheet_names)
        return jsonify({
            "status": "ok",
            "excel_file": file_path,
            "sheets_found": sheet_names,
            "sheet_count": len(sheet_names)
        })
    except Exception as e:
        print("💔 HEALTHCHECK ERROR:", e)
        return jsonify({
            "status": "error",
            "message": str(e)
        })


# ---------------------------------------------------------
# Full Health‑route — testar ALLA endpoints
# ---------------------------------------------------------
@app.route("/health/full")
def full_health():
    try:
        file_path = download_excel_from_drive()
        sheets = read_excel_data(file_path)
        sheet_names = list(sheets.keys())
        print("🧪 FULL HEALTHCHECK: Excel-blad:", sheet_names)

        results = {
            "dashboard": sheets.get("dashboard"),
            "spelare": sheets.get("spelare"),
            "lagspel": sheets.get("lagspel"),
            "tourstallning": sheets.get("tourstallning"),
            "deltavlingar": {
                namn: data for namn, data in sheets.items()
                if namn.lower().startswith("deltävling")
            }
        }

        return jsonify({
            "status": "ok",
            "excel_file": file_path,
            "sheets_found": sheet_names,
            "sheet_count": len(sheet_names),
            "endpoint_results": results
        })
    except Exception as e:
        print("💔 FULL HEALTHCHECK ERROR:", e)
        return jsonify({
            "status": "error",
            "message": str(e)
        })


# ---------------------------------------------------------
# Loggning av inkommande anrop 
# ---------------------------------------------------------
@app.before_request
def log_request_info():
    from flask import request
    origin = request.headers.get("Origin", "okänd")
    print(f"➡️ Route: {request.path} | Method: {request.method} | IP: {request.remote_addr} | Origin: {origin}")


# ---------------------------------------------------------
# Starta Flask‑servern
# ---------------------------------------------------------
if __name__ == "__main__":
    print("🚀 Server running on port 10000...")
    app.run(host="0.0.0.0", port=10000)
