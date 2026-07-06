from flask import Blueprint, jsonify
from excel_reader import read_sheet

app = Blueprint("spelare", __name__)

@app.route("/spelare")
def spelare():
    """
    Hämtar spelarprofiler från fliken 'Spelare' i Bentus_Tour_2026.xlsx.
    """
    data = read_sheet("Spelare")
    return jsonify(data)
