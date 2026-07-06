from flask import Blueprint, jsonify
from excel_reader import read_sheet

app = Blueprint("lagspel", __name__)

@app.route("/lagspel")
def lagspel():
    df = read_sheet("Lagspel")

    if isinstance(df, dict) and "error" in df:
        return jsonify(df)

    df.columns = df.columns.astype(str).str.strip()

    try:
        data = df.dropna().to_dict(orient="records")
        return jsonify({"Lagspel": data})
    except Exception as e:
        return jsonify({"error": str(e), "columns": df.columns.tolist()})
