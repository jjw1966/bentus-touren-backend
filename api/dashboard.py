from fastapi import APIRouter
from data.parserdashboard import parsedashboard
from data.driveconnector import downloadexcelfromdrive
from data.excelreader import readexcel_sheets

router = APIRouter()

@router.get("/dashboard")
def get_dashboard():
    filepath = downloadexcelfromdrive()
        sheets = readexcelsheets(file_path)
            data = parse_dashboard(sheets)
                return data