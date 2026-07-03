from flask import Blueprint, jsonify
from data.drive_connector import download_excel_from_drive
from data.excel_reader import read_excel_data

# Skapa blueprint för deltävlingar
app = Blueprint("deltavlingar", __name__)

@app.route("/deltavlingar")
def deltavlingar():
    """
    Endpoint som returnerar data för alla deltävlingar från Excel-filen.
    """
    try:
        file_path = download_excel_from_drive()
        sheets = read_excel_data(file_path)

        # Plocka ut alla blad som börjar med "Deltävling"
        deltavlingar_data = {
            namn: data
            for namn, data in sheets.items()
            if namn.lower().startswith("deltävling")
        }

        return jsonify(deltavlingar_data)

    except Exception as e:
        return jsonify({"error": str(e)})
