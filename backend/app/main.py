from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.exceptions.handlers import register_exception_handlers 

from app.routes.image_converter import image_router
from app.routes.document_converter import document_router
from app.routes.spreadsheet_converter import spreadsheet_router

app = FastAPI(title="Conversor de Arquivos")

register_exception_handlers(app)

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
