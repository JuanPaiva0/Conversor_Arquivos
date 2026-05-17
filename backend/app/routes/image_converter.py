from fastapi import APIRouter, UploadFile, File
from fastapi.responses import FileResponse
from app.services.image_service import ImageService

image_router = APIRouter(prefix="/images", tags=["Imagens"])
service = ImageService()

@image_router.post("/png-to-pdf")
async def png_to_pdf(file: UploadFile = File(...)):
    output = await service.convert_png_to_pdf(file)
    return FileResponse(output)

@image_router.post("/pdf-to-png")
async def pdf_to_png(file: UploadFile = File(...)):
    output = await service.convert_pdf_to_png(file)
    return FileResponse(output)

@image_router.post("/jpg-to-png")
async def jpg_to_png(file: UploadFile = File(...)):
    output = await service.convert_jpg_to_png(file)
    return FileResponse(output)
