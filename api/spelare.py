from flask import Blueprint, jsonify
from excel_reader import read_sheet

# Skapa blueprint för spelare
app = Blueprint("spelare", __name__)

@app.route("/spelare")
def spelare():
    """
    Endpoint som returnerar spelarprofiler från Excel-filen.
    """
    data = read_sheet("Spelare")
    return jsonify(data)
