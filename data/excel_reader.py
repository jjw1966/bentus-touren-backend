import pandas as pd
import requests
import time
from io import BytesIO

FILE_ID = "1Y7NhhTDfZJQAFVtQVniJpLoY6BYahbuf"
FILE_URL = f"https://docs.google.com/spreadsheets/d/{FILE_ID}/export?format=xlsx"

CACHE = {}
CACHE_TIME = 0
CACHE_TTL = 60  # sekunder

def read_sheet(sheet_name):
    """Läser ett blad från Google Drive Excel-filen med 60 sekunders cache."""
    global CACHE, CACHE_TIME
    now = time.time()

    if (now - CACHE_TIME) < CACHE_TTL and sheet_name in CACHE:
        return CACHE[sheet_name]

    try:
        response = requests.get(FILE_URL)
        response.raise_for_status()
        excel_data = BytesIO(response.content)
        df = pd.read_excel(excel_data, sheet_name=sheet_name)
        df = df.where(pd.notnull(df), None)

        CACHE[sheet_name] = df.to_dict(orient="records")
        CACHE_TIME = now

        return CACHE[sheet_name]

    except Exception as e:
        return {"error": str(e)}
