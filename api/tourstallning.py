from flask import Blueprint, jsonify
from excel_reader import read_sheet

app = Blueprint("tourstallning", __name__)

@app.route("/tourstallning")
def tourstallning():
    data = read_sheet("Tourställning")
    return jsonify(data)
