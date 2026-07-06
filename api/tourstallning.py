from flask import Blueprint, jsonify
from excel_reader import read_sheet

app = Blueprint("tourstallning", __name__)

@app.route("/tourstallning")
def tourstallning():
    df = read_sheet("Tourställning")

    if isinstance(df, dict) and "error" in df:
        return jsonify(df)

    df.columns = df.columns.astype(str).str.strip()

    try:
        data = df.dropna().to_dict(orient="records")
        return jsonify({"Tourställning": data})
    except Exception as e:
        return jsonify({"error": str(e), "columns": df.columns.tolist()})
