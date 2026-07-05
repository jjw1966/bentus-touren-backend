from flask import Blueprint, jsonify
from data.excel_reader import read_sheet

lagspel_bp = Blueprint("lagspel", __name__, url_prefix="/lagspel")

@lagspel_bp.route("/")
def get_lagspel():
    data = read_sheet("Lagspel")
    return jsonify(data)
