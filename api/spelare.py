from flask import Blueprint, jsonify
from data.excel_reader import read_sheet

spelare_bp = Blueprint("spelare", __name__, url_prefix="/spelare")

@spelare_bp.route("/")
def get_spelare():
    data = read_sheet("Spelare")
    return jsonify(data)
