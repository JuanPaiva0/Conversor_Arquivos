from fastapi import APIRouter, UploadFile, File
from fastapi.responses import FileResponse
from app.services.document_service import DocumentService

document_router = APIRouter(prefix="/document", tags=["Documentos"])
service = DocumentService()

@document_router.post("/txt-to-pdf")
async def txt_to_pdf(file: UploadFile = File(...)):
    output = await service.convert_txt_to_pdf(file)
    return FileResponse(output)

@document_router.post("/txt-to-docx")
async def txt_to_docx(file: UploadFile = File(...)):
    output = await service.convert_txt_to_docx(file)
    return FileResponse(output)

@document_router.post("/docx-to-pdf")
async def docx_to_pdf(file: UploadFile = File(...)):
    output = await service.convert_docx_to_pdf(file)
    return FileResponse(output)

@document_router.post("/pdf-to-docx")
async def pdf_to_docx(file: UploadFile = File(...)):
    output = await service.convert_pdf_to_docx(file)
    return FileResponse(output)