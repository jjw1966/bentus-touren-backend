import pandas as pd

def readexcelsheets(file_path: str) -> dict:
    xls = pd.ExcelFile(file_path)
        sheets = {}

            for sheetname in xls.sheetnames:
                    try:
                                df = pd.readexcel(filepath, sheetname=sheetname)
                                            df = df.dropna(axis=1, how="all")
                                                        df = df.dropna(axis=0, how="all")
                                                                    df.columns = [str(c).strip() for c in df.columns]
                                                                                sheets[sheet_name] = df
                                                                                        except Exception as e:
                                                                                                    print(f"Fel vid läsning av blad '{sheet_name}': {e}")

                                                                                                        return sheets