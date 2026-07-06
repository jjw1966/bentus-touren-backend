from flask import Blueprint, jsonify
from excel_reader import read_sheet

app = Blueprint("resultat", __name__)

@app.route("/resultat")
def resultat():
    data = read_sheet("Resultat")
    return jsonify(data)
