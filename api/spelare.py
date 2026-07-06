from flask import Blueprint, jsonify

app = Blueprint("spelare", __name__)

@app.route("/spelare")
def spelare_home():
    # Exempeldata – byt till din riktiga datakälla
    data = [
        {"namn": "Joachim", "hcp": 12.3},
        {"namn": "Anders", "hcp": 9.8},
        {"namn": "Maria", "hcp": 15.1}
    ]
    return jsonify(data)
