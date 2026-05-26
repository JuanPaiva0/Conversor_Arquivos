from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.exceptions.custom_exceptions import (
    ConversionError,
    InvalidFileExtensionError,
    InvalidMimeTypeError,
    FileTooLargeError,
    MissingFilenameError
)

from app.routes.image_converter import image_router
from app.routes.document_converter import document_router
from app.routes.spreadsheet_converter import spreadsheet_router

app = FastAPI(title="Conversor de Arquivos")

@app.exception_handler(ConversionError)
async def conversion_exception_handler(request: Request, exception: ConversionError):
    return JSONResponse(
        status_code=500,
        content={"detail": str(exception)}
    )

@app.exception_handler(InvalidFileExtensionError)
async def invalid_extension_exception_handler(request: Request, exception: InvalidFileExtensionError):
    return JSONResponse(
        status_code=400,
        content={"detail": str(exception)}
    )

@app.exception_handler(InvalidMimeTypeError)
async def invalid_mime_type_exception_handler(request: Request, exception: InvalidMimeTypeError):
    return JSONResponse(
        status_code=400,
        content={"detail": str(exception)}
    )

@app.exception_handler(FileTooLargeError)
async def file_too_large_exception_handler(request: Request, exception: FileTooLargeError):
    return JSONResponse(
        status_code=413,
        content={"detail": str(exception)}
    )

@app.exception_handler(MissingFilenameError)
async def missing_filename_exception_handler(request: Request, exception: MissingFilenameError):
    return JSONResponse(
        status_code=400,
        content={"detail": str(exception)}
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(image_router)
app.include_router(document_router)
app.include_router(spreadsheet_router)
