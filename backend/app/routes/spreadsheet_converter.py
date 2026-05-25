from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from app.services.spreadsheet_service import SpreadsheetService
from app.exceptions.custom_exceptions import ConversionError
from app.core.utils import remove_file

spreadsheet_router = APIRouter(prefix="/spreadsheet", tags=["Planilhas"])
service = SpreadsheetService()

@spreadsheet_router.post("/csv-to-xlsx")
async def csv_to_xlsx(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    try:
        output = await service.convert_csv_to_xlsx(file)

        background_tasks.add_task(remove_file, output)

        return FileResponse(output)
    
    except ConversionError as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@spreadsheet_router.post("/xlsx-to-csv")
async def xlsx_to_csv(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    try:
        output = await service.convert_xlsx_to_csv(file)

        background_tasks.add_task(remove_file, output)

        return FileResponse(output)
    
    except ConversionError as e:
        raise HTTPException (
            status_code=500,
            detail=str(e)
        )
        