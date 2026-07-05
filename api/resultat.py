from flask import Blueprint, jsonify
from data.excel_reader import read_sheet

resultat_bp = Blueprint("resultat", __name__, url_prefix="/resultat")

@resultat_bp.route("/")
def get_resultat():
    data = read_sheet("Dashboard")
    return jsonify(data)
