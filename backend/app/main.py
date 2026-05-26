from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.exceptions.custom_exceptions import ConversionError, InvalidFileExtensionError

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
