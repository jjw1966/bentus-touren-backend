from fastapi import APIRouter
from data.parserdeltavling import parsedeltavlingar
from data.driveconnector import downloadexcelfromdrive
from data.excelreader import readexcel_sheets

router = APIRouter()

@router.get("/deltavlingar")
def getalldeltavlingar():
    filepath = downloadexcelfromdrive()
        sheets = readexcelsheets(file_path)
            data = parse_deltavlingar(sheets)
                return data

                @router.get("/deltavlingar/{namn}")
                def getsingledeltavling(namn: str):
                    filepath = downloadexcelfromdrive()
                        sheets = readexcelsheets(file_path)
                            data = parse_deltavlingar(sheets)
                                return data.get(namn, {"error": "Deltävlingen finns inte"})