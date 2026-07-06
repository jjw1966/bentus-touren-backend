from flask import Blueprint, jsonify
from data.excel_reader import read_sheet

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/resultat")

@dashboard_bp.route("/")
def get_dashboard():
    data = read_sheet("Dashboard")
    return jsonify(data)
from flask import Blueprint

app = Blueprint("dashboard", __name__)

@app.route("/dashboard")
def dashboard_home():
    return {"status": "Dashboard live"}
