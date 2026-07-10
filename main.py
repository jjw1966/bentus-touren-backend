from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
import pandas as pd
import time

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

# ---------------------------------------------------------
# Konfiguration
# ---------------------------------------------------------
FILE_URL = "https://docs.google.com/spreadsheets/d/1oBF2HfyMOp1xjGAcuUrduvgds4ToyuQz/export?format=xlsx"
CACHE_TTL = 300
_cache_workbook = None
_cache_timestamp = 0

# ---------------------------------------------------------
# Hjälpfunktioner
# ---------------------------------------------------------
def load_workbook():
    global _cache_workbook, _cache_timestamp
    now = time.time()

    if _cache_workbook is not None and (now - _cache_timestamp) < CACHE_TTL:
        return _cache_workbook

    try:
        wb = pd.ExcelFile(FILE_URL)
        _cache_workbook = wb
        _cache_timestamp = now
        print("Excel nedladdad OK")
        return wb
    except Exception as e:
        print("Excel FEL:", e)
        return str(e)

def safe_sheet(wb, name):
    for sheet in wb.sheet_names:
        if sheet.lower().startswith(name.lower()):
            print(f"Flik hittad: {sheet}")
            return wb.parse(sheet, header=None), None, None

    print(f"Flik saknas: {name}")
    return None, jsonify({"error": f"Fliken '{name}' finns inte."}), 404

def lowercase_dict(d):
    return {k.lower(): v for k, v in d.items()}

def to_number(value):
    try:
        if pd.isna(value):
            return None
        if isinstance(value, (int, float)):
            return value
        value = str(value).strip().replace(",", ".")
        return float(value)
    except Exception:
        return None

# ---------------------------------------------------------
# Hälsokontroll
# ---------------------------------------------------------
@app.route("/")
def health():
    return jsonify({"status": "ok"}), 200

# ---------------------------------------------------------
# Dashboard-läsare
# ---------------------------------------------------------
@app.route("/dashboard")
def dashboard():
    wb = load_workbook()
    if isinstance(wb, str):
        return jsonify({"error": wb}), 500

    df, err, code = safe_sheet(wb, "Dashboard")
    if err:
        return err, code

    df = df.dropna(how="all")

    headers = [
        "Topp",
        "Närmast",
        "Längsta",
        "Spelade",
        "Deltävlingsvinster",
        "Landskamper",
        "Deltävlingar"
    ]

    def extract_table(label, columns):
        print(f"\nSöker tabell: {label}")

        label_rows = df.index[
            df.apply(lambda r: r.astype(str).str.contains(label, case=False).any(), axis=1)
        ]

        if len(label_rows) == 0:
            print(f"Tabell '{label}' hittades inte.")
            return []

        start_row = label_rows[0]
        col_row = start_row + 1

        next_rows = df.index[
            df.apply(lambda r: r.astype(str).str.contains("|".join(headers), case=False).any(), axis=1)
        ]
        next_rows = [r for r in next_rows if r > start_row]

        end_row = next_rows[0] if next_rows else len(df)

        rows = []

        for r in range(col_row + 1, end_row):
            row = df.iloc[r, :].dropna().tolist()
            if len(row) < len(columns):
                continue
            entry = dict(zip(columns, row))
            rows.append(lowercase_dict(entry))

        print(f"Tabell '{label}' rader hittade:", len(rows))
        return rows

    topp5 = extract_table("Topp", ["Placering", "Spelare", "Tourpoäng"])
    nh = extract_table("Närmast", ["Placering", "Spelare", "Nh"])
    ld = extract_table("Längsta", ["Placering", "Spelare", "Ld"])
    spelade = extract_table("Spelade", ["Placering", "Spelare", "Antal"])
    vinster = extract_table("Deltävlingsvinster", ["Placering", "Spelare", "Vinster"])
    landskamper = extract_table("Landskamper", ["Placering", "Lag", "Vinster", "Poäng"])
    deltävlingar = extract_table("Deltävlingar", ["Datum", "Klubb"])

    return jsonify({
        "topp5": topp5,
        "nh": nh,
        "ld": ld,
        "spelade": spelade,
        "vinster": vinster,
        "landskamper": landskamper,
        "deltävlingar": deltävlingar
    })

# ---------------------------------------------------------
# Tourställning
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
            df, err, code = safe_sheet(wb, sheet)
            if err:
                continue

            try:
                start_row = 3
                end_row = len(df)

                main_table = df.iloc[start_row:end_row, 0:9]
                main_table.columns = [
                    "Plac", "Spelare", "HCP", "PB", "NH",
                    "LD", "Bonus", "Tot", "Tourpoäng"
                ]
                main_table = main_table.fillna("")
            except Exception:
                continue

            for _, row in main_table.iterrows():
                player = str(row["Spelare"]).strip()
                points = to_number(row["Tourpoäng"])

                if points is None:
                    continue

                totals[player] = totals.get(player, 0) + points

    sorted_totals = sorted(totals.items(), key=lambda x: x[1], reverse=True)

    result = [
        lowercase_dict({"Spelare": p, "Totalpoäng": round(v, 1)})
        for p, v in sorted_totals
    ]

    return jsonify(result)

# ---------------------------------------------------------
# Version
# ---------------------------------------------------------
@app.route("/version")
def version():
    return jsonify({"backend_version": "2026-07-10-02:25"})

# ---------------------------------------------------------
# Startpunkt
# ---------------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
