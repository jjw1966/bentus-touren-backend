from flask import Flask, jsonify
import pandas as pd
import time

app = Flask(__name__)

# ---------------------------------------------------------
# Konfiguration
# ---------------------------------------------------------
FILE_URL = "https://docs.google.com/spreadsheets/d/1oBF2HfyMOp1xjGAcuUrduvgds4ToyuQz/export?format=xlsx"
CACHE_TTL = 300  # 5 minuter cache
_cache_workbook = None
_cache_timestamp = 0


# ---------------------------------------------------------
# Hjälpfunktioner
# ---------------------------------------------------------
def load_workbook():
    """Laddar Excel-filen från Google Sheets med caching."""
    global _cache_workbook, _cache_timestamp
    now = time.time()

    if _cache_workbook is not None and (now - _cache_timestamp) < CACHE_TTL:
        return _cache_workbook

    try:
        wb = pd.ExcelFile(FILE_URL)
        _cache_workbook = wb
        _cache_timestamp = now
        return wb
    except Exception as e:
        return str(e)


def safe_sheet(wb, name):
    """Returnerar DataFrame eller felmeddelande."""
    if name not in wb.sheet_names:
        return None, jsonify({"error": f"Fliken '{name}' finns inte."}), 404
    return wb.parse(name, header=None), None, None


def is_event_sheet(df):
    """
    Identifierar deltävlingar baserat på cellvärden.
    Spelarnamnen ligger i kolumn B (index 1), rader 3–12.
    """
    players = df.iloc[2:12, 1]  # kolumn B
    return players.notna().sum() >= 5


# ---------------------------------------------------------
# Hälsokontroll
# ---------------------------------------------------------
@app.route("/")
@app.route("/dashboard")
def health_check():
    return jsonify({"status": "ok"}), 200


# ---------------------------------------------------------
# Lista riktiga deltävlingar
# ---------------------------------------------------------
@app.route("/events")
def list_events():
    wb = load_workbook()
    if isinstance(wb, str):
        return jsonify({"error": wb}), 500

    events = []
    for sheet in wb.sheet_names:
        name = sheet.lower()

        # Ignorera icke-deltävlingar
        if name in ["dashboard", "tourställning"]:
            continue
        if name.startswith("deltävling"):
            continue

        df, err, code = safe_sheet(wb, sheet)
        if err:
            continue

        if is_event_sheet(df):
            events.append(sheet)

    return jsonify(events)


# ---------------------------------------------------------
# Huvudtabell för en deltävling
# ---------------------------------------------------------
@app.route("/event/<name>")
def event_main(name):
    wb = load_workbook()
    if isinstance(wb, str):
        return jsonify({"error": wb}), 500

    df, err, code = safe_sheet(wb, name)
    if err:
        return err, code

    # Huvudtabell: rader 3–12, kolumner A–I
    main_table = df.iloc[2:12, 0:9]
    main_table.columns = ["Plac", "Spelare", "HCP", "PB", "NH", "LD", "Bonus", "Tot", "Tourpoäng"]

    # Lagresultat: rader 22–27, kolumner Q–T
    team_table = df.iloc[21:27, 16:20]
    team_table.columns = ["Lag", "Resultat", "Plac", "Bonus"]

    return jsonify({
        "event": name,
        "main": main_table.to_dict(orient="records"),
        "teams": team_table.to_dict(orient="records")
    })


# ---------------------------------------------------------
# Närmast hål (NH)
# ---------------------------------------------------------
@app.route("/event/<name>/nh")
def event_nh(name):
    wb = load_workbook()
    if isinstance(wb, str):
        return jsonify({"error": wb}), 500

    df, err, code = safe_sheet(wb, name)
    if err:
        return err, code

    nh_table = df.iloc[20:26, 0:2]  # kolumner A–B
    nh_table.columns = ["Hål", "Vinnare"]

    return jsonify({"event": name, "nh": nh_table.to_dict(orient="records")})


# ---------------------------------------------------------
# Längsta drive (LD)
# ---------------------------------------------------------
@app.route("/event/<name>/ld")
def event_ld(name):
    wb = load_workbook()
    if isinstance(wb, str):
        return jsonify({"error": wb}), 500

    df, err, code = safe_sheet(wb, name)
    if err:
        return err, code

    ld_table = df.iloc[20:26, 3:5]  # kolumner D–E
    ld_table.columns = ["Hål", "Vinnare"]

    return jsonify({"event": name, "ld": ld_table.to_dict(orient="records")})


# ---------------------------------------------------------
# Tourställning – summera Tourpoäng per spelare
# ---------------------------------------------------------
@app.route("/tour")
def tour_summary():
    wb = load_workbook()
    if isinstance(wb, str):
        return jsonify({"error": wb}), 500

    totals = {}

    for sheet in wb.sheet_names:
        name = sheet.lower()
        if name in ["dashboard", "tourställning"]:
            continue
        if name.startswith("deltävling"):
            continue

        df, err, code = safe_sheet(wb, sheet)
        if err:
            continue

        # Huvudtabell: rader 3–12, kolumner A–I
        main_table = df.iloc[2:12, 0:9]
        main_table.columns = ["Plac", "Spelare", "HCP", "PB", "NH", "LD", "Bonus", "Tot", "Tourpoäng"]

        for _, row in main_table.iterrows():
            player = str(row["Spelare"]).strip()
            points = row["Tourpoäng"]
            if pd.notna(player) and pd.notna(points):
                totals[player] = totals.get(player, 0) + points

    # Sortera efter totalpoäng
    sorted_totals = sorted(totals.items(), key=lambda x: x[1], reverse=True)
    result = [{"Spelare": p, "Totalpoäng": round(v, 1)} for p, v in sorted_totals]

    return jsonify(result)


# ---------------------------------------------------------
# Debug: visa vad som hittas i varje flik
# ---------------------------------------------------------
@app.route("/debug/events")
def debug_events():
    wb = load_workbook()
    if isinstance(wb, str):
        return jsonify({"error": wb}), 500

    result = {}
    for sheet in wb.sheet_names:
        df, _, _ = safe_sheet(wb, sheet)
        players = df.iloc[2:12, 1].dropna().tolist()
        result[sheet] = players

    return jsonify(result)


# ---------------------------------------------------------
# Startpunkt för Docker / Render
# ---------------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
