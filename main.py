from flask import Flask, jsonify
from flask_cors import CORS
from excel_reader import read_sheet

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "Bentus Touren backend är igång!"

@app.route("/resultat")
def resultat():
    return jsonify(read_sheet("Resultat"))

@app.route("/spelare")
def spelare():
    return jsonify(read_sheet("Spelare"))

@app.route("/lagspel")
def lagspel():
    return jsonify(read_sheet("Lagspel"))

@app.route("/tourstallning")
def tourstallning():
    return jsonify(read_sheet("Tourställning"))

@app.route("/deltavlingar")
def deltavlingar():
    return jsonify(read_sheet("Deltävlingar"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
