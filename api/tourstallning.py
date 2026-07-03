from flask import Blueprint, jsonify
from data.drive_connector import download_excel_from_drive
from data.excel_reader import read_excel_data

# Skapa blueprint för tourställning
app = Blueprint("tourstallning", __name__)

@app.route("/tourstallning")
def tourstallning():
    """
    Endpoint som returnerar tourställningsdata från Excel-filen.
    """
    try:
        file_path = download_excel_from_drive()
        sheets = read_excel_data(file_path)

        # Plocka ut bladet "tourstallning" om det finns
        tourstallning_data = sheets.get("tourstallning", {})
        return jsonify(tourstallning_data)

    except Exception as e:
        return jsonify({"error": str(e)})
