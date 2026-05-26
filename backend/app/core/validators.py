from pathlib import Path
import magic
from fastapi import UploadFile

from app.exceptions.custom_exceptions import (
    InvalidFileExtensionError,
    InvalidMimeTypeError,
    FileTooLargeError,
    MissingFilenameError
)

MAX_FILE_SIZE = 10 * 1024 * 1024 # 10 MB

ALLOWED_FILE_TYPES = {
    "png": {
        "extensions": [".png"],
        "mime_types": [
            "image/png"
        ]
    },

    "pdf": {
        "extensions": [".pdf"],
        "mime_types": [
            "application/pdf"
        ]
    },

    "jpg": {
        "extensions": [".jpg", ".jpeg"],
        "mime_types": [
            "image/jpeg"
        ]
    },

    "txt": {
        "extensions": [".txt"],
        "mime_types": [
            "text/plain"
        ]
    },

    "docx": {
        "extensions": [".docx"],
        "mime_types": [
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "application/zip"
        ]
    },

    "xlsx": {
        "extensions": [".xlsx"],
        "mime_types": [
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            "application/zip"
        ]
    },

    "csv": {
        "extensions": [".csv"],
        "mime_types": [
            "text/csv",
            "application/csv",
            "application/vnd.ms-excel"
        ]
    }
}

def validate_extension(filename: str, allowed_extensions: list[str]):
    extension = Path(filename).suffix.lower()

    if extension not in allowed_extensions:
        raise InvalidFileExtensionError(
            f"Extensão inválida. Extensões permitidas: {', '.join(allowed_extensions)}"
        )
    
def validate_mime_type(file: UploadFile, allowed_mime_types: list[str]):
    if file.content_type not in allowed_mime_types:
        raise InvalidMimeTypeError(
            f"Tipo MIME inválido. Tipos MIME permitidos: {', '.join(allowed_mime_types)}"
        )
    
def validate_real_file_type(file: UploadFile, allowed_mime_types: list[str]):
    file_bytes = file.file.read(2048)

    mime = magic.from_buffer(
        file_bytes, 
        mime=True
    )

    file.file.seek(0)

    if mime not in allowed_mime_types:
        raise InvalidMimeTypeError(
            f"Conteúdo real do arquivo não corresponde ao tipo MIME declarado. Tipos MIME permitidos: {', '.join(allowed_mime_types)}"
        )
    
def validate_file_size(file: UploadFile) -> None:
    file.file.seek(0, 2)
    file_size = file.file.tell()
    file.file.seek(0)

    if file_size > MAX_FILE_SIZE:
        raise FileTooLargeError(
            f"O arquivo é muito grande. O tamanho máximo permitido é {MAX_FILE_SIZE / (1024 * 1024)} MB."
        )
    
def validate_file(file: UploadFile, file_type: str) -> None:
    if not file.filename:
        raise MissingFilenameError(
            "Nome do arquivo não informado."
        )

    config = ALLOWED_FILE_TYPES.get(file_type)
    if not config:
        raise ValueError(
            f"Tipo de arquivo '{file_type}' não suportado."
        )

    validate_extension(
        file.filename,
        config["extensions"]
    )

    validate_file_size(file)

    validate_mime_type(
        file,
        config["mime_types"]
    )

    validate_real_file_type(
        file,
        config["mime_types"]
    )
