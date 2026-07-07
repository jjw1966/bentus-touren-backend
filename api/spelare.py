from flask import Blueprint, jsonify
from excel_reader import read_sheet

app = Blueprint("spelare", __name__)

@app.route("/spelare")
def spelare():
    """
    Hämtar data från fliken 'Dashboard' i Bentus_Tour_2026.xlsx.
    Tolkar sektionerna 'Närmast hål' och 'Längsta drive' baserat på radpositioner.
    """
    df = read_sheet("Dashboard")

    if isinstance(df, dict) and "error" in df:
        return jsonify(df)

    # Rensa kolumnnamn
    df.columns = df.columns.astype(str).str.strip()

    # 🟦 Närmast hål (rad 12–17)
    nh_section = df.iloc[11:17, 0:3]  # kolumner A–C
    nh_section.columns = ["Placering", "Spelare", "NH"]
    nh_data = nh_section.dropna().to_dict(orient="records")

    # 🟩 Längsta drive (rad 12–16 men kolumner E–G)
    ld_section = df.iloc[11:16, 4:7]  # kolumner E–G
    ld_section.columns = ["Placering", "Spelare", "LD"]
    ld_data = ld_section.dropna().to_dict(orient="records")

    return jsonify({
        "NH-liga": nh_data,
        "LD-liga": ld_data
    })
