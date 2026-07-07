from flask import Flask, jsonify
import pandas as pd

app = Flask(__name__)

# ---------------------------------------------------------
# Konfiguration
# ---------------------------------------------------------
FILE_URL = "https://docs.google.com/spreadsheets/d/1Y7NhhTDfZJQAFVtQVniJpLoY6BYahbuf/export?format=xlsx"


# ---------------------------------------------------------
# Hjälpfunktioner
# ---------------------------------------------------------
def load_workbook():
    """Läser Excel-filen från Google Drive."""
    try:
        return pd.ExcelFile(FILE_URL)
    except Exception as e:
        return str(e)


def is_real_event(name):
    """Returnerar True om fliken är en riktig deltävling."""
    return not name.startswith("Deltävling")


def extract_table(df, columns):
    """Returnerar en tabell med endast de kolumner som finns."""
    cols = [c for c in columns if c in df.columns]
    return df[cols].dropna(how="all").to_dict(orient="records")


# ---------------------------------------------------------
# 1. Hälsokontroll
# ---------------------------------------------------------
@app.route("/")
@app.route("/dashboard")
def health_check():
    return jsonify({"status": "ok"}), 200


# ---------------------------------------------------------
# 2. Lista aktiva deltävlingar
# ---------------------------------------------------------
@app.route("/events")
def list_events():
    wb = load_workbook()
    if isinstance(wb, str):
        return jsonify({"error": wb}), 500

    base_events = ["Sura", "Fullerö", "Strand 1", "Strand 2"]
    events = []

    for sheet in wb.sheet_names:
        if sheet in base_events or is_real_event(sheet):
            events.append(sheet)

    return jsonify(events)


# ---------------------------------------------------------
# 3. En deltävling (huvudtabell + NH + LD + lagspel)
# ---------------------------------------------------------
@app.route("/event/<name>")
def event_data(name):
    wb = load_workbook()
    if isinstance(wb, str):
        return jsonify({"error": wb}), 500

    if name not in wb.sheet_names:
        return jsonify({"error": f"Fliken '{name}' finns inte."}), 404

    df = wb.parse(name)
    columns = ["Namn", "Poäng", "Placering", "Lag", "NH", "LD"]
    table = extract_table(df, columns)

    return jsonify({"event": name, "data": table})


# ---------------------------------------------------------
# 4. Startpunkt för Render
# ---------------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
