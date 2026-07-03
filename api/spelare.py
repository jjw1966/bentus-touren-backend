from flask import Blueprint, jsonify
from data.drive_connector import download_excel_from_drive
from data.excel_reader import read_excel_data

# Skapa blueprint för spelare
app = Blueprint("spelare", __name__)

@app.route("/spelare")
def spelare():
    """
    Endpoint som returnerar spelarprofiler från Excel-filen.
    """
    try:
        file_path = download_excel_from_drive()
        sheets = read_excel_data(file_path)

        # Plocka ut bladet "spelare" om det finns
        spelare_data = sheets.get("spelare", {})
        return jsonify(spelare_data)

    except Exception as e:
        return jsonify({"error": str(e)})
