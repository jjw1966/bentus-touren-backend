from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
import pandas as pd
import time
import unicodedata
import re

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": [
    "https://bentus-touren-frontend.onrender.com",
    "https://www.bentus-touren-frontend.onrender.com"
]}}, supports_credentials=True)

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

@app.route("/health")
def health_check():
    print("Health check OK")
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
    name_norm = name.lower()
    for sheet in wb.sheet_names:
        if name_norm in sheet.lower():
            print("Using sheet:", sheet)
            df = wb.parse(sheet, header=None)
            df = df.fillna("")
            return df, None, None

    print("Sheet not found:", name)
    return None, jsonify({"error": f"Fliken '{name}' finns inte."}), 404

def normalize_text(text):
    text = str(text).lower()
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    text = re.sub(r"[^a-z0-9]", "", text)
    return text

def find_row(df, keyword):
    key = normalize_text(keyword)
    for idx, row in df.iterrows():
        row_text = " ".join(str(x) for x in row)
        if key in normalize_text(row_text):
            return idx
    return None

def extract_table(df, header_keywords, columns):
    start = find_row(df, header_keywords)
    if start is None:
        print("Header not found:", header_keywords)
        return []

    # Find column row
    col_row = None
    for r in range(start + 1, len(df)):
        row_text = " ".join(str(x) for x in df.iloc[r])
        if any(word in row_text.lower() for word in ["placering", "spelare", "lag", "datum", "klubb", "poäng"]):
            col_row = r
            break

    if col_row is None:
        print("Column row not found for:", header_keywords)
        return []

    # Find end row
    end_row = len(df)
    for r in range(col_row + 1, len(df)):
        row_text = " ".join(str(x) for x in df.iloc[r])
        if any(normalize_text(h) in normalize_text(row_text) for h in ["topp", "narmast", "langsta", "spelade", "deltavlingsvinster", "landskamper", "deltavlingar"]):
            end_row = r
            break

    rows = []
    for r in range(col_row + 1, end_row):
        row = [x for x in df.iloc[r] if str(x).strip() != ""]
        if len(row) < len(columns):
            continue
        entry = dict(zip(columns, row))
        rows.append({k.lower(): v for k, v in entry.items()})

    return rows

@app.route("/dashboard")
def dashboard():
    print("Dashboard called")

    try:
        wb = load_workbook()
        if isinstance(wb, str):
            print("Workbook load error:", wb)
            return jsonify({"error": wb}), 500
    except Exception as e:
        print("Dashboard load error:", e)
        return jsonify({"error": str(e)}), 500

    df, err, code = safe_sheet(wb, "Dashboard")
    if err:
        print("Sheet error:", err)
        return err, code

    df = df.dropna(how="all")

    topp5 = extract_table(df, "topp", ["Placering", "Spelare", "Tourpoäng"])
    nh = extract_table(df, "narmast", ["Placering", "Spelare", "Nh"])
    ld = extract_table(df, "langsta", ["Placering", "Spelare", "Ld"])
    spelade = extract_table(df, "spelade", ["Placering", "Spelare", "Antal"])
    vinster = extract_table(df, "deltavlingsvinster", ["Placering", "Spelare", "Vinster"])
    landskamper = extract_table(df, "landskamper", ["Placering", "Lag", "Vinster", "Poäng"])
    deltävlingar = extract_table(df, "deltavlingar", ["Datum", "Klubb"])

    print("Dashboard extraction complete")

    return jsonify({
        "topp5": topp5,
        "nh": nh,
        "ld": ld,
        "spelade": spelade,
        "vinster": vinster,
        "landskamper": landskamper,
        "deltavlingar": deltävlingar
    })

@app.route("/version")
def version():
    return jsonify({"backend_version": "2026-07-10-14:30"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
