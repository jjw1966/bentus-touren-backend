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


def extract_table(df, columns):
    """Returnerar en tabell med endast de kolumner som finns."""
    cols = [c for c in columns if c in df.columns]
    return df[cols].dropna(how="all").to_dict(orient="records")


def safe_sheet(wb, name):
    """Returnerar DataFrame eller felmeddelande."""
    if name not in wb.sheet_names:
        return None, jsonify({"error": f"Fliken '{name}' finns inte."}), 404
    return wb.parse(name), None, None


def is_event_sheet(df):
    """
    Returnerar True om fliken har deltävlingens struktur.
    Vi letar efter typiska kolumner som finns i dina deltävlingar.
    """
    expected_cols = {
        "Namn", "Poäng", "Placering", "HCP", "PB",
        "NH", "LD", "Bonus", "Tot", "Tourpoäng"
    }
    return len(expected_cols.intersection(df.columns)) > 0


# ---------------------------------------------------------
# Hälsokontroll (Render kräver detta)
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

        # Dashboard och Tourställning ska inte visas som deltävlingar
        if name in ["dashboard", "tourställning"]:
            continue

        # Flikar som heter "Deltävling X" ska inte visas
        if name.startswith("deltävling"):
            continue

        # Kolla om fliken har deltävlingens struktur
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

    columns = ["Namn", "Poäng", "Placering", "Lag", "HCP", "PB", "NH", "LD", "Bonus", "Tot", "Tourpoäng"]
    table = extract_table(df, columns)

    return jsonify({"event": name, "main": table})


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

    columns = ["Namn", "NH"]
    table = extract_table(df, columns)

    return jsonify({"event": name, "nh": table})


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

    columns = ["Namn", "LD"]
    table = extract_table(df, columns)

    return jsonify({"event": name, "ld": table})


# ---------------------------------------------------------
# Lagspel
# ---------------------------------------------------------
@app.route("/event/<name>/teams")
def event_teams(name):
    wb = load_workbook()
    if isinstance(wb, str):
        return jsonify({"error": wb}), 500

    df, err, code = safe_sheet(wb, name)
    if err:
        return err, code

    columns = ["Lag", "Namn", "Poäng"]
    table = extract_table(df, columns)

    return jsonify({"event": name, "teams": table})


# ---------------------------------------------------------
# Startpunkt för Docker / Render
# ---------------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
