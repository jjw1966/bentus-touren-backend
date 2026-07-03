from flask import Blueprint, jsonify
from data.drive_connector import download_excel_from_drive
from data.excel_reader import read_excel_data

# Skapa blueprint för lagspel
app = Blueprint("lagspel", __name__)

@app.route("/lagspel")
def lagspel():
    """
    Endpoint som returnerar lagspelsdata från Excel-filen.
    """
    try:
        file_path = download_excel_from_drive()
        sheets = read_excel_data(file_path)

        # Plocka ut bladet "lagspel" om det finns
        lagspel_data = sheets.get("lagspel", {})
        return jsonify(lagspel_data)

    except Exception as e:
        return jsonify({"error": str(e)})
