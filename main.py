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

# 🟩 Hjälpfunktion för att läsa tabeller dynamiskt
def read_table(sheet, header_text):
    header_row = None
    for i, row in enumerate(sheet.iter_rows(values_only=True)):
        if row and str(row[0]).strip().startswith(header_text):
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


# 🟩 Endpoint för dashboard
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

    # Konvertera datum till ISO-format
    for d in dashboard.get("deltavlingar", []):
        try:
            if isinstance(d["Datum"], datetime):
                d["Datum"] = d["Datum"].strftime("%Y-%m-%d")
        except Exception:
            pass

    return dashboard


# 🟩 Root-endpoint
@app.get("/")
def root():
    return {"status": "Bentus Touren backend aktiv"}
