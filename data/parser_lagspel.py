for deltavling in DELTAVLINGAR:
        if deltavling not in sheets:
                continue

                    df = sheets[deltavling].dropna(how="all")
                        df.columns = [str(c).strip() for c in df.columns]

                            if "Lag" in df.columns and "Resultat" in df.columns:
                                    lag_df = df[df["Lag"].notna()][["Lag", "Resultat", "Plac", "Bonus"]]

                                            for _, row in lag_df.iterrows():
                                                        lag = row["Lag"]

                                                                    if lag not in lag_resultat:
                                                                                    lag_resultat[lag] = []
                                                                                                    lagbonus_trend[lag] = []
                                                                                                                    lagplacering_trend[lag] = []

                                                                                                                                lag_resultat[lag].append({
                                                                                                                                                "deltavling": deltavling,
                                                                                                                                                                "resultat": row.get("Resultat"),
                                                                                                                                                                                "placering": row.get("Plac"),
                                                                                                                                                                                                "bonus": row.get("Bonus")
                                                                                                                                                                                                            })

                                                                                                                                                                                                                        if pd.notna(row.get("Bonus")):
                                                                                                                                                                                                                                        lagbonus_trend[lag].append(row.get("Bonus"))