from flask import Blueprint, jsonify
from data.excel_reader import read_sheet

lagspel_bp = Blueprint("lagspel", __name__, url_prefix="/lagspel")

@lagspel_bp.route("/")
def get_lagspel():
    sheets = ["Sura", "Fullerö", "Strand 1", "Strand 2"]
    output = {s: read_sheet(s) for s in sheets}
    return jsonify(output)
