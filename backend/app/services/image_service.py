from app.exceptions.custom_exceptions import ConversionError
from PIL import Image
from pdf2image import convert_from_bytes
import os

class ImageService:
    def ensure_output_dir(self):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")

        os.makedirs(OUTPUT_DIR, exist_ok=True)
        return OUTPUT_DIR

    async def convert_png_to_pdf(self, file):
        try:
            output_dir = self.ensure_output_dir()

            name, _ = os.path.splitext(file.filename)
            output_path = os.path.join(output_dir, f"{name}.pdf")

            image = Image.open(file.file)
            image.convert("RGB").save(output_path)

            return output_path
        
        except Exception as e:
            raise ConversionError(
                f"Erro ao converter PNG para PDF: {str(e)}"
            )

    async def convert_pdf_to_png(self, file):
        try:
            output_dir = self.ensure_output_dir()

            name, _ = os.path.splitext(file.filename)
            output_path = os.path.join(output_dir, f"{name}.png")

            pdf_bytes = await file.read()
            images = convert_from_bytes(pdf_bytes)

            images[0].save(output_path, "PNG")

            return output_path
        
        except Exception as e:
            raise ConversionError(
                f"Erro ao converter PDF para PNG: {str(e)}"
            )
        
    async def convert_jpg_to_png(self, file):
        try:
            output_dir = self.ensure_output_dir()

            name, _ = os.path.splitext(file.filename)        
            output_path = os.path.join(output_dir, f"{name}.png")

            image = Image.open(file.file)
            image.convert("RGB").save(output_path)

            return output_path
        
        except Exception as e:
            raise ConversionError(
                f"Erro ao converter JPG para PNG: {str(e)}"
            )