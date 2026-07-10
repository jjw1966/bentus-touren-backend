from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
import pandas as pd
import time
import unicodedata
import re

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://bentus-touren-frontend.onrender.com"}}, supports_credentials=True)

@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "https://bentus-touren-frontend.onrender.com"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    response.headers["Access-Control-Allow-Methods"] = "GET, OPTIONS"
    response.headers["Access-Control-Max-Age"] = "3600"
    return response

@app.before_request
def handle_options():
    if request.method == "OPTIONS":
        response = make_response(jsonify({"status": "ok"}), 200)
        response.headers["Access-Control-Allow-Origin"] = "https://bentus-touren-frontend.onrender.com"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        response.headers["Access-Control-Allow-Methods"] = "GET, OPTIONS"
        response.headers["Access-Control-Max-Age"] = "3600"
        return response

# Health check for Render
@app.route("/health")
def health_check():
    return jsonify({"status": "ok"}), 200

FILE_URL = "https://docs.google.com/spreadsheets/d/1oBF2HfyMOp1xjGAcuUrduvgds4ToyuQz/export?format=xlsx"
CACHE_TTL = 300
_cache_workbook = None
_cache_timestamp = 0

def load_workbook():
    global _cache_workbook, _cache_timestamp
    now = time.time()
    if _cache_workbook is not None and (now - _cache_timestamp) < CACHE_TTL:
        print("Using cached workbook")
        return _cache_workbook
    try:
        print("Downloading workbook...")
        wb = pd.ExcelFile(FILE_URL)
        print("Workbook downloaded:", wb.sheet_names)
        _cache_workbook = wb
        _cache_timestamp = now
        return wb
    except Exception as e:
        print("Workbook error:", e)
        return str(e)

def safe_sheet(wb, name):
    for sheet in wb.sheet_names:
        if name.lower() in sheet.lower():
            print("Using sheet:", sheet)
            df = wb.parse(sheet, header=None)
            df = df.fillna(method="ffill", axis=1)
            return df, None, None
    print("Sheet not found:", name)
    return None, jsonify({"error": f"Fliken '{name}' finns inte."}), 404

def lowercase_dict(d):
    return {k.lower(): v for k, v in d.items()}

def normalize_text(text):
    text = str(text).lower()
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    text = re.sub(r"[^a-z0-9]", "", text)
    return text

def fuzzy_match(a, b):
    return normalize_text(a).startswith(normalize_text(b)) or normalize_text(b).startswith(normalize_text(a))

@app.route("/dashboard")
def dashboard():
    try:
        wb = load_workbook()
        if isinstance(wb, str):
            return jsonify({"error": wb}), 500
    except Exception as e:
        print("Dashboard load error:", e)
        return jsonify({"error": str(e)}), 500

    df, err, code = safe_sheet(wb, "Dashboard")
    if err:
        return err, code

    df = df.dropna(how="all")

    headers = [
        "topp",
        "narmast",
        "langsta",
        "spelade",
        "deltavlingsvinster",
        "landskamper",
        "deltavlingar"
    ]

    def extract_table(label, columns):
        print("Extracting:", label)
        label_norm = normalize_text(label)
        label_rows = df.index[
            df.apply(lambda r: any(label_norm in normalize_text(x) for x in r.astype(str)), axis=1)
        ]
        if len(label_rows) == 0:
            print("Label not found:", label)
            return []

        start_row = label_rows[0]
        print("Label row:", start_row)

        col_row = None
        for r in range(start_row + 1, len(df)):
            row_text = " ".join(df.iloc[r, :].astype(str)).lower()
            if any(word in row_text for word in ["placering", "spelare", "lag", "datum", "klubb", "poäng"]):
                col_row = r
                print("Column row:", col_row)
                break

        if col_row is None:
            col_row = start_row

        end_row = len(df)
        for r in range(col_row + 1, len(df)):
            row_text = " ".join(df.iloc[r, :].astype(str))
            if any(fuzzy_match(row_text, h) for h in headers):
                end_row = r
                print("Next header at row:", end_row)
                break

        rows = []
        for r in range(col_row + 1, end_row):
            row = df.iloc[r, :].dropna().tolist()
            print("Row:", r, row)

            if any(fuzzy_match(str(x), h) for h in headers):
                continue

            if len(row) < len(columns):
                print("Skipping short row:", row)
                continue

            entry = dict(zip(columns, row))
            rows.append(lowercase_dict(entry))

        return rows

    topp5 = extract_table("topp", ["Placering", "Spelare", "Tourpoäng"])
    nh = extract_table("narmast", ["Placering", "Spelare", "Nh"])
    ld = extract_table("langsta", ["Placering", "Spelare", "Ld"])
    spelade = extract_table("spelade", ["Placering", "Spelare", "Antal"])
    vinster = extract_table("deltavlingsvinster", ["Placering", "Spelare", "Vinster"])
    landskamper = extract_table("landskamper", ["Placering", "Lag", "Vinster", "Poäng"])
    deltävlingar = extract_table("deltavlingar", ["Datum", "Klubb"])

    return jsonify({
        "topp5": topp5,
        "nh": nh,
        "ld": ld,
        "spelade": spelade,
        "vinster": vinster,
        "landskamper": landskamper,
        "deltävlingar": deltävlingar
    })

@app.route("/version")
def version():
    return jsonify({"backend_version": "2026-07-10-11:30"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
