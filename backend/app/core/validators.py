from pathlib import Path
from app.exceptions.custom_exceptions import InvalidFileExtensionError

def validate_extension(filename: str, allowed_extensions: list[str]):
    extension = Path(filename).suffix.lower()

    if extension not in allowed_extensions:
        raise InvalidFileExtensionError(
            f"Extensão inválida. Extensões permitidas: {', '.join(allowed_extensions)}"
        )