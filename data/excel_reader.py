import pandas as pd
import requests
from io import BytesIO

FILE_ID = "1Y7NhhTDfZJQAFVtQVniJpLoY6BYahbuf"
FILE_URL = f"https://docs.google.com/spreadsheets/d/{FILE_ID}/export?format=xlsx"

def read_sheet(sheet_name):
    try:
        response = requests.get(FILE_URL)
        response.raise_for_status()
        excel_data = BytesIO(response.content)
        df = pd.read_excel(excel_data, sheet_name=sheet_name)
        return df.to_dict(orient="records")
    except Exception as e:
        return {"error": str(e)}
