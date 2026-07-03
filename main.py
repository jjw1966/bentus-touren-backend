from flask import Flask, jsonify

# Importera alla API‑blueprints
from api.dashboard import app as dashboard_app
from api.spelare import app as spelare_app
from api.lagspel import app as lagspel_app
from api.tourstallning import app as tourstallning_app
from api.deltavlingar import app as deltavlingar_app

# Importera datalager
from data.drive_connector import download_excel_from_drive
from data.excel_reader import read_excel_data

app = Flask(__name__)

# Registrera alla blueprints
app.register_blueprint(dashboard_app)
app.register_blueprint(spelare_app)
app.register_blueprint(lagspel_app)
app.register_blueprint(tourstallning_app)
app.register_blueprint(deltavlingar_app)

# ---------------------------------------------------------
# Root‑route (så du slipper 404 i Render)
# ---------------------------------------------------------
@app.route("/")
def home():
    return jsonify({"message": "API is running"})


# ---------------------------------------------------------
# Debug‑route (visar vilka blad som hittas i Excel‑filen)
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
# Starta Flask‑servern
# ---------------------------------------------------------
if __name__ == "__main__":
    print("🚀 Server running on port 10000...")
    app.run(host="0.0.0.0", port=10000)
