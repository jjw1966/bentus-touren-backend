from flask import Blueprint, jsonify
from data.excel_reader import read_sheet

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")

@dashboard_bp.route("/")
def get_dashboard():
    data = read_sheet("Resultat")
    return jsonify(data)
