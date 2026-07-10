from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from openpyxl import load_workbook
from datetime import datetime

app = FastAPI()

# Tillåt frontend på Render
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🟩 Dynamisk tabell-läsare (fungerar för alla flikar)
def read_table(sheet, header_text):
    header_row = None

    # Hitta rubrikraden
    for i, row in enumerate(sheet.iter_rows(values_only=True)):
        if row and isinstance(row[0], str) and row[0].strip().startswith(header_text):
            header_row = i + 1  # kolumnrad ligger direkt under rubriken
            break

    if header_row is None:
        return []

    # Läs kolumnnamn
    columns = [c for c in sheet[header_row] if c]

    # Läs data tills tom rad
    data = []
    for r in sheet.iter_rows(min_row=header_row + 1, values_only=True):
        if not any(r):  # tom rad = slut på tabellen
            break
        entry = dict(zip(columns, r))
        data.append(entry)

    return data


# 🟩 Dashboard-endpoint
@app.get("/dashboard")
def get_dashboard():
    wb = load_workbook("BentusTouren.xlsx", data_only=True)
    sheet = wb["Dashboard"]

    dashboard = {
        "topp5": read_table(sheet, "Topp"),
        "nh": read_table(sheet, "Närmast"),
        "ld": read_table(sheet, "Längsta"),
        "spelade": read_table(sheet, "Spelade"),
        "vinster": read_table(sheet, "Deltävlingsvinster"),
        "landskamper": read_table(sheet, "Landskamper"),
        "deltavlingar": read_table(sheet, "Deltävlingar"),
    }

    # Konvertera datum i deltävlingar
    for d in dashboard.get("deltavlingar", []):
        if "Datum" in d and isinstance(d["Datum"], datetime):
            d["Datum"] = d["Datum"].strftime("%Y-%m-%d")

    return dashboard


# 🟩 NY: Tourställning-endpoint
@app.get("/tourstallning")
def get_tourstallning():
    wb = load_workbook("BentusTouren.xlsx", data_only=True)
    sheet = wb["Tourställning"]

    tour = {
        "tourstallning": read_table(sheet, "Tourställning"),
        "poang": read_table(sheet, "Poäng"),
        "rundor": read_table(sheet, "Rundor"),
        "vinster": read_table(sheet, "Vinster"),
        "statistik": read_table(sheet, "Statistik"),
    }

    return tour


# 🟩 Root-endpoint
@app.get("/")
def root():
    return {"status": "Bentus Touren backend aktiv"}
