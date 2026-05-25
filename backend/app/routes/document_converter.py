from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from app.services.document_service import DocumentService
from app.exceptions.custom_exceptions import ConversionError

document_router = APIRouter(prefix="/document", tags=["Documentos"])
service = DocumentService()

@document_router.post("/txt-to-pdf")
async def txt_to_pdf(file: UploadFile = File(...)):
    try:
        output = await service.convert_txt_to_pdf(file)
        return FileResponse(output)
    
    except ConversionError as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    
@document_router.post("/txt-to-docx")
async def txt_to_docx(file: UploadFile = File(...)):
    try:
        output = await service.convert_txt_to_docx(file)
        return FileResponse(output)
    
    except ConversionError as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@document_router.post("/docx-to-pdf")
async def docx_to_pdf(file: UploadFile = File(...)):
    try:
        output = await service.convert_docx_to_pdf(file)
        return FileResponse(output)
    
    except ConversionError as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@document_router.post("/pdf-to-docx")
async def pdf_to_docx(file: UploadFile = File(...)):
    try:
        output = await service.convert_pdf_to_docx(file)
        return FileResponse(output)
    
    except ConversionError as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )