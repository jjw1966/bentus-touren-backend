import pandas as pd
import requests
from io import BytesIO

# Google Drive fil‑ID
FILE_ID = "1Y7NhhTDfZJQAFVtQVniJpLoY6BYahbuf"
FILE_URL = f"https://docs.google.com/spreadsheets/d/{FILE_ID}/export?format=xlsx"

def read_sheet(sheet_name):
    """Läser ett blad från Google Drive Excel‑filen."""
    try:
        response = requests.get(FILE_URL)
        response.raise_for_status()

        excel_data = BytesIO(response.content)
        df = pd.read_excel(excel_data, sheet_name=sheet_name)

        # Konvertera NaN → None för JSON‑kompatibilitet
        df = df.where(pd.notnull(df), None)

        return df.to_dict(orient="records")

    except Exception as e:
        return {"error": str(e)}
