from flask import Blueprint, jsonify
from data.excel_reader import read_sheet

deltavlingar_bp = Blueprint("deltavlingar", __name__, url_prefix="/deltavlingar")

@deltavlingar_bp.route("/")
def get_deltavlingar():
    sheets = [f"Deltävling {i}" for i in range(1, 9)]
    output = {s: read_sheet(s) for s in sheets}
    return jsonify(output)
