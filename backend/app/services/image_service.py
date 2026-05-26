from app.exceptions.custom_exceptions import ConversionError, InvalidFileExtensionError
from app.core.utils import ensure_output_dir
from app.core.validators import validate_extension
from PIL import Image
from pdf2image import convert_from_bytes
import os

class ImageService:
    async def convert_png_to_pdf(self, file):
        try:
            validate_extension(file.filename, [".png"])
            output_dir = ensure_output_dir()

            name, _ = os.path.splitext(file.filename)
            output_path = os.path.join(output_dir, f"{name}.pdf")

            image = Image.open(file.file)
            image.convert("RGB").save(output_path)

            return output_path
        
        except InvalidFileExtensionError:
            raise
        
        except Exception as e:
            raise ConversionError(
                f"Erro ao converter PNG para PDF: {str(e)}"
            )

    async def convert_pdf_to_png(self, file):
        try:
            validate_extension(file.filename, [".pdf"])
            output_dir = ensure_output_dir()

            name, _ = os.path.splitext(file.filename)
            output_path = os.path.join(output_dir, f"{name}.png")

            pdf_bytes = await file.read()
            images = convert_from_bytes(pdf_bytes)

            images[0].save(output_path, "PNG")

            return output_path
        
        except InvalidFileExtensionError:
            raise
        
        except Exception as e:
            raise ConversionError(
                f"Erro ao converter PDF para PNG: {str(e)}"
            )
        
    async def convert_jpg_to_png(self, file):
        try:
            validate_extension(file.filename, [".jpg", ".jpeg"])
            output_dir = ensure_output_dir()

            name, _ = os.path.splitext(file.filename)        
            output_path = os.path.join(output_dir, f"{name}.png")

            image = Image.open(file.file)
            image.convert("RGB").save(output_path)

            return output_path
        
        except InvalidFileExtensionError:
            raise
        
        except Exception as e:
            raise ConversionError(
                f"Erro ao converter JPG para PNG: {str(e)}"
            )