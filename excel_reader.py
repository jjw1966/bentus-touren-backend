import pandas as pd
import requests
from io import BytesIO
import time

FILE_ID = "1Y7NhhTDfZJQAFVtQVniJpLoY6BYahbuf"
FILE_URL = f"https://docs.google.com/spreadsheets/d/{FILE_ID}/export?format=xlsx"

# Cache för Excel-data
CACHE = {
    "timestamp": 0,
    "data": None
}

# Cache-livslängd i sekunder (t.ex. 5 minuter)
CACHE_TTL = 300


def fetch_excel():
    """
    Hämtar Excel-filen från Google Drive.
    Använder cache för att undvika onödiga nätverksanrop.
    """
    current_time = time.time()

    # Om cache är färsk, använd den
    if CACHE["data"] is not None and (current_time - CACHE["timestamp"] < CACHE_TTL):
        return CACHE["data"]

    try:
        response = requests.get(FILE_URL, timeout=10)
        response.raise_for_status()

        excel_data = BytesIO(response.content)

        # Uppdatera cache
        CACHE["data"] = excel_data
        CACHE["timestamp"] = current_time

        return excel_data

    except Exception as e:
        return {"error": f"Kunde inte hämta Excel-filen: {str(e)}"}


def read_sheet(sheet_name):
    """
    Läser en specifik flik från Excel-filen.
    Hanterar fel, saknade flikar och nätverksproblem.
    """
    excel_data = fetch_excel()

    # Om fetch_excel returnerade ett fel
    if isinstance(excel_data, dict) and "error" in excel_data:
        return excel_data

    try:
        df = pd.read_excel(excel_data, sheet_name=sheet_name)

        # Rensa kolumnnamn från mellanslag och konstiga tecken
        df.columns = df.columns.astype(str).str.strip()

        return df

    except ValueError:
        # Fliken finns inte
        return {"error": f"Fliken '{sheet_name}' finns inte i Excel-filen."}

    except Exception as e:
        return {"error": f"Kunde inte läsa fliken '{sheet_name}': {str(e)}"}
