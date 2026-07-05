from flask import Blueprint, jsonify
from data.excel_reader import read_sheet

tourstallning_bp = Blueprint("tourstallning", __name__, url_prefix="/tourstallning")

@tourstallning_bp.route("/")
def get_tourstallning():
    data = read_sheet("Tourställning")  # OBS: ä
    return jsonify(data)
