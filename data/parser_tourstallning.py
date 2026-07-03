import pandas as pd

def parse_tourstallning(sheets: dict) -> dict:
    if "Tourställning" not in sheets:
            return {"error": "Tourställning-bladet saknas i Excel-filen"}

                df = sheets["Tourställning"]
                    df = df.dropna(how="all")
                        df.columns = [str(c).strip() for c in df.columns]

                            placeringar = df.to_dict(orient="records")

                                tourpoang_trend = {}
                                    if "Spelare" in df.columns and "Tourpoäng" in df.columns:
                                            for _, row in df.iterrows():
                                                        tourpoang_trend[row["Spelare"]] = row["Tourpoäng"]

                                                            pb_trend = {}
                                                                pb_cols = [c for c in df.columns if "PB" in c or c in ["Sura", "Fullerö", "Strand 1", "Strand 2", "D5", "D6", "D7", "D8"]]

                                                                    for _, row in df.iterrows():
                                                                            spelare = row["Spelare"]
                                                                                    pbtrend[spelare] = [row[c] for c in pbcols if c in row and pd.notna(row[c])]

                                                                                        formkurva = {}
                                                                                            for spelare, pblist in pbtrend.items():
                                                                                                    formkurva[spelare] = pblist[-3:] if len(pblist) >= 3 else pb_list

                                                                                                        return {
                                                                                                                "placeringar": placeringar,
                                                                                                                        "diagramdata": {
                                                                                                                                    "tourpoangtrend": tourpoangtrend,
                                                                                                                                                "pbtrend": pbtrend,
                                                                                                                                                            "formkurva": formkurva
                                                                                                                                                                    }
                                                                                                                                                                        }