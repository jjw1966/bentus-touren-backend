from flask import Flask, jsonify
import pandas as pd
import time

app = Flask(__name__)

# ---------------------------------------------------------
# Konfiguration
# ---------------------------------------------------------
FILE_URL = "https://docs.google.com/spreadsheets/d/1Y7NhhTDfZJQAFVtQVniJpLoY6BYahbuf/export?format=xlsx"

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
    """Identifierar deltävlingar baserat på cellvärden, inte kolumnnamn."""
    # Om kolumn B (spelare) har minst 5 namn mellan rad 3–12
    players = df.iloc[2:12, 1]
    if players.notna().sum() >= 5:
        return True
    return False


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

    nh_table = df.iloc[20:26, 0:2]
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

    ld_table = df.iloc[20:26, 3:5]
    ld_table.columns = ["Hål", "Vinnare"]

    return jsonify({"event": name, "ld": ld_table.to_dict(orient="records")})


# ---------------------------------------------------------
# Startpunkt för Docker / Render
# ---------------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
