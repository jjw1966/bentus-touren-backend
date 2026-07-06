from flask import Blueprint, jsonify
from excel_reader import read_sheet

app = Blueprint("deltavlingar", __name__)

@app.route("/deltavlingar")
def deltavlingar():
    data = read_sheet("Deltävlingar")
    return jsonify(data)
