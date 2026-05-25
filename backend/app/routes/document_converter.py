from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from app.services.document_service import DocumentService
from app.exceptions.custom_exceptions import ConversionError
from app.core.utils import remove_file

document_router = APIRouter(prefix="/document", tags=["Documentos"])
service = DocumentService()

@document_router.post("/txt-to-pdf")
async def txt_to_pdf(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    try:
        output = await service.convert_txt_to_pdf(file)

        background_tasks.add_task(remove_file,output)

        return FileResponse(output)
    
    except ConversionError as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    
@document_router.post("/txt-to-docx")
async def txt_to_docx(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    try:
        output = await service.convert_txt_to_docx(file)

        background_tasks.add_task(remove_file, output)

        return FileResponse(output)
    
    except ConversionError as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@document_router.post("/docx-to-pdf")
async def docx_to_pdf(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    try:
        result = await service.convert_docx_to_pdf(file)

        background_tasks.add_task(remove_file, result['output_path'])
        background_tasks.add_task(remove_file, result['input_path'])

        return FileResponse(result['output_path'])
    
    except ConversionError as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@document_router.post("/pdf-to-docx")
async def pdf_to_docx(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    try:
        result = await service.convert_pdf_to_docx(file)

        background_tasks.add_task(remove_file, result['output_path'])
        background_tasks.add_task(remove_file, result['input_path'])

        return FileResponse(result['output_path'])
    
    except ConversionError as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )