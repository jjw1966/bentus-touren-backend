from fastapi import APIRouter
from data.parserspelare import parsespelare
from data.driveconnector import downloadexcelfromdrive
from data.excelreader import readexcel_sheets

router = APIRouter()

@router.get("/spelare")
def getallspelare():
    filepath = downloadexcelfromdrive()
        sheets = readexcelsheets(file_path)
            data = parse_spelare(sheets)
                return data

                @router.get("/spelare/{namn}")
                def getsinglespelare(namn: str):
                    filepath = downloadexcelfromdrive()
                        sheets = readexcelsheets(file_path)
                            data = parse_spelare(sheets)
                                return data.get(namn, {"error": "Spelaren finns inte"})