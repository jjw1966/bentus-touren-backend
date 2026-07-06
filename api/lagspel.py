from flask import Blueprint, jsonify

app = Blueprint("lagspel", __name__)

@app.route("/lagspel")
def lagspel_home():
    # Exempeldata – byt till din riktiga datakälla
    data = [
        {"lag": "Team Bentus", "poang": 42},
        {"lag": "Hallsta Masters", "poang": 37},
        {"lag": "Touren Legends", "poang": 33}
    ]
    return jsonify(data)
