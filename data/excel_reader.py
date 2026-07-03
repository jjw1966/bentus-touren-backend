import pandas as pd

def read_excel_data(file_path):
    """
    Läser alla blad i Excel-filen och returnerar dem som JSON-vänliga dicts.
    """
    try:
        # Läs alla blad i filen
        excel_data = pd.read_excel(file_path, sheet_name=None, engine="openpyxl")

        result = {}

        for sheet_name, df in excel_data.items():
            # Konvertera NaN → None och DataFrame → list of dicts
            cleaned = df.where(pd.notnull(df), None)
            result[sheet_name.lower()] = cleaned.to_dict(orient="records")

        return result

    except Exception as e:
        # Returnera fel som JSON-vänlig text
        return {"error": str(e)}
