import pandas as pd

DELTAVLINGAR = [
    "Sura", "Fullerö", "Strand 1", "Strand 2",
        "Deltävling 5", "Deltävling 6", "Deltävling 7", "Deltävling 8"
        ]

        def parsesingledeltavling(df: pd.DataFrame, name: str) -> dict:
            df = df.dropna(how="all")
                df.columns = [str(c).strip() for c in df.columns]

                    resultat = df.to_dict(orient="records")

                        pb_values = [row["PB"] for row in resultat if "PB" in row and pd.notna(row["PB"])]

                            nh_count = sum(1 for row in resultat if str(row.get("NH", "")).strip() not in ["0", "", None])
                                ld_count = sum(1 for row in resultat if str(row.get("LD", "")).strip() not in ["0", "", None])

                                    lagspel = {"lag": [], "bonus": [], "placering": [], "halvinnare": []}

                                        try:
                                                lag_df = df[df["Lag"].notna()][["Lag", "Resultat", "Plac", "Bonus"]]
                                                        lagspel["lag"] = lagdf.todict(orient="records")
                                                            except:
                                                                    pass

                                                                        if "Vinnare" in df.columns:
                                                                                halvinnare = df[["Hål", "Vinnare"]].dropna()
                                                                                        lagspel["halvinnare"] = halvinnare.to_dict(orient="records")

                                                                                            return {
                                                                                                    "namn": name,
                                                                                                            "resultat": resultat,
                                                                                                                    "diagramdata": {
                                                                                                                                "pbfordelning": pbvalues,
                                                                                                                                            "nhcount": nhcount,
                                                                                                                                                        "ldcount": ldcount
                                                                                                                                                                },
                                                                                                                                                                        "lagspel": lagspel
                                                                                                                                                                            }

                                                                                                                                                                            def parse_deltavlingar(sheets: dict) -> dict:
                                                                                                                                                                                output = {}
                                                                                                                                                                                    for namn in DELTAVLINGAR:
                                                                                                                                                                                            if namn not in sheets:
                                                                                                                                                                                                        continue
                                                                                                                                                                                                                df = sheets[namn]
                                                                                                                                                                                                                        output[namn] = parsesingledeltavling(df, namn)
                                                                                                                                                                                                                            return output