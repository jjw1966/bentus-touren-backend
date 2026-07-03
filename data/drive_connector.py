import os

def download_excel_from_drive():
    file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Bentus_Tour_2026.xlsx")
    return file_path