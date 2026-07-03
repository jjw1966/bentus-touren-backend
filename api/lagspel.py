from fastapi import APIRouter
from data.parserlagspel import parselagspel
from data.driveconnector import downloadexcelfromdrive
from data.excelreader import readexcel_sheets

router = APIRouter()

@router.get("/lagspel")
def get_lagspel():
    filepath = downloadexcelfromdrive()
        sheets = readexcelsheets(file_path)
            data = parse_lagspel(sheets)
                return data