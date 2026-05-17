from fastapi import APIRouter, UploadFile, File
from fastapi.responses import FileResponse
from app.services.spreadsheet_service import SpreadsheetService


spreadsheet_router = APIRouter(prefix="/spreadsheet", tags=["Planilhas"])
service = SpreadsheetService()


@spreadsheet_router.post("/csv-to-xlsx")
async def csv_to_xlsx(file: UploadFile = File(...)):
    output = await service.convert_csv_to_xlsx(file)
    return FileResponse(output)

@spreadsheet_router.post("/xlsx-to-csv")
async def xlsx_to_csv(file: UploadFile = File(...)):
    output = await service.convert_xlsx_to_csv(file)
    return FileResponse(output)