from flask import Blueprint, jsonify
from excel_reader import read_sheet

app = Blueprint("spelare", __name__)

@app.route("/spelare")
def spelare():
    """
    Hämtar spelarinfo från fliken 'Dashboard' i Bentus_Tour_2026.xlsx.
    Returnerar NH-liga och LD-liga med spelarnamn och poäng.
    """
    df = read_sheet("Dashboard")

    # Om något gick fel i läsningen
    if isinstance(df, dict) and "error" in df:
        return jsonify(df)

    # Plocka ut kolumner som innehåller NH- och LD-liga
    nh_data = df.loc[:, ["NH-liga", "Spelare", "NH"]].dropna().to_dict(orient="records")
    ld_data = df.loc[:, ["LD-liga", "Spelare.1"]].dropna().to_dict(orient="records")

    return jsonify({
        "NH-liga": nh_data,
        "LD-liga": ld_data
    })
