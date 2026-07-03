from fastapi import APIRouter
from data.parsertourstallning import parsetourstallning
from data.driveconnector import downloadexcelfromdrive
from data.excelreader import readexcel_sheets

router = APIRouter()

@router.get("/tourstallning")
def get_tourstallning():
    filepath = downloadexcelfromdrive()
    sheets = readexcelsheets(file_path)
    data = parse_tourstallning(sheets)
    return data