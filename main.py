from flask import Flask, jsonify
import pandas as pd

app = Flask(__name__)

FILE_URL = "https://docs.google.com/spreadsheets/d/1Y7NhhTDfZJQAFVtQVniJpLoY6BYahbuf/export?format=xlsx"

def load_workbook():
    return pd.ExcelFile(FILE_URL)

def is_real_event(name):
    return not name.startswith("Deltävling")

def extract_table(df, columns):
    cols = [c for c in columns if c in df.columns]
    return df[cols].dropna(how="all").to_dict(orient="records")

# ---------------------------------------------------------
# 1. Lista aktiva deltävlingar
# ---------------------------------------------------------
@app.route("/events")
def list_events():
    wb = load_workbook()
    base_events = ["Sura", "Fullerö", "Strand 1", "Strand 2"]

    events = []

    for sheet in wb.sheet_names:
        if sheet in base_events:
            events.append(sheet)
        elif is_real_event(sheet):
            events.append(sheet)

    return jsonify(events)

# ---------------------------------------------------------
# 2. En deltävling (huvudtabell + NH + LD + lagspel)
# ---------------------------------------------------------
@app.route("/event/<name>")
def event_data(name):
    wb = load_workbook()
    df = wb.parse(name)

    main_cols = ["Plac", "Spelare", "HCP", "PB", "NH", "LD", "Bonus", "Tot", "Tourpoäng"]
    nh_cols = ["Plac", "Spelare", "NH"]
    ld_cols = ["Plac", "Spelare", "LD"]

    main_table = extract_table(df, main_cols)
    nh_table = extract_table(df, nh_cols)
    ld_table = extract_table(df, ld_cols)

    lagspel = None
    if "Lagspel på?" in df.columns:
        if str(df["Lagspel på?"].iloc[0]).strip().lower() == "ja":
            lag_cols = ["Lag", "Resultat", "Plac", "Bonus"]
            lagspel = extract_table(df, lag_cols)

    return jsonify({
        "event": name,
        "main": main_table,
        "nh": nh_table,
        "ld": ld_table,
        "lagspel": lagspel
    })

# ---------------------------------------------------------
# 3. Tourställning (endast aktiva deltävlingar)
# ---------------------------------------------------------
@app.route("/tourstallning")
def tourstallning():
    wb = load_workbook()
    df = wb.parse("Tourställning")

    valid_cols = [
        "Plac", "Spelare", "Aktuellt HCP", "Spelade",
        "Sura", "Fullerö", "Strand 1", "Strand 2",
        "Tourpoäng"
    ]
