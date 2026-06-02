from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse

from app.exceptions.custom_exceptions import AppException

async def app_exception_handler(request: Request, exc: Exception):
    if isinstance(exc, AppException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.message}
        )

    return JSONResponse(
        status_code=500,
        content={"detail": "Ocorreu um erro inesperado."}
    )

def register_exception_handlers(app: FastAPI):
    app.add_exception_handler(
        AppException,
        app_exception_handler
    )