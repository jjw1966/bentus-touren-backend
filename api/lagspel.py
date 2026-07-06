from flask import Blueprint, jsonify
from excel_reader import read_sheet

app = Blueprint("lagspel", __name__)

@app.route("/lagspel")
def lagspel():
    data = read_sheet("Lagspel")
    return jsonify(data)
