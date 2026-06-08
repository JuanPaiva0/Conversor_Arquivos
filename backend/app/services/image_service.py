from app.exceptions.custom_exceptions import ConversionError
from app.core.utils import ensure_output_dir, get_output_path
from app.core.validators import validate_file
from PIL import Image
from pdf2image import convert_from_bytes
import os

class ImageService:
    async def convert_png_to_pdf(self, file):
        validate_file(file, "png")
        
        try:
            output_dir = ensure_output_dir()
            output_path = get_output_path(file, output_dir, "pdf")

            image = Image.open(file.file)
            image.convert("RGB").save(output_path)

            return output_path
        
        except Exception as e:
            raise ConversionError(
                f"Erro ao converter PNG para PDF: {str(e)}"
            )

    async def convert_pdf_to_png(self, file):
        validate_file(file, "pdf")

        try:
            output_dir = ensure_output_dir()
            output_path = get_output_path(file, output_dir, "png")

            pdf_bytes = await file.read()
            images = convert_from_bytes(pdf_bytes)

            images[0].save(output_path, "PNG")

            return output_path
        
        except Exception as e:
            raise ConversionError(
                f"Erro ao converter PDF para PNG: {str(e)}"
            )
        
    async def convert_jpg_to_png(self, file):
        validate_file(file, "jpg")

        try:
            output_dir = ensure_output_dir()
            output_path = get_output_path(file, output_dir, "png")

            image = Image.open(file.file)
            image.convert("RGB").save(output_path)

            return output_path
        
        except Exception as e:
            raise ConversionError(
                f"Erro ao converter JPG para PNG: {str(e)}"
            )
