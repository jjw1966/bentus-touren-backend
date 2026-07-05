from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd
import requests
from io import BytesIO

app = Flask(__name__)
CORS(app)

# Google Drive fil-ID
FILE_ID = "1Y7NhhTDfZJQAFVtQVniJpLoY6BYahbuf"
FILE_URL = f"https://docs.google.com/spreadsheets/d/{FILE_ID}/export?format=xlsx"

def read_sheet(sheet_name):
    """Läser ett blad från Google Drive Excel-filen."""
    try:
        response = requests.get(FILE_URL)
        response.raise_for_status()
        excel_data = BytesIO(response.content)
        df = pd.read_excel(excel_data, sheet_name=sheet_name)
        return df.to_dict(orient="records")
    except Exception as e:
        return {"error": str(e)}

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
    return jsonify(read_sheet("Tourstallning"))

@app.route("/deltavlingar")
def deltavlingar():
    return jsonify(read_sheet("Deltavlingar"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
