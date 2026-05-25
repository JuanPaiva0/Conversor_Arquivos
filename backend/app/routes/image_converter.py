from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from app.exceptions.custom_exceptions import ConversionError
from app.services.image_service import ImageService
from app.core.utils import remove_file

image_router = APIRouter(prefix="/images", tags=["Imagens"])
service = ImageService()

@image_router.post("/png-to-pdf")
async def png_to_pdf(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    try:
        output = await service.convert_png_to_pdf(file)

        background_tasks.add_task(remove_file, output)

        return FileResponse(output)
    
    except ConversionError as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@image_router.post("/pdf-to-png")
async def pdf_to_png(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    try:
        output = await service.convert_pdf_to_png(file)

        background_tasks.add_task(remove_file,output)

        return FileResponse(output)
    
    except ConversionError as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@image_router.post("/jpg-to-png")
async def jpg_to_png(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    try:
        output = await service.convert_jpg_to_png(file)

        background_tasks.add_task(remove_file,output)

        return FileResponse(output)
    
    except ConversionError as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    