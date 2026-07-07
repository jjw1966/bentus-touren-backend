from flask import Blueprint, jsonify
from excel_reader import read_sheet

app = Blueprint("dashboard", __name__)

@app.route("/dashboard")
def dashboard():
    """
    Hämtar alla sektioner från fliken 'Dashboard' i Bentus_Tour_2026.xlsx.
    Tolkar Topp 5, Spelade rundor, Närmast hål, Längsta drive och Deltävlingsvinster.
    """
    df = read_sheet("Dashboard")

    if isinstance(df, dict) and "error" in df:
        return jsonify(df)

    df.columns = df.columns.astype(str).str.strip()

    # 🟦 Topp 5 (rad 4–9, kolumner A–C)
    topp5 = df.iloc[3:9, 0:3]
    topp5.columns = ["Placering", "Spelare", "Tourpoäng"]
    topp5_data = topp5.dropna().to_dict(orient="records")

    # 🟩 Spelade rundor (rad 4–9, kolumner E–G)
    rundor = df.iloc[3:9, 4:7]
    rundor.columns = ["Placering", "Spelare", "Antal"]
    rundor_data = rundor.dropna().to_dict(orient="records")

    # 🟦 Närmast hål (rad 12–17, kolumner A–C)
    nh = df.iloc[11:17, 0:3]
    nh.columns = ["Placering", "Spelare", "NH"]
    nh_data = nh.dropna().to_dict(orient="records")

    # 🟩 Längsta drive (rad 12–16, kolumner E–G)
    ld = df.iloc[11:16, 4:7]
    ld.columns = ["Placering", "Spelare", "LD"]
    ld_data = ld.dropna().to_dict(orient="records")

    # 🟦 Deltävlingsvinster (rad 20–24, kolumner A–C)
    vinster = df.iloc[19:24, 0:3]
    vinster.columns = ["Placering", "Spelare", "Vinster"]
    vinster_data = vinster.dropna().to_dict(orient="records")

    return jsonify({
        "Topp5": topp5_data,
        "Spelade_rundor": rundor_data,
        "NH-liga": nh_data,
        "LD-liga": ld_data,
        "Deltävlingsvinster": vinster_data
    })
