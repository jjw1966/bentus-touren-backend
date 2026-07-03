from flask import Flask, jsonify
from flask_cors import CORS

# Importera alla API‑blueprints
from api.dashboard import app as dashboard_app
from api.spelare import app as spelare_app
from api.lagspel import app as lagspel_app
from api.tourstallning import app as tourstallning_app
from api.deltavlingar import app as deltavlingar_app

# Importera datalager
from data.drive_connector import download_excel_from_drive
from data.excel_reader import read_excel_data

# ---------------------------------------------------------
# Skapa Flask‑app + aktivera CORS
# ---------------------------------------------------------
app = Flask(__name__)
CORS(app, origins=["https://jjw1966.github.io"])

# ---------------------------------------------------------
# Registrera alla blueprints
# ---------------------------------------------------------
app.register_blueprint(dashboard_app)
app.register_blueprint(spelare_app)
app.register_blueprint(lagspel_app)
app.register_blueprint(tourstallning_app)
app.register_blueprint(deltavlingar_app)

# ---------------------------------------------------------
# Root‑route
# ---------------------------------------------------------
@app.route("/")
def home():
    print("🔍 DEBUG: Root route anropad")
    return jsonify({"message": "API is running"})


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
    app.run(host="0.0.0.0", port=10000)            "excel_file": file_path,
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
    print(f"➡️ Route: {request.path} | Method: {request.method} | IP: {request.remote_addr}")

# ---------------------------------------------------------
# Starta Flask‑servern
# ---------------------------------------------------------
if __name__ == "__main__":
    print("🚀 Server running on port 10000...")
    app.run(host="0.0.0.0", port=10000)
