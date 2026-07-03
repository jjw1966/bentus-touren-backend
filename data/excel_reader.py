import pandas as pd

def read_excel_data(file_path):
    """
    Läser alla blad i Excel-filen och returnerar dem som JSON-vänliga dicts.
    Loggar vilka blad som hittas.
    """
    try:
        # Läs alla blad i filen
        excel_data = pd.read_excel(file_path, sheet_name=None, engine="openpyxl")

        # Logga vilka blad som hittades
        print("📊 Excel-blad funna:", list(excel_data.keys()))

        result = {}

        for sheet_name, df in excel_data.items():
            # Ersätt NaN med None
            cleaned = df.where(pd.notnull(df), None)

            # Konvertera DataFrame → list of dicts
            result[sheet_name.lower()] = cleaned.to_dict(orient="records")

        return result

    except Exception as e:
        print("❌ Fel vid läsning av Excel:", e)
        return {"error": str(e)}
