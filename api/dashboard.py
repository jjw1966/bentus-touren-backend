from flask import Blueprint, jsonify
from data.drive_connector import download_excel_from_drive
from data.excel_reader import read_excel_data

# Skapa blueprint för dashboard
app = Blueprint("dashboard", __name__)

@app.route("/dashboard")
def dashboard():
    """
    Endpoint som hämtar och returnerar dashboard-data från Excel-filen.
    """
    try:
        file_path = download_excel_from_drive()
        sheets = read_excel_data(file_path)

        # Returnera bara dashboard-bladet om det finns
        dashboard_data = sheets.get("dashboard", {})
        return jsonify(dashboard_data)

    except Exception as e:
        return jsonify({"error": str(e)})
