from flask import Flask, jsonify
import pandas as pd

app = Flask(__name__)

# Din Google Sheets-fil
FILE_URL = "https://docs.google.com/spreadsheets/d/1Y7NhhTDfZJQAFVtQVniJpLoY6BYahbuf/export?format=xlsx"


# ---------------------------------------------------------
# Hjälpfunktioner
# ---------------------------------------------------------

def load_workbook():
    """Läser Excel-filen från Google Drive."""
    return pd.ExcelFile(FILE_URL)


def is_real_event(name):
    """Returnerar True om fliken är en riktig deltävling."""
    return not name.startswith("Deltävling")


def extract_table(df, columns):
    """Returnerar en tabell med endast de kolumner som finns."""
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
    wb = load
