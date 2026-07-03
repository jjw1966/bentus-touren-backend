import pandas as pd

def parse_dashboard(sheets: dict) -> dict:
    if "Dashboard" not in sheets:
            return {"error": "Dashboard-bladet saknas i Excel-filen"}

                df = sheets["Dashboard"]
                    df = df.dropna(how="all")
                        df.columns = [str(c).strip() for c in df.columns]

                            topp5 = []
                                if "Spelare" in df.columns and "Tourpoäng" in df.columns:
                                        df_topp = df[["Spelare", "Tourpoäng"]].dropna()
                                                dftopp = dftopp.sort_values("Tourpoäng", ascending=False).head(5)
                                                        topp5 = dftopp.todict(orient="records")

                                                            nh_liga = []
                                                                if "NH" in df.columns:
                                                                        df_nh = df[["Spelare", "NH"]].dropna()
                                                                                dfnh = dfnh.sort_values("NH", ascending=False)
                                                                                        nhliga = dfnh.to_dict(orient="records")

                                                                                            ld_liga = []
                                                                                                if "LD" in df.columns:
                                                                                                        df_ld = df[["Spelare", "LD"]].dropna()
                                                                                                                dfld = dfld.sort_values("LD", ascending=False)
                                                                                                                        ldliga = dfld.to_dict(orient="records")

                                                                                                                            vinster = []
                                                                                                                                if "Vinster" in df.columns:
                                                                                                                                        df_v = df[["Spelare", "Vinster"]].dropna()
                                                                                                                                                dfv = dfv.sort_values("Vinster", ascending=False)
                                                                                                                                                        vinster = dfv.todict(orient="records")

                                                                                                                                                            spelade = []
                                                                                                                                                                if "Spelade" in df.columns:
                                                                                                                                                                        df_s = df[["Spelare", "Spelade"]].dropna()
                                                                                                                                                                                dfs = dfs.sort_values("Spelade", ascending=False)
                                                                                                                                                                                        spelade = dfs.todict(orient="records")

                                                                                                                                                                                            return {
                                                                                                                                                                                                    "topp5": topp5,
                                                                                                                                                                                                            "nhliga": nhliga,
                                                                                                                                                                                                                    "ldliga": ldliga,
                                                                                                                                                                                                                            "vinster": vinster,
                                                                                                                                                                                                                                    "spelade": spelade
                                                                                                                                                                                                                                        }