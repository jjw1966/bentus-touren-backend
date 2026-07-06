from flask import Blueprint, jsonify
from excel_reader import read_sheet

app = Blueprint("spelare", __name__)

@app.route("/spelare")
def spelare():
    """
    Hämtar spelarinfo från fliken 'Dashboard' i Bentus_Tour_2026.xlsx.
    Returnerar NH-liga och LD-liga med spelarnamn och poäng.
    Hanterar saknade kolumner och mellanslag automatiskt.
    """
    df = read_sheet("Dashboard")

    # Om något gick fel i läsningen
    if isinstance(df, dict) and "error" in df:
        return jsonify(df)

    # Rensa kolumnnamn från mellanslag och dolda tecken
    df.columns = df.columns.astype(str).str.strip()

    # Kontrollera vilka kolumner som faktiskt finns
    columns = df.columns.tolist()

    # Förbered svar
    result = {}

    # NH-liga
    nh_cols = [c for c in columns if "NH" in c or "Spelare" in c]
    if len(nh_cols) >= 3:
        try:
            nh_data = df.loc[:, nh_cols[:3]].dropna().to_dict(orient="records")
            result["NH-liga"] = nh_data
        except Exception as e:
            result["NH-liga_error"] = str(e)
    else:
        result["NH-liga_error"] = f"Kolumner saknas: {nh_cols}"

    # LD-liga
    ld_cols = [c for c in columns if "LD" in c or "Spelare.1" in c]
    if len(ld_cols) >= 2:
        try:
            ld_data = df.loc[:, ld_cols[:2]].dropna().to_dict(orient="records")
            result["LD-liga"] = ld_data
        except Exception as e:
            result["LD-liga_error"] = str(e)
    else:
        result["LD-liga_error"] = f"Kolumner saknas: {ld_cols}"

    # Returnera resultatet
    return jsonify(result)
